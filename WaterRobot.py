import cv2
import numpy as np
import time
from tkinter import *
import datetime
import imageio
from PIL import ImageTk, Image
import math
import pickle




# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
# Create some random colors
color = np.random.randint(0,255,(100,3))

detector = cv2.CascadeClassifier("haarcascade_frontalcatface.xml")
backsub  = cv2.createBackgroundSubtractorMOG2()
#fgbg = cv2.cv2.BackgroundSubtractorMOG2()
#import RPi.GPIO as GPIO  # always needed with RPi.GPIO
#GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM
#GPIO.setup(25, GPIO.OUT)  # set GPIO 25 as an output. You can use any GPIO port
# p0 = GPIO.PWM(25, 50)  # create an object p for PWM on port 25 at 50 Hertz
# p0.start(50)  # start the PWM on 50 percent duty cycle
# p1 = GPIO.PWM(XX, 50)  # create an object p for PWM on port 25 at 50 Hertz
# p1.start(50)  # start the PWM on 50 percent duty cycle

#Global variables
flowers = []
#tkflower = []
flowerbox = []
flowerinfobox = []
ServoPos = [0.5,0.5]
var = []
movementXBuffer = []
movementYBuffer = []

def mainIsh():
    print("Main loop here")

class flower:
    def __init__(self):
        self.name = ""
        self.waterPos = [0.5, 0.5]
        self.waterPos[0] = ServoPos[0]
        self.waterPos[1] = ServoPos[1]
        self.created = datetime.datetime.now()
        self.lastWatered = datetime.datetime.now()
        self.Active = True;

def move_servo():
    #p0.ChangeDutyCycle(Servopos[0]*100)  # change the duty cycle
    #p1.ChangeDutyCycle(Servopos[1]*100)  # change the duty cycle
    updateGui()
def roundup(x):
    return int(math.ceil(x *100)) / 100
def updateGui():
    for i in range(0,len(flowers)):
        if flowers[i].Active:
            flowerbox[i].grid(column=i, row=1)
        else:
            flowerbox[i].grid_forget()
    servoStr.set("Servoposition: \n{}\n{}".format(roundup(ServoPos[0]), roundup(ServoPos[1])))
    f = open('store.pckl', 'wb')
    pickle.dump(flowers, f)
    f.close()
    for i in range (0, 4):
        var[i].set("Name : Flower {} \nLast watered: {}\nServo position: {},{}".format(str(flowers[i].name), str(
            flowers[i].lastWatered.strftime("%d/%m-%Y, %H:%M ")), roundup(flowers[i].waterPos[0]),
                                                                                       roundup(flowers[i].waterPos[1])))
def close(event):
    root.withdraw() # if you want to bring it back
    # p.stop()  # stop the PWM output
    # GPIO.cleanup()  # when your program exits, tidy up after yourself
    sys.exit() # if you want to exit the entire thing

def clickRename():

    toplevel = Toplevel()
    label = Label(toplevel, text="Rename flowers", height=50, width=100).grid(row = 0,columnspan = 4)
    Label(toplevel, text="First Name").grid(row=1)
    Label(toplevel, text="Last Name").grid(row=2)
    e1 = Entry(toplevel)
    flvar = StringVar()
    e2 = Entry(toplevel,textvariable=flvar)
    #flowers[0].name.replace = flvar.get
    e1.grid(row=1, column=1)
    e2.grid(row=2, column=1)
    Button(toplevel, text='Quit', command=toplevel.quit).grid(row=3, column=0, sticky=W, pady=4)


def waterPlants(event):
    for i in range (0,len(flowers)):
        if flowers[i].Active:
            print(str("Flower {} have not been watered in {} secounds.").format(i+1,(datetime.datetime.now() - flowers[i].lastWatered).seconds))
            if (datetime.datetime.now() - flowers[i].lastWatered).seconds > 5 and flowers[i].Active  :
                ServoPos[0] =  flowers[i].waterPos[0]
                ServoPos[1] = flowers[i].waterPos[1]
                print("Watering plant {}".format(i+1))
                move_servo()
                time.sleep(1.3)
                flowers[i].lastWatered = datetime.datetime.now()

def centerRobot(event):
    print("Go home here")
    test = "Hello, I have been saved!"
    # m1.ChangeDutyCycle(50)  # change the duty cycle to 50%
    # m2.ChangeDutyCycle(50)  # change the duty cycle to 50%
    ServoPos[0] = 0.5
    ServoPos[1] = 0.5
    move_servo()

def spray(event):
    print("Spray here")
def saveServo1(event):
    flowers[0].waterPos[0] = ServoPos[0]
    flowers[0].waterPos[1] = ServoPos[1]
    updateGui()
def saveServo2(event):
    flowers[1].waterPos[0] = ServoPos[0]
    flowers[1].waterPos[1] = ServoPos[1]
    updateGui()
def saveServo3(event):
    flowers[2].waterPos[0] = ServoPos[0]
    flowers[2].waterPos[1] = ServoPos[1]
    updateGui()
def saveServo4(event):
    flowers[3].waterPos[0] = ServoPos[0]
    flowers[3].waterPos[1] = ServoPos[1]
    updateGui()
def goLeft(event):
    print("Go Left.")
    ServoPos[0] = ServoPos[0]-(0.01)
    move_servo()
def goRight(event):
    print('Go Right.')
    ServoPos[0] = ServoPos[0]+(0.01)
    move_servo()
def goUp(event):
    print('Go Up.')
    ServoPos[1] = ServoPos[1]+(0.01)
    move_servo()
def goDown(event):
    print('Go Down.')
    ServoPos[1] = ServoPos[1]-(0.01)
    move_servo()
def toggleFlower1(event):
    flowers[0].Active ^= 1
    updateGui()
def toggleFlower2(event):
    flowers[1].Active ^= 1
    updateGui()
def toggleFlower3(event):
    flowers[2].Active ^= 1
    updateGui()
def toggleFlower4(event):
    flowers[3].Active ^= 1
    updateGui()
def resetTracker():
    resetTra.set(True)

def show_frame():
    rval, frame = cap.read()
    if radvar.get() == 1:
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif radvar.get() == 2:
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    elif radvar.get() == 3:
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect cats
        rects = detector.detectMultiScale(cv2image, scaleFactor=1.3,
                                          minNeighbors=10, minSize=(10, 10))
        # loop over the cat faces and draw a rectangle surrounding each
        for (i, (x, y, w, h)) in enumerate(rects):
            cv2.rectangle(cv2image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(cv2image, "Cat #{}".format(i + 1), (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

    elif radvar.get() == 4:
        global old_gray
        global p0
        global mask
        if resetTra.get() == True:
            # Take first frame and find corners in it
            ret, old_frame = cap.read()
            old_gray = cv2.cvtColor(old_frame, cv2.COLOR_RGB2GRAY)
            p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
            # Create a mask image for drawing purposes
            mask = np.zeros_like(old_frame)
            resetTra.set(False)

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        # Select good points
        good_new = p1[st == 1]
        good_old = p0[st == 1]
        # draw the tracks
        for i, (new, old) in enumerate(zip(good_new, good_old)):

            a, b = new.ravel()
            c, d = old.ravel()
            lengthx = (a-c)
            lengthy = (b-d)
            if lengthx > 10 or lengthy > 10:
                #Movement!

                #Calculate average position of movement:
                movementXBuffer.append(lengthx)
                movementYBuffer.append(lengthx)
                print("Something moved at: {},{}".format((a), (b)))

                print("Robot gain: {},{}".format((a-(800/2)), (b-(600/2))))

            mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)

            frame = cv2.circle(frame, (a, b), 5, color[i].tolist(), -1)

        img = cv2.add(frame, mask)
        #Show only dots
        #img = mask
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Now update the previous frame and previous points
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1, 1, 2)

    else:
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        Arr = np.asarray(cv2image)

        # Blue
        lower = np.array([0, 0, 150], dtype="uint8")
        upper = np.array([100, 250, 250], dtype="uint8")

        # Yellow
        # lower = np.array([17, 100, 15], dtype="uint8")
        # upper = np.array([50, 200, 56], dtype="uint8")

        # Red
        #lower = np.array([100, 15, 17], dtype="uint8")
        #upper = np.array([200, 56, 50], dtype="uint8")

        testcv22image = cv2.inRange(Arr, lower, upper)

        cv2image = backsub.apply(cv2image, None, 0.01)



    img = Image.fromarray(cv2image)
    # If CatKill, do it here

    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    del img
    del frame
    del cv2image
    del imgtk
    mainIsh()
    lmain.after(50, show_frame)


width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
root = Tk();
root.bind('<Escape>', close)
root.title("Gaia")
root.geometry("1200x1000")
root.resizable(width=False, height=False)

lmain = Label(root)
lmain.grid(row=0, columnspan=5)

# Load images
freshPlantImg = Image.open("freshPlant.png")
tkflower = ImageTk.PhotoImage(freshPlantImg)

ArrowLeft = Image.open("Left.jpg")
ArrowLeftTk = ImageTk.PhotoImage(ArrowLeft)
ArrowRightTk = ImageTk.PhotoImage(ArrowLeft.rotate(180))

ArrowUp = Image.open("Up.jpg")
ArrowUpTk = ImageTk.PhotoImage(ArrowUp)
ArrowDownTk = ImageTk.PhotoImage(ArrowUp.rotate(180))

buttonLabel = Label(root)
buttonLabel.grid(row = 0,column = 5)
buttonLabel.columnconfigure(0, weight=3)


for i in range (len(flowers),4):
        flowers.append(flower())
        flowerbox.append(Label(root, width=50, height=50, image=tkflower))
        print("Flower added! Number of flowers registerd are now {}.".format(len(flowers)))
        flowerbox[i].grid(column= i , row=1)
        var.append(StringVar())
        var[i].set("Name : Flower {} \nLast watered: {}\nServo position: {},{}".format(i,str(flowers[i].lastWatered.strftime("%d/%m-%Y, %H:%M ")),str(flowers[i].waterPos[0]),str(flowers[i].waterPos[1])))
        flowerinfobox.append(Label(root, textvariable=var[i]))
        flowerinfobox[i].grid(column=i, row=2)

f = open('store.pckl', 'rb')
flowers = pickle.load(f)
f.close()

saveServoButton = Button(root, text="Save servo position", fg="green")
saveServoButton.bind("<Button-1>", saveServo1)
saveServoButton.grid(column=0, row=4)

saveServoButton = Button(root, text="Save servo position", fg="green")
saveServoButton.bind("<Button-1>", saveServo2)
saveServoButton.grid(column=1, row=4)


saveServoButton = Button(root, text="Save servo position", fg="green")
saveServoButton.bind("<Button-1>", saveServo3)
saveServoButton.grid(column=2, row=4)

saveServoButton = Button(root, text="Save servo position", fg="green")
saveServoButton.bind("<Button-1>", saveServo4)
saveServoButton.grid(column=3, row=4)


chooseLabel = Label(root)
chooseLabel.grid(row = 1,column = 5)
chooseLabel.columnconfigure(0, weight=3)
radvar = IntVar()
radvar.set(1)
Radiobutton(chooseLabel, text="Grayscale", variable=radvar, value=1).pack(anchor=W)
Radiobutton(chooseLabel, text="Color", variable=radvar, value=2).pack(anchor=W)
Radiobutton(chooseLabel, text="Find cat", variable=radvar, value=3).pack(anchor=W)
Radiobutton(chooseLabel, text="Track all", variable=radvar, value=4).pack(anchor=W)
Radiobutton(chooseLabel, text="Background subtraction", variable=radvar, value=5).pack(anchor=W)



checkLabel = Label(root)
checkLabel.grid(row = 3,column = 5)
checkLabel.columnconfigure(0, weight=3)
soundvar = BooleanVar()
soundvar.set(True)
resetTra = BooleanVar()
resetTra.set(True)
cSound = Checkbutton(checkLabel, text="Sound: on", variable=soundvar).pack(anchor=W)
waterPlantsChoice = BooleanVar()
waterPlantsChoice.set(False)
cWater = Checkbutton(checkLabel, text="Autmatic watering of plants: on", variable=waterPlantsChoice).pack(anchor=W)

arrowLabel = Label(root)
arrowLabel.grid(row = 2,column = 5)
arrowLabel.columnconfigure(0, weight=3)

leftArrowButton = Button(arrowLabel,image = ArrowLeftTk ,fg = "red")
leftArrowButton.bind("<Button-1>",goLeft)
leftArrowButton.grid(row=1,column=0)
rightArrowButton = Button(arrowLabel,image = ArrowRightTk,fg = "red")
rightArrowButton.bind("<Button-1>",goRight)
rightArrowButton.grid(row=1,column=2)
upArrowButton = Button(arrowLabel,image = ArrowUpTk,fg = "red")
upArrowButton.bind("<Button-1>",goUp)
upArrowButton.grid(row=0,column=1)
downArrowButton = Button(arrowLabel,image = ArrowDownTk,fg = "red")
downArrowButton.bind("<Button-1>",goDown)
downArrowButton.grid(row=2,column=1)
servoStr = StringVar()
servoInfo = Label(arrowLabel, textvariable=servoStr)
servoInfo.grid(row=1,column=1)
servoStr.set("Servoposition: \n{}\n{}".format(ServoPos[0],ServoPos[1]))

sprayButton = Button(arrowLabel,text="Spray" ,fg = "blue")
sprayButton.bind("<Button-1>",spray)
sprayButton.grid(row=0,column=2)
goHomeButton = Button(arrowLabel,text = "Center robot",fg = "blue")
goHomeButton.bind("<Button-1>",centerRobot)
goHomeButton.grid(row=0,column=0)



toggleFl1 = Button(root, text="Add/remove flower", fg="green")
toggleFl1.bind("<Button-1>",toggleFlower1)
toggleFl1.grid(column=0, row=3)
toggleFl1 = Button(root, text="Add/remove flower", fg="green")
toggleFl1.bind("<Button-1>",toggleFlower2)
toggleFl1.grid(column=1, row=3)
toggleFl1 = Button(root, text="Add/remove flower", fg="green")
toggleFl1.bind("<Button-1>",toggleFlower3)
toggleFl1.grid(column=2, row=3)
toggleFl1 = Button(root, text="Add/remove flower", fg="green")
toggleFl1.bind("<Button-1>",toggleFlower4)
toggleFl1.grid(column=3, row=3)
waterPlantsButton = Button(buttonLabel,text = "Water plants",fg = "red")
waterPlantsButton.bind("<Button-1>",waterPlants)
waterPlantsButton.pack()
resetTrack = Button(buttonLabel, text="Reset tracker", width=20, command=resetTracker)
resetTrack.pack()
renameButton = Button(buttonLabel, text="Rename flowers", width=20, command=clickRename)
renameButton.pack()
updateGui()


show_frame()
root.mainloop()