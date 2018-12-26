#!/usr/bin/env python
from __future__ import print_function

import sys
import rospy
import cv2

#ROS related imports 
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

#Import keras related
from keras.applications.mobilenet_v2 import MobileNetV2
from keras.preprocessing import image
from keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import numpy as np
import tensorflow as tf

global model 
model = MobileNetV2(weights='imagenet')
global graph
graph = tf.get_default_graph()

class image_converter:

  def __init__(self):
    self.prediction_pub = rospy.Publisher("/videofile/image_raw/classifier_output",String)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/videofile/image_raw",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape

    #import ipdb;ipdb.set_trace()
    x = cv2.resize(cv_image, (224,224))
    x = x[...,::-1].astype(np.float32)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    
    with graph.as_default():
        preds = model.predict(x)

    if cols > 60 and rows > 60 :
      cv2.circle(cv_image, (50,50), 10, 255)
    decoded=decode_predictions(preds, top=3)[0]
    top3=[t[1] for t in decoded]
    predicted_str =  str(top3) +" %s" % rospy.get_time()
    print (predicted_str)
    
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,400)
    fontScale              = 1.0
    fontColor              = (0,0,255)
    lineType               = 2

    classif_OutputText=np.zeros((513,1200,3),np.uint8)

    cv2.putText(cv_image,predicted_str, 
     bottomLeftCornerOfText, 
     font, 
     fontScale,
     fontColor,
                lineType)

    cv2.imshow("Top3 Predictions", cv_image)

    cv2.waitKey(3)

    try:
      self.prediction_pub.publish(predicted_str)
    except CvBridgeError as e:
      print(e)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
