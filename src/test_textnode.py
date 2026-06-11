import unittest
from textnode import TextNode, TextType
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

if __name__ == '__main__':
    unittest.main()