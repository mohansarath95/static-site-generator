
import os
from block_markdown import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode


def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Title not found in markdown")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating path from {from_path} using template {template_path} to destination {dest_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()
    title = extract_title(markdown)
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    final_html = final_html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    with open(dest_path, "w") as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, relative_path[:-3] + ".html")
                generate_page(from_path, template_path, dest_path, basepath)
        