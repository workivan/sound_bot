from userBot import config


class ReferralService:
    @staticmethod
    async def get_or_create_user(from_user, text):
        user = await config.storage.get_user(from_user.id)
        if not user:
            deep_link = None
            if len(text.split(" ")) > 1 and (text.split(" ")[1] != from_user.username):
                deep_link = text.split(" ")[1]
            user = await config.storage.create_user(from_user.id, from_user.username, deep_link)
        return user
