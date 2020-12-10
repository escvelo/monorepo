import glob
import imageio 
import os
from PIL import Image
from PIL import ImageTk, Image
from tkinter import filedialog
import numpy as np
import tkinter as tk
from UI.workspace import WorkSpace
import sys
sys.path.append(".")

root =tk.Tk()
# Allow Window to be resizable 
root.resizable(width = True, height = True) 
app = WorkSpace(master = root)	
root.mainloop()

