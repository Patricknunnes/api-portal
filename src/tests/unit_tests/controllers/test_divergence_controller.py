from src.controllers.divergence_controller import DivergenceController
from src.tests.settings import BaseTestCase


class DivergenceControllerTestClass(BaseTestCase):
    def test_handle_list(self):
        '''
          Should return list with all divergences
        '''
        result = DivergenceController().handle_list(db=self.session)

        self.assertEqual(result, {'page': 1, 'total': 0, 'results': []})
