import os
import random
import string

from bot.userBot import config

import soundfile as sf


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
        for _, _, files in os.walk(pack.path):
            for file in files:
                file_name = file.split(".")[0]
                if file_name == '':
                    break

                data, samplerate = sf.read(pack.path + "/" + file)
                sf.write(temp_dir + "/" + file_name + '.ogg', data, samplerate)

                ogg_files.append((temp_dir + "/" + file_name + '.ogg', file_name + '.wav'))

        return ogg_files, temp_dir

    @staticmethod
    def upload_sounds_by_path(sounds):
        temp_dir = config.TMP_FILES_DIR + Uploader.get_random_dir_name()
        os.mkdir(temp_dir)
        for sound in sounds:
            file_name = sound.name.split(".")[0]
            if file_name == '':
                break

            data, samplerate = sf.read(sound.path)
            sf.write(temp_dir + "/" + file_name + '.ogg', data, samplerate)

            sound.ogg_path = temp_dir + "/" + file_name + '.ogg'

        return sounds, temp_dir
