import unittest
from bacdive.utils import check_allow


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_check_allow(self):

        good = check_allow('clos lj')  # returns true
        bad = check_allow('b./_ subit')  # resutns false
        self.assertEqual(good, True)
        self.assertEqual(bad, False)


if __name__ == "__main__":
    unittest.main()
