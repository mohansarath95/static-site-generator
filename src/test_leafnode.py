import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    
    def test_leaf_to_html_p(self):
        """Tests that a LeafNode with a tag and value correctly converts to HTML."""
        node = LeafNode(tag="p", value="Hello World")
        expected_html = '<p>Hello World</p>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_tag_and_props(self):
        """Tests that a LeafNode with a tag and properties correctly converts to HTML."""
        node = LeafNode(
            tag="a", 
            value="Click me", 
            props={"href": "https://google.com", "target": "_blank"}
        )
        expected_html = '<a href="https://google.com" target="_blank">Click me</a>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_tag_no_props(self):
        """Tests that a LeafNode with a tag but no properties correctly converts to HTML."""
        node = LeafNode(tag="p", value="Hello World")
        expected_html = '<p>Hello World</p>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_without_tag(self):
        """Tests that a LeafNode without a tag returns just the value as HTML."""
        node = LeafNode(value="Just text")
        expected_html = 'Just text'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_without_value_raises_error(self):
        """Tests that a LeafNode without a value raises a ValueError when converting to HTML."""
        node = LeafNode(tag="span")
        with self.assertRaises(ValueError):
            node.to_html()