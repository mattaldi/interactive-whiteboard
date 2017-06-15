import numpy as np
from pykalman import KalmanFilter
from matplotlib import pyplot as plt


Measured=np.load("ballTrajectory.npy")
while True:
   if Measured[0,0]==-1.:
       Measured=np.delete(Measured,0,0)
   else:
       break
numMeas=Measured.shape[0]

MarkedMeasure=np.ma.masked_less(Measured,0)

Transition_Matrix=[[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]]
Observation_Matrix=[[1,0,0,0],[0,1,0,0]]

xinit=MarkedMeasure[0,0]
yinit=MarkedMeasure[0,1]
vxinit=MarkedMeasure[1,0]-MarkedMeasure[0,0]
vyinit=MarkedMeasure[1,1]-MarkedMeasure[0,1]
initstate=[xinit,yinit,vxinit,vyinit]
initcovariance=1.0e-3*np.eye(4)
transistionCov=1.0e-4*np.eye(4)
observationCov=1.0e-1*np.eye(2)
kf=KalmanFilter(transition_matrices=Transition_Matrix,
            observation_matrices =Observation_Matrix,
            initial_state_mean=initstate,
            initial_state_covariance=initcovariance,
            transition_covariance=transistionCov,
            observation_covariance=observationCov)

(filtered_state_means, filtered_state_covariances) = kf.filter(MarkedMeasure)


plt.plot(MarkedMeasure[:,0],MarkedMeasure[:,1],'xr',label='measured')
plt.hold(True)
plt.plot(filtered_state_means[:,0],filtered_state_means[:,1],'ob',label='kalman output')
##plt.legend(loc=2)
##plt.title("Constant Velocity Kalman Filter")
plt.show()
