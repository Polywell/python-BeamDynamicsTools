#import scipy as sp
from numpy import *

# Br = B0*R0/R * (1 + f(r,z,phi))
# Bz = BZ0

class bfield:
	# Br =  ra
	def __init__(self,B0,R0,B0z=0.0,fR=0,fz=0):
		self.B0 = B0
		self.B0z = B0z
		self.R0 = R0
		self.fR = fR
		self.fz = fz
		print 'bfield initialized'

	def localRZP(self,R,Z,Phi):
		Btor = self.B0 * self.R0 / R * (1+self.fR)
		Bx = Btor*sin(Phi)
		By = Btor*cos(Phi)
		Bz = self.B0z
		return([Bx,By,Bz])

	def local(self,r):
		R = sqrt(r[0]**2+r[1]**2)
		Phi = arctan(r[1]/r[0])
		Btor = self.B0 * self.R0 / R  * (1+self.fR) 
		Bx = Btor*sin(Phi)
		By = Btor*cos(Phi)
		Bz = self.B0z
		return(array([Bx,By,Bz]))

