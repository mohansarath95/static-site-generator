import unittest
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)

class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
        "This is **bolded** paragraph",
        "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
        "- This is a list\n- with items",
    ])

    def test_excessive_newlines(self):
        md = """
First block




Second block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_empty_string(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])

class TestBlockToBlockType(unittest.TestCase):
    
    def test_paragraph(self):
        block = "This is a simple paragraph of text with no special markdown formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_headings(self):
        # Happy paths h1 through h6
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

        # Edge cases (should be paragraphs)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### Too Many Hashes"), BlockType.PARAGRAPH)

    def test_code_blocks(self):
        # Happy path
        block = "```\ndef my_func():\n    return True\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        # Edge cases (should be paragraphs)
        # Missing closing backticks
        self.assertEqual(block_to_block_type("```\nprint('hello')"), BlockType.PARAGRAPH)
        # Missing opening backticks
        self.assertEqual(block_to_block_type("print('hello')\n```"), BlockType.PARAGRAPH)

    def test_quotes(self):
        # Happy path (single and multi-line)
        self.assertEqual(block_to_block_type("> Single line quote"), BlockType.QUOTE)
        
        multi_line = "> Line 1\n> Line 2\n> Line 3"
        self.assertEqual(block_to_block_type(multi_line), BlockType.QUOTE)

        # Edge case: one line is missing the '>'
        bad_quote = "> Line 1\nLine 2 without quote\n> Line 3"
        self.assertEqual(block_to_block_type(bad_quote), BlockType.PARAGRAPH)

    def test_unordered_lists(self):
        # Happy path (single and multi-line)
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.ULIST)
        
        multi_line = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(multi_line), BlockType.ULIST)

        # Edge cases (should be paragraphs)
        # Missing space after the dash
        self.assertEqual(block_to_block_type("-NoSpace"), BlockType.PARAGRAPH)
        # One line is missing the dash
        bad_list = "- Item 1\nItem 2\n- Item 3"
        self.assertEqual(block_to_block_type(bad_list), BlockType.PARAGRAPH)

    def test_ordered_lists(self):
        # Happy path (starts at 1 and increments sequentially)
        multi_line = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(multi_line), BlockType.OLIST)

        # Edge cases (should be paragraphs)
        # Does not start at 1
        self.assertEqual(block_to_block_type("2. First\n3. Second"), BlockType.PARAGRAPH)
        # Skips a number
        self.assertEqual(block_to_block_type("1. First\n3. Third"), BlockType.PARAGRAPH)
        # Missing the space after the dot
        self.assertEqual(block_to_block_type("1.First"), BlockType.PARAGRAPH)



if __name__ == "__main__":
    unittest.main()