import unittest
from bacdive.build_url import get_url


class TestBuildUrl(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_url(self):

        truth_genus = ('https://bacdive.dsmz.de/api/'
                       'bacdive/taxon/Acaricomes/')
        truth_Spec = ('https://bacdive.dsmz.de/api/'
                      'bacdive/taxon/Bacillus/halodurans/')
        truth_seq = ('https://bacdive.dsmz.de/api/'
                     'bacdive/sequence/KT935587/')

        test_genus = get_url('Acaricomes', search_type='genus')
        test_Spec = get_url('Bacillus halodurans', search_type='species')
        test_seq = get_url('KT935587', search_type='sequence accession number')

        self.assertEqual(truth_genus, test_genus)
        self.assertEqual(truth_Spec, test_Spec)
        self.assertEqual(truth_seq, test_seq)


if __name__ == "__main__":
    unittest.main()
