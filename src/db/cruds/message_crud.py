from src.db.cruds.pagination_oriented_crud import PaginationOrientedCRUD
from src.db.models.models import MessageModel


class MessageCRUD(PaginationOrientedCRUD):
    def __init__(self):
        super(MessageCRUD, self).__init__(MessageModel)
