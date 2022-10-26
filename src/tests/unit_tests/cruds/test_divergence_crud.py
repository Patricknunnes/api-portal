from src.tests.settings import BaseTestCase

from src.db.cruds.divergence_crud import DivergenceCRUD


class DivergenceCrudTestClass(BaseTestCase):

    def test_list_divergences(self):
        '''
          Should return list of divergences
        '''
        result = DivergenceCRUD().list(db=self.session)

        self.assertEqual(type(result), list)
