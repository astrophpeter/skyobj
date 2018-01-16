#############################
##        skyobj           ##
##    A class to find      ##
## microlensing candidates ##
## @author Peter McGill    ##
## @email pm625@cam.ac.uk  ##
#############################

import numpy as np
from astropy.time import Time
from scipy.optimize import minimize_scalar
import tangentPlaneUtils as tp
import microlens as m
import matplotlib.pylab as plt
from astropy.time import Time

class skyobj(object):

	MAS_TO_DEG = 1.0 / (3600.0 * 1000.0)

	def __init__(self,id=None,ra=None,dec=None,epoch=None,pmra=None,pmdec=None,parallax=None,Gmag=None):
		"""

		

		"""
		
		
		self.id  = id
		self.ra_0 = ra
		self.dec_0 = dec
		self.epoch_0 = epoch

		self.xi_0,self.eta_0 = tp.s2tp(ra,dec,ra,dec)
		
		self.gMag = Gmag
				
		#set proper motions and parallax to zero if
		#not specified.
		self.pmra = pmra if pmra else 0.0
		self.pmdec = pmdec if pmdec else 0.0
		self.parallax = parallax if parallax else 0.0
		

	def getRaDecNoPlx(self,epoch):	
		"""
		Get Equtorial coordinates of the skyobj 
                at epoch time - does not take into 
		account parallax.

		Args:
			epoch (float): Decimal Julian Year 
				       time. 

		Returns:
			ra,dec (float,float): Right ascesnion,
					      Declination 
					      [Degrees]			
		"""

		decfinal = (self.dec_0 + (epoch - self.epoch_0) * 
			self.pmdec * self.MAS_TO_DEG)
		rafinal = (self.ra_0 + (epoch - self.epoch_0) * 
			(self.pmra / np.cos(np.deg2rad(self.dec_0))) * self.MAS_TO_DEG)
		
		return rafinal, decfinal

	def getRaDec(self,epoch):
		"""Get Equtorial coordinates of skyobj
                at time epoch, taking into acount parallax.

		Args:
		   epoch (float) : Decimal Julian Years time.

		Returns:
		   ra, dec, (float,float): Right ascesnion,Declination
					   [Degrees]

		"""

		Xi,Eta = self.getXiEta(epoch)

		ra,dec = tp.tp2s(Xi,Eta,self.ra_0,self.dec_0)
		
		return ra,dec 
	
	def getXiEta(self,epoch):
		"""	
		Get Tangent Plane coordinations 
		of source (Xi,Eta) of skyobj at time epoch
		defined from the position of the skyobj
		at it's initial referece position.

		Args:
			epoch (float): Decimal Julian Year
				       Time.

		Returns:

			Xi,Eta (float,float): Tangent Plane
					      coordinatea [mas]
		"""
		
		mjd = Time(epoch, format='decimalyear').mjd
		
		EtaFinal = ((self.parallax) *tp.RdotN(mjd, self.ra_0, self.dec_0) + 
			(self.pmdec) * (epoch - self.epoch_0) + self.eta_0)
		XiFinal = ((self.parallax)* tp.RdotW(mjd, self.ra_0) + 
			(self.pmra) * (epoch - self.epoch_0) + self.xi_0)

		return XiFinal, EtaFinal

	def getSeparation(self,epoch,source):
		"""
		Get angular separation of two skyobj
		(self,source) at time epoch, in tangent
		plane coordinates.

		Args: 
			epoch (float): Decimal Julian Year
				       Time
		
			source (skyobj): source to find separation
					 between.

		Returns: 
			separation (float): Angular Separation
					    [mas]
			
		"""

		lens_xi ,lens_eta = self.getXiEta(epoch)
	
		#set the source tanget plane coords
		#defined by the lens reference position.
		source.xi_0,source.eta_0 = tp.s2tp(source.ra_0,source.dec_0,self.ra_0,self.dec_0)

		source_xi,source_eta = source.getXiEta(epoch)
	
  
		return np.hypot(lens_xi-source_xi, lens_eta-source_eta)
	
	def getMinTime(self,source):
		"""
		Get the time of closest approach between 
		the skyobj and a source.

		Args:
			source (skyobj): source skyobj to 
					 to get closest approach
					 time for.
					
		Returns: 
			minTime (float): The time of closest
					 approach. [Decimal Years]
		"""
	
		minimum = minimize_scalar(self.getSeparation,args=(source))
		return minimum.x

	def getMinDist(self,source):
		"""
                Get the closest approach
		separation between the skyobj 
		and source.
	
		Args:
			source (skyobj): source skyobj to
                                         to get closest separation
                                         distance for.
		Returns:

			minDist (float): Distance of Closest
					 Approach [mas]
		"""

		minTime = self.getMinTime(source)
		return self.getSeparation(minTime,source)

	def getCentroidShift(self,source,lensMass):
		"""Calculates the astrometric centroid 
		shift for a given lens Mass.

		"""
		
		lensDist = m.get_dist(self.parallax)
		minSep = self.getMinDist(source)		

		return m.get_centroid_shift(lensMass,lensDist,minSep,lensMag=self.gMag,sourceMag=source.gMag)
 	
	def getCentriodShift_at(self,source,lensMass,sep):

		lensDist = m.get_dist(self.parallax)

		return m.get_centroid_shift(lensMass,lensDist,sep,lensMag=self.gMag,sourceMag=source.gMag)	
	

refepoch = Time(2015.0,format='jyear')
print(refepoch.jd)


lens = skyobj(id=1,ra=176.4549073, dec=-64.84295714, pmra=2662.03572627, pmdec=-345.18255501, parallax=215.782333,epoch=2015.0)
source1 = skyobj(id=2,ra=176.46360456, dec=-64.84329779, pmra=-19.5, pmdec=-17.89999962,epoch=2015.0)



refposRa,refposDec = lens.getRaDec(refepoch.decimalyear)

print(refposRa)
print(refposDec)

time = np.linspace(2018.86480945,2020.893842442573,num=1000)
astrotime = Time(time,format='jyear')
print(astrotime.jd)

ras = np.array([])
decs = np.array([])
raSources = np.array([])
decSources = np.array([])

#for t in time:
#	ra,dec = lens.getRaDec(t)
#	raSource,decSource = source.getRaDec(t)
#	ras = np.append(ras,ra)
#	decs = np.append(decs,dec)
#	raSources = np.append(raSources,raSource)
#	decSources = np.append(decSources,decSource)


#plt.plot((ras-refposRa)*3600.0,(decs-refposDec)*3600.0,label='lens')
#plt.plot((raSources-refposRa)*3600.0*np.cos(np.deg2rad(refposDec)),(decSources-refposDec)*3600.0*np.cos(np.deg2rad(refposDec)),label='source')

#plt.xlabel('relative ra*cos(dec) position [arcseconds]')
#plt.ylabel('relative dec position [arcseconds]')
#plt.ylim(-0.6,0.6)
#plt.title('lawd37 2019.9pm1yr')
#plt.legend()
#plt.show()


 


#lens = skyobj(id=1,ra=176.454907296219, dec=-64.842957135494, pmra=2662.03572627, pmdec=-345.18255501, parallax=215.78,epoch=2015.0)
#source = skyobj(id=2,ra=176.46360456073, dec=-64.8432977866831, pmra=-19.5, pmdec=-17.89999962,epoch=2015.0)

print(lens.getMinTime(source1))
print(lens.getMinDist(source1))


#print("Centroid Shift a Closest Approach: "+ str(lens.getCentroidShift(source,0.75)))
#print("Centriod Shift at 300 mas: " + str(lens.getCentriodShift_at(source,0.75,300.0)))
