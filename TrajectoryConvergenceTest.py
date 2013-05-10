from numpy import *
from boundary import *
from bfield import *
from trajectory import *
import pylab as pl

Rb = [   0.1,   0.1, 100.0, 100.0]
Zb = [-100.0, 100.0, 100.0,-100.0]

Vessel = boundary(Rb,Zb)
#Vessel.Plot2D(0)



if True:
	B = bfieldc(B0=0.1)
	d0 = 10.0
	dS = logspace(-5,-2,15)
	dr = []; T=[];
	for i in range(len(dS)):
		T.append(trajectory(Vessel,B,r0=[20.0,0.0,0.0],v0=[0.0,0.0,1.0],dS=dS[i],Nmax=round(d0/dS[i])) )
		RL = (T[-1].m0*T[-1].v0) / (T[-1].q0*B.B0)
		R = T[-1].r[-1] - array([20.0-RL,0,0.0])
		dr.append( sqrt(R[0]**2+R[1]**2+R[2]**2)*(d0/T[-1].s[-1]) - RL)  # -RL)/d0 ) #/T.s[-1]*d0 - RL)
		#T.Plot2D()
	pl.figure(1); pl.loglog(dS,dr,'.')
	pl.xlabel(r'Step Size $\Delta$S [m]'); pl.ylabel(r'$\Delta R/S$')
	pl.title(r'Error / Arc length')

pl.figure(2); pl.loglog(dS,dr/RL,'.')
pl.xlabel(r'Step Size $\Delta$S [m]'); pl.ylabel(r'${\Delta R}/{R S}$ [1/m]')
pl.title(r'Normalized Bending Radius Error per Arc Length')



# Test Varying Total Distance S
if False:
	B = bfieldc(B0=0.1)
	T = trajectory(Vessel,B,r0=[20.0,0.0,0.0],v0=[0.0,0.0,1.0],Nmax=100000)
	#T.Plot2D()

	x=[]; y=[]; z=[]; S=[]; r=[]; R=[]; rN=[];
	RL = (T.m0*T.v0) / (T.q0*B.B0)  # mV/qB
	R0 = array([20.0-RL,0,0.0]) 

	for i in range(len(T.r)):
		R.append(T.r[i] - R0)

	for i in range(len(T.r)):
		x.append(R[i][0])
		y.append(R[i][1])
		z.append(R[i][2])
		S.append(T.s[i])
		r.append( sqrt(x[-1]**2 +y[-1]**2 + z[-1]**2) )
		rN.append((r[-1]-RL)/T.s[i])

	pl.figure(1); pl.plot(x,z);
	pl.figure(2); pl.plot(S,1-r/RL);
	pl.xlabel('S Coordinate'); pl.ylabel(r'Error $\epsilon $'); pl.title(r'$\epsilon = \Delta $r/Rc')
	pl.figure(3); pl.loglog(S,1-r/RL);
	pl.xlabel('S Coordinate'); pl.ylabel(r'$\epsilon $'); pl.title(r'$\epsilon = \Delta $r/Rc') 
	pl.figure(4); pl.plot(S,array(rN))
	pl.xlabel('S Coordinate'); pl.ylabel(r'Normalized Error $\epsilon_N $'); pl.title(r'$\epsilon_N = \Delta$ r/S')  
	pl.figure(5); pl.semilogx(S,array(rN))
	pl.xlabel('S Coordinate'); pl.ylabel(r'Normalized Error $\epsilon_N $'); pl.title(r'$\epsilon_N = \Delta$ r/S')

pl.show()