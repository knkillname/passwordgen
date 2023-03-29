import tempfile
import unittest
from pathlib import Path
from unittest import mock

from passwordgen.utils import dicfiles


class TestHunspellDicFile(unittest.TestCase):
    def mock_dic_file(self, word_list: list[str], path: Path) -> None:
        """Mock a dictionary file with the given word list."""
        with path.open("w") as f:
            f.write(f"{len(word_list)}\n")  # First line is the number of words
            f.writelines([f"{word}\n" for word in word_list])

    def test_instantiation(self):
        # Instantiation with wrong type should raise TypeError
        with self.assertRaises(TypeError):
            dicfiles.HunspellDicFile(1)

    def test_download(self):
        # Instantiate a HunspellDicFile object
        dic_file = dicfiles.HunspellDicFile(
            file_name="te_ST.dic",
            language_name="Test",
            language_code="te_ST",
            encoding="utf-8",
            url="https://example.com/te_ST.dic",
        )

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as tmp_dirname:
            tmp_dir = Path(tmp_dirname)
            # Mock a dictionary file inside the temporary directory
            dic_file = tmp_dir / "te_ST.dic"
            word_list = ["this", "is", "a/AAAAA", "test/BBB"]
            self.mock_dic_file(word_list, dic_file)
