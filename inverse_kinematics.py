import matplotlib.pyplot as plt
import numpy as np
import math

L1=7#link1 length (cm)
L2=13#link2 length (cm)

x_vals= []#np.linspace(-7.6,5.1,100)
step=(7.6+5.1)/40
y_vals=[]
print(step*10000)
#need to scale up for for loop to work (for loops need int values)
for q in range(-76000,51000,int(step*10000)):
	cur_x=q/10000#scaling back down for input data
	x_vals.append(cur_x)
	cur_y=(-.08*(cur_x+7.6)*(cur_x-5.1)) +4.8
	y_vals.append(cur_y)
#now that I have my x and y values it's time for inverse kinematics!


theta2=[]
theta1=[]

#inverse kinematics at eachpoint
for i in range(len(x_vals)):
	L3 = math.sqrt(x_vals[i]**2 + y_vals[i]**2)

	beta1 = ((L2**2)-(L1**2) - (L3**2))/(-2*L1*L3)
	beta2 = ((L3**2)-(L1**2) - (L2**2))/(-2*L1*L2)

	phi1= math.atan2(math.sqrt(1-(beta1**2)),beta1)
	phi2=math.atan2(y_vals[i],x_vals[i])
	phi3=math.atan2(math.sqrt(1-(beta2**2)),beta2)

	theta1.append(math.degrees(phi2-phi1))
	theta2.append(180-math.degrees(phi3))

print('-----------------------------theta1 values-----------------------------')
print(theta1)
print('-----------------------------theta2 values-----------------------------')
print(theta2)
print('-----------------------------x values-----------------------------')
print(x_vals)
print('-----------------------------y values-----------------------------')
print(y_vals)

#plotting my trajectory as well as my x position and y position with respect to time
time=np.linspace(0,4,40)#I want the step to take 4 seconds in total

fig1, ax1= plt.subplots()
ax1.plot(x_vals,y_vals)
ax1.set(xlabel="x position (cm)", ylabel="y position (cm)")


fig2, (ax2,ax3) = plt.subplots(2)
ax2.plot(time,x_vals)
ax2.set(xlabel="time", ylabel="x position (cm)")
ax3.plot(time,y_vals)
ax3.set(xlabel="time", ylabel="y position (cm)")

plt.show()