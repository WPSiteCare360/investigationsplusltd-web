#!/usr/bin/env python3
"""Extract readable markdown from WordPress/Elementor HTML."""

from __future__ import annotations

import re
import subprocess
import tempfile
from html import unescape
from pathlib import Path


SKIP_WIDGETS = {
	"spacer.default",
	"divider.default",
	"menu-anchor.default",
	"template.default",
	"form.default",
	"google_maps.default",
	"shortcode.default",
	"html.default",
	"slides.default",
	"image-carousel.default",
	"posts.default",
	"archive-posts.archive_cards",
	"nav-menu.default",
	"social-icons.default",
}


def strip_html(text: str) -> str:
	text = unescape(text)
	text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
	text = re.sub(r"<[^>]+>", "", text)
	return re.sub(r"\s+", " ", text).strip()


def normalize_heading_level(tag: str, classes: str) -> int:
	match = re.search(r"elementor-size-(\w+)", classes)
	if match:
		size = match.group(1)
		return {"small": 4, "medium": 3, "large": 2, "xl": 2, "xxl": 1}.get(size, 2)
	return {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 6}.get(tag.lower(), 2)


def heading_to_md(html: str) -> str:
	match = re.search(
		r"<h([1-6])[^>]*class=\"[^\"]*elementor-heading-title[^\"]*\"[^>]*>(.*?)</h\1>",
		html,
		re.S | re.I,
	)
	if not match:
		match = re.search(r"<h([1-6])[^>]*>(.*?)</h\1>", html, re.S | re.I)
	if not match:
		text = strip_html(html)
		return f"## {text}\n" if text else ""
	level = normalize_heading_level(f"h{match.group(1)}", match.group(0))
	text = strip_html(match.group(2))
	if not text:
		return ""
	prefix = "#" * min(max(level, 1), 6)
	return f"{prefix} {text}\n"


def simplify_inline_html(html: str) -> str:
	html = unescape(html)
	html = re.sub(r"<strong[^>]*>(.*?)</strong>", r"<strong>\1</strong>", html, flags=re.S | re.I)
	html = re.sub(r"<b[^>]*>(.*?)</b>", r"<strong>\1</strong>", html, flags=re.S | re.I)
	html = re.sub(r"<em[^>]*>(.*?)</em>", r"<em>\1</em>", html, flags=re.S | re.I)
	html = re.sub(r"<i[^>]*>(.*?)</i>", r"<em>\1</em>", html, flags=re.S | re.I)
	html = re.sub(r"\s+", " ", html)
	return html.strip()


def image_to_md(html: str) -> str:
	match = re.search(r'<img[^>]+src="([^"]+)"[^>]*(?:alt="([^"]*)")?', html, re.I)
	if not match:
		return ""
	src = match.group(1).split("?", 1)[0]
	alt = strip_html(match.group(2) or "")
	return f"![{alt}]({src})\n"


def icon_list_to_md(html: str) -> str:
	items = [strip_html(item) for item in re.findall(r'class="elementor-icon-list-text"[^>]*>(.*?)</span>', html, re.S | re.I)]
	items = [item for item in items if item]
	if not items:
		return ""
	return "\n".join(f"- {item}" for item in items) + "\n"


def icon_box_to_md(html: str) -> str:
	title = re.search(r'class="elementor-icon-box-title"[^>]*>.*?<span[^>]*>(.*?)</span>', html, re.S | re.I)
	desc = re.search(r'class="elementor-icon-box-description"[^>]*>(.*?)</p>', html, re.S | re.I)
	parts: list[str] = []
	if title:
		text = strip_html(title.group(1))
		if text:
			parts.append(f"### {text}")
	if desc:
		text = strip_html(desc.group(1))
		if text:
			parts.append(text)
	return "\n\n".join(parts) + ("\n" if parts else "")


def button_to_md(html: str) -> str:
	match = re.search(
		r'<a[^>]+href="([^"]+)"[^>]*>.*?elementor-button-text"[^>]*>(.*?)</span>',
		html,
		re.S | re.I,
	)
	if not match:
		return ""
	href = unescape(match.group(1))
	if href.startswith("#elementor-action"):
		return ""
	label = strip_html(match.group(2))
	if not label:
		return ""
	return f"[{label}]({href})\n"


def testimonial_to_md(html: str) -> str:
	text = re.search(r'class="elementor-testimonial__text"[^>]*>(.*?)</div>', html, re.S | re.I)
	name = re.search(r'class="elementor-testimonial__name"[^>]*>(.*?)</', html, re.S | re.I)
	if not text:
		return ""
	quote = strip_html(text.group(1))
	author = strip_html(name.group(1)) if name else ""
	block = f"> {quote}"
	if author:
		block += f"\n>\n> -- {author}"
	return block + "\n"


def extract_tab_content(item_html: str) -> str:
	match = re.search(r'class="elementor-tab-content[^"]*"[^>]*>', item_html, re.I)
	if not match:
		return ""
	return extract_balanced_div_content(item_html, match.end())


def toggle_to_md(html: str) -> str:
	parts: list[str] = []
	title_patterns = [
		r'class="elementor-toggle-title"[^>]*>(.*?)</a>',
		r'class="elementor-accordion-title"[^>]*>(.*?)</a>',
	]
	item_pattern = re.compile(
		r'class="elementor-(?:toggle|accordion)-item"[^>]*>(.*?)(?=class="elementor-(?:toggle|accordion)-item"[^>]*>|$)',
		re.S | re.I,
	)
	for item in item_pattern.findall(html):
		title = ""
		for pattern in title_patterns:
			match = re.search(pattern, item, re.S | re.I)
			if match:
				title = strip_html(match.group(1))
				break
		body = html_fragment_to_markdown(extract_tab_content(item))
		if title:
			parts.append(f"### {title}")
		if body.strip():
			parts.append(body.strip())
	return "\n\n".join(parts) + ("\n" if parts else "")


def clean_markdown(text: str) -> str:
	text = re.sub(r"\{[^}]+\}", "", text)
	text = re.sub(r"</?div>", "", text)
	text = re.sub(r"^:::.*$", "", text, flags=re.M)
	text = re.sub(r"\[\[\s*\[([^\]]+)\]\s*\]\]\(([^)]+)\)", r"[\1](\2)", text)
	text = re.sub(r"\[\[([^\]]+)\]\(([^)]+)\)\]", r"[\1](\2)", text)
	text = re.sub(r"^\[([^\]]{20,})\]$", r"\1", text, flags=re.M)
	text = re.sub(r"\n{3,}", "\n\n", text)
	return text.strip()


def html_fragment_to_markdown(html: str) -> str:
	html = simplify_inline_html(html)
	if not strip_html(html):
		return ""
	with tempfile.NamedTemporaryFile("w", suffix=".html", encoding="utf-8", delete=False) as tmp:
		tmp.write(f"<!DOCTYPE html><html><body>{html}</body></html>")
		tmp_path = tmp.name
	try:
		result = subprocess.run(
			["pandoc", tmp_path, "-f", "html", "-t", "markdown", "--wrap=none"],
			check=True,
			capture_output=True,
			text=True,
		)
		text = clean_markdown(result.stdout)
		return text + "\n" if text else ""
	except (subprocess.CalledProcessError, FileNotFoundError):
		return strip_html(html) + "\n"
	finally:
		Path(tmp_path).unlink(missing_ok=True)


def widget_to_markdown(widget_type: str, html: str) -> str:
	if widget_type in SKIP_WIDGETS:
		return ""
	if widget_type == "heading.default":
		return heading_to_md(html)
	if widget_type == "text-editor.default":
		return html_fragment_to_markdown(html)
	if widget_type == "image.default":
		return image_to_md(html)
	if widget_type == "icon-list.default":
		return icon_list_to_md(html)
	if widget_type == "icon-box.default":
		return icon_box_to_md(html)
	if widget_type == "button.default":
		return button_to_md(html)
	if widget_type == "testimonial.default" or widget_type == "testimonial-carousel.default":
		return testimonial_to_md(html)
	if widget_type.startswith("toggle.") or widget_type.startswith("accordion."):
		return toggle_to_md(html)
	if widget_type == "video.default":
		match = re.search(r'src="([^"]+)"', html, re.I)
		return f"[Video]({match.group(1)})\n" if match else ""
	return ""


def extract_balanced_div_content(html: str, open_tag_end: int) -> str:
	depth = 1
	pos = open_tag_end
	while pos < len(html) and depth > 0:
		next_open = html.find("<div", pos)
		next_close = html.find("</div>", pos)
		if next_close == -1:
			break
		if next_open != -1 and next_open < next_close:
			depth += 1
			pos = next_open + 4
			continue
		depth -= 1
		if depth == 0:
			return html[open_tag_end:next_close]
		pos = next_close + 6
	return html[open_tag_end:]


def iter_widget_blocks(html: str) -> list[tuple[str, str]]:
	blocks: list[tuple[str, str]] = []
	pos = 0
	pattern = re.compile(r'data-widget_type="([^"]+)"', re.I)
	container_pattern = re.compile(r'<div class="elementor-widget-container">', re.I)
	while True:
		match = pattern.search(html, pos)
		if not match:
			break
		widget_type = match.group(1)
		start = match.start()
		container = container_pattern.search(html, start)
		if container:
			inner = extract_balanced_div_content(html, container.end())
			blocks.append((widget_type, inner))
			close_end = container.end() + len(inner) + len("</div>")
			pos = close_end
		else:
			pos = match.end()
	return blocks


def extract_background_images(css: str) -> list[str]:
	images: list[str] = []
	for match in re.finditer(r"background-image:\s*url\(([^)]+)\)", css, re.I):
		url = match.group(1).strip("'\"")
		if url and not url.startswith("data:"):
			images.append(url.split("?", 1)[0])
	return images


def elementor_html_to_markdown(html: str) -> str:
	root_match = re.search(
		r'<div[^>]*data-elementor-type="wp-page"[^>]*>(.*)',
		html,
		re.S | re.I,
	)
	content = root_match.group(1) if root_match else html
	# Blog/post body sometimes uses elementor-299 without wp-page wrapper.
	if not root_match:
		content_match = re.search(
			r'<div[^>]*class="[^"]*elementor[^"]*"[^>]*data-elementor-post-type="page"[^>]*>(.*)',
			html,
			re.S | re.I,
		)
		if content_match:
			content = content_match.group(1)

	chunks: list[str] = []
	seen: set[str] = set()
	for widget_type, widget_html in iter_widget_blocks(content):
		md = widget_to_markdown(widget_type, widget_html).strip()
		if not md or md in seen:
			continue
		seen.add(md)
		chunks.append(md)

	if not chunks:
		# Fallback: plain article content for simple posts.
		article = re.search(r'<div class="entry-content[^"]*">(.*?)</div>', html, re.S | re.I)
		if article:
			return html_fragment_to_markdown(article.group(1)).strip()
		return html_fragment_to_markdown(content).strip()

	return clean_markdown("\n\n".join(chunks)) + "\n"
