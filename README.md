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



