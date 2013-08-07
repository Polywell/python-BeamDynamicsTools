from numpy import *
from ellipse import *
import pylab as pl

S1 = matrix([
[0.577100, 0.398000, 0.000000, 0.000000, 0.000000, 0.000000],
[0.398000, 171.8262, 0.000000, 0.000000, 0.000000, 0.000000],
[0.000000, 0.000000, 0.343900, -0.27150, 0.000000, 0.000000],
[0.000000, 0.000000, -0.27150, 238.3722, 0.000000, 0.000000],
[0.000000, 0.000000, 0.000000, 0.000000, 1.297156, 2.343722],
[0.000000, 0.000000, 0.000000, 0.000000, 2.343722, 134.9344]],float)

S0 = matrix([
[1.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],
[0.000000, 1.000000, 0.000000, 0.000000, 0.000000, 0.000000],
[0.000000, 0.000000, 1.000000, 0.000000, 0.000000, 0.000000],
[0.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000],
[0.000000, 0.000000, 0.000000, 0.000000, 1.000000, 0.000000],
[0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 1.000000]],float)


E0 = ellipse(S0)

E0.PlotProjectionXY()
E0.PlotProjectionXY(Axz=pi/4,Ayz=0*pi/3)


w = 2
pl.xlim(-w,w); pl.ylim(-w,w)
pl.show()
