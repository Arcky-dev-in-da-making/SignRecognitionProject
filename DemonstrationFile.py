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

conn = mysql.connect(host = "localhost",password = "Ch3atosiscool",user = "root" ,database = "ModuleScores")
cursor = conn.cursor()

#Window configuration
Window = Tk()
Frame(Window, bg="black").pack()
Window.geometry("1920x1080")
Window.configure(bg="#1C1A1D")
Window.title("Sign Recognition Project!")
Window.minsize(200, 200)


title = Label(text="Sign Recognition Project", bg="#D62768", fg="white", padx=60, pady=50,
              font=("roboto", "24", "bold"))

title.pack(padx=50, pady=50)  # Setting the Title Box location (change the color schemes if yall want)

abcdimage = Image.open("images/abcd.jpg")
abcdphoto = ImageTk.PhotoImage(abcdimage)
abcdlabel = Label(image=abcdphoto)

startTime = 0
endTime = 0
def timer(seconds):
    start_time = time.time()
    time_elapsed = 0
    while time_elapsed < seconds:
        time_elapsed = time.time() - start_time
    print("Time's up!")


def GoingBackLsns():
    remove_all_widgets_exceptImages(window=Window)
    unpackAll()
    timer(1)
    InterpreterButton = Button(Window, text="Interpreter",command = switchInterpreterWindow, fg="white",
                               bg="#4F3475",
                               font=("roboto", "24", "bold"), relief=GROOVE, padx=50, pady=50)
    title = Label(Window,text="Sign Recognition Project", bg="#D62768", fg="white", padx=60, pady=50,
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


def unpackAll():
    abcdlabel.pack_forget()


def remove_all_widgets_exceptImages(window):
    for widget in window.winfo_children():
        if widget not in [abcdlabel]:
            widget.destroy()


def switchInterpreterWindow():
    remove_all_widgets_exceptImages(window=Window)

    BackButton = Button(Window, text="Back", command=GoingBackLsns, fg="black", bg="light blue", relief=GROOVE,
                        font=("roboto", "20", "bold"), pady=10, padx=25)
    BackButton.pack(anchor="sw")

    InterpreterCamTxt = Label(Window, text="InterpreterCam", font=("sans serif", 30, "bold"), bg="black", fg="white")
    InterpreterCamTxt.pack()
    f1 = LabelFrame(Window, bg="red")
    f1.pack()
    L1 = Label(f1, bg="red")
    L1.pack()

    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)  # Class based on detecting the hands
    classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

    offset = 20
    imgSize = 300

    counter = 0
    counter2 = 0
    newString = ''
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
                                #Square image [300x300], 3 showing color in image, *255 for white color
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]  # Cropped image(only for hands)
                         #starting height:end height,starting width:ending width
            imgCropShape = imgCrop.shape

            aspectRatio = h / w

            if aspectRatio > 1: #Height greater than width
                k = imgSize / h
                wCal = math.ceil(k * w) #Stretching width to get the image in proportion
                try:
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize)) #wCal = width,imgSize = height
                    imgResizeShape = imgResize.shape
                    wGap = math.ceil((imgSize - wCal) / 2) #So that image is centered
                    imgWhite[:, wGap:wCal + wGap] = imgResize  # merging the images, width stays the same
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)  
                    print(prediction, index)
                except cv2.error:
                    print("e")


            else: #Width greater than height
                k = imgSize / w
                hCal = math.ceil(k * h) #Stretching height to get image in proportion
                try:
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal)) #hCal = Calculated height
                    imgResizeShape = imgResize.shape
                    hGap = math.ceil((imgSize - hCal) / 2) #hGap = Gap from the edges (so as to center image)
                    imgWhite[hGap:hCal + hGap, :] = imgResize  # merging the images, height stays the same
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)
                    print(prediction, index)
                except cv2.error:
                    print("e")
            # Customizing the output frame
            try:
                cv2.rectangle(imgOutput, (x - offset, y - offset - 50), (x - offset + 100, y - offset), (46, 168, 34),
                              cv2.FILLED)
                cv2.putText(imgOutput, labels[index], (x, y - 40), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 4)
                if labels[index] in ["A", "B", 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                                     'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', "_"]:
                    counter += 1
                    if counter % 10 == 0:
                        newString = newString + labels[index]
                        print(newString)
                else:
                    counter2 += 1
                    if counter2 >= 5:
                        newString = ""
                        counter2 = 0
                cv2.putText(imgOutput, newString, (x + 100, y - 40), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 4)

                cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (46, 168, 34), 4)
            except cv2.error:
                print("e")
            except NameError:
                print("e")
        FinalOutput = ImageTk.PhotoImage(Image.fromarray(imgOutput))
        L1['image'] = FinalOutput
        Window.update()


InterpreterButton = Button(Window, text="Interpreter", command=switchInterpreterWindow, fg="white", bg="#4F3475",
                           font=("roboto", "24", "bold"), relief=GROOVE, padx=50, pady=50)

def switchLeaderboardWindow():
    remove_all_widgets_exceptImages(window = Window)

    BackButton = Button(Window, text="Back", command=GoingBackLsns, fg="black", bg="light blue", relief=GROOVE,
                        font=("roboto", "20", "bold"), pady=10, padx=25)
    BackButton.pack(anchor="sw")

    Leaderboard = ttk.Treeview(Window, columns=("Position", "Name", "Time"), show="headings")


    Leaderboard.heading("Position", text="Position")
    Leaderboard.heading("Name", text="Name")
    Leaderboard.heading("Time", text="Time")

    style = ttk.Style(Window)
    style.theme_use("clam")
    style.configure("Treeview", background="black", fieldbackground="black", foreground="white")
    style.map("Treeview", background=[("selected", "blue")])

    Leaderboard.place(x=200,y=50,width=1300,height=700)

    cursor.execute("SELECT * FROM LEADERBOARD ORDER BY TIME DESC")
    data = cursor.fetchall()
    for i in data:
        pos = len(data) - data.index(i)
        Leaderboard.insert(parent='', index=0, values=(pos, i[0], i[1]))

    font = ("Arial", 90)
    Leaderboard.tag_configure("tree_font", font=font)

LeaderboardButton = Button(Window, text="Leaderboard", command=switchLeaderboardWindow, fg="white", bg="#4F3475",
                           font=("roboto", "24", "bold"), relief=GROOVE, padx=50, pady=50)

def LessonABCD():
    remove_all_widgets_exceptImages(window=Window)
    global startTime
    startTime = time.time()
    ABCDtext = Label(text="Hand signs for ABCD are:", padx=60, pady=50,
                     font=("Times", "24", "bold"))

    ABCDtext.pack(padx=50, pady=100)
    labelABCD = ["A", "B", "C", "D"]

    abcdlabel.pack()

    def QuestionsABCD():
        unpackAll()
        remove_all_widgets_exceptImages(window=Window)
        QuestionIndex = randint(0, 3)
        QuestionTxt = "Show \"" + str(labelABCD[QuestionIndex]) + "\" in ASL"

        QuestionLabel = Label(text=QuestionTxt, font=("times new roman", 30, "bold"))
        QuestionLabel.pack(padx=20, pady=20)

        f2 = LabelFrame(Window, bg="red")
        f2.pack()
        L2 = Label(f2, bg="red")
        L2.pack()

        cap = cv2.VideoCapture(0)
        detector = HandDetector(maxHands=1)  # Class based on detecting the hands
        classifier = Classifier("Model/ModelABCD.h5", "Model/labels.ABCD.txt")

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
                        prediction, index = classifier.getPrediction(imgWhite, draw=False)
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
                        prediction, index = classifier.getPrediction(imgWhite, draw=False)
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
                        LessonsDone()
                except UnboundLocalError:
                    print("u")
            FinalOutput = ImageTk.PhotoImage(Image.fromarray(imgOutput))
            L2['image'] = FinalOutput
            Window.update()

    NextButton = Button(Window, text="Next", command=QuestionsABCD, fg="black", bg="light blue", relief=GROOVE,
                        font=("roboto", "20", "bold"), pady=1, padx=9)
    NextButton.place(x=1430, y=400)

    BackButtonTM = Button(Window, text="Back", command=GoingBackLsns, fg="black", bg="light blue", relief=GROOVE,
                          font=("roboto", "20", "bold"), pady=1, padx=9)
    BackButtonTM.place(x=5, y=400)



def LessonsDone():

    unpackAll()
    global endTime
    endTime = time.time()
    finalTime = ":".join([str(int(endTime - startTime) // 60), str(int(endTime - startTime) % 60)])

    def ModuleComplete():
        Name = NameBox.get(1.0, END)
        if Name == "":
            cursor.execute("INSERT INTO LEADERBOARD VALUES('Anonymous','{}')".format(finalTime))
        else:
            cursor.execute("INSERT INTO LEADERBOARD VALUES('{}','{}')".format(Name,finalTime))

        conn.commit()

        remove_all_widgets_exceptImages(window=Window)
        unpackAll()
        timer(1)
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
    CongoWindow = Label(text="Congratulations!", pady=10, padx=30, fg="white", bg="#4F3475",
                        font=('roboto', "40", "bold"))
    CongoWindow.place(x=350, y=100)

    CongoText = Label(text="Congratulations! You have completed this lesson!", font=('roboto', "20", "bold"),
                      fg="white", bg="#211e1e")
    CongoText.place(x=370, y=300)

    CongoText = Label(text="Your time is: {}".format(finalTime), font=('roboto', "20", "bold"),
                      fg="white", bg="#211e1e")
    CongoText.place(x=370, y=400)

    NameFrame = Frame(Window)
    NameFrame.place(x=370, y=600)
    NameText = Label(NameFrame, text="Please enter your name:", font=('roboto', "20", "bold"),
                     fg="white", bg="#211e1e")
    NameText.pack()
    NameBox = Text(NameFrame, width=20, height=1, padx=10, pady=10, font=('Helvetica', 16))
    NameBox.pack()

    ReturnButton = Button(text="Back to menu!", command=ModuleComplete, font=("roboto", "20", "bold"), fg="white",
                          bg="#4C6FBE")
    ReturnButton.place(x=960, y=500)

LessonButton = Button(Window, text="Lessons", fg="white", command=LessonABCD, bg="#4C6FBE",
                      font=("roboto", "24", "bold"), relief=GROOVE, padx=70, pady=40)

InterpreterButton.pack(pady=15)
LessonButton.pack(pady=15)
LeaderboardButton.pack(pady=15)

Window.mainloop()
cursor.close()
conn.close()
