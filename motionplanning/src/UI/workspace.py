
import tkinter as tk
import os
from PIL import Image
from PIL import ImageTk, Image
from tkinter import filedialog
import numpy as np
from MotionPlanner.planner import sPRM
from UI.configspace import ConfigSpace2D
from custom_types import Point2D

class ElementSize:
	def __init__(self, width, height):
		self.width = width
		self.height = height 

class WorkSpace(object):
	def __init__(self, master=None):
		self.root = master
		self.create_widgets()
		
		#State variables of application
		self.cspace_2D = ConfigSpace2D()
		self.planner = sPRM(self.cspace_2D, self)
		self.robot_size = None
		self.room_size = None

	def create_widgets(self):
		self.load_button = tk.Button(self.root, text = 'Load', state = 'normal', command = self.load_button_callback)
		self.load_button.grid(row = 0 , column = 0)
		
		self.reset_button = tk.Button(self.root, text = 'Reset to default position', state = 'disabled' , command = self.reset_button_callback)
		self.reset_button.grid(row = 0 , column = 1)
		
		self.start_button = tk.Button(self.root, text = 'Start', state = 'disabled' , command = self.start_button_callback)
		self.start_button.grid(row = 0 , column = 2)
		
		self.confirm_button = tk.Button(self.root, text = 'Confirm', state = 'disabled' , command = self.confirm_button_callback)
		self.confirm_button.grid(row = 0 , column = 3)
		
		self.quit = tk.Button(self.root, text="QUIT", fg="red", command=self.root.destroy)
		self.quit.grid(row = 0, column = 4)
		
		self.status_bar = tk.Label (self.root, text = 'Click on Load button to load the image ...', bg = 'white', fg='ROYALBLUE',  font='Helvetica 13 bold')
		self.status_bar.grid(row = 1 , columnspan = 5)
		
	def load_button_callback(self):
		bmp_dir_path = "./../images" 
		
		self.robot_img, self.room_img = [Image.open(i).convert('L') for i in (os.path.join(bmp_dir_path , "robot.bmp") , os.path.join(bmp_dir_path , "Room.bmp"))] # list comprehension

		self.room_widget = ImageTk.PhotoImage(self.room_img)
		self.robot_widget = ImageTk.PhotoImage(self.robot_img)
		self.robot_img_numpy = np.array(self.robot_img)
		self.room_img_numpy = np.array(self.room_img)
		robot_h, robot_w = self.robot_img_numpy.shape
		room_h, room_w = self.room_img_numpy.shape
		self.robot_size = ElementSize(width= robot_w, height= robot_h)
		self.room_size = ElementSize(width= room_w, height= room_h)
		self.cspace_2D.setConfig_max(self.room_size, self.robot_size)
		self.room_widget_id = None
		self.robot_widget_id = None		
		
		self.canvas = tk.Canvas(self.root, width= 1500, height= 1000)
		
		self.printEnvToCanvas()
		self.canvas.bind("<Button-1>" , self.leftClick)
		
		self.status_bar['text'] = ' Now click on the Room image to place the Robot'
		self.load_button['state'] = 'disabled'
		self.reset_button['state'] = 'disabled'
		self.start_button['state'] = 'disabled'
		
	def reset_button_callback(self):
		#import ipdb; ipdb.set_trace()
		self.start = False
		self.start_button['state'] = 'disabled'
		self.cspace_2D.reset()
		self.clear_all_widgets()
		print ("pressed reset button")
		self.status_bar['text'] = ' Choose Start position again'
		
	def robot_task(self):
		try: 
			_pos = next(self.curr_pos_iter)
			self.printRobotToCanvas(_pos)
			self.current_pos = _pos			
			self.root.after(2000, self.robot_task)  # reschedule event in 2 seconds	
		except StopIteration:
			self.status_bar['text'] = ' Robot reached destination. !!! HURRAY !!!'
			pass		
	def printEnvToCanvas(self):
		self.canvas.create_image(0,0, anchor= 'nw', image = self.room_widget)
		self.canvas.image= self.room_widget
		self.canvas.grid(row = 2, columnspan = 4)
	def printRobotToCanvas(self, point2d):
		if self.IsInCollision(point2d):
			self.status_bar['text'] = '..... COLLISION DETECTED .....'
		if self.robot_widget_id is not None:
			self.robot_widget_id = self.canvas.delete(self.robot_widget_id)
		self.robot_widget_id = self.canvas.create_image(point2d.x,point2d.y, anchor= 'nw', image = self.robot_widget)
	def printBoxToCanvas(self, point2d, color):
		return self.canvas.create_rectangle(point2d.x, point2d.y, point2d.x+8, point2d.y+8, fill = color)
	def printRobotOnSolutionPath(self, cofiguration):
		pass
	def IsInCollision(self, configuration):
		max_config_x, max_config_y = self.cspace_2D.getConfig_max()
		
		if (configuration.x >= max_config_x) or (configuration.y >= max_config_y):
			return True
		
		x, y =  configuration.x, configuration.y
		room_patch = self.room_img_numpy[y:y+self.robot_size.height, x:x+self.robot_size.width]
		if room_patch.mean() == 255:
			return False
		else:
			return True

	def start_button_callback(self):
		samples = 1000
		radius = 100
		self.status_bar['text'] = ' Robot started'
		self.cspace_2D.initSolutionPath(self.planner, samples=samples, radius=radius)
		# Comment below for fast run.
		#self.planner.printEdgeVertices()
		self.curr_pos_iter = self.cspace_2D.next_position()
		if self.cspace_2D.pathExistFrmSrcToDest():
			self.robot_task()
		else: 
			print(".... STATISTICS FOR CURRENT RUN .... ")
			print (f"number of samples={samples}")
			print (f"number of samples={radius}")
			self.status_bar['text'] = f" Path not Found [Error], Stat---> n={samples}, r={radius}"
		self.reset_button['state'] = 'normal'
		self.start_button['state'] = 'disabled'
	def clear_all_widgets(self):
		if self.robot_start_widget_id:
			self.canvas.delete(self.robot_start_widget_id)
			self.canvas.delete(self.robot_dest_widget_id)
			self.canvas.delete(self.robot_widget_id)
	def confirm_button_callback(self):
		point2d = self.curr_clicked_pos
		if not self.cspace_2D.isStartSet():
			self.cspace_2D.setInitial(point2d)
			self.status_bar['text'] = ' Now click on the Room image to choose destination position' 
			self.robot_start_widget_id = self.printBoxToCanvas(point2d, "green")
		elif not self.cspace_2D.isGoalSet():
			self.cspace_2D.setGoal(point2d)
			self.status_bar['text'] = ' Now click on Start button'
			self.robot_dest_widget_id = self.printBoxToCanvas(point2d, "red")
			self.start_button['state'] = 'normal'
		self.confirm_button['state'] = 'disabled'
			
		
	def leftClick(self, event):
		
		if not self.cspace_2D.isStartSet():
			if self.robot_widget_id is not None:
				self.canvas.delete(self.robot_widget_id)			
			self.printRobotToCanvas(Point2D(event.x,event.y))
			if self.IsInCollision(Point2D(event.x,event.y)):
				self.status_bar['text'] = '..... COLLISION DETECTED .....'
			else:
				self.status_bar['text'] = ' Start position at = ' + 'x: ' + str(event.x) + ' y:' + str(event.y) + ' press confirm ...' 
			self.confirm_button['state'] = 'normal'
		elif not self.cspace_2D.isGoalSet():
			if self.IsInCollision(Point2D(event.x,event.y)):
				self.status_bar['text'] = '..... COLLISION WILL OCCUR AT THIS POINT .....'
			else:
				self.status_bar['text'] = ' Destination position at = ' + 'x: ' + str(event.x) + ' y:' + str(event.y) + ' press confirm ...' 
			self.confirm_button['state'] = 'normal'
			
		self.curr_clicked_pos = Point2D(event.x, event.y)
		
	
		
		
	
		
		
		
		
		
		
		
