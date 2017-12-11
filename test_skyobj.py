import sys
from skyobj import skyobj
import unittest

class Testskyobj(unittest.TestCase):
	
	
	def setUp(self):
		self.obj1 = skyobj(123456789,30.0,60.0,2015.0,100.0,100.0,200.0)
		self.obj2 = skyobj(123456789,30.0,60.0,2015.0)
	
	def test_id_init(self):
		self.assertEqual(self.obj1.id,123456789)

	def test_ra_init(self):
		self.assertEqual(self.obj1.ra_0,30.0)

	def test_dec_init(self):
		self.assertEqual(self.obj1.dec_0,60.0)

	def test_epoch_init(self):
		self.assertEqual(self.obj1.epoch_0,2015.0)

	def test_pmra_init(self):
		self.assertEqual(self.obj1.pmra,100.0)
	
	def test_pmdec_init(self):
		self.assertEqual(self.obj1.pmdec,100.0)

	def test_parallax_init(self):
		self.assertEqual(self.obj1.parallax,200.0)

	def test_pmra_none_init(self):
		self.assertEqual(self.obj2.pmra,0.0)
	
	def test_pmdec_none_init(self):
                self.assertEqual(self.obj2.pmdec,0.0)

	def test_parallax_none_init(self):
                self.assertEqual(self.obj2.parallax,0.0)


if __name__ == '__main__':
	unittest.main()

		
	 




