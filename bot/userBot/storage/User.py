class User(object):
    chat_id = None
    username = None
    deep_link = None
    subscription_to = None
    is_connected= None

    def __init__(self, row):
        self.chat_id = row["chat_id"]
        self.username = row["username"].strip()
        self.deep_link = row["deep_link"].strip()
        self.subscription_to = row["subscription_to"]
        self.is_connected = row["is_connected"]