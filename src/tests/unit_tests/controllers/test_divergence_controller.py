from unittest.mock import patch

from src.db.cruds.divergence_crud import DivergenceCRUD
from src.controllers.divergence_controller import DivergenceController
from src.tests.mocks.divergence_mocks import divergences
from src.tests.settings import BaseTestCase


class DivergenceControllerTestClass(BaseTestCase):
    @patch.object(DivergenceCRUD, 'list', return_value=divergences)
    def test_handle_list(self, mock):
        '''
          Should return list with all divergences
        '''
        result = DivergenceController().handle_list(db=self.session)

        self.assertEqual(divergences, result)