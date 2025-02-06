from tkinter import *
from tkinter import ttk
import time
startTime = time.time()
Window = Tk()
Frame(Window, bg = "black").pack()
Window.geometry("1920x1080")
Window.configure(bg = "black")
Window.title("Sign Recognition Project!")
Window.minsize(200, 200)
endTime = time.time()
finalTime = ":".join([str(int(endTime - startTime) // 60), str(int(endTime - startTime) % 60)])
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
NameFrame.place(x=370,y=600)
NameText = Label(NameFrame,text="Please enter your name:",font=('roboto', "20", "bold"),
                  fg="white", bg="#211e1e")
NameText.pack()
NameBox = Text(NameFrame,width=20,height=1,padx=10,pady=10,font=('Helvetica',16))
NameBox.pack()

ReturnButton = Button(text="Back to menu!",font=("roboto", "20", "bold"), fg="white",
                      bg="#4C6FBE")
ReturnButton.place(x=960, y=500)



Window.mainloop()