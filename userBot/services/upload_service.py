import os
import random
import string

from userBot import config


class Uploader:

    @staticmethod
    def get_random_dir_name():
        s = string.ascii_lowercase + string.digits
        return ''.join(random.sample(s, 4))

    @staticmethod
    def upload_sounds_from_pack(pack):
        temp_dir = config.TMP_FILES_DIR + Uploader.get_random_dir_name()
        os.mkdir(temp_dir)

        ogg_files = []
        for root, _, files in os.walk(pack.path):
            for file in files:
                file_name = file.split(".")[0]
                if file_name == '':
                    break
                ogg_files.append((root + "/" + file_name + '.wav', file_name))

        return ogg_files, temp_dir
