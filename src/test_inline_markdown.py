import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_nodes_delimiter_basic(self):
        """Tests a standard split with bold text in the middle."""
        old_nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_code(self):
        """Tests a standard split using backticks for code blocks."""
        node = TextNode("Check out this `print('hello')` code!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("Check out this ", TextType.TEXT),
            TextNode("print('hello')", TextType.CODE),
            TextNode(" code!", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_at_start(self):
        """Tests that delimiters at the very beginning of a string are handled cleanly without empty nodes."""
        node = TextNode("_Italic_ at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        expected = [
            TextNode("Italic", TextType.ITALIC),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_multiple(self):
        """Tests that multiple instances of the same delimiter in one string are all processed."""
        node = TextNode("A **bold** word and another **one** here.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word and another ", TextType.TEXT),
            TextNode("one", TextType.BOLD),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_unclosed_delimiter(self):
        """Tests that an unclosed markdown delimiter throws a ValueError."""
        node = TextNode("This is **broken markdown syntax", TextType.TEXT)
        
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_nodes_ignores_non_text(self):
        """Tests that nodes that aren't of type TextType.TEXT are passed through untouched."""
        node = TextNode("Already a link", TextType.LINK, "https://boot.dev")
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(new_nodes, [node])

def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

def test_extract_markdown_links(self):
    matches = extract_markdown_links(
        "This is text with a [link](https://boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("link", "https://boot.dev")], matches)

if __name__ == '__main__':
    unittest.main()