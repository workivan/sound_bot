class PacksCallback:
    TEN = 'ten'
    MORE = 'more'
    PACKS = 'get_packs'
    DOWNLOAD = 'download_pack'
    FILTRED = 'filtred'
    BUY = 'buy'
    GENRES = 'genres'

    @staticmethod
    def MORE_PACKS(fr):
        return 'more' + f',{fr}'

    @staticmethod
    def TEN_PACKS(message_id):
        return 'ten' + f',{message_id}'

    @staticmethod
    def DOWNLOAD_PACK(pack_name, bought=False):
        return 'download_pack' + f',{pack_name},{bought}'

    @staticmethod
    def BUY_PACK(pack_name):
        return 'buy' + f',{pack_name}'


class SoundCallback:
    FIFTY = 'fifty'


class PaymentCallback:
    MONTH = '1 месяц'
    TH_MONTH = '3 месяца'
    YEAR = '1 год'
