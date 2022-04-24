class Payment(object):
    chat_id = None
    product = None
    cost = None

    def __init__(self, row):
        if row:
            self.poduct = row['product']
            self.cost = row['cost']
            self.chat_id = row['chat_id']
