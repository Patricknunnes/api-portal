from src.db.cruds.base import BaseCRUD
from src.db.models.models import MessageUserModel


class MessageUserCRUD(BaseCRUD):
    def __init__(self):
        super(MessageUserCRUD, self).__init__(MessageUserModel)
