class Pack(object):
    path = None
    genre = None
    name = None
    uploaded = None
    cost = None
    rate = None

    def __init__(self, row):
        self.path = row["path"].strip()
        self.genre = row["genre"].strip()
        self.uploaded = row["uploaded"]
        self.name = row["full_name"].strip()
        self.cost = row["cost"]
        self.rate = row["rate"]
