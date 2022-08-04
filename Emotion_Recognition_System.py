# These are the imported modules that were required to make the emotion recognition program work. The OpenCV (cv2) module is responsible for the main webcam access
# and drawing the window to show the webcam video. The cvzone module is the library which is used to access the SelfiSegmentation function to carry
# out background subtraction around the user in the webcam video. The Datetime module is used to display the time of each frame recorded for the experimentation.
# The OS module is used to create the necessary directory needed to store the data correctly. The Tkinter module was used to create the GUI for the main menu,
# the buttons and the about and credits windows. The DeepFace module is the key module in this program and it was used to help with detecting the emotions
# from the faces captured on the webcam video. 

# Author: Thomas Shavin Croos
# Credits: See credit function.
# Version: ERS Visual V3.0
# Maintainer: Thomas Shavin Croos
# Email: shavinminecraft@gmail.com

import cv2
import cvzone
import datetime
import os
from tkinter import *
from deepface import DeepFace
from cvzone.SelfiSegmentationModule import SelfiSegmentation

# These 6 lines of code will generate the window for the main menu for the emotion detection program.
win = Tk()
win.geometry('500x350')
win.title("ERS Visual V3.0")
Label(win, text = "ERS VISUAL V3.0\n", font = 'arial 20 bold').pack()
Label(win, text = "Emotion Recognition System", font = 'arial 20 bold').place(x = 50, y = 45)
Label(win, text = 'MENU', font = 'arial 15 bold').place(x = 210, y = 90)

def emotRegSys():

    # Any code commented out was used for the purposes for testing the program in the background and carrying out the main experimentation used
    # for my final year project. You may uncomment them to try to record the data if you wish.
    
    # User inputs the name of the folder to store the data for experimentation and is assigned to the child_dir variable as a string.
    # name = input("input folder name: ")

    # child_dir = str(name) 

    # Directory path of the folder is given in string form and assigned to parent_dir.
    # parent_dir = 'D:\ERST'

    # os.path.join joins the name of the folder with the directory path the folder will be stored in. When this is done, os.mkdir
    # will create the folder in the output of the os.path.join() function.
    # os.mkdir(os.path.join(parent_dir, child_dir))

    # A new text folder will be opened and written in, which will be saved
    # as the same name as the folder it will be stored in.
    # txt = open(parent_dir + '\\' + child_dir + '\\' + name + '.txt', "w")

    # This will write the headers of the emotions in the text file.
    # txt.write("Frame_no.\tTime\t\tAngry\t\tFear\t\tNeutral\tSad\t\tDisgust\tHappy\t\tSurprise")

    # A check print statement to confirm that the folder is created, along with the text file.
    # print("Directory '%s' created" % child_dir)

    # The haarcascade_frontalface_default.xml file is imported and called through the OpenCV module.
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Any internal webcam on the system is attempted to be found and accessed by VideoCapture(0).
    # If successful, the program will connect to a chosen internal webcam.
    cam = cv2.VideoCapture(0)

    # The class behind the background subtraction function is called and assigned to segmentor. 
    segmentor = SelfiSegmentation()

    # img_counter = 0
    
    # f initialises the frame number variable, starting at 0 each time the program is called.
    f = 0

    # if statement checks are carried out if any internal webcam cannot be be either found or accessed.
    # When an internal webcam cannot be found or accessed, then any external webcam on the the system
    # is attempted to be found and accessed by VideoCapture(1). When no webcams can be found or accessed,
    # the program will print an error telling the user that the camera cannot be found or accessed and to
    # try the program again after the webcam is plugged in or installed.
    if not cam.isOpened():
        cam = cv2.VideoCapture(1)
    if not cam.isOpened():
        raise IOError("Error! Camera not detected or cannot access Camera! Please fix the issue and try again!")
        print("Error! Inbuilt camera not detected or cannot access inbuilt camera! Please fix the issue and try again!")

    # The main functionality of the program runs in this while loop.
    while True:
        # The frame is read from the web camera and is passed into the background subtraction function removeBG() to remove the background
        # of the frame around the user. When this is done, the analyze() function of DeepFace is called and all the 7 emotions are recorded
        # and stored in emotRes.
        ret, frame = cam.read()
        frame = segmentor.removeBG(frame, (218, 197, 99), threshold=0.825)
        emotRes = DeepFace.analyze(frame, actions = ['emotion'], enforce_detection = False)

        # Frame is grayscaled for easier detection of a face due to only one colour channel being involved.
        # detectMultiScale() function will scale any faces detected on the frame to compare to images stored
        # in the cascade file called earlier.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.1, 4)

        # Simply draws a rectange around a face when one is detected in frame.
        for(x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        font = cv2.FONT_HERSHEY_SIMPLEX

        # The emotRes function is called to print out all the emotions as percentages on the frame.
        cv2.putText(frame, 'Angry: ' + str('%.1f' % (emotRes['emotion'].get('angry'))) + '%', (10, 20), font, 0.5, (255, 0, 0), 2, cv2.LINE_4)
        cv2.putText(frame, 'Fear: ' + str('%.1f' % (emotRes['emotion'].get('fear'))) + '%', (10, 40), font, 0.5, (255, 0, 0), 2, cv2.LINE_4)
        cv2.putText(frame, 'Neutral: ' + str('%.1f' % (emotRes['emotion'].get('neutral'))) + '%', (10, 60), font, 0.5, (255, 0, 0), 2, cv2.LINE_4)
        cv2.putText(frame, 'Sad: ' + str('%.1f' % (emotRes['emotion'].get('sad'))) + '%', (10, 80), font, 0.5, (255, 0, 0), 2, cv2.LINE_4)
        cv2.putText(frame, 'Disgust: ' + str('%.1f' % (emotRes['emotion'].get('disgust'))) + '%', (10, 100), font, 0.5, (255, 0, 0), 2, cv2.LINE_4)
        cv2.putText(frame, 'Happy: ' + str('%.1f' % (emotRes['emotion'].get('happy'))) + '%', (10, 120), font, 0.5, (255, 0, 0), 2, cv2.LINE_4)
        cv2.putText(frame, 'Surprise: ' + str('%.1f' % (emotRes['emotion'].get('surprise'))) + '%', (10, 140), font, 0.5, (255, 0, 0), 2, cv2.LINE_4)

        # Prints FPS counter on screen to check program is running smoothly.
        cv2.putText(frame, "FPS: {}".format(cam.get(cv2.CAP_PROP_FPS)), (475,30), font, 1, (255, 0, 0), 2, cv2.LINE_4)

        # Obtains the current date and time.
        ct = datetime.datetime.now()

        # Strips date to only show the time.
        current_time = ct.strftime("%H:%M:%S")

        # The emotRes function is called again to print out all the emotions as long decimal numbers on the terminal.
        print("Frame no.: " + str(f))
        print("Time: ", current_time)
        print("Angry: " + str('%.8f' % (emotRes['emotion'].get('angry'))) + " (" + str('%.1f' % (emotRes['emotion'].get('angry'))) + '%)')
        print("Fear: " + str('%.8f' % (emotRes['emotion'].get('fear'))) + " (" + str('%.1f' % (emotRes['emotion'].get('fear'))) + '%)')
        print("Neutral: " + str('%.8f' % (emotRes['emotion'].get('neutral'))) + " (" + str('%.1f' % (emotRes['emotion'].get('neutral'))) + '%)')
        print("Sad: " + str('%.8f' % (emotRes['emotion'].get('sad'))) + " (" + str('%.1f' % (emotRes['emotion'].get('sad'))) + '%)')
        print("Disgust: " + str('%.8f' % (emotRes['emotion'].get('disgust'))) + " (" + str('%.1f' % (emotRes['emotion'].get('disgust'))) + '%)')
        print("Happy: " + str('%.8f' % (emotRes['emotion'].get('happy'))) + " (" + str('%.1f' % (emotRes['emotion'].get('happy'))) + '%)')
        print("Surprise: " + str('%.8f' % (emotRes['emotion'].get('surprise'))) + " (" + str('%.1f' % (emotRes['emotion'].get('surprise'))) + '%)')
        print("\n")

        # The data for the experiment is printed in the text in this format underneath the headers
        # that were called previously.
        # txt.write("\n" + str(f) + "\t\t" + str(current_time) + "\t" + str('%.8f' % (emotRes['emotion'].get('angry'))) + "\t" + str('%.8f' % (emotRes['emotion'].get('fear'))) + "\t" + str('%.8f' % (emotRes['emotion'].get('neutral'))) + "\t" + str('%.8f' % (emotRes['emotion'].get('sad'))) + "\t" + str('%.8f' % (emotRes['emotion'].get('disgust'))) + "\t" + str('%.8f' % (emotRes['emotion'].get('happy'))) + "\t" + str('%.8f' % (emotRes['emotion'].get('surprise'))))        

        # If anger exceeds 80%, then this message will print on the screen and terminal.
        if(emotRes['emotion'].get('angry') > 80):
            cv2.putText(frame, 'Angry: ' + str('%.1f' % (emotRes['emotion'].get('angry'))) + '%', (10, 20), font, 0.5, (0, 0, 255), 2, cv2.LINE_4)
            cv2.putText(frame, 'You are getting a bit too angry, please try to enjoy the game!', (75, 400), font, 0.5, (0, 0, 255), 2, cv2.LINE_4)
            print("WARNING! Anger levels detected above set threshold of 80%!\n")

        # If happy exceeds 70%, then this message will print on the screen and terminal.
        if(emotRes['emotion'].get('happy') > 70):
            cv2.putText(frame, 'Happy: ' + str('%.1f' % (emotRes['emotion'].get('happy'))) + '%', (10, 120), font, 0.5, (0, 255, 0), 2, cv2.LINE_4)
            cv2.putText(frame, 'Great job, keep enjoying the game!', (185, 400), font, 0.5, (0, 255, 0), 2, cv2.LINE_4)
            print("NOTICE! Happy levels deteced above set threshold of 70%! Great job, please keep it up!\n")

        # Frame number incremented.
        # f += 1

        # Prints message to give user visual clue to close the window if they wish to stop the program after use.
        # The frame is drawn in a window.
        cv2.putText(frame, 'Press c to close', (200,450), font, 1, (0, 255, 0), 2, cv2.LINE_4)
        output = cv2.resize(frame, (1920,1080))
        cv2.imshow("ERS Visual V3.0 - Emotion Recognition System", output)

        # When c is pressed, the while loop breaks.
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break

    # The text file is saved and closed, the camera is released from use and
    # the window for the emotion detection program is destroyed.
    # txt.close()
    cam.release()
    cv2.destroyAllWindows()

def credit():
    # Credits page with details the program's libraries and those who helped
    # contribute to the program in terms of experimentation.
    winCredit = Tk()
    winCredit.geometry('500x600')
    winCredit.title('ERS Visual V3.0 - Credits')

    Label(winCredit, text = "CREDITS", font = 'arial 20 bold').pack()
    Label(winCredit, text = "Created and Tested by Shavin Croos", font = 'arial 15').pack()
    Label(winCredit, text = "With thanks to the Testers:", font = 'arial 15').pack()
    Label(winCredit, text = "Ali Al-Dibouni", font = 'arial 15').pack()
    Label(winCredit, text = "Charith Fragoso", font = 'arial 15').pack()
    Label(winCredit, text = "Uthman Maigari", font = 'arial 15').pack()
    Label(winCredit, text = "Samuel Alsford", font = 'arial 15').pack()
    Label(winCredit, text = "Morgan Rees\n", font = 'arial 15').pack()

    Label(winCredit, text = "Libraries Used: ", font = 'arial 15').pack()
    Label(winCredit, text = "OpenCV - To access camera.", font = 'arial 15').pack()
    Label(winCredit, text = "Deepface - To detect emotions.", font = 'arial 15').pack()
    Label(winCredit, text = "Tkinter - Provides overall GUI, especially fo the menu.", font = 'arial 15').pack()
    Label(winCredit, text = "DateTime - Records time for data collection.", font = 'arial 15').pack()
    Label(winCredit, text = "CVZone - To replace background \n(using SelfiSegmentation function). ", font = 'arial 15').pack()
    Label(winCredit, text = "OS (This is for saving files for data collection)", font = 'arial 15').pack()
    
def about():
    # About page tells the user how to use the program and what is shown in the program.
    winAbout = Tk()
    winAbout.geometry('750x500')
    winAbout.title('ERS Visual V3.0 - About')

    Label(winAbout, text = "ABOUT", font = 'arial 20 bold').pack()
    Label(winAbout, text = "Click on START to start detecting the emotions\n in real-time, using your webcam of choice.", font = 'arial 15').pack()
    Label(winAbout, text = "The emotions are displayed on the top left hand corner of\n the window and shows the extent of the emotion being detected.", font = 'arial 15').pack()
    Label(winAbout, text = "100 means that this is the emotion strongly being detected\n and 0 means that the emotion isn't being detected at all.", font = 'arial 15')
    Label(winAbout, text = "To make sure this software works at its best,\n please make sure you are in a well lit area\n and that the area is free of clutter, \nespecially in the background where the camera will be pointing.", font = 'arial 15').pack()
    Label(winAbout, text = "The background has been removed to improve the detection accuracy, \n but it's still highly recommended that you follow the afforementioned advice.", font = 'arial 15').pack()
    Label(winAbout, text = "You may adjust your sitting position\n and posture to make sure the detector is picking up on your face nicely.", font = 'arial 15').pack()
    Label(winAbout, text = "Please note that the emotions picked up \nby the detector may not always be accurate. ", font = 'arial 15').pack()
    Label(winAbout, text = "The aim of this program is to try to help make gameplay more enjoyable. ", font = 'arial 15').pack()

# Buttons created will lead to the other functions in this program.
Button(win, text = 'START', font = 'arial 15', command = emotRegSys, bg = '#4dff00').place(x = 200, y = 140)
Button(win, text = 'ABOUT', font = 'arial 15', command = about, bg = 'yellow').place(x = 198, y = 200)
Button(win, text = 'CREDITS', font = 'arial 15', command = credit, bg = 'cyan').place(x = 188, y = 260)
win.mainloop()

# END
