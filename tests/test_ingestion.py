"""Local tests: run 'python -m unittest discover -s tests -v'."""

import unittest
from src.ingestion import chunk_pages


class ChunkingTests(unittest.TestCase):
    def setUp(self):
        self.pages = [{
            "document_name": "deployment_options.pdf",
            "page_number": 4,
            "text": "one two three four five six seven eight nine ten",
        }]

    def test_chunk_overlap_and_stable_ids(self):
        first = chunk_pages(self.pages, chunk_size=6, chunk_overlap=2)
        second = chunk_pages(self.pages, chunk_size=6, chunk_overlap=2)
        self.assertEqual(len(first), 2)
        self.assertEqual(first, second)
        self.assertEqual(first[0]["chunk_text"], "one two three four five six")
        self.assertEqual(first[1]["chunk_text"], "five six seven eight nine ten")
        self.assertEqual(first[0]["page_number"], 4)
        self.assertIn("docs.aws.amazon.com", first[0]["source_url"])

    def test_invalid_overlap_rejected(self):
        with self.assertRaises(ValueError):
            chunk_pages(self.pages, chunk_size=10, chunk_overlap=10)

    def test_empty_page_text(self):
        self.assertEqual(chunk_pages([{**self.pages[0], "text": ""}]), [])

    def test_page_metadata_is_preserved(self):
        pages = self.pages + [{**self.pages[0], "page_number": 5}]
        chunks = chunk_pages(pages, chunk_size=20, chunk_overlap=2)
        self.assertEqual([x["page_number"] for x in chunks], [4, 5])
        self.assertNotEqual(chunks[0]["chunk_id"], chunks[1]["chunk_id"])


if __name__ == "__main__":
    unittest.main()
