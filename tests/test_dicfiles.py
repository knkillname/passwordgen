import tempfile
import unittest
from pathlib import Path
from unittest import mock

from passwordgen.utils import dicfiles


class TestHunspellDicFile(unittest.TestCase):
    def mock_dic_file(self, path: Path, word_list: list[str]) -> None:
        """Mock a dictionary file with the given word list."""
        with path.open("w") as f:
            f.write(f"{len(word_list)}\n")  # First line is the number of words
            f.writelines([f"{word}\n" for word in word_list])

    def test_instantiation(self):
        # Instantiation with wrong type should raise TypeError
        with self.assertRaises(TypeError):
            dicfiles.HunspellDicFile(1)

    def test_download(self):
        test_url = "https://example.com/te_ST.dic"
        # Instantiate a HunspellDicFile object
        dic_file = dicfiles.HunspellDicFile(
            file_name="te_ST.dic",
            language_name="Test",
            language_code="te_ST",
            encoding="utf-8",
            url=test_url,
        )

        # Create a temporary directory for downloads and mock the urlretrieve function
        with (
            tempfile.TemporaryDirectory() as temp_dir,
            mock.patch("urllib.request.urlretrieve") as mock_urlretrieve,
        ):
            # Download the dictionary file
            dic_file.download(download_dir=temp_dir, overwrite=False)
            file_path = Path(temp_dir) / "te_ST.dic"

            # Check if the mock function was called with the correct arguments
            mock_urlretrieve.assert_called_once_with(test_url, file_path)

            # Touch the file to make sure it exists
            file_path.touch()

            # Attempting to download the file again should raise FileExistsError
            with self.assertRaises(FileExistsError):
                dic_file.download(download_dir=temp_dir, overwrite=False)

            # Overwriting the file should work ok
            dic_file.download(download_dir=temp_dir, overwrite=True)
            mock_urlretrieve.assert_called_with(test_url, file_path)

    def test_load_words(self):
        # Instantiate a HunspellDicFile object
        dic_file = dicfiles.HunspellDicFile(
            file_name="te_ST.dic",
            language_name="Test",
            language_code="te_ST",
            encoding="utf-8",
            url="https://example.com/te_ST.dic",
        )

        # Create a temporary directory for downloads
        with tempfile.TemporaryDirectory() as temp_dir:
            # Mock a dictionary file
            file_path = Path(temp_dir) / "te_ST.dic"
            word_list = ["this", "is", "a/AAAAA", "test/BBB"]
            self.mock_dic_file(file_path, word_list)

            # Load the words from the file
            words = dic_file.load_words(file_path.parent)

            # Check if the words are loaded correctly
            self.assertEqual(words, ["this", "is", "a", "test"])


if __name__ == "__main__":
    unittest.main()
