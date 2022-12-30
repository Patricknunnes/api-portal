from src.db.cruds.base import BaseCRUD
from src.db.models.models import MessageModel


class MessageCRUD(BaseCRUD):
    def __init__(self):
        super(MessageCRUD, self).__init__(MessageModel)
