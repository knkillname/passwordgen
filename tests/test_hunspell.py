import tempfile
import unittest
from pathlib import Path
from unittest import mock

from passwordgen.dictionaries import hunspell


class TestHunspell(unittest.TestCase):
    def test_download(self):
        test_url = "https://example.com/te_ST.dic"
        with (
            tempfile.TemporaryDirectory() as temp_dir,
            mock.patch("urllib.request.urlretrieve") as mock_urlretrieve,
        ):
            temp_dir = Path(temp_dir)
            dic = hunspell.HunspellDictionary(
                file_path=temp_dir / "te_ST.dic",
                language_code="te_ST",
                language_name="Test",
                encoding="utf-8",
                url=test_url,
            )
            dic.download()
            mock_urlretrieve.assert_called_once_with(test_url, dic.file_path)

    def test_extract_word(self):
        test_line = "test/TEST"
        dic = hunspell.HunspellDictionary(
            file_path=Path("test.dic"),
            language_code="te_ST",
            language_name="Test",
            encoding="utf-8",
            url=None,
        )
        self.assertEqual(dic.extract_word(test_line), "test")

    def test_load_words(self):
        word_list = ["this", "is", "a", "test"]
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)

            # Create a test dictionary file
            with (temp_dir / "te_ST.dic").open("w") as f:
                f.write("4\n")  # First line is the number of words
                f.writelines((word + "\n" for word in word_list))

            dic = hunspell.HunspellDictionary(
                file_path=temp_dir / "te_ST.dic",
                language_code="te_ST",
                language_name="Test",
                encoding="utf-8",
                url=None,
            )

            self.assertEqual(dic.load_words(), word_list)
