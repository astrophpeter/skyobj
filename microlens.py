##################################
# micorlens.py                   #
# Some functions to help with    #
# microlensing event calculations#
# @auther P. McGill              #
# @email pm625@cam.ac.uk         #
##################################

import numpy as np



def get_enstien_R(lensMass,lensDist,sourceDist=None):
	"""Calculates the enstien radius of a lens and 
	source system.


	Args:
	   lensMass (float) : Mass of the foreground
                              lens object [Msol]

           lensDist (float) : Distance to the lens
			      [pc]

	   SourceDist (float,optional) : Distance to the source.
                                         defaults to None. If none,
					 caculation will assume sourceDist
					 to be at infinity. [pc]


	Returns:
	   enstienR (float) : The Enstien radius [mas]

	"""
	if sourceDist is None:
		return 90.2 * np.sqrt(lensMass / lensDist)

	else:
		return 90.2 * np.sqrt((lensMass / lensDist) * (1- lensDist / sourceDist)) 	

def get_centroid_shift(lensMass,lensDist,minSep,sourceDist=None,
				lensMag=None,sourceMag=None):
	"""Calculates the expected astrometric centriod shift
	of a lens source system.
	
	Args:
	   lensMass (float) : lensMass (float) : Mass of the foreground
                              lens object [Msol]

           lensDist (float) : Distance to the lens
                              [pc]

           SourceDist (float,optional) : Distance to the source. 
                                         defaults to None. If none,
                                         caculation will assume sourceDist
                                         to be at infinity. [pc]

	   minSep (float) : Minumin angular separation between the lens
			    abd source [mas]

	   lensMag (float,optional) : Magnitude of the lens. Defaults to None.
				      If none will assume the dark lens equation.

	   sourceMag (float,optional) : Magnitude of the source. Defaults to None.
					If none will assume the dark lens eqution.

	 Returns:
	    centriodShift (float) : The expected centriod shift [mas]
	"""

	EnstienR = get_enstien_R(lensMass,lensDist,sourceDist)	
	mu = minSep / EnstienR

	if lensMag is None and sourceMag is None:
	
		return (mu * EnstienR) / (mu**2 +2)
	
	else:
		lumFactor = 1+(10** ((lensMag - sourceMag) / (-2.5)))
		return (mu * EnstienR) / ((mu**2 + 2)*lumFactor) 

def get_enstien_T(lensMass,lensDist,minSep,lensPmMag,sourceDist=None):
	"""Calculates the enstien time, or duration of the photo
	metric signal of the event.
	
	Args: 
	   lensMass (float) : lensMass (float) : Mass of the foreground
                              lens object [Msol]

           lensDist (float) : Distance to the lens
                              [pc]

           SourceDist (float,optional) : Distance to the source.
                                         defaults to None. If none,
                                         caculation will assume sourceDist
                                         to be at infinity. [pc]

           minSep (float) : Minumin angular separation between the lens
                            abd source [mas]

	   lensPmMag (float) : Magnitude of Lens Proper motion 
			      [mas/yr]

	Returns:
	   EnstienTime (float) : Photmetric signal duration of the event.
				 [yrs]
	"""
	EnstienR = get_enstien_R(lensMass,lensDist,sourceDist=sourceDist)

	return EnstienR / lensPmMag

def get_astrometric_T(lensMass,lensDist,minSep,accuracy,lensPmMag,sourceDist=None):
	"""Calcualte the duration of the astrometric signal given,
	a detection accuracy.

	Formula taken from Honma 2006 or can be found as Eq. (15)
	in Proft et al (2012).

	Args: 
	   lensMass (float) : lensMass (float) : Mass of the foreground
                              lens object [Msol]

           lensDist (float) : Distance to the lens
                              [pc]

           SourceDist (float,optional) : Distance to the source.
                                         defaults to None. If none,
                                         caculation will assume sourceDist
                                         to be at infinity. [pc]

           minSep (float) : Minumin angular separation between the lens
                            abd source [mas]
	   
	   accuracy (float) : Minimum detection accuracy [mas]

           lensPmMag (float) : Magnitude of Lens Proper motion
                              [mas/yr]

	Returns:
	   astrometricTime (float) : Duration of Astrometric Signal 
				     [yrs]

	"""
	
	enstienR = get_enstien_R(lensMass,lensDist,sourceDist=sourceDist)
	enstienT = get_enstien_T(lensMass,lensDist,minSep,lensPmMag,sourceDist=sourceDist)

	return (np.pi / 2.0) * ((enstienT * enstienR) / accuracy)	
 
def get_dist(parallax):
	"""Calculates the distance to an object given
	   its parallax.

	Args:
	   parallax (float) : parallax [mas]

	Returns:
	   distance (float) : distance [pc]

	"""

	return 1000.0 / parallax
	

	
