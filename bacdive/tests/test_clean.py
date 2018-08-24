from bacdive.clean import implode_fattened_df,flatten_df
import unittest
from skbio.util import get_data_path
import json
import pandas as pd

class TestClean(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_implode_fattened_df(self):

        ulr_test='https://bacdive.dsmz.de/api/bacdive/bacdive_id/132558/?format=json'
        test_json=get_data_path('test.json')
        truth_df=pd.read_csv(get_data_path('test.csv'), index_col=[0,1,2]).sort_index()
        with open(test_json) as json_data:
            test_data = json.load(json_data)

        test_data=flatten_df(test_data)
        test_data['DSMZ_id']=[ulr_test.split('/')[-2]]*test_data.shape[0]
        test_data.index=(test_data['DSMZ_id']+'||'+test_data['Section']+'||'+test_data['Subsection']+'||'+test_data['Field_ID']).values
        test_data=implode_fattened_df(test_data).sort_index()
        self.assertListEqual(list(truth_df.index.get_level_values('Section')), list(test_data.index.get_level_values('Section')))
        self.assertListEqual(list(truth_df.index.get_level_values('Field')), list(test_data.index.get_level_values('Field')))
        #self.assertListEqual(list(truth_df.index.get_level_values('Subsection')), list(test_data.index.get_level_values('Subsection')))

    def test_flatten_df(self):

        ulr_test='https://bacdive.dsmz.de/api/bacdive/bacdive_id/132558/?format=json'
        test_json=get_data_path('test.json')
        truth_df=pd.read_csv(get_data_path('test.csv'), index_col=[0,1,2]).sort_index()
        with open(test_json) as json_data:
            test_data = json.load(json_data)

        test_data=flatten_df(test_data)
        test_data['DSMZ_id']=[ulr_test.split('/')[-2]]*test_data.shape[0]
        test_data.index=(test_data['DSMZ_id']+'||'+test_data['Section']+'||'+test_data['Subsection']+'||'+test_data['Field_ID']).values
        test_data=implode_fattened_df(test_data).sort_index()
        self.assertListEqual(list(truth_df.index.get_level_values('Section')), list(test_data.index.get_level_values('Section')))
        self.assertListEqual(list(truth_df.index.get_level_values('Field')), list(test_data.index.get_level_values('Field')))
        #self.assertListEqual(list(truth_df.index.get_level_values('Subsection')), list(test_data.index.get_level_values('Subsection')))



if __name__ == "__main__":
    unittest.main()

