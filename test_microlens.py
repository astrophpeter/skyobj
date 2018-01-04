import microlens as m
import unittest

class TestmicroLens(unittest.TestCase):

        #Testing Centriod Shift calculations agains those in
	#Table 2 of Proft et al (2012).
        
	def test_get_enstien_R(self):
		#check to 0.1 mas precision (limited by data provided by proft)
		self.assertAlmostEqual(m.get_enstien_R(0.3,57.7),6.507,places=1)
		self.assertAlmostEqual(m.get_enstien_R(0.3,26.1),9.678,places=1)		
		self.assertAlmostEqual(m.get_enstien_R(0.3,169.3),3.797,places=1)
		self.assertAlmostEqual(m.get_enstien_R(0.55,192.3),4.824,places=1)
		self.assertAlmostEqual(m.get_enstien_R(0.6,5.6),29.560,places=1)
		self.assertAlmostEqual(m.get_enstien_R(0.35,19.3),12.141,places=1)
		self.assertAlmostEqual(m.get_enstien_R(0.45,42.9),9.243,places=1)
		self.assertAlmostEqual(m.get_enstien_R(0.3,92.5),5.138,places=1)
		self.assertAlmostEqual(m.get_enstien_R(0.35,55.7),7.149,places=1)

	def test_get_centroid_shift_dark_lens(self):
		#check to 0.1 mas precision (limited by data provided by Proft)
		self.assertAlmostEqual(m.get_centroid_shift(0.3,57.7,6.507*10.7),0.597,places=1)
		self.assertAlmostEqual(m.get_centroid_shift(0.3,26.1,5.2*9.678),1.733,places=1)
		self.assertAlmostEqual(m.get_centroid_shift(0.3,169.3,3.797*32.9),0.115,places=1)	
		self.assertAlmostEqual(m.get_centroid_shift(0.55,192.3,4.824*26.7),0.180,places=1)
		self.assertAlmostEqual(m.get_centroid_shift(0.6,5.6,29.560*4.5),5.972,places=1)
		self.assertAlmostEqual(m.get_centroid_shift(0.35,19.3,12.141*5.0),2.239,places=1)
		self.assertAlmostEqual(m.get_centroid_shift(0.45,42.9,9.243*4.0),2.069,places=1)
		self.assertAlmostEqual(m.get_centroid_shift(0.3,92.5,5.138*2.4),1.591,places=1)
		self.assertAlmostEqual(m.get_centroid_shift(0.35,55.7,7.149*21.3),0.355,places=1)

	def test_get_centroid_shift_luminos_lens(self):
		#check to 0.01 mas precisoin (limited by data provided by Proft)
		self.assertAlmostEqual(m.get_centroid_shift(0.3,57.7,6.507*10.7,lensMag=15.3,sourceMag=18.5),0.030,places=2)	
		self.assertAlmostEqual(m.get_centroid_shift(0.3,26.1,5.2*9.678,lensMag=13.6,sourceMag=19.6),0.007,places=2)
		self.assertAlmostEqual(m.get_centroid_shift(0.3,169.3,3.797*32.9,lensMag=17.6,sourceMag=16.2),0.092,places=2)
		self.assertAlmostEqual(m.get_centroid_shift(0.55,192.3,4.824*26.7,lensMag=14.9,sourceMag=17.0),0.022,places=2)
		self.assertAlmostEqual(m.get_centroid_shift(0.6,5.6,29.560*4.5,lensMag=12.1,sourceMag=19.7),0.006,places=2)
		self.assertAlmostEqual(m.get_centroid_shift(0.35,19.3,12.141*5.0,lensMag=12.1,sourceMag=18.7),0.005,places=2)
		#self.assertAlmostEqual(m.get_centroid_shift(0.45,42.9,9.243*4.0,lensMag=12.7,sourceMag=12.7),1.083,places=1)
		self.assertAlmostEqual(m.get_centroid_shift(0.3,92.5,5.138*2.4,lensMag=16.3,sourceMag=19.6),0.093,places=1)
		self.assertAlmostEqual(m.get_centroid_shift(0.35,55.7,7.149*21.3,lensMag=14.4,sourceMag=17.9),0.013,places=2)

if __name__ == '__main__':
        unittest.main()
