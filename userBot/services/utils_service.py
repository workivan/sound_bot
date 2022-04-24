

class Utils:
    @staticmethod
    def remove_s_if_need(text):
        if text == 'fx' or text == 'bass' or text == 'more drums' or text == 'synth' or text == 'more melodies':
            return text
        return text[:-1]