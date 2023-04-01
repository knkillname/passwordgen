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


class TestHunspellShelf(unittest.TestCase):
    def test_get_dictionary(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)

            # Create a test dictionary file
            dic_file = hunspell.HunspellDictionary(
                file_path=temp_dir / "te_ST.dic",
                language_code="te_ST",
                language_name="Test",
                encoding="utf-8",
                url=None,
            )

            word_list = ["this", "is", "a", "test"]
            self.create_dic(dic_file, word_list)

            shelf = hunspell.HunspellDictionaryShelf(
                dictionaries=[dic_file], shelf_directory=temp_dir
            )

            # Test that the dictionary is loaded correctly
            self.assertEqual(shelf.get_dictionary("te_ST"), dic_file)

            # Test that retrieving a non-existent dictionary raises an error
            with self.assertRaises(KeyError):
                shelf.get_dictionary("en_US")

    def test_load_words(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = Path(temp_dir)

            # Create a test dictionary file
            dic_file = hunspell.HunspellDictionary(
                file_path=temp_dir / "te_ST.dic",
                language_code="te_ST",
                language_name="Test",
                encoding="utf-8",
                url=None,
            )

            word_list = ["this", "is", "a", "test"]
            self.create_dic(dic_file, word_list)

            shelf = hunspell.HunspellDictionaryShelf(
                dictionaries=[dic_file], shelf_directory=temp_dir
            )

            # Test that the dictionary is loaded correctly
            self.assertEqual(shelf.load_words("te_ST"), word_list)

            # Test that retrieving a non-existent dictionary raises an error
            with self.assertRaises(KeyError):
                shelf.load_words("en_US")

    def create_dic(self, dic_file, word_list):
        with dic_file.file_path.open("w", encoding=dic_file.encoding) as f:
            f.write(f"{len(word_list)}\n")
            f.writelines((word + "\n" for word in word_list))


if __name__ == "__main__":
    unittest.main()
