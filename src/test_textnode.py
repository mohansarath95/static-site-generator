import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    
    def test_eq(self):
        """Tests that two nodes with identical text and type (and default None URL) are equal."""
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a test node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_with_url(self):
        """Tests that two nodes with identical text, type, and matching URL strings are equal."""
        node = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_different_type(self):
        """Tests that nodes with identical text but different text types are NOT equal."""
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a test node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text(self):
        """Tests that nodes with different text content are NOT equal."""
        node = TextNode("Apple", TextType.TEXT)
        node2 = TextNode("Banana", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_url_mismatch(self):
        """Tests that nodes where one has a URL and the other has None (or a different URL) are NOT equal."""
        node = TextNode("Link node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Link node", TextType.LINK, None)
        self.assertNotEqual(node, node2)


class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_text_node_to_html_node_text(self):
        text_node = TextNode("Hello", TextType.TEXT)
        expected_html_node = LeafNode(value="Hello")
        self.assertEqual(text_node_to_html_node(text_node), expected_html_node)

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Bold Text", TextType.BOLD)
        expected_html_node = LeafNode(tag="b", value="Bold Text")
        self.assertEqual(text_node_to_html_node(text_node), expected_html_node)

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("Italic Text", TextType.ITALIC)
        expected_html_node = LeafNode(tag="i", value="Italic Text")
        self.assertEqual(text_node_to_html_node(text_node), expected_html_node)

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("Code Snippet", TextType.CODE)
        expected_html_node = LeafNode(tag="code", value="Code Snippet")
        self.assertEqual(text_node_to_html_node(text_node), expected_html_node)

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Google", TextType.LINK, url="https://google.com")
        expected_html_node = LeafNode(tag="a", value="Google", props={"href": "https://google.com"})
        self.assertEqual(text_node_to_html_node(text_node), expected_html_node)

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("Alt Text", TextType.IMAGE, url="https://example.com/image.png")
        expected_html_node = LeafNode(tag="img", value="", props={"src": "https://example.com/image.png", "alt": "Alt Text"})
        self.assertEqual(text_node_to_html_node(text_node), expected_html_node)

    def test_text_node_to_html_link_without_url_raises_error(self):
        text_node = TextNode("Broken Link", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

    def test_text_node_to_html_image_without_url_raises_error(self):
        text_node = TextNode("Broken Image", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

if __name__ == '__main__':
    unittest.main()