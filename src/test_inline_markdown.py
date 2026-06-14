import unittest
from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
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

    def test_split_nodes_image_basic(self):
        """Tests standard text with an image."""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(new_nodes, expected)

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

class TestSplitNodesLinkAndImage(unittest.TestCase):

    # ==================== LINK TESTS ====================

    def test_split_nodes_link_basic(self):
        """Tests standard text with two links in the middle."""
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_at_start_and_end(self):
        """Tests a link that occupies the very beginning and very end of a string."""
        node = TextNode("[Start](https://start.com) text [End](https://end.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Start", TextType.LINK, "https://start.com"),
            TextNode(" text ", TextType.TEXT),
            TextNode("End", TextType.LINK, "https://end.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_none_found(self):
        """Tests that a text node with zero links returns unchanged."""
        node = TextNode("Just plain text with no links here.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])


    # ==================== IMAGE TESTS ====================

    def test_split_nodes_image_basic(self):
        """Tests standard text with two markdown images embedded."""
        node = TextNode(
            "Look at my ![dog](https://example.com/dog.jpg) and my ![cat](https://example.com/cat.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Look at my ", TextType.TEXT),
            TextNode("dog", TextType.IMAGE, "https://example.com/dog.jpg"),
            TextNode(" and my ", TextType.TEXT),
            TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_only(self):
        """Tests a string that contains absolutely nothing except a markdown image."""
        node = TextNode("![only image](https://example.com/alone.gif)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("only image", TextType.IMAGE, "https://example.com/alone.gif")
        ]
        self.assertEqual(new_nodes, expected)


    # ==================== MIXED / GUARDRAIL TESTS ====================

    def test_split_links_ignores_images(self):
        """Tests that split_nodes_link ignores image syntax completely (![alt](url))."""
        node = TextNode("This is a link [web](https://google.com) and an image ![pic](https://img.jpg)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        
        # The image should remain flat text inside the normal text node chunks
        expected = [
            TextNode("This is a link ", TextType.TEXT),
            TextNode("web", TextType.LINK, "https://google.com"),
            TextNode(" and an image ![pic](https://img.jpg)", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_ignores_non_text_nodes(self):
        """Tests that both functions leave existing non-TEXT nodes completely alone."""
        bold_node = TextNode("I am already bold", TextType.BOLD)
        
        self.assertEqual(split_nodes_link([bold_node]), [bold_node])
        self.assertEqual(split_nodes_image([bold_node]), [bold_node])

class TestTextToTextNodes(unittest.TestCase):

    def test_text_to_textnodes_full(self):
        """Tests a comprehensive string containing every single inline markdown type."""
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_plain_only(self):
        """Tests that a string with absolutely no markdown formats stays a single text node."""
        text = "This is just a normal sentence with absolutely no special formatting."
        nodes = text_to_textnodes(text)
        
        expected = [TextNode(text, TextType.TEXT)]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_multiple_of_same_type(self):
        """Tests that multiple formatting blocks of the exact same type are all processed."""
        text = "This has **one bold** chunk and **another bold** chunk."
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("one bold", TextType.BOLD),
            TextNode(" chunk and ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD),
            TextNode(" chunk.", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_images_and_links(self):
        """Tests that images and links co-exist peacefully without breaking each other."""
        text = "Give me a ![picture](https://img.png) and a [url](https://site.com)"
        nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("Give me a ", TextType.TEXT),
            TextNode("picture", TextType.IMAGE, "https://img.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("url", TextType.LINK, "https://site.com"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_unclosed_raises_error(self):
        """Tests that the pipeline still throws an exception if any markdown delimiter goes unclosed."""
        text = "This has an unclosed `code snippet element"
        
        with self.assertRaises(ValueError):
            text_to_textnodes(text)

if __name__ == '__main__':
    unittest.main()