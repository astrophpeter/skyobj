#############################
##        skyobj           ##
##    A class to find      ##
## microlensing candidates ##
## @author Peter McGill    ##
## @email pm625@cam.ac.uk  ##
#############################

class skyobj(object):


	def __init__(self,id=None,ra=None,dec=None,epoch=None,pmra=None,pmdec=None,parallax=None):
		"""

		

		"""
		
		
		self.id  = id
		self.ra = ra
		self.dec = dec
		self.epoch = epoch
		
		#set proper motions and parallax to zero if
		#not specified.
		self.pmra = pmra if pmra else 0.0
		self.pmdec = pmdec if pmdec else 0.0
		self.parallax = parallax if parallax else 0.0
		


