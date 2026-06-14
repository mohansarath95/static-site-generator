import re
from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for oldnode in old_nodes:
        if oldnode.text_type != TextType.TEXT:
            new_nodes.append(oldnode)
            continue
        split_texts = oldnode.text.split(delimiter)
        if len(split_texts) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: matching delimeter '{delimiter}' not found.")
        for i in range(len(split_texts)):
            if split_texts[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split_texts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_texts[i], text_type))
    return new_nodes

def extract_markdown_images(text) -> list[(str, str)]:
     return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text) -> list[(str, str)]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for oldnode in old_nodes:
        if oldnode.text_type != TextType.TEXT:
            new_nodes.append(oldnode)
            continue
        current_text = oldnode.text
        images = extract_markdown_images(current_text)
        if not images:
            new_nodes.append(oldnode)
            continue
        for image_alt, image_url in images:
            syntax = f"![{image_alt}]({image_url})"
            sections = current_text.split(syntax, 1)
            if len(sections) != 2:
                raise ValueError(f"Invalid Markdown syntax: image syntax '{syntax}' not found in text.")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            current_text = sections[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for oldnode in old_nodes:
        if oldnode.text_type != TextType.TEXT:
            new_nodes.append(oldnode)
            continue
        current_text = oldnode.text
        links = extract_markdown_links(current_text)
        if not links:
            new_nodes.append(oldnode)
            continue
        for link_text, link_url in links:
            syntax = f"[{link_text}]({link_url})"
            sections = current_text.split(syntax, 1)
            if len(sections) != 2:
                raise ValueError(f"Invalid Markdown syntax: link syntax '{syntax}' not found in text.")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            current_text = sections[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes