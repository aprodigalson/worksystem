import unittest
from unittest import mock

from worksystem.database.connect import DbUtils
from worksystem.database.model.village import Village


class TestDbUtils(unittest.TestCase):
    def test_add_item(self):
        village = Village(id=-100)
        ret = DbUtils.add_item(village)
        self.assertEqual(ret, True)
        villages = DbUtils.get_all(Village)
        self.assertEqual(village in villages, True)
        DbUtils.delete_item(village)
        villages = DbUtils.get_all(Village)
        self.assertEqual(village in villages, False)


if __name__ == '__main__':
    unittest.main()