import mongoengine


class Player(mongoengine.Document):
    chat_id = mongoengine.LongField(required=True, primary_key=True)
    name = mongoengine.StringField(required=True, max_length=200)
    active_game = mongoengine.StringField(null=True)
    status_message_id = mongoengine.IntField(null=True)
