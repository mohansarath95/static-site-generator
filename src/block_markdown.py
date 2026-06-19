
from htmlnode import HTMLNode, LeafNode, ParentNode
from enum import Enum
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_blocks(markdown) -> list[str]:
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip() != ""]

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
         return BlockType.CODE
    
    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    
    elif block.startswith("1. "):
        for i, line in enumerate(lines):
            if not (line.startswith(f"{i+1}. ")):
                return BlockType.PARAGRAPH
        return BlockType.OLIST
    
    else:
        return BlockType.PARAGRAPH
    
def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def markdown_to_html_node(markdown) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        print(repr(block))
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            paragraph = " ".join(block.split("\n"))
            children.append(ParentNode(tag="p", children=text_to_children(paragraph)))
        
        elif block_type == BlockType.HEADING:
            heading_level = block.count("#", 0, block.find(" "))
            text = block[heading_level + 1:].strip()
            children.append(ParentNode(tag= f"h{heading_level}", children= text_to_children(text)))
        
        elif block_type == BlockType.CODE:
            code_text = "```".join(block.split("```")[1:-1])
            code_text = code_text[1:] if code_text.startswith("\n") else code_text
            code_text_node = TextNode(code_text, text_type=TextType.CODE)
            code_html_node = text_node_to_html_node(code_text_node)
            children.append(ParentNode(tag="pre", children=[code_html_node]))
        
        elif block_type == BlockType.QUOTE:
            quote_lines = [line[1:].strip() for line in block.split("\n")]
            quote_text = "\n".join(quote_lines)
            children.append(ParentNode(tag="blockquote", children=text_to_children(quote_text)))

        elif block_type == BlockType.ULIST:
            list_items = [line[2:].strip() for line in block.split("\n")]
            list_item_nodes = [ParentNode(tag="li", children=text_to_children(item)) for item in list_items]
            children.append(ParentNode(tag="ul", children=list_item_nodes))

        elif block_type == BlockType.OLIST:
            list_items = [line[line.find(". ")+2:].strip() for line in block.split("\n")]
            list_item_nodes = [ParentNode(tag="li", children=text_to_children(item)) for item in list_items]
            children.append(ParentNode(tag="ol", children=list_item_nodes))
    
    return ParentNode(tag="div", children=children)