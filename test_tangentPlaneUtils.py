import sys
import tangentPlaneUtils as tp
import unittest
from astropy.time import Time


t = Time(2445680.5,format='jd')
time = t.mjd

print(t.decimalyear)

l=tp.lSol(time)
e = tp.epsilonSol(time)


print(tp.makeR(l,e))
