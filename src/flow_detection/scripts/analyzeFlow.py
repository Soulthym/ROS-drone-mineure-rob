#!/usr/bin/env python
# *************************
#     MINEURE ROBOTIQUE 5A
#          ESIEA - ONERA
# *************************

import rospy
#from std_msgs.msg import String
from opencv_apps.msg import FlowArrayStamped, Flow
import numpy as np
from std_msgs.msg import Float32

# variables globales
flow = Flow()

# initialisation du noeud
rospy.init_node('flow_analyzer', anonymous=True)

norms = [0]
npub = rospy.Publisher("norms", Float32, queue_size=10)
msgflow = Float32()

# fonction de lecture des mesures et d'envoi de la commande
def getFlowData(data):
    global norms, npub
    flow = data.flow
    norms = sum(sorted(np.asarray([np.linalg.norm(
                        (d.velocity.x, d.velocity.y))
                        for d in flow]))[:10])
    msgflow.data = norms
    npub.publish(msgflow)

    # **************** A COMPLETER EN TP ********************
    #
    #      calculs pour detection de mouvement
    #
    # *******************************************************


# declaration d'un subscriber : appelle getAltitude a chq arrivee d'une donnee sur le topic Navdata
rospy.Subscriber("/fback_flow/flows", FlowArrayStamped, getFlowData)

# fonction main executee en boucle 
if __name__ == '__main__':
    rospy.spin()

