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
		
		self.xi,self.eta = self.s2tp(ra,dec)
	
				
		#set proper motions and parallax to zero if
		#not specified.
		self.pmra = pmra if pmra else 0.0
		self.pmdec = pmdec if pmdec else 0.0
		self.parallax = parallax if parallax else 0.0
		



	def s2tp(self,ra, dec):
    		"""
		Convert from spherical coordinate system
		to tagent plane coordinates
		"""
 
		#Set the position of the tagent plane
                #at the position of the lens
		raz = self.ra
		decz = self.dec
 
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
		xi = ((180/np.pi)*3600)*_cdecj*_sradifj/_denomj
		eta = ((180/np.pi)*3600)*(_sdecj*_cdecz-_cdecj*_sdecz*_cradifj)/_denomj
 
		return xi, eta
