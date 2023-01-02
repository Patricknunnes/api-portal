from src.controllers.pagination_oriented_controller import PaginationOrientedController
from src.db.cruds.message_crud import MessageCRUD


class MessageController(PaginationOrientedController):
    def __init__(self):
        super(MessageController, self).__init__(MessageCRUD)
