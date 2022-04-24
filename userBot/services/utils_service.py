

class Utils:
    @staticmethod
    def remove_s_if_need(text):
        if text == 'fx' or text == 'bass' or text == 'more' or text == 'synth':
            return text
        return text[:-1]