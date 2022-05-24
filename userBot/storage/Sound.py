class Sound:
    path = None
    name = None
    sound_type = None
    ogg_path = None
    cost=None

    def __init__(self, sound):
        self.path = sound["path"].strip()
        self.name = sound["name"].strip()
        self.sound_type = sound["sound_type"].strip()
        self.cost = int(sound["cost"])