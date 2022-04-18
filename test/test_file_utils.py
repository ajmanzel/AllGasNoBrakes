import unittest
import os

from src.utils.file import save_file_to_server, get_server_filename


class TestFileUtils(unittest.TestCase):
    def test_get_server_filename(self):
        test_file_dir = 'data/kitten.jpg'
        filename = "kitten.jpg"

        server_filename = get_server_filename(filename)
        assert server_filename[-4:] == ".jpg"

    def test_save_file_to_server(self):
        image_dir = 'images/'
        test_file_dir = 'data/kitten.jpg'
        filename = "kitten.jpg"

        server_filename = get_server_filename(filename)

        with open(test_file_dir, "rb") as f:
            contents = f.read()

        save_file_to_server(server_filename, contents)

        assert os.path.exists(image_dir + server_filename)

        with open(image_dir + server_filename, 'rb') as f:
            saved_contents = f.read()

        assert contents == saved_contents

        # Cleanup
        os.remove(image_dir + server_filename)
        os.rmdir(image_dir)
