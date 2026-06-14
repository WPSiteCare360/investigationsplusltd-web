#!/usr/bin/env python3
"""Migrate WordPress posts into Astro content/blog markdown files."""

from __future__ import annotations

import json
import re
import shutil
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = ROOT / "resources/old-website/api"
UPLOADS = ROOT / "resources/old-website/investigationsplusltd.com/wp-content/uploads"
OUT_CONTENT = ROOT / "src/content/blog"
OUT_IMAGES = ROOT / "public/images/blog"
OUT_DATA = ROOT / "src/data/blog"
USER_AGENT = "Mozilla/5.0 (compatible; BlogMigrator/1.0)"


def load_json(name: str) -> list[dict] | dict:
	return json.loads((API / name).read_text(encoding="utf-8"))


def yaml_string(value: str) -> str:
	return json.dumps(value, ensure_ascii=False)


def uploads_rel_from_url(url: str) -> str | None:
	url = unescape(url.split("?", 1)[0])
	for marker in (
		"/wp-content/uploads/",
		"investigationsplusltd.com/wp-content/uploads/",
	):
		if marker in url:
			return url.split(marker, 1)[1]
	return None


def local_image_url(rel: str) -> str:
	return f"/images/blog/{rel}"


def find_upload_file(rel: str) -> Path | None:
	candidate = UPLOADS / rel
	if candidate.exists():
		return candidate
	parent = candidate.parent
	if not parent.exists():
		return None
	stem = candidate.stem
	normalized_stem = stem.replace("\u2014", "-").replace("\u2002", " ")
	for path in parent.iterdir():
		if not path.is_file():
			continue
		if path.name == candidate.name or path.stem == stem:
			return path
		if path.stem == normalized_stem:
			return path
		if stem[:20] and stem[:20] in path.name:
			return path
	return None


def copy_image(rel: str) -> str | None:
	src = find_upload_file(rel)
	if src is None:
		return None
	dest = OUT_IMAGES / rel
	dest.parent.mkdir(parents=True, exist_ok=True)
	if not dest.exists():
		shutil.copy2(src, dest)
	return local_image_url(rel)


def download_image(rel: str) -> str | None:
	encoded = urllib.parse.quote(rel, safe="/")
	url = f"https://investigationsplusltd.com/wp-content/uploads/{encoded}"
	dest = OUT_IMAGES / rel
	dest.parent.mkdir(parents=True, exist_ok=True)
	try:
		request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
		with urllib.request.urlopen(request, timeout=60) as response:
			dest.write_bytes(response.read())
		return local_image_url(rel)
	except OSError:
		return None


def ensure_image(rel: str) -> str | None:
	return copy_image(rel) or download_image(rel)


def rewrite_html_images(html: str) -> str:
	def replace_url(match: re.Match[str]) -> str:
		quote = match.group(1)
		url = match.group(2)
		rel = uploads_rel_from_url(url)
		if not rel:
			return match.group(0)
		local = ensure_image(rel)
		if not local:
			return match.group(0)
		return f"{quote}{local}{quote}"

	html = re.sub(r"""(src|href)=(['"])([^'"]+)\2""", replace_url, html, flags=re.I)
	html = re.sub(
		r"(https?://(?:i0\.wp\.com/)?investigationsplusltd\.com)?/wp-content/uploads/([^\"'\s>?]+)",
		lambda m: ensure_image(m.group(2)) or m.group(0),
		html,
	)
	return html


def strip_html(text: str) -> str:
	return re.sub(r"<[^>]+>", "", unescape(text)).strip()


def extract_author(post: dict) -> dict[str, object]:
	embedded = post.get("_embedded", {}).get("author", [])
	if embedded and "name" in embedded[0]:
		author = embedded[0]
		return {
			"id": author["id"],
			"name": author["name"],
			"slug": author.get("slug"),
		}
	yoast = post.get("yoast_head_json", {})
	return {
		"id": post.get("author", 0),
		"name": yoast.get("author") or "Unknown",
		"slug": None,
	}


def extract_taxonomy(post: dict) -> dict[str, list[dict[str, str]]]:
	categories: list[dict[str, str]] = []
	tags: list[dict[str, str]] = []
	for group in post.get("_embedded", {}).get("wp:term", []):
		for term in group:
			item = {
				"slug": term["slug"],
				"name": unescape(term["name"]),
			}
			if term.get("taxonomy") == "category":
				categories.append(item)
			elif term.get("taxonomy") == "post_tag":
				tags.append(item)
	return {"categories": categories, "tags": tags}


def extract_seo(post: dict, description: str) -> dict[str, object]:
	yoast = post.get("yoast_head_json", {})
	og_images = yoast.get("og_image") or []
	og_image = None
	if og_images:
		og_image = og_images[0].get("url")
		rel = uploads_rel_from_url(og_image or "")
		if rel:
			local = ensure_image(rel)
			if local:
				og_image = local
	seo = {
		"title": yoast.get("title") or unescape(post["title"]["rendered"]),
		"description": yoast.get("description") or description,
		"canonical": yoast.get("canonical"),
		"ogTitle": yoast.get("og_title"),
		"ogDescription": yoast.get("og_description"),
		"ogImage": og_image,
		"ogType": yoast.get("og_type"),
		"ogLocale": yoast.get("og_locale"),
		"twitterCard": yoast.get("twitter_card"),
		"twitterSite": yoast.get("twitter_site"),
		"articlePublishedTime": yoast.get("article_published_time"),
		"articleModifiedTime": yoast.get("article_modified_time"),
	}
	robots = yoast.get("robots")
	if isinstance(robots, dict):
		seo["robots"] = {
			"index": robots.get("index"),
			"follow": robots.get("follow"),
		}
	return seo


def export_taxonomy_files(
	category_records: list[dict],
	tag_records: list[dict],
	posts: list[dict],
) -> None:
	OUT_DATA.mkdir(parents=True, exist_ok=True)

	def simplify_term(record: dict) -> dict:
		return {
			"id": record["id"],
			"slug": record["slug"],
			"name": unescape(record["name"]),
			"description": strip_html(record.get("description", "") or ""),
			"count": record.get("count", 0),
			"parent": record.get("parent", 0),
		}

	(OUT_DATA / "categories.json").write_text(
		json.dumps([simplify_term(record) for record in category_records], indent=2, ensure_ascii=False),
		encoding="utf-8",
	)
	(OUT_DATA / "tags.json").write_text(
		json.dumps([simplify_term(record) for record in tag_records], indent=2, ensure_ascii=False),
		encoding="utf-8",
	)

	authors: dict[int, dict] = {}
	for post in posts:
		author = extract_author(post)
		authors[int(author["id"])] = author
	(OUT_DATA / "authors.json").write_text(
		json.dumps(list(authors.values()), indent=2, ensure_ascii=False),
		encoding="utf-8",
	)
	slugs = sorted(post["slug"] for post in posts)
	(OUT_DATA / "slugs.json").write_text(
		json.dumps(slugs, indent=2, ensure_ascii=False) + "\n",
		encoding="utf-8",
	)


def featured_image(media_by_id: dict[int, dict], media_id: int) -> dict[str, str] | None:
	if not media_id:
		return None
	media = media_by_id.get(media_id)
	if not media:
		return None
	rel = uploads_rel_from_url(media.get("source_url", ""))
	if not rel:
		return None
	local = ensure_image(rel)
	if not local:
		return None
	return {"src": local, "alt": media.get("alt_text") or media.get("title", {}).get("rendered", "")}


def write_post(
	post: dict,
	categories: dict[int, str],
	tags: dict[int, str],
	media_by_id: dict[int, dict],
) -> None:
	slug = post["slug"]
	title = unescape(post["title"]["rendered"])
	excerpt = strip_html(post.get("excerpt", {}).get("rendered", ""))
	description = post.get("yoast_head_json", {}).get("description") or excerpt
	body = rewrite_html_images(post["content"]["rendered"])
	image = featured_image(media_by_id, post.get("featured_media", 0))
	author = extract_author(post)
	taxonomy = extract_taxonomy(post)
	seo = extract_seo(post, description)
	category_slugs = [item["slug"] for item in taxonomy["categories"]]
	tag_slugs = [item["slug"] for item in taxonomy["tags"]]

	lines = [
		"---",
		f"title: {yaml_string(title)}",
		f"description: {yaml_string(description)}",
		f"excerpt: {yaml_string(excerpt)}",
		f"pubDate: {yaml_string(post['date'])}",
		f"updatedDate: {yaml_string(post['modified'])}",
		f"slug: {yaml_string(slug)}",
		f"categories: {json.dumps(category_slugs, ensure_ascii=False)}",
		f"tags: {json.dumps(tag_slugs, ensure_ascii=False)}",
		f"taxonomy: {json.dumps(taxonomy, ensure_ascii=False)}",
		f"author: {json.dumps(author, ensure_ascii=False)}",
		f"seo: {json.dumps(seo, ensure_ascii=False)}",
		f"legacyId: {post['id']}",
	]
	if image:
		lines.append(f"image: {json.dumps(image, ensure_ascii=False)}")
	lines.append("---")
	lines.append("")

	output = OUT_CONTENT / f"{slug}.md"
	output.write_text("\n".join(lines) + body, encoding="utf-8")
	print(f"  wrote {output.relative_to(ROOT)}")


def main() -> None:
	posts = load_json("posts.json")
	category_records = load_json("categories.json")
	tag_records = load_json("tags.json")
	categories = {c["id"]: c["slug"] for c in category_records}
	tags = {t["id"]: t["slug"] for t in tag_records}
	media_by_id = {m["id"]: m for m in load_json("media.json")}

	if OUT_CONTENT.exists():
		shutil.rmtree(OUT_CONTENT)
	OUT_CONTENT.mkdir(parents=True)
	OUT_IMAGES.mkdir(parents=True, exist_ok=True)
	export_taxonomy_files(category_records, tag_records, posts)

	print(f"Migrating {len(posts)} posts...")
	for post in sorted(posts, key=lambda item: item["date"]):
		try:
			write_post(post, categories, tags, media_by_id)
		except Exception as error:
			print(f"  failed {post['slug']}: {error}")

	print("Done.")


if __name__ == "__main__":
	main()
