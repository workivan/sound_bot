import os
import psycopg2

from global_config import ROOT_DIR

DB_USER = 'ikuzin'
DB_NAME = 'sound_market'
DB_USER_PASSWORD = 'Pabotahard1$'
DB_URL = f"postgresql://{DB_USER}:{DB_USER_PASSWORD}@localhost:5432/{DB_NAME}"


def get_sound_type(file_name):
    if 'loop' in file_name:
        return 'loop'
    if 'drum' in file_name:
        return 'drum'
    if 'hat' in file_name:
        return 'hat'
    if 'kick' in file_name:
        return 'kick'
    if 'perc' in file_name:
        return 'percussion'
    if 'synth' in file_name:
        return 'synth'
    if 'sample' in file_name:
        return 'sample'
    if 'snare' in file_name:
        return 'snare'
    if 'bass' in file_name:
        return 'bass'
    if 'guitar' in file_name:
        return 'guitar'
    if 'clap' in file_name:
        return 'clap'
    if ('piano' or 'key') in file_name:
        return 'key'
    if 'melody' in file_name:
        return 'more melodies'
    return 'more drums'


def get_genre(file_name):
    if 'hip hop' in file_name or 'drill' in file_name or 'trap' in file_name:
        return 'hip-hop'
    if 'rnb' in file_name:
        return 'rnb'
    if 'rock' in file_name:
        return 'rock'
    if 'house' in file_name or 'techno' in file_name:
        return 'house/techno'
    if 'pop' in file_name:
        return 'pop'
    if 'dancehall' in file_name or 'afro' in file_name:
        return 'dancehall/afro'
    return 'more'


def upload_sounds_from_pack(pack, cur):
    for _, _, files in os.walk(pack):
        for file in files:
            file_name = file.split(".")[0]
            if file_name == '':
                break

            sound_type = get_sound_type(file_name.lower())
            cur.execute(f"""
                insert into "sound"  values('{pack + '/' + file_name + '.wav'}','{file_name + '.wav'}', '{sound_type}')
            on conflict DO NOTHING  """)


def upload_pack(pack, genre, pack_name, cur):
    cur.execute(f"""
        insert into "pack"  values('{pack}','{genre}', '{pack_name}', 0)on conflict DO NOTHING 
    """)


if __name__ == "__main__":
    connection = psycopg2.connect("dbname='sound_market' user='ikuzin' host='localhost' password='Pabotahard1$'")
    print("ok")
    cur = connection.cursor()
    for root, packs, _ in os.walk(ROOT_DIR + "/music"):
        for pack in packs:
            upload_pack(root + '/' + pack, get_genre(pack.lower()), pack, cur)
            upload_sounds_from_pack(root + '/' + pack, cur)
    connection.commit()
