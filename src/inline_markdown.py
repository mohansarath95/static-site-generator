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
