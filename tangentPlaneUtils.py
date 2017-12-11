#some functions for calculating
#of proper motion and parallax in the 
#tanget plane coordnates for a skyobj


from astropy.time import Time
import numpy as np


def s2tp(ra, dec,raz,decz):
	"""
	Convert from spherical coordinate system
	to tagent plane coordinates
	"""

	#Set the position of the tagent plane
	#at the position of the lens

	# convert to radians
	_rar = np.radians(ra)
	_razr = np.radians(raz)
	_decr = np.radians(dec)
	_deczr = np.radians(decz)

	# Trig functions
	_sdecz = np.sin(_deczr)
	_sdecj = np.sin(_decr)
	_cdecz = np.cos(_deczr)
	_cdecj = np.cos(_decr)
	_radifj = _rar - _razr
	_sradifj = np.sin(_radifj)
	_cradifj = np.cos(_radifj)

	# Reciprocal of star vector length to tangent plane
	_denomj = (_sdecj*_sdecz)+(_cdecj*_cdecz*_cradifj)

	# Compute tangent plane coordinates
	xi = ((180/np.pi)*3600*1000)*_cdecj*_sradifj/_denomj
	eta = ((180/np.pi)*3600*1000)*(_sdecj*_cdecz-_cdecj*_sdecz*_cradifj)/_denomj

	return xi, eta


def lSol(mjd):
	# ecliptic longitude of the sun
	# number of days since noon 1/1/2000
	n = Time(mjd, format='mjd', scale='utc')-Time('2000-01-01T12:00:00', format='isot', scale='utc')
	# mean longitude of the sun
	L = (280.460 + 0.9856474*n.jd) % 360.0
	# mean anomaly of the sun
	g = (357.528 + 0.9856003*n.jd) % 360.0
	# ecliptic longitude of the sun
	l = L + 1.915*np.sin(np.radians(g)) + 0.020*np.sin(np.radians(2*g))
	return l


def epsilonSol(mjd):
	# axial tilt of the ear
	# (obliquity of the ecliptic)
	# number of days since noon 1/1/2000	
	n = Time(mjd, format='mjd', scale='utc')-Time('2000-01-01T12:00:00', format='isot', scale='utc')
	# Obliquity of the ecliptic	
	epsilon = 23.439 - 0.0000004*n.jd;
	return epsilon


def makeR(l, epsilon):
	# position vector of the observer
	R = np.array([np.cos(np.radians(l)),
		np.cos(np.radians(epsilon))*np.sin(np.radians(l))
		,np.sin(np.radians(epsilon))*np.sin(np.radians(l))]) * -1.0
	return R


def RdotW(mjd, alpha):
	# dot product of position vector of the observer and the local west unit vector
	#
	# local west unit vector
	W = np.array([np.sin(alpha),-np.cos(alpha),0])
	# ecliptic longitude of the sun
	longitude = lSol(mjd)
	# Obliquity of the ecliptic
	epsilon = epsilonSol(mjd)
	# fix in the event only one epoch is given
	#longitude = [longitude] if longitude.size==1 else longitude
	#epsilon = [epsilon] if type(epsilon)==float else epsilon
	
	# return R(dot)W
	R = makeR(longitude,epsilon)

	return np.inner(R,W)
  
	


def RdotN(mjd, alpha, delta):
	# dot product of position vector of the observer and the local north unit vector
	#
	# local north unit vector
	N = np.array([
		-np.cos(alpha)*np.sin(delta),	
		-np.sin(alpha)*np.sin(delta),
		np.cos(delta)])
	# ecliptic longitude of the sun
	longitude = lSol(mjd)
	# Obliquity of the ecliptic
	epsilon = epsilonSol(mjd)

	# fix in the event only one epoch is given
	#longitude = [longitude] if longitude.size==1 else longitude
	#epsilon = [epsilon] if type(epsilon)==float else epsilon

	# return R(dot)N
	R = makeR(longitude,epsilon)
	return np.inner(R,N)

