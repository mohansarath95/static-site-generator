import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_conversion(self):
        """Tests that a dictionary of attributes is properly converted to an HTML string."""
        node = HTMLNode(
            tag="a", 
            value="Click me", 
            props={"href": "https://google.com", "target": "_blank"}
        )
        expected_str = ' href="https://google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_str)

    def test_props_to_html_empty_or_none(self):
        """Tests that props_to_html returns an empty string when props is None or empty."""
        node_none = HTMLNode(tag="p", value="Hello")
        node_empty = HTMLNode(tag="p", value="Hello", props={})
        
        self.assertEqual(node_none.props_to_html(), "")
        self.assertEqual(node_empty.props_to_html(), "")

    def test_to_html_raises_error(self):
        """Tests that the base HTMLNode class raises a NotImplementedError for to_html."""
        node = HTMLNode(tag="div", value="Content")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_values_and_defaults(self):
        """Tests that instance variables are correctly assigned and defaults are set to None."""
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_children_assignment(self):
        """Tests that child nodes can be cleanly attached to a parent node."""
        child_node = HTMLNode(tag="span", value="child text")
        parent_node = HTMLNode(tag="div", children=[child_node])
        
        self.assertEqual(len(parent_node.children), 1)
        self.assertEqual(parent_node.children[0].tag, "span")

if __name__ == '__main__':
    unittest.main()