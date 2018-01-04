###############################################
#      tangentPlaneUtils                      #
# Some functions to help with calculating     #
# proper motion of stars in the tangent plane,#
# including parallax.                         #
# @author Peter McGill                        #
# @email pm625@cam.ac.uk                      #
###############################################


from astropy.time import Time       
import numpy as np


def s2tp(ra, dec,raz,decz):
	"""Convert from spherical coordinate system to 
        tagent plane coordinates.

	Taken directly from the starlink sub-routine
        'sla_S2TP'. https://github.com/Starlink.

	Args:
           ra (float) : Right ascension of the point
                        to be projected onto the
			tangent plane. [degrees]

           dec (float) : Delination of the point to
                         be projected onto the 
                         tangent plane. [degrees]

           raz (float) : Right ascention of tangent 
			 plane [degrees]

	   decz (float) : Declination of tangent 
			  plane [degrees]

        Returns:
	   coords: (np.array): Rectangular tangent plane
                               coordinates [xi,eta]. 
                               Units of [mas] from tangent 
 			       plane point. 
                         
	"""

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

	return np.array([xi, eta])

def tp2s(xi,eta,raz,decz):
	"""
	Convert from tangent plane coordinate system
	to spherical coordinate system.

	Taken directly from the starlink sub-routine
        'sla_TP2S'. https://github.com/Starlink.

	Args:
	   xi (float) : Xi tangent plane coordinate
			to be mapped onto the sphere
			[mas]
	
	   Eta (float) : Eta tagenet planr coordinate to
                         to be mapped onto the sphere
			 [mas]

	   raz (float) : Right ascention of tangent
                         plane [degrees]

	   decz (float) : Declination of tangent
                          plane [degrees]

	Returns:
	   coords: (np.array): Spherical coordinates [Ra,Dec].
                               Units of [degrees]

	"""
	
	xir = xi * (np.pi /180.0) / ((3600.0 * 1000.0))
	etar = eta * (np.pi / 180.0) / ((3600.0 * 1000.0))

	sdecz = np.sin(np.deg2rad(decz))
	cdecz = np.cos(np.deg2rad(decz))
	
	denom = cdecz-(etar*sdecz)
	
	#Get ra in range 0-2Pi
	ra = np.mod(np.arctan2(xir,denom) + np.deg2rad(raz),2*np.pi)

	if (ra < 0):
		ra += 2*np.pi
	
	ra = ra * (180.0 / np.pi)	
	
	dec = (180.0 / np.pi) * np.arctan2(sdecz+etar*cdecz,np.hypot(xir,denom))

	return np.array([ra,dec])

	
	


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
	# Returns Barycentric position of the observer (earth),
	# l: is heliocentric elciptic londitude of the earth
	R = np.array([np.cos(np.radians(l)),
		np.cos(np.radians(epsilon))*np.sin(np.radians(l))
		,np.sin(np.radians(epsilon))*np.sin(np.radians(l))]) * -1.0
	return R


def RdotW(mjd, alpha):
	# dot product of position vector of the observer and the local west unit vector
	#
	# local west unit vector
	W = np.array([np.sin(np.deg2rad(alpha)),-np.cos(np.deg2rad(alpha)),0])
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
		np.cos(np.deg2rad(alpha))*np.sin(np.deg2rad(delta)),	
		- np.sin(np.deg2rad(alpha))*np.sin(np.deg2rad(delta)),
		-np.cos(np.deg2rad(delta))])
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


