from src.tests.settings import BaseTestCase

from src.db.cruds.divergence_crud import DivergenceCRUD


class DivergenceCrudTestClass(BaseTestCase):

    def test_divergences_list(self):
        '''
        Should return page info with list
        '''
        result = DivergenceCRUD().handle_list(db=self.session)
        self.assertEqual(result['page'], 1)
        self.assertEqual(result['total'], 0)
        self.assertEqual(len(result['divergences']), 0)
