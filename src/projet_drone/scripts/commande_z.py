#!/usr/bin/env python

# *************************
#     MINEURE ROBOTIQUE 5A
#          ESIEA - ONERA
# *************************


import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from ardrone_autonomy.msg import Navdata # for receiving navdata feedback
#from nav_msgs.msg import Odometry # for receiving odometry feedback




# Global variables 

# ********* A COMPLETER EN TP ******
z_ref = 1.70
# **********************************
command = Twist() # command
z = z_ref  # altitude measurement (defined equal to z_ref to get zero command value until first measurement is read)



# Node init
rospy.init_node('commande_z', anonymous=True)


# Publisher declaration on the topic of command
pubCommand = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
commandPubRate = rospy.Rate(40) # frequency



# Callback function for altitude measurements reading
def readAltitude(data):
	global z	
	# Data reading Z axis
	z = data.altd / 1000.0   
	# print measurement 
	rospy.loginfo(" z (m) = %f", z)
	


# Subscriber declaration 
rospy.Subscriber("/ardrone/navdata", Navdata, readAltitude)




# Main: looping execution
if __name__ == '__main__':

	while not rospy.is_shutdown():

		# update command value
		# ********* A MODIFIER EN TP ******
		command.linear.z = - 1 * (z - z_ref)
		# *********************************
	
		# Command sending
		pubCommand.publish(command)

		# do nothing during one time step
		commandPubRate.sleep()

