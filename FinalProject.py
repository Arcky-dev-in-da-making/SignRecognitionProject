#Importing modules
from tkinter import *
from tkinter import ttk
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
from PIL import Image, ImageTk
import time
from random import randint
import mysql.connector as mysql

#Establishing connections
conn = mysql.connect(host = "localhost",password = "Ch3atosiscool",user = "root" ,database = "ModuleScores")
cursor = conn.cursor()

#Module Completion time variables
startTime = 0
endTime = 0

#Defining functions
def timer(seconds): #Stops function for seconds
    start_time = time.time()
    time_elapsed = 0
    while time_elapsed < seconds:
        time_elapsed = time.time() - start_time
    print("Time's up!")


def GoingBackLsns(): #Function for Back button
    remove_all_widgets_exceptImages(window=Window)
    unpackAll()
    timer(1)
    InterpreterButton = Button(Window, text="Interpreter",command = switchInterpreterWindow, fg="white",
                               bg="#4F3475",
                               font=("roboto", "24", "bold"), relief=GROOVE, padx=50, pady=50)
    title = Label(text="Sign Recognition Project", bg="#D62768", fg="white", padx=60, pady=50,
                  font=("roboto", "24", "bold"))
    LessonButton = Button(Window, text="Lessons",command= LessonABCD,fg="white", bg="#4C6FBE",
                          font=("roboto", "24", "bold"), relief=GROOVE, padx=70, pady=40)
    LeaderboardButton = Button(Window, text="Leaderboard", command= switchLeaderboardWindow, fg="white",
                               bg="#4F3475",
                               font=("roboto", "24", "bold"), relief=GROOVE, padx=50, pady=50)

    title.pack(padx=50, pady=50)
    InterpreterButton.pack(pady=15)
    LessonButton.pack(pady=15)
    LeaderboardButton.pack(pady=15)


lessonAD = False

#Window Object Creation
Window = Tk()
Frame(Window, bg="black").pack()
Window.geometry("1920x1080")
Window.configure(bg="#1C1A1D")
Window.title("Sign Recognition Project!")
Window.minsize(200, 200)

#Main Page
title = Label(text="Sign Recognition Project", bg="#D62768", fg="white", padx=60, pady=50,
              font=("roboto", "24", "bold"))

title.pack(padx=50, pady=50)  # Setting the Title Box location

#Intialising all images
abcdimage = Image.open("images/abcd.jpg")
abcdphoto = ImageTk.PhotoImage(abcdimage)
abcdlabel = Label(image=abcdphoto)

efghimage = Image.open("images/efgh.jpg")
efghphoto = ImageTk.PhotoImage(efghimage)
efghlabel = Label(image=efghphoto)

ijklimage = Image.open("images/ijkl.jpg")
ijklphoto = ImageTk.PhotoImage(ijklimage)
ijkllabel = Label(image=ijklphoto)

mnopimage = Image.open("images/mnop.jpg")
mnopphoto = ImageTk.PhotoImage(mnopimage)
mnoplabel = Label(image=mnopphoto)

qrstuimage = Image.open("images/qrstu.jpg")
qrstuphoto = ImageTk.PhotoImage(qrstuimage)
qrstulabel = Label(image=qrstuphoto)

vwxyzimage = Image.open("images/vwxyz.jpg")
vwxyzphoto = ImageTk.PhotoImage(vwxyzimage)
vwxyzlabel = Label(image=vwxyzphoto)


#Hides all images from view
def unpackAll():
    abcdlabel.pack_forget()
    efghlabel.pack_forget()
    ijkllabel.pack_forget()
    mnoplabel.pack_forget()
    qrstulabel.pack_forget()
    vwxyzlabel.pack_forget()

#Deletes all objects except images (Redefining images creates errors)
def remove_all_widgets_exceptImages(window):
    for widget in window.winfo_children():
        if widget not in [abcdlabel, efghlabel, ijkllabel, mnoplabel, qrstulabel, vwxyzlabel]:
            widget.destroy()


#Function for Interpreter Button
def switchInterpreterWindow():
    remove_all_widgets_exceptImages(window=Window)

    BackButton = Button(Window, text="Back", command=GoingBackLsns, fg="black", bg="light blue", relief=GROOVE,
                        font=("roboto", "20", "bold"), pady=10, padx=25)
    BackButton.pack(anchor="sw") #Intialising Back Button

    #Initialising Webcam Frame
    InterpreterCamTxt = Label(Window, text="InterpreterCam", font=("sans serif", 30, "bold"), bg="black", fg="white")
    InterpreterCamTxt.pack()
    f1 = LabelFrame(Window, bg="red")
    f1.pack()
    L1 = Label(f1, bg="red")
    L1.pack()

    #Initialising webcam
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)  # Class based on detecting the hands
    classifier = Classifier("Model/keras_model.h5", "Model/labels.txt") #Classifying using main model (A-Z, Father, NO, Hello, _)

    offset = 20
    imgSize = 300

    counter = 0
    counter2 = 0
    newString = '' #Sentence formation
    labels = ["A", "B", 'C', 'D', 'E', 'F', "Father", 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'NO', 'O', 'P', 'Q', 'R',
              'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_', "Hello"]

    while True:
        success, img = cap.read()  # Create webcam
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgOutput = img.copy()
        hands, img = detector.findHands(img)  # Finding and mapping the hands

        if hands:  # Cropping the image of hands for precise detection
            hand = hands[0]
            x, y, w, h = hand['bbox']  # taking parameters from boundary box.

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255  # White image

            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]  # Cropped image(only for hands)

            imgCropShape = imgCrop.shape

            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                try:
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    imgResizeShape = imgResize.shape
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize  # merging the images
                    prediction, index = classifier.getPrediction(imgWhite, draw=False) #Final sign prediction
                    print(prediction, index)
                except cv2.error:
                    print("e")


            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                try:
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    imgResizeShape = imgResize.shape
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize  # merging the images
                    prediction, index = classifier.getPrediction(imgWhite, draw=False) #Final sign prediction
                    print(prediction, index)
                except cv2.error:
                    print("e")
            # Customizing the output frame
            try:
                cv2.rectangle(imgOutput, (x - offset, y - offset - 50), (x - offset + 100, y - offset), (46, 168, 34),
                              cv2.FILLED) #Rectangle that covers the hand
                cv2.putText(imgOutput, labels[index], (x, y - 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 4) #Shows sign
                if labels[index] in ["A", "B", 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                                     'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', "_"]: #Sentence formation
                    counter += 1 #wait for some time before registering letter into sentence
                    if counter % 10 == 0:
                        newString = newString + labels[index]
                        print(newString)
                else:
                    counter2 += 1 #Reset sentence
                    if counter2 >= 5:
                        newString = ""
                        counter2 = 0
                cv2.putText(imgOutput, newString, (x + 100, y - 40), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 4) #Displays Sentence

                cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (46, 168, 34), 4)
            except cv2.error:
                print("e")
            except NameError:
                print("e")
        FinalOutput = ImageTk.PhotoImage(Image.fromarray(imgOutput)) #Displays webcam on tkinter window
        L1['image'] = FinalOutput
        Window.update()

#Interpreter button
InterpreterButton = Button(Window, text="Interpreter", command=switchInterpreterWindow, fg="white", bg="#4F3475",
                           font=("roboto", "24", "bold"), relief=GROOVE, padx=50, pady=50)

def switchLeaderboardWindow(): #Function for Leaderboard Button
    remove_all_widgets_exceptImages(window = Window)

    #Initialising back button
    BackButton = Button(Window, text="Back", command=GoingBackLsns, fg="black", bg="light blue", relief=GROOVE,
                        font=("roboto", "20", "bold"), pady=10, padx=25)
    BackButton.pack(anchor="sw")

    #Leaderboard table presented through Treeview (tkinter.ttk.Treeview)
    Leaderboard = ttk.Treeview(Window, columns=("Position", "Name", "Time"), show="headings")
    #Initialising headings
    Leaderboard.heading("Position", text="Position")
    Leaderboard.heading("Name", text="Name")
    Leaderboard.heading("Time", text="Time")
    #Showing table
    Leaderboard.pack()

    cursor.execute("SELECT * FROM LEADERBOARD ORDER BY TIME DESC") #MySQL query which shows by shortest time
    data = cursor.fetchall()
    for i in data:
        pos = len(data) - data.index(i) #Shows their current position (1st,2nd..)
        Leaderboard.insert(parent='', index=0, values=(pos, i[0], i[1])) #Inserts values from MySQl to Leaderboard table

#Leaderboard Table
LeaderboardButton = Button(Window, text="Leaderboard", command=switchLeaderboardWindow, fg="white", bg="#4F3475",
                           font=("roboto", "24", "bold"), relief=GROOVE, padx=50, pady=50)

#----------------------------------------------------------------------------------------------------------------------------#
#All Modules functions
def LessonABCD(): #First Lesson (ABCD)
    remove_all_widgets_exceptImages(window=Window)
    global startTime
    startTime = time.time() #Time starts here

    #Info Page
    ABCDtext = Label(text="Hand signs for ABCD are:", padx=60, pady=50,
                     font=("Times", "24", "bold"))

    ABCDtext.pack(padx=50, pady=100)
    labelABCD = ["A", "B", "C", "D"]

    abcdlabel.pack()

    def QuestionsABCD(): #Runs as NextButton is pressed
        unpackAll()
        remove_all_widgets_exceptImages(window=Window)
        QuestionIndex = randint(0, 3) #Randomized question
        QuestionTxt = "Show \"" + str(labelABCD[QuestionIndex]) + "\" in ASL"

        QuestionLabel = Label(text=QuestionTxt, font=("times new roman", 30, "bold"))
        QuestionLabel.pack(padx=20, pady=20) #Displays question

        #Frame holding webcam
        f2 = LabelFrame(Window, bg="red")
        f2.pack()
        L2 = Label(f2, bg="red")
        L2.pack()

        #Initiallising webcam
        cap = cv2.VideoCapture(0)
        detector = HandDetector(maxHands=1)  # Class based on detecting the hands
        classifier = Classifier("Model/ModelABCD.h5","Model/labels.ABCD.txt") #Using ModelABCD and its labels (Only detects A,B,C,D)

        offset = 20
        imgSize = 300

        #Counters
        counter = 0
        counter2 = 0
        while True:
            success, img = cap.read()  # Create webcam
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgOutput = img.copy()
            hands, img = detector.findHands(img)  # Finding and mapping the hands

            if hands:  # Cropping the image of hands for precise detection
                hand = hands[0]
                x, y, w, h = hand['bbox']  # taking parameters from boundary box.

                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255  # White image

                imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]  # Cropped image(only for hands)

                imgCropShape = imgCrop.shape

                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    try:
                        imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                        imgResizeShape = imgResize.shape
                        wGap = math.ceil((imgSize - wCal) / 2)
                        imgWhite[:, wGap:wCal + wGap] = imgResize  # merging the images
                        prediction, index = classifier.getPrediction(imgWhite, draw=False) #Image prediction
                        print(prediction, index)
                    except cv2.error:
                        print("e")


                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    try:
                        imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                        imgResizeShape = imgResize.shape
                        hGap = math.ceil((imgSize - hCal) / 2)
                        imgWhite[hGap:hCal + hGap, :] = imgResize  # merging the images
                        prediction, index = classifier.getPrediction(imgWhite, draw=False) #Image prediction
                        print(prediction, index)
                    except cv2.error:
                        print("e")
                # Customizing the output frame
                try:
                    cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (46, 168, 34),
                                  4)
                    cv2.putText(imgOutput, labelABCD[index], (x, y - 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
                except cv2.error:
                    print("e")
                except NameError:
                    print("e")
                try:
                    #Counter to check if the signs weren't a fluke
                    if labelABCD[QuestionIndex] == labelABCD[index]:
                        counter += 1
                        print(counter)
                    else:
                        counter = 0

                    if counter < 10 and counter > 5:
                        Correct = Label(text="Correct!", padx=200, pady=200, bg="black", fg="white")
                        Correct.pack()
                        timer(1)
                        remove_all_widgets_exceptImages(window=Window)
                        unpackAll()
                        LessonEFGH() #Proceeds to the next lesson directly
                except UnboundLocalError:
                    print("u")
            FinalOutput = ImageTk.PhotoImage(Image.fromarray(imgOutput))
            L2['image'] = FinalOutput
            Window.update()

    NextButton = Button(Window, text="Next", command=QuestionsABCD, fg="black", bg="light blue", relief=GROOVE,
                        font=("roboto", "20", "bold"), pady=1, padx=9)
    NextButton.place(x=1258, y=400)

    BackButtonTM = Button(Window, text="Back", command=GoingBackLsns, fg="black", bg="light blue", relief=GROOVE,
                          font=("roboto", "20", "bold"), pady=1, padx=9)
    BackButtonTM.place(x=5, y=400)


def LessonEFGH():#Lessons for EFGH
    remove_all_widgets_exceptImages(window=Window)

    #Info Page
    EFGHtext = Label(text="Hand signs for EFGH are:", padx=60, pady=50,
                     font=("Times", "24", "bold"))
    EFGHtext.pack(padx=50, pady=100)
    labelEFGH = ["E", "F", "G", "H"]

    efghlabel.pack()

    def QuestionsEFGH():
        unpackAll()
        remove_all_widgets_exceptImages(window=Window)
        #Question Text
        QuestionIndex = randint(0, 3)
        QuestionTxt = "Show \"" + str(labelEFGH[QuestionIndex]) + "\" in ASL"
        QuestionLabel = Label(text=QuestionTxt, font=("times new roman", 30, "bold"))
        QuestionLabel.pack(padx=20, pady=20)

        #Webcam Frame
        f2 = LabelFrame(Window, bg="red")
        f2.pack()
        L2 = Label(f2, bg="red")
        L2.pack()

        cap = cv2.VideoCapture(0) #Initialising webcam
        detector = HandDetector(maxHands=1)  # Class based on detecting the hands
        classifier = Classifier("Model/ModelEFGH.h5", "Model/labels.EFGH.txt")

        offset = 20
        imgSize = 300

        #Counters
        counter = 0
        counter2 = 0
        while True:
            success, img = cap.read()  # Create webcam
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgOutput = img.copy()
            hands, img = detector.findHands(img)  # Finding and mapping the hands

            if hands:  # Cropping the image of hands for precise detection
                hand = hands[0]
                x, y, w, h = hand['bbox']  # taking parameters from boundary box.

                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255  # White image

                imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]  # Cropped image(only for hands)

                imgCropShape = imgCrop.shape

                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    try:
                        imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                        imgResizeShape = imgResize.shape
                        wGap = math.ceil((imgSize - wCal) / 2)
                        imgWhite[:, wGap:wCal + wGap] = imgResize  # merging the images
                        prediction, index = classifier.getPrediction(imgWhite, draw=False) #Image detection
                        print(prediction, index)
                    except cv2.error:
                        print("e")


                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    try:
                        imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                        imgResizeShape = imgResize.shape
                        hGap = math.ceil((imgSize - hCal) / 2)
                        imgWhite[hGap:hCal + hGap, :] = imgResize  # merging the images
                        prediction, index = classifier.getPrediction(imgWhite, draw=False) #Image detection
                        print(prediction, index)
                    except cv2.error:
                        print("e")
                # Customizing the output frame
                try:
                    cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (46, 168, 34),
                                  4)
                    cv2.putText(imgOutput, labelEFGH[index], (x, y - 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
                except cv2.error:
                    print("e")
                except NameError:
                    print("e")
                try:
                    #Counters to check if the shown sign wasnt a fluke
                    if labelEFGH[QuestionIndex] == labelEFGH[index]:
                        counter += 1
                        print(counter)
                    else:
                        counter = 0

                    if counter < 10 and counter > 5:
                        Correct = Label(text="Correct!", padx=200, pady=200, bg="black", fg="white")
                        Correct.pack()
                        timer(1)
                        remove_all_widgets_exceptImages(window=Window)
                        unpackAll()
                        LessonIJKL()
                except UnboundLocalError:
                    print("u")
            #Showing webcam in tkinter
            FinalOutput = ImageTk.PhotoImage(Image.fromarray(imgOutput))
            L2['image'] = FinalOutput
            Window.update()
    #Next Button for Info page EFGH
    NextButton2 = Button(Window, text="Next", command=QuestionsEFGH, fg="black", bg="light blue", relief=GROOVE,
                         font=("roboto", "20", "bold"), pady=9)
    NextButton2.place(x=1258, y=400)
    #Back Button for Info page EFGH
    BackButtonTM2 = Button(Window, text="Back", command=GoingBackLsns, fg="black", bg="light blue", relief=GROOVE,
                           font=("roboto", "20", "bold"), pady=9)
    BackButtonTM2.place(x=5, y=400)


def LessonIJKL(): #Lesson for IJKL
    remove_all_widgets_exceptImages(window=Window)
    #Info page
    IJKLtext = Label(text="Hand signs for IJKL are:", padx=60, pady=50,
                     font=("Times", "24", "bold"))
    IJKLtext.pack(padx=50, pady=100)
    labelIJKL = ["I", "J", "K", "L"]

    ijkllabel.pack()

    def QuestionsIJKL():
        unpackAll()
        remove_all_widgets_exceptImages(window=Window)
        #Question Text
        QuestionIndex = randint(0, 3)
        QuestionTxt = "Show \"" + str(labelIJKL[QuestionIndex]) + "\" in ASL"
        QuestionLabel = Label(text=QuestionTxt, font=("times new roman", 30, "bold"))
        QuestionLabel.pack(padx=20, pady=20)

        #Frame holding webcam
        f3 = LabelFrame(Window, bg="red")
        f3.pack()
        L3 = Label(f3, bg="red")
        L3.pack()

        cap = cv2.VideoCapture(0) #Initialising webcam
        detector = HandDetector(maxHands=1)  # Class based on detecting the hands
        classifier = Classifier("Model/ModelIJKL.h5", "Model/labels.IJKL.txt")

        offset = 20
        imgSize = 300

        counter = 0
        counter2 = 0
        while True:
            success, img = cap.read()  # Create webcam
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgOutput = img.copy()
            hands, img = detector.findHands(img)  # Finding and mapping the hands

            if hands:  # Cropping the image of hands for precise detection
                hand = hands[0]
                x, y, w, h = hand['bbox']  # taking parameters from boundary box.

                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255  # White image

                imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]  # Cropped image(only for hands)

                imgCropShape = imgCrop.shape

                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    try:
                        imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                        imgResizeShape = imgResize.shape
                        wGap = math.ceil((imgSize - wCal) / 2)
                        imgWhite[:, wGap:wCal + wGap] = imgResize  # merging the images
                        prediction, index = classifier.getPrediction(imgWhite, draw=False) #Image prediction
                        print(prediction, index)
                    except cv2.error:
                        print("e")


                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    try:
                        imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                        imgResizeShape = imgResize.shape
                        hGap = math.ceil((imgSize - hCal) / 2)
                        imgWhite[hGap:hCal + hGap, :] = imgResize  # merging the images
                        prediction, index = classifier.getPrediction(imgWhite, draw=False) #Image prediction
                        print(prediction, index)
                    except cv2.error:
                        print("e")
                # Customizing the output frame
                try:
                    cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (46, 168, 34),
                                  4)
                    cv2.putText(imgOutput, labelIJKL[index], (x, y - 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
                except cv2.error:
                    print("e")
                except NameError:
                    print("e")
                try: #Counters to check if the given sign was a fluke or not
                    if labelIJKL[QuestionIndex] == labelIJKL[index]:
                        counter += 1
                        print(counter)
                    else:
                        counter = 0

                    if counter < 10 and counter > 5:
                        Correct = Label(text="Correct!", padx=200, pady=200, bg="black", fg="white")
                        Correct.pack()
                        timer(1)
                        remove_all_widgets_exceptImages(window=Window)
                        unpackAll()
                        lessonAD = True
                        LessonMNOP()
                except UnboundLocalError:
                    print("u")
            #Showing webcam in Window
            FinalOutput = ImageTk.PhotoImage(Image.fromarray(imgOutput))
            L3['image'] = FinalOutput
            Window.update()

    #Next and Back button for Info Page IJKL
    NextButton3 = Button(Window, text="Next", command=QuestionsIJKL, fg="black", bg="light blue", relief=GROOVE,
                         font=("roboto", "20", "bold"), pady=5)
    NextButton3.place(x=1258, y=400)

    BackButtonTM3 = Button(Window, text="Back", command=GoingBackLsns, fg="black", bg="light blue", relief=GROOVE,
                           font=("roboto", "20", "bold"), pady=5)
    BackButtonTM3.place(x=5, y=400)


def LessonMNOP(): #Lesson for MNOP
    remove_all_widgets_exceptImages(window=Window)
    #Info Page
    MNOPtext = Label(text="Hand signs for MNOP are", padx=60, pady=50,
                     font=("Times", "24", "bold"))
    MNOPtext.pack(padx=50, pady=100)
    labelMNOP = ["M", "N", "O", "P"]

    mnoplabel.pack()

    def QuestionsMNOP():
        unpackAll()
        remove_all_widgets_exceptImages(window=Window)
        #Question Text
        QuestionIndex = randint(0, 3)
        QuestionTxt = "Show \"" + str(labelMNOP[QuestionIndex]) + "\" in ASL"
        QuestionLabel = Label(text=QuestionTxt, font=("times new roman", 30, "bold"))
        QuestionLabel.pack(padx=20, pady=20)

        #Frame holding webcam
        f4 = LabelFrame(Window, bg="red")
        f4.pack()
        L4 = Label(f4, bg="red")
        L4.pack()

        cap = cv2.VideoCapture(0) #Initialising webcam
        detector = HandDetector(maxHands=1)  # Class based on detecting the hands
        classifier = Classifier("Model/keras_ModelMNOP.h5", "Model/labels_MNOP.txt")

        offset = 20
        imgSize = 300

        counter = 0 #Counters
        counter2 = 0
        while True:
            success, img = cap.read()  # Create webcam
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgOutput = img.copy()
            hands, img = detector.findHands(img)  # Finding and mapping the hands

            if hands:  # Cropping the image of hands for precise detection
                hand = hands[0]
                x, y, w, h = hand['bbox']  # taking parameters from boundary box.

                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255  # White image

                imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]  # Cropped image(only for hands)

                imgCropShape = imgCrop.shape

                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    try:
                        imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                        imgResizeShape = imgResize.shape
                        wGap = math.ceil((imgSize - wCal) / 2)
                        imgWhite[:, wGap:wCal + wGap] = imgResize  # merging the images
                        prediction, index = classifier.getPrediction(imgWhite, draw=False) #Image prediction
                        print(prediction, index)
                    except cv2.error:
                        print("e")


                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    try:
                        imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                        imgResizeShape = imgResize.shape
                        hGap = math.ceil((imgSize - hCal) / 2)
                        imgWhite[hGap:hCal + hGap, :] = imgResize  # merging the images
                        prediction, index = classifier.getPrediction(imgWhite, draw=False) #Image prediction
                        print(prediction, index)
                    except cv2.error:
                        print("e")
                # Customizing the output frame
                try:
                    cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (46, 168, 34),
                                  4)
                    cv2.putText(imgOutput, labelMNOP[index], (x, y - 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
                except cv2.error:
                    print("e")
                except NameError:
                    print("e")
                try: #counter to check if given sign wasnt a fluke
                    if labelMNOP[QuestionIndex] == labelMNOP[index]:
                        counter += 1
                        print(counter)
                    else:
                        counter = 0

                    if counter < 10 and counter > 5:
                        timer(1)
                        remove_all_widgets_exceptImages(window=Window)
                        unpackAll()
                        lessonAD = True
                        LessonQRSTU()
                except UnboundLocalError:
                    print("u")
            FinalOutput = ImageTk.PhotoImage(Image.fromarray(imgOutput))
            L4['image'] = FinalOutput
            Window.update()

    #Back and Next button for Info Page MNOP
    NextButton4 = Button(Window, text="Next", command=QuestionsMNOP, fg="black", bg="light blue", relief=GROOVE,
                         font=("roboto", "20", "bold"), pady=5)
    NextButton4.place(x=1258, y=400)

    BackButtonTM4 = Button(Window, text="Back", command=GoingBackLsns, fg="black", bg="light blue", relief=GROOVE,
                           font=("roboto", "20", "bold"), pady=5)
    BackButtonTM4.place(x=5, y=400)


def LessonQRSTU(): #Lesson for QRSTU
    remove_all_widgets_exceptImages(window=Window)
    #Info Page
    QRSTUtext = Label(text="Hand signs for QRSTU are:", padx=60, pady=50,
                      font=("Times", "24", "bold"))
    QRSTUtext.pack(padx=50, pady=100)
    labelQRSTU = ["Q", "R", "S", "T", "U"]

    qrstulabel.pack()

    def QuestionsQRSTU():
        unpackAll()
        remove_all_widgets_exceptImages(window=Window)
        #Question Text
        QuestionIndex = randint(0, 3)
        QuestionTxt = "Show \"" + str(labelQRSTU[QuestionIndex]) + "\" in ASL"
        QuestionLabel = Label(text=QuestionTxt, font=("times new roman", 30, "bold"))
        QuestionLabel.pack(padx=20, pady=20)

        f5 = LabelFrame(Window, bg="red")
        f5.pack()
        L5 = Label(f5, bg="red")
        L5.pack()

        cap = cv2.VideoCapture(0)
        detector = HandDetector(maxHands=1)  # Class based on detecting the hands
        classifier = Classifier("Model/ModelQRSTU.h5", "Model/labels.QRSTU.txt")

        offset = 20
        imgSize = 300

        counter = 0
        counter2 = 0
        while True:
            success, img = cap.read()  # Create webcam
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgOutput = img.copy()
            hands, img = detector.findHands(img)  # Finding and mapping the hands

            if hands:  # Cropping the image of hands for precise detection
                hand = hands[0]
                x, y, w, h = hand['bbox']  # taking parameters from boundary box.

                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255  # White image

                imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]  # Cropped image(only for hands)

                imgCropShape = imgCrop.shape

                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    try:
                        imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                        imgResizeShape = imgResize.shape
                        wGap = math.ceil((imgSize - wCal) / 2)
                        imgWhite[:, wGap:wCal + wGap] = imgResize  # merging the images
                        prediction, index = classifier.getPrediction(imgWhite, draw=False) #Sign Prediction
                        print(prediction, index)
                    except cv2.error:
                        print("e")


                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    try:
                        imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                        imgResizeShape = imgResize.shape
                        hGap = math.ceil((imgSize - hCal) / 2)
                        imgWhite[hGap:hCal + hGap, :] = imgResize  # merging the images
                        prediction, index = classifier.getPrediction(imgWhite, draw=False) #Sign prediction
                        print(prediction, index)
                    except cv2.error:
                        print("e")
                # Customizing the output frame
                try:
                    cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (46, 168, 34),
                                  4)
                    cv2.putText(imgOutput, labelQRSTU[index], (x, y - 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
                except cv2.error:
                    print("e")
                except NameError:
                    print("e")
                try: #Counter to check if given question was answered in fluke
                    if labelQRSTU[QuestionIndex] == labelQRSTU[index]:
                        counter += 1
                        print(counter)
                    else:
                        counter = 0

                    if counter < 10 and counter > 5:
                        timer(1)
                        remove_all_widgets_exceptImages(window=Window)
                        unpackAll()
                        lessonAD = True
                        LessonVWXYZ()
                except UnboundLocalError:
                    print("u")
            #Webcam shown in Window
            FinalOutput = ImageTk.PhotoImage(Image.fromarray(imgOutput))
            L5['image'] = FinalOutput
            Window.update()
    #Back and Next Button for Info page QRSTU
    NextButton5 = Button(Window, text="Next", command=QuestionsQRSTU, fg="black", bg="light blue", relief=GROOVE,
                         font=("roboto", "20", "bold"), pady=5)
    NextButton5.place(x=1258, y=400)

    BackButtonTM5 = Button(Window, text="Back", command=GoingBackLsns, fg="black", bg="light blue", relief=GROOVE,
                           font=("roboto", "20", "bold"), pady=5)
    BackButtonTM5.place(x=5, y=400)


def LessonVWXYZ(): #Lesson for VWXYZ
    remove_all_widgets_exceptImages(window=Window)
    #Question text
    VWXYZtext = Label(text="Hand signs for VWXYZ are", padx=60, pady=50,
                      font=("Times", "24", "bold"))
    VWXYZtext.pack(padx=50, pady=100)
    labelVWXYZ = ["V", "W", "X", "Y", "Z"]

    vwxyzlabel.pack()

    def QuestionsVWXYZ():
        unpackAll()
        remove_all_widgets_exceptImages(window=Window)
        #Question Text
        QuestionIndex = randint(2, 4)
        QuestionTxt = "Show \"" + str(labelVWXYZ[QuestionIndex]) + "\" in ASL"
        QuestionLabel = Label(text=QuestionTxt, font=("times new roman", 30, "bold"))
        QuestionLabel.pack(padx=20, pady=20)

        #Frame holding webcam
        f6 = LabelFrame(Window, bg="red")
        f6.pack()
        L6 = Label(f6, bg="red")
        L6.pack()

        cap = cv2.VideoCapture(0) #Initialising webcam
        detector = HandDetector(maxHands=1)  # Class based on detecting the hands
        classifier = Classifier("Model/Modellastl.h5", "Model/labels.last.txt")

        offset = 20
        imgSize = 300

        counter = 0
        counter2 = 0
        while True:
            success, img = cap.read()  # Create webcam
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgOutput = img.copy()
            hands, img = detector.findHands(img)  # Finding and mapping the hands

            if hands:  # Cropping the image of hands for precise detection
                hand = hands[0]
                x, y, w, h = hand['bbox']  # taking parameters from boundary box.

                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255  # White image

                imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]  # Cropped image(only for hands)

                imgCropShape = imgCrop.shape

                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    try:
                        imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                        imgResizeShape = imgResize.shape
                        wGap = math.ceil((imgSize - wCal) / 2)
                        imgWhite[:, wGap:wCal + wGap] = imgResize  # merging the images
                        prediction, index = classifier.getPrediction(imgWhite, draw=False) #Sign prediction
                        print(prediction, index)
                    except cv2.error:
                        print("e")


                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    try:
                        imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                        imgResizeShape = imgResize.shape
                        hGap = math.ceil((imgSize - hCal) / 2)
                        imgWhite[hGap:hCal + hGap, :] = imgResize  # merging the images
                        prediction, index = classifier.getPrediction(imgWhite, draw=False) #Sign prediction
                        print(prediction, index)
                    except cv2.error:
                        print("e")
                # Customizing the output frame
                try:
                    cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (46, 168, 34),
                                  4)
                    cv2.putText(imgOutput, labelVWXYZ[index], (x, y - 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 2)
                except cv2.error:
                    print("e")
                except NameError:
                    print("e")
                try: #Counter to check if shown sign was a fluke
                    if labelVWXYZ[QuestionIndex] == labelVWXYZ[index]:
                        counter += 1
                        print(counter)
                    else:
                        counter = 0

                    if counter < 10 and counter > 5:
                        timer(1)
                        remove_all_widgets_exceptImages(window=Window)
                        unpackAll()
                        LessonsDone()

                except UnboundLocalError:
                    print("u")
            #Showing webcam to Window
            FinalOutput = ImageTk.PhotoImage(Image.fromarray(imgOutput))
            L6['image'] = FinalOutput
            Window.update()
    #Back and Next button for Info Page VWXYZ
    NextButton6 = Button(Window, text="Next", command=QuestionsVWXYZ, fg="black", bg="light blue", relief=GROOVE,
                         font=("roboto", "20", "bold"), pady=5)
    NextButton6.place(x=1258, y=400)

    BackButtonTM6 = Button(Window, text="Back", command=GoingBackLsns, fg="black", bg="light blue", relief=GROOVE,
                           font=("roboto", "20", "bold"), pady=5)
    BackButtonTM6.place(x=5, y=400)

def ModuleComplete(): #Updating data into Leaderboard
    Name = NameBox.get(1.0,END) #Gets Name from Text box
    if Name == "": #If name not given
        cursor.execute("INSERT INTO LEADERBOARD VALUES('Anonymous','{}')".format(finalTime))
    else: #If name given
        cursor.execute("INSERT INTO LEADERBOARD VALUES('{}','{}')".format(Name,finalTime))

    remove_all_widgets_exceptImages(window=Window)
    unpackAll()
    timer(1)
    #Main Page
    InterpreterButton = Button(Window, text="Interpreter", command=switchInterpreterWindow, fg="white",
                               bg="#4F3475",
                               font=("roboto", "24", "bold"), relief=GROOVE, padx=50, pady=50)
    title = Label(text="Sign Recognition Project", bg="#D62768", fg="white", padx=60, pady=50,
                  font=("roboto", "24", "bold"))
    LessonButton = Button(Window, text="Lessons", command=LessonABCD, fg="white", bg="#4C6FBE",
                          font=("roboto", "24", "bold"), relief=GROOVE, padx=70, pady=40)
    LeaderboardButton = Button(Window, text="Leaderboard", command=switchLeaderboardWindow, fg="white",
                               bg="#4F3475",
                               font=("roboto", "24", "bold"), relief=GROOVE, padx=50, pady=50)

    title.pack(padx=50, pady=50)
    InterpreterButton.pack(pady=15)
    LessonButton.pack(pady=15)
    LeaderboardButton.pack(pady=15)

def LessonsDone(): #After lessons complete
    unpackAll()
    global endTime
    endTime = time.time() #Registers end time
    #Compiles Final time taken (end time - start time) and puts it in mins:secs
    finalTime = ":".join([str(int(endTime - startTime) // 60), str(int(endTime - startTime) % 60)])

    #Congratulations page
    CongoWindow = Label(text="Congratulations!", pady=10, padx=30, fg="white", bg="#4F3475",
                        font=('roboto', "40", "bold"))
    CongoWindow.place(x=350, y=100)

    CongoText = Label(text="Congratulations! You have completed this lesson!", font=('roboto', "20", "bold"),
                      fg="white", bg="#211e1e")
    CongoText.place(x=370, y=300)

    #Shows Time taken to finish
    CongoText = Label(text="Your time is: {}".format(finalTime), font=('roboto', "20", "bold"),
                      fg="white", bg="#211e1e")
    CongoText.place(x=370, y=400)

    NameFrame = Frame(Window)
    NameFrame.place(x=370, y=600)

    #Text box to take name
    NameText = Label(NameFrame, text="Please enter your name:", font=('roboto', "20", "bold"),
                     fg="white", bg="#211e1e")
    NameText.pack()
    NameBox = Text(NameFrame, width=20, height=1, padx=10, pady=10, font=('Helvetica', 16))
    NameBox.pack()

    #Return button
    ReturnButton = Button(text="Back to menu!",command= ModuleComplete,font=("roboto", "20", "bold"), fg="white",
                          bg="#4C6FBE")
    ReturnButton.place(x=960, y=500)

#Lessons button from main page
LessonButton = Button(Window, text="Lessons", fg="white", command=LessonABCD, bg="#4C6FBE",
                      font=("roboto", "24", "bold"), relief=GROOVE, padx=70, pady=40)

#Shows main page buttons
InterpreterButton.pack(pady=15)
LessonButton.pack(pady=15)
LeaderboardButton.pack(pady=15)


Window.mainloop()
cursor.close()
conn.close()

#Code END