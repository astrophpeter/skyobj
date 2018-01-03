import tangentPlaneUtils as tp
import unittest

class TesttangentPlaneUtils(unittest.TestCase):

	# test if the zero point maps to the zero point on
	# tangent plane.
	def test_s2tp(self):
		self.assertEqual(tp.s2tp(30.0,60.0,30.0,60)[0],0.0)
		self.assertEqual(tp.s2tp(30.0,60.0,30.0,60)[1],0.0)

	def test_tp2s(self):
		self.assertAlmostEqual(tp.tp2s(0.0,0.0,30.0,60.0)[0],30.0)
		self.assertAlmostEqual(tp.tp2s(0.0,0.0,30.0,60.0)[1],60.0)

if __name__ == '__main__':
	unittest.main()
