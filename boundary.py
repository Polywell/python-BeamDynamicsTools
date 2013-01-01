from numpy import *
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D

class boundary:

	def __init__(self,Rb,Zb,cw=-1):
		Cvec = []; # Corner Locations 
		Mvec = []; # Middle of line locations
		Tvec = []; # Tangent vectors of border
		Nvec = []; # Normal Vectors of border
		self.Rb = Rb
		self.Zb = Zb
		for i in range(len(Rb)):
			Cvec.append(array([Rb[i],Zb[i]]))
			Mvec.append(array([(Rb[i]+Rb[i-1])/2,(Zb[i]+Zb[i-1])/2]))
			Tvec.append((array([Rb[i]-Rb[i-1],Zb[i]-Zb[i-1]])))
			Nvec.append((array([-Tvec[-1][1],Tvec[-1][0]])))
			Nvec[-1] = cw * Nvec[-1] / 10 / sqrt(Nvec[-1][0]**2 + Nvec[-1][1]**2)
		for i in range(len(Rb)):
			print Cvec[i-1]-Cvec[i-2]
		self.Cvec = Cvec
		self.Mvec = Mvec
		self.Tvec = Tvec
		self.Nvec = Nvec
		self.Nv = len(Nvec)
		print 'boundary initialized'

	def Plot2D(self,FIG=1):
		pl.figure(FIG)
		Cvec = self.Cvec; Mvec = self.Mvec; Tvec = self.Tvec; Nvec = self.Nvec

		for i in range(self.Nv):
			pl.plot([Cvec[i][0],Cvec[i-1][0]],[Cvec[i][1],Cvec[i-1][1]])
			pl.plot([Nvec[i][0]+Mvec[i][0],Mvec[i][0]],[Nvec[i][1]+Mvec[i][1],Mvec[i][1]])
			pl.plot(Mvec[i][0],Mvec[i][1],'o')

		pl.xlim(0.3-1,0.3+1)
		pl.ylim(-1,1)

	def InVolume(self,r):
		x0 = [sqrt(r[0]*r[0] + r[1]*r[1]) ,r[2]]
		IN = True; i=-1;
		D1 = []
		while (IN == True and i<self.Nv-1):
			D1 = x0-self.Cvec[i-1]
			D2 = x0-self.Cvec[i]
			if (dot(D1,self.Tvec[i-1])>0 and dot(D2,self.Nvec[i-1])<0):
				if dot(D1,self.Nvec[i])<0:
					IN = False
			i = i+1
		return IN

	def Xboundary(self,r0,r1):
		x0 = [sqrt(r0[0]*r0[0] + r0[1]*r0[1]) ,r0[2]]
		x1 = [sqrt(r1[0]*r1[0] + r1[1]*r1[1]) ,r1[2]]
		IN = True; i=-1; Di1 = []; Di2 = []; Df = []; NORM=[]
		while (IN == True and i<self.Nv-1):
			Di1 = x0-self.Cvec[i-1]
			Di2 = x0-self.Cvec[i]
			Df = x1-self.Cvec[i-1]
			if dot(Di1,self.Tvec[i-1])>0 and dot(Di2,self.Tvec[i-1])<0:
				if dot(Di1,self.Nvec[i])>0 and dot(Di2,self.Nvec[i])>0:
					if dot(Df,self.Nvec[i])<0 and dot(Df,self.Nvec[i])<0:
						IN = False
						NORM = self.Nvec[i]
			i=i+1
		return NORM

	def Figure3D(self,FIG=1):
		fig = pl.figure(FIG)
		ax = Axes3D(fig)
		return ax

	def Plot3D(self,ax,Nt=16,Color='b',PhiMin=-pi/8,PhiMax=3*pi/2):
		#Phi = linspace(0,2*pi*(1-1/Nt),Nt)
		Phi = linspace(PhiMin,PhiMax,Nt)
		xp=[]; yp=[]; zp=[];
		for i in range(Nt):
			Nr = len(self.Rb)+1
			x=[]; y=[]; z=[];
			for j in range(Nr):
				x.append(cos(Phi[i])*self.Rb[j-1])
				y.append(sin(Phi[i])*self.Rb[j-1])
				z.append(self.Zb[j-1])
			ax.plot(x,y,z,Color)
			xp.append(x); yp.append(y); zp.append(z)
		
		Nc = Nt*10
		Phi = linspace(PhiMin,PhiMax,Nc)
		xt=[]; yt=[]; zt=[];
		for j in range(Nr):
			for i in range(Nc):
				xp.append(cos(Phi[i])*self.Rb[j-1])
				yp.append(sin(Phi[i])*self.Rb[j-1])
				zp.append(self.Zb[j-1])
			ax.plot(xp[-Nc:-1], yp[-Nc:-1], zp[-Nc:-1],Color)
		pl.xlim(-1,1); pl.ylim(-1,1)
		return ax
		#return xp,yp,zp,xt,yt,zt



# Test Case

def TestInVolume(Bound,Ni):
	pl.figure(1)
	Xrand = array([0.0,0.0])
	for i in range(Ni):
		Xrand[0] = random.rand()
		Xrand[1] = random.rand()*2 - 1
		print i
		if Bound.InVolume(Xrand):
			pl.plot(Xrand[0],Xrand[1],'.g')
		else:
			pl.plot(Xrand[0],Xrand[1],'.r')

Rb = [ 0.2 , 0.25, 0.4 , 0.6 , 0.8 , 0.8 , 0.6 , 0.4 , 0.25, 0.2 ]
Zb = [-0.55,-0.6 ,-0.6 ,-0.5 ,-0.2 , 0.2 , 0.5 , 0.6 , 0.6 , 0.55]


Wall = boundary(Rb,Zb)
#Wall.Plot2D(1)

#TestInVolume(Wall,1000)

#Wall.Plot3D(Nt=16,FIG=2)
pl.show()

