#!/usr/bin/env python

# *************************
#     MINEURE ROBOTIQUE 5A
#          ESIEA - ONERA
# *************************

import rospy
import numpy as np
from geometry_msgs.msg import Twist
from ardrone_autonomy.msg import Navdata # for receiving navdata feedback
from nav_msgs.msg import Odometry # for receiving odometry feedback

# Global variables 
x = 0.0
y = 0.0
z = 0.0
psi_deg = 0.0
vx = 0.0
vy = 0.0


# Node init
rospy.init_node('cmd', anonymous=True)


# reference values for stabilization
# ***************** A COMPLETER EN TP **************
x_ref = 1.0 # m
y_ref = 1.0 # m
z_ref = 2.0 # mm
psi_deg_ref = 40.0 # deg
# **************************************************


# Commande msg and publisher declaration on the topic of command
command = Twist()
pubCommand = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
commandRate = rospy.Rate(10) 


# Callback functions for measurement readings (see subscribers below)
 
# ------------------------------
def readXY(data):
# ------------------------------
    global x, y
    # Data reading X axis
    x = data.pose.pose.position.x 
    # Data reading Y axis
    y = data.pose.pose.position.y     
    

# ------------------------------    
def readZPsiVxVy(data):
# ------------------------------
    global z, psi_deg, vx, vy
    # Data reading Z axis
    z = data.altd / 1000.0   
    # Data reading yaw angle (deg)
    psi_deg = data.rotZ
    vx = data.vx
    vy = data.vy
    

# Subscriber declaration 
rospy.Subscriber("/ground_truth/state", Odometry, readXY)   # ground truth for simulation
#rospy.Subscriber("/ardrone/odometry", Odometry, readXY)    # ardrone odom for experiments
rospy.Subscriber("/ardrone/navdata", Navdata, readZPsiVxVy)

def go_to(xpos=0, ypos=0, zpos=0, yawdeg=0):
    yawrad = np.radians(yawdeg)
    error = abs(xpos-x) + \
            abs(ypos-y) + \
            abs(zpos-z) + \
            abs(yawdeg-psi_deg)/180
    com_x, com_y, com_z, com_yaw = (xpos - x) *  .5,\
                                   (ypos - y) *  .5,\
                                   (zpos - z) *  .5,\
                                   (yawdeg - psi_deg) * 0.5
    com_x, \
    com_y = com_x *  np.cos(yawrad) + com_y *  np.sin(yawrad), \
            com_x * -np.sin(yawrad) + com_y *  np.cos(yawrad)

    return error,\
           com_x,\
           com_y,\
           com_z,\
           com_yaw

# Main loop
# ------------------------------
pos = [(0  ,0 ,1,  000),
       (2  ,0 ,2,  120),
       (2  ,2 ,1, -70),
       (0  ,2 ,2, -120),
       (-2 ,0 ,1,  000),
       (0  ,0 ,1,  000)
       ]
if __name__ == '__main__':
# ------------------------------

    global x, y, z, vx, vy, psi_deg, x_ref, y_ref, z_ref, psi_deg_ref


    target = pos.pop(0)
    while not rospy.is_shutdown():
	x_ref,y_ref,z_ref,psi_deg_ref = target
        (error,\
        command.linear.x,\
        command.linear.y,\
        command.linear.z,\
        command.angular.z) = go_to(
                                  xpos=   target[0],
                                  ypos=   target[1],
                                  zpos=   target[2],
                                  yawdeg= target[3])
        if error < 0.2:
            print("pos ({}, {}, {}, {}) reached".format(target[0], target[1], target[2], target[3]))
            if len(pos)>0:
                target=pos.pop(0)
                print("going to pos ({}, {}, {}, {})".format(target[0], target[1], target[2], target[3]))
            else:
                break

        # display in console
        rospy.loginfo(" xref=%f m,  x=%f m", x_ref, x)
        rospy.loginfo(" yref=%f m,  y=%f m", y_ref, y)
        rospy.loginfo(" zref=%f m,  z=%f m", z_ref, z)
        rospy.loginfo(" psiref=%f deg,  psi=%f deg", psi_deg_ref, psi_deg)

        # conversion deg to rad
        psi = psi_deg * np.pi / 180.0

        # update command value
        # ***************** A COMPLETER EN TP ********************
        # *******************************************************
    
        # Send commands
        pubCommand.publish(command)
        commandRate.sleep()




