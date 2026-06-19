import unittest
from gen_content import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# This is h1\n## This is h2\n### This is h3"
        title = extract_title(markdown)
        self.assertEqual(title, "This is h1")

    def test_no_title(self):
        markdown = "No title here."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertTrue("Title not found in markdown" in str(context.exception))

if __name__ == '__main__':    unittest.main()