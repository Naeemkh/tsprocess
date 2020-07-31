import os
import glob
import unittest

from tsprocess import ts_utils as tsu

class TestTsUtils(unittest.TestCase):

    def test_valid_latitude(self):
        self.assertFalse(tsu.is_lat_valid(-177))

class TestCESMDV2(unittest.TestCase):

    def setUp(self):
        self.filename = 'CE12102.V2'
        signal, metadata = tsu.read_smc_v2(
            os.path.join(os.path.dirname(os.path.realpath(__file__)),
             'sample_test_files',self.filename))
        
        self.signal = signal
        self.metadata = metadata

    def test_read_non_existing_cesmdv2_file(self):
        self.assertFalse(tsu.read_smc_v2(
            os.path.join(os.path.dirname(os.path.realpath(__file__)),
             'sample_test_files','NotCE12502.V2')))

    def test_meta_data(self):
        self.assertEqual(self.metadata['network'],'CE')
        self.assertEqual(self.metadata['station_id'],'12102')
        self.assertEqual(self.metadata['type'],'V2')
        self.assertEqual(self.metadata['date'],'3/29/14')
        self.assertEqual(self.metadata['longitude'],'116.959W')
        self.assertEqual(self.metadata['latitude'],'33.787N')
        self.assertEqual(self.metadata['high_pass'],0.1)
        self.assertEqual(self.metadata['low_pass'],40)

    def test_signal(self):
        self.assertEqual(len(self.signal),3)
        self.assertEqual(self.signal[0][0],11400)
        self.assertEqual(self.signal[1][0],11400)
        self.assertEqual(self.signal[2][0],11400)
        self.assertEqual(self.signal[0][1],0.005)
        self.assertEqual(self.signal[1][1],0.005)
        self.assertEqual(self.signal[2][1],0.005)
        self.assertEqual(self.signal[0][2],0)
        self.assertEqual(self.signal[1][2],'up')
        self.assertEqual(self.signal[2][2],90.0)
        
        

        
        


    # def test_cesmdv2_file(self):

    # def tearDown(self):
    #     files = [glob.glob(e) for e in ['*.sqlite', '*.log']]
    #     flat_list = [item for sublist in files for item in sublist]
    #     f_files = [os.path.join(os.path.dirname(os.path.realpath(__file__)),e)
    #      for e in flat_list]
       
    #     for f in f_files:
    #         try:
    #             os.remove(f)
    #         except Exception:
    #             pass
