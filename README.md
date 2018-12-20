# monorepo


# Ubuntu 18.04 in windows 10
Windows Subsystem for Linux Installation Guide for Windows 10
https://docs.microsoft.com/en-us/windows/wsl/install-win10
Once ubuntu is installed go to the respective ubuntu terminal and setup the python environment 

To enable xeyes display: https://virtualizationreview.com/articles/2017/02/08/graphical-programs-on-windows-subsystem-on-linux.aspx
I installed Xming and I set the display environment variable to 0. See in above link for detailed explanation.

# Python environment
1) Install python 2.7.x. I used sudo apt-get to install python2. 
2) Install ipython and jupyter notebook --  pip install jupyter
3) Install pillow library (PIL) --  pip install pillow 

# Tensorflow current release for CPU-only
Next install tensorflow using pip command (https://www.tensorflow.org/install/)
pip install tensorflow
tensorflow version installed is latest one i.e r1.12. 
Additionally, install keras recent verision using (pip install keras)

# ROS installation for python
http://wiki.ros.org/
Follow below link for Ubuntu 18.04
https://rtt-lwr.readthedocs.io/en/latest/install/install-18.04-melodic.html

# Building and Running the two packages in the code

Follow steps described in:
http://wiki.ros.org/ROS/Tutorials/ExaminingPublisherSubscriber

Created two packages:
   beginners_tutorials : simple hello world text is printed
   image_classification: a pre-trained ResNet tensorflow model classifies simple input image "elephant.jpg" and prints the predicted output
	Output looks like this on screen:

              [INFO] [1545328572.996465]: [(u'n02504458', u'African_elephant', 0.8857361), (u'n01871265', u'tusker', 0.067711234), (u'n02504013', u'Indian_elephant', 0.03694539)] 1545328573.0
              [INFO] [1545328573.093978]: [(u'n02504458', u'African_elephant', 0.8857361), (u'n01871265', u'tusker', 0.067711234), (u'n02504013', u'Indian_elephant', 0.03694539)] 1545328573.09
	




