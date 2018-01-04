import microlens as m
import unittest

class TestmicroLens(unittest.TestCase):

        #Testing Centriod Shift calculations agains those in
	#Table 2 of Proft et al (2012).
        
	def test_get_enstien_R(self):
		#check to 0.1 mas precision
		self.assertAlmostEqual(m.get_enstien_R(0.3,57.7),6.507,places=1)
		self.assertAlmostEqual(m.get_enstien_R(0.3,26.1),9.678,places=1)		
		self.assertAlmostEqual(m.get_enstien_R(0.3,169.3),3.797,places=1)
		self.assertAlmostEqual(m.get_enstien_R(0.55,192.3),4.824,places=1)
		self.assertAlmostEqual(m.get_enstien_R(0.6,5.6),29.560,places=1)
		self.assertAlmostEqual(m.get_enstien_R(0.35,19.3),12.141,places=1)
		self.assertAlmostEqual(m.get_enstien_R(0.45,42.9),9.243,places=1)
		self.assertAlmostEqual(m.get_enstien_R(0.3,92.5),5.138,places=1)
		self.assertAlmostEqual(m.get_enstien_R(0.35,55.7),7.149,places=1)

	def test_get_centroid_shift_dark(self):

	
if __name__ == '__main__':
        unittest.main()
