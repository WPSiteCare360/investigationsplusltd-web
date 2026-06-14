#!/usr/bin/env python3
"""Export WordPress pages, categories, blog posts, and assets into resources/."""

from __future__ import annotations

import json
import re
import shutil
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path

from content_extract import elementor_html_to_markdown, extract_background_images

ROOT = Path(__file__).resolve().parents[1]
OLD_SITE = ROOT / "resources/old-website/investigationsplusltd.com"
API = ROOT / "resources/old-website/api"
UPLOADS_SRC = OLD_SITE / "wp-content/uploads"
BLOG_IMAGES_SRC = ROOT / "public/images/blog"
OUT_PAGES = ROOT / "resources/pages"
OUT_CATEGORIES = ROOT / "resources/categories"
OUT_BLOG = ROOT / "resources/blog"
OUT_IMAGES = ROOT / "resources/images/uploads"
OUT_MANIFEST = ROOT / "resources/site-content-manifest.json"
USER_AGENT = "Mozilla/5.0 (compatible; SiteExporter/1.0)"
IMAGE_PREFIX = "images/uploads"

# Logical export paths and nav labels. WordPress slugs are kept in frontmatter only.
PAGE_EXPORT_NAMES: dict[str, tuple[str, str]] = {
	"toronto-private-investigators": ("home.md", "Home"),
	"private-investigation-about": ("about.md", "About"),
	"private-investigators-services": ("services.md", "Services"),
	"private-investigation-experts-collaboration": ("collaboration.md", "Collaboration"),
	"private-investigator-toronto-ontario": ("locations/toronto.md", "Toronto"),
	"private-investigator-brampton-ontario": ("locations/brampton.md", "Brampton"),
	"private-investigator-vaughan-ontario": ("locations/vaughan.md", "Vaughan"),
	"private-investigator-markham-ontario": ("locations/markham.md", "Markham"),
	"private-investigator-mississauga-ontario": ("locations/mississauga.md", "Mississauga"),
	"private-investigator-richmond-hill-ontario": ("locations/richmond-hill.md", "Richmond Hill"),
	"infidelity-investigation": ("services/infidelity-investigation.md", "Infidelity Investigation"),
	"bug-sweeping-services-tscm": ("services/bug-sweeping-tscm.md", "Bug Sweeping & TSCM"),
	"legal-services": ("services/legal-services.md", "Legal Services"),
}


def load_json(name: str) -> list[dict] | dict:
	return json.loads((API / name).read_text(encoding="utf-8"))


def yaml_string(value: str) -> str:
	return json.dumps(value, ensure_ascii=False)


def strip_html(text: str) -> str:
	return re.sub(r"<[^>]+>", "", unescape(text)).strip()


def uploads_rel_from_url(url: str) -> str | None:
	url = unescape(url.split("?", 1)[0])
	for marker in ("/wp-content/uploads/", "investigationsplusltd.com/wp-content/uploads/"):
		if marker in url:
			return url.split(marker, 1)[1]
	return None


def local_image_ref(rel: str) -> str:
	return f"{IMAGE_PREFIX}/{rel}"


def find_upload_file(rel: str) -> Path | None:
	for base in (UPLOADS_SRC, BLOG_IMAGES_SRC):
		candidate = base / rel
		if candidate.exists():
			return candidate
		parent = candidate.parent
		if not parent.exists():
			continue
		stem = candidate.stem
		normalized_stem = stem.replace("\u2014", "-").replace("\u2002", " ")
		for path in parent.iterdir():
			if not path.is_file():
				continue
			if path.name == candidate.name or path.stem == stem or path.stem == normalized_stem:
				return path
			if stem[:20] and stem[:20] in path.name:
				return path
	return None


def download_image(rel: str) -> bool:
	encoded = urllib.parse.quote(rel, safe="/")
	url = f"https://investigationsplusltd.com/wp-content/uploads/{encoded}"
	dest = OUT_IMAGES / rel
	dest.parent.mkdir(parents=True, exist_ok=True)
	try:
		request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
		with urllib.request.urlopen(request, timeout=60) as response:
			dest.write_bytes(response.read())
		return True
	except OSError:
		return False


def ensure_image(rel: str, manifest: dict) -> None:
	if not rel:
		return
	manifest["imagesReferenced"].add(rel)
	dest = OUT_IMAGES / rel
	if dest.exists():
		manifest["imagesCopied"].add(rel)
		return
	src = find_upload_file(rel)
	if src and src.exists():
		dest.parent.mkdir(parents=True, exist_ok=True)
		shutil.copy2(src, dest)
		manifest["imagesCopied"].add(rel)
		return
	if download_image(rel):
		manifest["imagesCopied"].add(rel)
	else:
		manifest["imagesMissing"].add(rel)


def collect_upload_paths_from_text(text: str) -> set[str]:
	paths: set[str] = set()
	for match in re.finditer(
		r"(?:https?://(?:i0\.wp\.com/)?investigationsplusltd\.com)?/wp-content/uploads/([^\"')>\s]+)",
		text,
		re.I,
	):
		paths.add(unescape(match.group(1).split("?", 1)[0]))
	for match in re.finditer(r"""(?:src|href|content)=['"]([^'"]+)['"]""", text, re.I):
		rel = uploads_rel_from_url(match.group(1))
		if rel:
			paths.add(rel)
	for match in re.finditer(r"url\(([^)]+)\)", text, re.I):
		raw = match.group(1).strip("'\"")
		rel = uploads_rel_from_url(raw)
		if rel:
			paths.add(rel)
	return paths


def rewrite_asset_paths(text: str) -> str:
	def replace_url(match: re.Match[str]) -> str:
		rel = uploads_rel_from_url(match.group(1))
		if not rel:
			return match.group(0)
		return local_image_ref(rel)

	text = re.sub(
		r"(?:https?://(?:i0\.wp\.com/)?investigationsplusltd\.com)?/wp-content/uploads/([^\"'\s>)?]+)",
		lambda m: local_image_ref(unescape(m.group(1).split("?", 1)[0])),
		text,
		flags=re.I,
	)
	text = re.sub(r"""(src|href|content)=(['"])([^'"]+)\2""", replace_url, text, flags=re.I)
	text = re.sub(
		r"url\((['\"]?)([^)'\"]+)\1\)",
		lambda m: f"url({local_image_ref(uploads_rel_from_url(m.group(2)) or m.group(2))})"
		if uploads_rel_from_url(m.group(2))
		else m.group(0),
		text,
		flags=re.I,
	)
	return text


def extract_seo(record: dict) -> dict[str, object]:
	yoast = record.get("yoast_head_json") or {}
	og_images = yoast.get("og_image") or []
	og_image = og_images[0].get("url") if og_images else None
	rel = uploads_rel_from_url(og_image or "")
	if rel:
		og_image = local_image_ref(rel)
	seo: dict[str, object] = {
		"title": yoast.get("title"),
		"description": yoast.get("description"),
		"canonical": yoast.get("canonical"),
		"ogTitle": yoast.get("og_title"),
		"ogDescription": yoast.get("og_description"),
		"ogImage": og_image,
		"ogType": yoast.get("og_type"),
		"ogLocale": yoast.get("og_locale"),
		"twitterCard": yoast.get("twitter_card"),
		"twitterSite": yoast.get("twitter_site"),
		"articleModifiedTime": yoast.get("article_modified_time"),
	}
	robots = yoast.get("robots")
	if isinstance(robots, dict):
		seo["robots"] = robots
	if yoast.get("schema"):
		seo["schema"] = yoast["schema"]
	return {k: v for k, v in seo.items() if v is not None}


def page_url_path(page: dict, pages_by_id: dict[int, dict]) -> str:
	slug = page["slug"]
	if slug == "toronto-private-investigators":
		return "/"
	parent_id = page.get("parent") or 0
	if parent_id:
		parent = pages_by_id.get(parent_id)
		if parent:
			return f"/{parent['slug']}/{slug}/"
	return f"/{slug}/"


def mirror_html_path(url_path: str) -> Path | None:
	if url_path == "/":
		candidate = OLD_SITE / "index.html"
	else:
		candidate = OLD_SITE / url_path.strip("/") / "index.html"
	return candidate if candidate.exists() else None


def extract_elementor_css(html: str, post_id: int) -> str:
	blocks: list[str] = []
	for match in re.finditer(r"<style[^>]*id=['\"]([^'\"]+)['\"][^>]*>(.*?)</style>", html, re.S | re.I):
		style_id = match.group(1)
		css = match.group(2)
		if style_id == "elementor-frontend-inline-css" or f"elementor-{post_id}" in css:
			blocks.append(css.strip())
	for match in re.finditer(rf"<style id=['\"]elementor-post-{post_id}['\"][^>]*>(.*?)</style>", html, re.S | re.I):
		blocks.append(match.group(1).strip())
	return "\n\n".join(block for block in blocks if block)


def extract_main_content(html: str) -> str:
	match = re.search(
		r'<div[^>]*data-elementor-type="wp-page"[^>]*>(.*)</div>\s*</div>\s*(?:<footer|</body)',
		html,
		re.S | re.I,
	)
	if match:
		return match.group(1).strip()
	match = re.search(r"<main[^>]*>(.*?)</main>", html, re.S | re.I)
	if match:
		return match.group(1).strip()
	return ""


def extract_category_posts(html: str) -> list[dict[str, str]]:
	posts: list[dict[str, str]] = []
	for match in re.finditer(r'<article[^>]*class="[^"]*post-(\d+)[^"]*"[^>]*>(.*?)</article>', html, re.S | re.I):
		block = match.group(2)
		title_match = re.search(
			r'class="[^"]*(?:entry-title|elementor-post__title)[^"]*"[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
			block,
			re.S | re.I,
		)
		if not title_match:
			title_match = re.search(r'<a[^>]*class="[^"]*elementor-post__title[^"]*"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', block, re.S | re.I)
		if not title_match:
			continue
		excerpt_match = re.search(
			r'class="[^"]*(?:entry-excerpt|elementor-post__excerpt)[^"]*"[^>]*>(.*?)</div>',
			block,
			re.S | re.I,
		)
		thumb_match = re.search(r'<img[^>]+src="([^"]+)"', block, re.I)
		posts.append(
			{
				"legacyId": match.group(1),
				"url": title_match.group(1),
				"title": strip_html(title_match.group(2)),
				"excerpt": strip_html(excerpt_match.group(1)) if excerpt_match else "",
				"image": rewrite_asset_paths(thumb_match.group(1)) if thumb_match else None,
			}
		)
	return posts


def html_to_content_markdown(html: str) -> str:
	return rewrite_asset_paths(elementor_html_to_markdown(html))


def write_markdown(path: Path, frontmatter: dict, body: str) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	lines = ["---"]
	for key, value in frontmatter.items():
		if isinstance(value, (dict, list)):
			lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
		elif isinstance(value, bool):
			lines.append(f"{key}: {'true' if value else 'false'}")
		elif value is None:
			lines.append(f"{key}: null")
		else:
			lines.append(f"{key}: {yaml_string(str(value))}")
	lines.append("---")
	lines.append("")
	lines.append(body.strip())
	lines.append("")
	path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def export_pages(pages: list[dict], manifest: dict) -> None:
	pages_by_id = {page["id"]: page for page in pages}
	if OUT_PAGES.exists():
		shutil.rmtree(OUT_PAGES)
	OUT_PAGES.mkdir(parents=True)

	for page in sorted(pages, key=lambda item: (item.get("parent", 0), item.get("menu_order", 0))):
		if page["slug"] == "blog":
			continue

		url_path = page_url_path(page, pages_by_id)
		slug = page["slug"]
		export_name, nav_label = PAGE_EXPORT_NAMES.get(slug, (f"{slug}.md", None))
		title = unescape(page["title"]["rendered"])
		excerpt = strip_html(page.get("excerpt", {}).get("rendered", ""))
		source_html = page["content"]["rendered"]
		body = html_to_content_markdown(source_html)
		seo = extract_seo(page)

		mirror = mirror_html_path(url_path)
		background_images: list[str] = []
		if mirror:
			html = mirror.read_text(encoding="utf-8", errors="replace")
			elementor_css = extract_elementor_css(html, page["id"])
			background_images = [
				rewrite_asset_paths(url) for url in extract_background_images(elementor_css)
			]

		for rel in collect_upload_paths_from_text(source_html + body + "\n".join(background_images)):
			ensure_image(rel, manifest)

		featured = None
		media_id = page.get("featured_media") or 0
		if media_id:
			media = {m["id"]: m for m in load_json("media.json")}.get(media_id)
			if media:
				rel = uploads_rel_from_url(media.get("source_url", ""))
				if rel:
					ensure_image(rel, manifest)
					featured = {
						"src": local_image_ref(rel),
						"alt": media.get("alt_text") or strip_html(media.get("title", {}).get("rendered", "")),
					}

		frontmatter = {
			"type": "page",
			"title": title,
			"navLabel": nav_label or title,
			"slug": slug,
			"urlPath": url_path,
			"legacyId": page["id"],
			"parentId": page.get("parent") or 0,
			"menuOrder": page.get("menu_order", 0),
			"pubDate": page.get("date"),
			"updatedDate": page.get("modified"),
			"excerpt": excerpt,
			"seo": seo,
			"featuredImage": featured,
			"backgroundImages": background_images or None,
			"source": "wordpress-api",
		}
		frontmatter = {k: v for k, v in frontmatter.items() if v is not None}

		output = OUT_PAGES / export_name
		write_markdown(output, frontmatter, body)
		manifest["pages"].append(
			{
				"file": str(output.relative_to(ROOT)),
				"urlPath": url_path,
				"title": title,
				"navLabel": nav_label or title,
				"slug": slug,
			}
		)
		print(f"  page {output.relative_to(ROOT)}")


def category_url_path(category: dict, categories_by_id: dict[int, dict]) -> str:
	parts = [category["slug"]]
	parent_id = category.get("parent") or 0
	while parent_id:
		parent = categories_by_id.get(parent_id)
		if not parent:
			break
		parts.insert(0, parent["slug"])
		parent_id = parent.get("parent") or 0
	return "/category/" + "/".join(parts) + "/"


def export_categories(categories: list[dict], manifest: dict) -> None:
	categories_by_id = {cat["id"]: cat for cat in categories}
	if OUT_CATEGORIES.exists():
		shutil.rmtree(OUT_CATEGORIES)
	OUT_CATEGORIES.mkdir(parents=True)

	for category in sorted(categories, key=lambda item: category_url_path(item, categories_by_id)):
		url_path = category_url_path(category, categories_by_id)
		mirror = mirror_html_path(url_path)
		if not mirror:
			manifest["categoriesMissingMirror"].append(url_path)
			continue

		html = mirror.read_text(encoding="utf-8", errors="replace")
		title_match = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
		title = strip_html(title_match.group(1)) if title_match else unescape(category["name"])
		description = strip_html(category.get("description", "") or "")
		posts = extract_category_posts(html)
		intro = html_to_content_markdown(extract_main_content(html))

		for rel in collect_upload_paths_from_text(html + intro):
			ensure_image(rel, manifest)

		rel_parts = url_path.strip("/").split("/")[1:]
		output = OUT_CATEGORIES.joinpath(*rel_parts).with_suffix(".md")
		frontmatter = {
			"type": "category",
			"title": title,
			"slug": category["slug"],
			"urlPath": url_path,
			"legacyId": category["id"],
			"parentId": category.get("parent") or 0,
			"name": unescape(category["name"]),
			"description": description,
			"count": category.get("count", 0),
			"posts": posts,
			"source": "html-mirror",
		}
		body_parts: list[str] = []
		if description:
			body_parts.append(description)
		if intro:
			body_parts.append(intro.strip())
		if posts:
			body_parts.append("## Posts\n")
			for post in posts:
				line = f"- [{post['title']}]({post['url']})"
				if post.get("excerpt"):
					line += f" - {post['excerpt']}"
				body_parts.append(line)

		write_markdown(output, frontmatter, "\n\n".join(body_parts))
		manifest["categories"].append(
			{"file": str(output.relative_to(ROOT)), "urlPath": url_path, "title": title, "postCount": len(posts)}
		)
		print(f"  category {output.relative_to(ROOT)}")


def export_blog(posts: list[dict], manifest: dict) -> None:
	if OUT_BLOG.exists():
		shutil.rmtree(OUT_BLOG)
	OUT_BLOG.mkdir(parents=True)

	for post in sorted(posts, key=lambda item: item["date"]):
		slug = post["slug"]
		title = unescape(post["title"]["rendered"])
		excerpt = strip_html(post.get("excerpt", {}).get("rendered", ""))
		source_html = post["content"]["rendered"]
		body = html_to_content_markdown(source_html)
		seo = extract_seo(post)

		for rel in collect_upload_paths_from_text(source_html + body):
			ensure_image(rel, manifest)

		featured = None
		media_id = post.get("featured_media") or 0
		if media_id:
			media = {m["id"]: m for m in load_json("media.json")}.get(media_id)
			if media:
				rel = uploads_rel_from_url(media.get("source_url", ""))
				if rel:
					ensure_image(rel, manifest)
					featured = {
						"src": local_image_ref(rel),
						"alt": media.get("alt_text") or strip_html(media.get("title", {}).get("rendered", "")),
					}

		frontmatter = {
			"type": "post",
			"title": title,
			"slug": slug,
			"urlPath": f"/{slug}/",
			"legacyId": post["id"],
			"pubDate": post.get("date"),
			"updatedDate": post.get("modified"),
			"excerpt": excerpt,
			"categories": post.get("categories", []),
			"tags": post.get("tags", []),
			"seo": seo,
			"featuredImage": featured,
			"source": "wordpress-api",
		}
		output = OUT_BLOG / f"{slug}.md"
		write_markdown(output, frontmatter, body)
		manifest["blogPosts"].append({"file": str(output.relative_to(ROOT)), "slug": slug, "title": title})
		print(f"  blog {output.relative_to(ROOT)}")


def copy_all_uploads(manifest: dict) -> None:
	if not UPLOADS_SRC.exists():
		return
	OUT_IMAGES.mkdir(parents=True, exist_ok=True)
	for src in UPLOADS_SRC.rglob("*"):
		if not src.is_file():
			continue
		rel = str(src.relative_to(UPLOADS_SRC))
		dest = OUT_IMAGES / rel
		if not dest.exists():
			dest.parent.mkdir(parents=True, exist_ok=True)
			shutil.copy2(src, dest)
		manifest["imagesCopied"].add(rel)
	manifest["uploadsCopied"] = len(list(OUT_IMAGES.rglob("*")))


def scan_mirror_assets(manifest: dict) -> None:
	for css_file in OLD_SITE.rglob("*.css"):
		text = css_file.read_text(encoding="utf-8", errors="replace")
		for rel in collect_upload_paths_from_text(text):
			ensure_image(rel, manifest)
	for html_file in OLD_SITE.rglob("index.html"):
		text = html_file.read_text(encoding="utf-8", errors="replace")
		for rel in collect_upload_paths_from_text(text):
			ensure_image(rel, manifest)


def main() -> None:
	manifest: dict = {
		"pages": [],
		"categories": [],
		"blogPosts": [],
		"categoriesMissingMirror": [],
		"imagesReferenced": set(),
		"imagesCopied": set(),
		"imagesMissing": set(),
	}

	pages = load_json("pages.json")
	posts = load_json("posts.json")
	categories = load_json("categories.json")

	print("Exporting pages...")
	export_pages(pages, manifest)

	print("Exporting categories...")
	export_categories(categories, manifest)

	print("Exporting blog archive...")
	export_blog(posts, manifest)

	print("Copying uploads and resolving referenced images...")
	copy_all_uploads(manifest)
	scan_mirror_assets(manifest)

	for rel in sorted(manifest["imagesReferenced"]):
		ensure_image(rel, manifest)

	manifest["backgroundImages"] = sorted(
		rel
		for rel in manifest["imagesCopied"]
		if any(
			token in rel.lower()
			for token in (
				"background",
				"featured",
				"hero",
				"banner",
				"investigator-at-work",
				"hire-us",
			)
		)
		or rel.endswith((".jpg", ".jpeg", ".png", ".webp", ".gif"))
	)

	serializable = {
		**{k: v for k, v in manifest.items() if k not in {"imagesReferenced", "imagesCopied", "imagesMissing"}},
		"imageStats": {
			"referenced": len(manifest["imagesReferenced"]),
			"copied": len(manifest["imagesCopied"]),
			"missing": sorted(manifest["imagesMissing"]),
		},
		"counts": {
			"pages": len(manifest["pages"]),
			"categories": len(manifest["categories"]),
			"blogPosts": len(manifest["blogPosts"]),
		},
	}
	OUT_MANIFEST.write_text(json.dumps(serializable, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
	print(f"Wrote {OUT_MANIFEST.relative_to(ROOT)}")
	print(
		f"Images: {serializable['imageStats']['copied']} copied, "
		f"{len(serializable['imageStats']['missing'])} missing"
	)


if __name__ == "__main__":
	main()
