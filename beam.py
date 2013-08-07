# Beam.py

from numpy import *
#import scipy as sp
import pylab as pl
from numpy.linalg import inv,norm

class beam:
	# inputs:
	# sigma = 6x6 sigma matrix
	# s0 = 3x3 matrix for local beam coordinate system
	def __init__(self,Trajectory,Sigma0):
		self.Sigma = [Sigma0]

		self.q0 = Trajectory.q0
		self.c0 = Trajectory.c0
		self.m0 = Trajectory.m0
		self.I0	= Trajectory.I0
		self.Frequency = Trajectory.Frequency
#		self.Z0 = Trajectory.z0
		self.A0 = Trajectory.A0
#		self.Beta = Trajectory.Beta
#		self.Ellipse = [ellipse(sigma0)]
		self.r = Trajectory.r
		self.v0 = Trajectory.v0
		self.v = Trajectory.v
		self.Beta = Trajectory.Beta
		self.beta = Trajectory.beta
		self.gamma = Trajectory.gamma
		self.a = Trajectory.a
		self.B = Trajectory.B
		self.s = Trajectory.s
		self.dS = Trajectory.dS
		self.dt = Trajectory.dt
		self.BasisM3 = Trajectory.BasisM3
		self.BasisM6 = Trajectory.BasisM6
		self.NormalV = Trajectory.NormalV
		self.IncidentV = Trajectory.IncidentV

		# lists of matrices for reverse calculations
		self.RevSigma = []
		self.RevTransferM = []

#		self.e1=Trajectory.e1
#		self.e2=Trajectory.e2
#		self.e3=Trajectory.e3

	def Trace(self):
		Ni = len(self.r)
		self.TransferM = []
		for i in range(Ni):
			D = self.Drift(self.dS[i])
			# Mb is the matrix form of Acc = (q/m) v x B
			S = self.BasisM3[i] #matrix(identity(6))
			B = self.BMatrix(S,self.B[i],self.dS[i])
			#print B
			Q = self.SpaceCharge(self.Sigma[i],self.dS[i],self.beta[i],self.gamma[i])
			M = B*Q
			self.TransferM.append(M)
			self.Sigma.append( M * self.Sigma[-1] * M.T )
			print i
		
	def ReverseTrace(self,SigmaF):
		Ni = len(self.r)
		RevTransferM = []
		RevSigma = [SigmaF]
		for i in range(Ni-1,-1,-1):
			D = self.Drift(self.dS[i])
			# Mb is the matrix form of Acc = (q/m) v x B
			S = self.BasisM3[i] #matrix(identity(6))
			B = self.BMatrix(S,self.B[i],self.dS[i])
			M = inv(B)
			RevTransferM.append(M)
			RevSigma.append( M * RevSigma[-1] * M.T )
			print i
		self.RevSigma.append(RevSigma)
		self.RevTransferM.append(RevTransferM)

	def Drift(self,ds=1e-3):
		Mdrift = matrix([
		[1,  ds, 0 , 0 , 0 , 0 ],
		[0 , 1 , 0 , 0 , 0 , 0 ],
		[0 , 0 , 1 , ds, 0 , 0 ],
		[0 , 0 , 0 , 1 , 0 , 0 ],
		[0 , 0 , 0 , 0 , 1 , ds],
		[0 , 0 , 0 , 0 , 0 , 1 ]],float)
		#print Mdrift
		return Mdrift

#	def BMatrix(self,B):
#		k=-(self.q0/self.m0*(self.dt/self.v0)/self.dS)
#		Mb = matrix([
#		[   1  ,   0   ,   0  ,    0  ,  0  ,   0    ],
#		[   0  ,   1   ,   0  , k*B[2],  0  ,-k*B[1] ],
#		[   0  ,   0   ,   1  ,    0  ,  0  ,   0    ],
#		[   0  ,-k*B[2],   0  ,    1  ,  0  , k*B[0] ],
#		[   0  ,   0   ,   0  ,    0  ,  1  ,   0    ],
#		[   0  , k*B[1],   0  ,-k*B[0],  0  ,   1    ]],float)
#
#		return Mb

	def BMatrix(self,Basis,Bin,dS):

		Bperp = matrix([[dot(Bin,Basis[:,0])],[dot(Bin,Basis[:,1])],[0.0]])

		B0 = norm(Bperp) 
		if B0!=0:
			r = (self.m0*self.v0)/(self.q0*B0) 
			da = dS/r
			C = cos(da)
			S = sin(da)

			dA = arctan(Bperp[0,0]/Bperp[1,0])
			Cr = cos(dA)
			Sr = sin(dA)

			R0 = matrix([
			[ Cr , 0  , Sr , 0  , 0  ,  0  ],
			[ 0  , Cr , 0  , Sr , 0  ,  0  ],
			[-Sr , 0  , Cr , 0  , 0  ,  0  ],
			[ 0  ,-Sr , 0  , Cr , 0  ,  0  ],
			[ 0  , 0  , 0  , 0  , 1  ,  0  ],
			[ 0  , 0  , 0  , 0  , 0  ,  1  ]],float)

			Mb = matrix([
			[ 1  , dS , 0  , 0 , 0  ,  0  ],
			[ 0  , 1  , 0  , 0 , 0  ,  0  ],
			[ 0  , 0  , C  ,r*S, 0  ,r-r*C],
			[ 0  , 0  ,-S/r, C , 0  ,  S  ],
			[ 0  , 0  , 0  , 0 , 1  , dS  ],
			[ 0  , 0  , 0  , 0 , 0  ,  1  ]],float)

			Mb = R0.T * Mb * R0
#			Mb = R0 * Mb * R0.T
		else:
			Mb = self.Drift(self.dS)

		return Mb

	def BMatrix0(self,Vin,Bin):
		Bn = (self.q0/self.m0/self.v0) * Bin #/ 1e3 #(self.dt/self.v0)
		Vn = Vin/self.v0  * self.dS

		Fxy =  Vn[0]*Bn[1]
		Fyx = -Vn[1]*Bn[0]
		Fyz =  Vn[1]*Bn[2]
		Fzy = -Vn[2]*Bn[1]
		Fzx =  Vn[2]*Bn[0]
		Fxz = -Vn[0]*Bn[2]

		Mb = matrix([
		[ 1  , 0 , 0  , 0 , 0  , 0 ],
		[ 0  , 1 , 0  ,Fyz, 0  ,Fyx],
		[ 0  , 0 , 1  , 0 , 0  , 0 ],
		[ 0  ,Fxz, 0  , 1 , 0  ,Fzx],
		[ 0  , 0 , 0  , 0 , 1  , 0 ],
		[ 0  ,Fxy, 0  ,Fyx, 0  , 1 ]],float)
#		Mb = matrix(identity(6))
		return Mb

	def SpaceCharge(self,SigmaIN,dS,beta,gamma):
		Sigma = matrix(SigmaIN)

		# Rotate upright in XY Plane
		ThetaXY = 0.5 * arctan(2*Sigma[0,2]/(Sigma[2,2]-Sigma[0,0]))
		C = cos(ThetaXY); S = sin(ThetaXY) 
		Rxy = matrix([
		[  C  ,  0  , -S  ,  0  , 0  ,  0  ],
		[  0  ,  C  ,  0  , -S  , 0  ,  0  ],
		[  S  ,  0  ,  C  ,  0  , 0  ,  0  ],
		[  0  ,  S  ,  0  ,  C  , 0  ,  0  ],
		[  0  ,  0  ,  0  ,  0  , 1  ,  0  ],
		[  0  ,  0  ,  0  ,  0  , 0  ,  1  ]],float)
#		Sigma = Rxy * Sigma * Rxy.T

		# Rotate upright in YZ Plane
		ThetaYZ = 0.5 * arctan(2*Sigma[2,4]/(Sigma[4,4]-Sigma[2,2]))
		C = cos(ThetaYZ); S = sin(ThetaYZ) 
		Ryz = matrix([
		[  1  ,  0  ,  0  ,  0  ,  0  ,  0  ],
		[  0  ,  1  ,  0  ,  0  ,  0  ,  0  ],
		[  0  ,  0  ,  C  ,  0  , -S  ,  0  ],
		[  0  ,  0  ,  0  ,  C  ,  0  , -S  ],
		[  0  ,  0  ,  S  ,  0  ,  C  ,  0  ],
		[  0  ,  0  ,  0  ,  S  ,  0  ,  C  ]],float)
#		Sigma = Ryz * Sigma * Ryz.T

		# Rotate upright in XZ Plane
		C = 1.0; S = 0.0;
		ThetaZX = 0.5 * arctan(2*Sigma[4,0]/(Sigma[0,0]-Sigma[4,4]))
		C = cos(ThetaZX); S = sin(ThetaZX)
		Rzx = matrix([
		[  C  ,  0  ,  0  ,  0  , -S  ,  0  ],
		[  0  ,  C  ,  0  ,  0  ,  0  , -S  ],
		[  0  ,  0  ,  1  ,  0  ,  0  ,  0  ],
		[  0  ,  0  ,  0  ,  1  ,  0  ,  0  ],
		[  S  ,  0  ,  0  ,  0  ,  C  ,  0  ],
		[  0  ,  S  ,  0  ,  0  ,  0  ,  C  ] ],float)
#		Sigma = Rzx * Sigma * Rzx.T

		# Beam semiaxes
		rx = 0.005
		ry = 0.005
		rz = 0.005

		# normalized radial component for form factor fit
		p = gamma*rz/sqrt(rx*ry)

		# Form factor f polyfit Coefficient
		C0 = [0.32685993, -1.10422029, 1.64157723, -1.52987752, 0.99919503]
		f = polyval(C0,p)

		# Constants for E-Field Calcuation
		k = 1.0/(4*pi*8.85e-12)
		Q = 3.0*self.I0/(self.Frequency)

		# Calculate E-Field Components
		Ex = (k*Q/gamma**2) * (1.0 - f) / (rx*(rx+ry)*rz) 
		Ey = (k*Q/gamma**2) * (1.0 - f) / (ry*(rx+ry)*rz)
		Ez = (k*Q) * f/(rx*ry*rz)

		# Constant to convert E-field to delta Xi'
		d = (self.q0 * dS) / (self.m0 * self.c0**2 * beta)

		# Apply SPace Charge Impulses to momentum		
		ME = matrix([
		[ 1  , 0  , 0  , 0  , 0  ,  0  ],
		[d*Ex, 1  , 0  , 0  , 0  ,  0  ],
		[ 0  , 0  , 1  , 0  , 0  ,  0  ],
		[ 0  , 0  ,d*Ey, 1  , 0  ,  0  ],
		[ 0  , 0  , 0  , 0  , 1  ,  0  ],
		[ 0  , 0  , 0  , 0  ,d*Ez,  1  ]],float)
#		Sigma = ME * Sigma * ME.T
#		print d*Ex,d*Ey,d*Ez

#		print Rxy
#		print Ryz
#		print Rzx
#		print ME
#		print Sigma
#		print ME
#		print ThetaXY, ThetaYZ, ThetaZX

		# Rotate back to orignial orientation
#		Sigma = (Rxy.T * Ryz.T * Rzx.T) * Sigma * (Rzx * Ryz * Rxy)
		return (Rzx.T * Ryz.T * Rxy.T) * ME * ( Rxy *Ryz * Rzx )



