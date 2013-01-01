import pylab as pl
from pylab import det
from numpy import *
#import scipy as 

import math
#======================================================================================================================
#                                   Beam Class stores Beam parameters
#======================================================================================================================

class beam:
	# inputs:
	# sigma = 6x6 sigma matrix
	# s0 = 3x3 matrix for local beam coordinate system
	def __init__(self, sigma0,s0,E0=0.9,m0=2.0,z0=1.0):
		self.Sigma = [sigma0]
		self.SVector = s0
		self.m0 = m0
		self.Z0 = z0
		beta = math.sqrt(2*E0*1.0e6/(m0*938.5))
		self.Beta = beta
		self.Ellipse = [ellipse(sigma0)]
		self.SCoordinate = [0]
		#self.Gamma = 1.0/sqrt(1.0-beta**2.0)

	# Advances sigma forward by 1 step using transfer matrix M
	def Advance(self,M,ds=1e-3): 
		for i in range(Ni):
#			self.Ellipse[0].Plot()
#			pl.show()
			SIGMA = self.Sigma[-1]
			SIGMA = M*SIGMA*M.T
			SCOORD = self.SCoordinate[-1] + ds
			self.Sigma.append(SIGMA)
			self.SCoordinate.append(SCOORD)

	# Advances sigma forward by Ni steps using transfer matrix M
	def AdvanceN(self,M,ds=1e-3,Ni=10): 
		for i in range(Ni):
#			self.Ellipse[0].Plot()
#			pl.show()
			SIGMA = self.Ellipse[-1].Sigma
			SIGMA = M*SIGMA*M.T
			SCOORD = self.SCoordinate[-1] + ds
			self.Ellipse.append(ellipse(SIGMA))
			self.SCoordinate.append(SCOORD)

	def Trace(self,FIG=1):
		self.X = []; self.Y = []; self.Z = []
		for i in range(len(self.SCoordinate)):
			self.X.append(self.Ellipse[i].WidthX)
			self.Y.append(self.Ellipse[i].WidthY)
			self.Z.append(self.Ellipse[i].WidthZ)
		pl.figure(FIG)
		pl.plot(array(self.SCoordinate)*1e3,self.X)
		pl.plot(array(self.SCoordinate)*1e3,self.Y)
		pl.plot(array(self.SCoordinate)*1e3,self.Z)
		pl.xlabel('S-Coordinate [mm]'); pl.ylabel(r'Beam Radius r$_{x,y,z}$ [mm]')
		pl.legend(('X','Y','Z'))

#======================================================================================================================
#                                   Generate Sigma Matrix  from Twiss Parameters
#======================================================================================================================

#def Sigma2D(Ax,Bx,Ex)

def Sigma(Ax,Bx,Ex,Ay,By,Ey,Az,Bz,Ez):
	Cx = (1+Ax**2)/Bx
	Cy = (1+Ay**2)/By
	Cz = (1+Az**2)/Bz

	SIGMA = matrix([
	[ Bx*Ex ,-Ax*Ex,   0   ,   0   ,  0    ,   0   ],
	[-Ax*Ex , Cx*Ex,   0   ,   0   ,  0    ,   0   ],
	[   0   ,   0  , By*Ey ,-Ay*Ey ,  0    ,   0   ],
	[   0   ,   0  ,-Ay*Ey , Cy*Ey ,  0    ,   0   ],
	[   0   ,   0  ,   0   ,   0   , Bz*Ez ,-Az*Ez ],
	[   0   ,   0  ,   0   ,   0   ,-Az*Ez , Cz*Ez ]])

	return SIGMA

#======================================================================================================================
#                                   Defines Class for 6-D ellispsoid 
#======================================================================================================================

class ellipse:
	def __init__(self,SIG):
		self.Sigma = SIG
		self.SigX = self.Sigma[0:2,0:2];
		self.SigY = self.Sigma[2:4,2:4];
		self.SigZ = self.Sigma[4:6,4:6];

		# self.EpsilonX = self.Sigma[0,0]*self.Sigma[1,1] - self.Sigma[0,1]**2
		self.EmittenceX = sqrt(math.fabs(det(self.SigX)))
		self.EmittenceY = sqrt(math.fabs(det(self.SigY)))
		self.EmittenceZ = sqrt(math.fabs(det(self.SigZ)))

		self.TwissXX1 = array([-(self.SigX[0,1]),self.SigX[0,0],self.SigX[1,1],self.EmittenceX**2]/self.EmittenceX)
		self.TwissYY1 = array([-(self.SigY[0,1]),self.SigY[0,0],self.SigY[1,1],self.EmittenceY**2]/self.EmittenceY)
		self.TwissZZ1 = array([-(self.SigZ[0,1]),self.SigZ[0,0],self.SigZ[1,1],self.EmittenceZ**2]/self.EmittenceZ)

		self.WidthX = sqrt(self.TwissXX1[1]*self.TwissXX1[3])
		self.WidthY = sqrt(self.TwissYY1[1]*self.TwissYY1[3])
		self.WidthZ = sqrt(self.TwissZZ1[1]*self.TwissZZ1[3])

		self.EmittenceXY = sqrt( det(matrix([[SIG[0,0],SIG[0,2]] ,[SIG[2,0],SIG[2,2]] ])) )
		self.TwissXY = array([-SIG[0,2],SIG[0,0],SIG[2,2],self.EmittenceXY**2])/self.EmittenceXY

#		self.XMax = [sqrt(self.TwissXX1[1]*self.TwissXX1[3]),sqrt(self.TwissXX1[2]*self.TwissXX1[3])];
#		self.YMax = [sqrt(self.TwissYY1[1]*self.TwissYY1[3]),sqrt(self.TwissYY1[2]*self.TwissYY1[3])];
#		self.ZMax = [sqrt(self.TwissZZ1[1]*self.TwissZZ1[3]),sqrt(self.TwissZZ1[2]*self.TwissZZ1[3])];



	def Plot(self,NPoints=1000,FIG=0,Mod='-'):
#		TwissList = [self.TwissXX1,self.TwissYY1,self.TwissZZ1]
#		Xlab = ['X','Y','Z']; Ylab = ['dx/ds','dy/ds','dz/ds'];
#		pl.figure(FIG)
#		XPoints = zeros((NPoints,3),float); YPoints = zeros((NPoints,3),float)
#		for j in range(3):
#			TWISS = TwissList[j]
#			XPoints[:,j],YPoints[:,j] = GenerateEllipse(TWISS,NPoints)
#			pl.subplot(2,2,j+1);
#			pl.plot(XPoints[:,j],YPoints[:,j],Mod); pl.xlabel(Xlab[j]); pl.ylabel(Ylab[j]);
		pl.figure(FIG)
		X,Y = GenerateEllipse(self.TwissXX1,NPoints)
		pl.subplot(2,2,1); pl.plot(X,Y,Mod); pl.xlabel('X [mm]');  pl.ylabel('dx/ds [mrad]');

		X,Y = GenerateEllipse(self.TwissYY1,NPoints)
		pl.subplot(2,2,2); pl.plot(X,Y,Mod); pl.xlabel('Y [mm]');  pl.ylabel('dY/ds [mrad]');

		X,Y = GenerateEllipse(self.TwissZZ1,NPoints)
		pl.subplot(2,2,3); pl.plot(X,Y,Mod); pl.xlabel('Z [mm]');  pl.ylabel('dZ/ds [mrad]');

		X,Y = GenerateEllipse(self.TwissXY,NPoints)
		pl.subplot(2,2,4); pl.plot(X,Y,Mod); pl.xlabel('X [mm]');  pl.ylabel('Y [mm]');
		pl.xlim([-2,2]); pl.ylim([-2,2])


def GenerateEllipse(TWISS,NPoints=1000):
	Theta = linspace(0,2*pi,NPoints);
	XPoints = zeros((NPoints),float); YPoints = zeros((NPoints),float)
	m11=math.sqrt(math.fabs(TWISS[1]));
	m21=-TWISS[0]/math.sqrt(math.fabs(TWISS[1]));
	m22=1/math.sqrt(math.fabs(TWISS[1]));
	Radius=math.sqrt(math.fabs(TWISS[3]))#/pi;
	m12=0;
	PHI = arctan(2.0*TWISS[0]/(TWISS[2]-TWISS[1]))/2.0
	for i in range(NPoints):
		XPoints[i] = Radius*(m11*cos(Theta[i]) + m12*sin(Theta[i]))
		YPoints[i] = Radius*(m21*cos(Theta[i]) + m22*sin(Theta[i]))
	return XPoints,YPoints

#======================================================================================================================
#                               Generate transfer matricies
#======================================================================================================================
def Drift(ds=1e-3):
	Mdrift = matrix([
	[1, ds, 0 , 0 , 0 , 0 ],
	[0 , 1 , 0 , 0 , 0 , 0 ],
	[0 , 0 , 1 , ds, 0 , 0 ],
	[0 , 0 , 0 , 1 , 0 , 0 ],
	[0 , 0 , 0 , 0 , 1 , ds],
	[0 , 0 , 0 , 0 , 0 , 1 ]],float)
	#print Mdrift
	return Mdrift

def ThinLens(fx=1.0,fy=-1.0):
	MLens = matrix([
	[1,    0,  0 ,  0 , 0 , 0 ],
	[1.0/fx, 1 , 0 ,  0 , 0 , 0 ],
	[0 ,   0 , 1 ,  0 , 0 , 0 ],
	[0 ,   0 ,1.0/fy, 1 , 0 , 0 ],
	[0 ,   0 , 0 , 0 , 1 , 0 ],
	[0 ,   0 , 0 , 0 , 0 , 1 ]],float)
	return MLens


def PMQ(ds=1e-3,GradB=45.0,m0=2.0,z0=1.0,beta=0.03097,gamma=1.000499):
	BR = (m0*1.67e-27)/(z0*1.6022e-19)*2.998e8*beta*gamma  # BR = m0*c*beta*gamma/q (magnetic rigidity)
	k2 = GradB/BR
	MPMQ = matrix([
	[   1 , 0 ,  0  , 0 , 0 , 0 ],
	[-k2*ds,1 ,  0  , 0 , 0 , 0 ],
	[   0 , 0 ,  1  , 0 , 0 , 0 ],
	[   0 , 0 ,k2*ds, 1 , 0 , 0 ],
	[   0 , 0 ,  0  , 0 , 1 , 0 ],
	[   0 , 0 ,  0  , 0 , 0 , 1 ]],float)
	return MPMQ


def BField3D(ds=1e-3,beta=0.03097,B0=matrix([[0],[0.1],[0]],float),S0=matrix([[1,0,0],[0,1,0],[0,0,1]],float),m=2,q=1):
	K = 2*938.7e6*beta/2.998e8*ds

	B = K*(S0.T*B0)

	BFIELD = matrix([
	[   1  ,  0   ,   0  ,   0  ,  0  ,   0   ],
	[   0  ,  1   ,   0  ,  B[2],  0  , -B[1] ],
	[   0  ,  0   ,   1  ,   0  ,  0  ,   0   ],
	[   0  ,-B[2] ,   0  ,   1  ,  0  ,  B[0] ],
	[   0  ,  0   ,   0  ,   0  ,  1  ,   0   ],
	[   0  , B[1] ,   0  , -B[0],  0  ,   1   ]],float)
	return BFIELD

def RotationXY(Theta):
	C = math.cos(Theta)
	S = math.sin(Theta)
	Mrotate = matrix([
	[C , 0 ,-S , 0 , 0 , 0 ],
	[0 , C , 0 ,-S , 0 , 0 ],
	[S , 0 , C , 0 , 0 , 0 ],
	[0 , S , 0 , C , 0 , 0 ],
	[0 , 0 , 0 , 0 ,1.0, 0 ],
	[0 , 0 , 0 , 0 , 0 ,1.0]],float)
	#print Mdrift
	return Mrotate

def Iterate(M,S0,Ri=0,ds=1e-3,Ni=100):
	RNew = zeros((Ni,3),float)
	for i in range(Ni):
		S0 = M*S0*M.T
#		RNew = 
	if Ri==0:
		return S0
	else:
		R0 = vstack((Ri,RNew))
		return S0,R0

	#Norm2 = (VecS[0]**2 + VecS[1]**2 + VecS[5])
	#if Norm2 != 1:
	#	VecS = VecS*(1/math.sqrt(Norm2))
 
	#Ax = (B[0]*VecS[3]+B[1]*VecS[4]+B[2]*VecS[5])*VecS[0]
	#Ay = (B[0]*VecS[3]+B[1]*VecS[4]+B[2]*VecS[5])*VecS[1]
	#Az = (B[0]*VecS[3]+B[1]*VecS[4]+B[2]*VecS[2])*VecS[2]
	


#======================================================================================================================
#=============== Extra Code ===========================================================================================
#======================================================================================================================



#	def New(self, TwissNew):
#		self.Twiss = TwissNew

# Transform Twiss Parameters using matrix transformation M (2x2)
#	def Transform(self, M = pl.array([[1,0],[0,1]],'f'):
#		m11 = M[0,0];  m12=M[0,1];  m21=M[1,0];  m22=M[1,1];
#		MT = pl.array([[-m11*m21,  m11*m22+m12*m21,  -m12*m22,0],[m11*m11,  -2*m11*m12,  m12*m12, 0],[m21*m21,  -2*m21*m22,  m22*m22, 0],[0,0,0,1]],'f')
		#self.Twiss = 

# (1) defines N points circle of Radius sqrt(emittance), 
# (2) then transforms it to an ellipse with defined by twiss parameters,
# (3) plots the ellipse points
