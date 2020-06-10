
import cv2
def readFrame():
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame

filename = './data/shaky2.mp4'
cap = cv2.VideoCapture(filename)
#cap = cv2.VideoCapture(filename)
#ImgLeft = Image.open('./data/picLeft.jpg')
#ImgRight = Image.open('./data/picRight.jpg')
totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
ImgLeft = readFrame()