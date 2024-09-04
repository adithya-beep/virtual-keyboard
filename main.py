import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller,Key

cap = cv2.VideoCapture(0)
cap.set(4, 1280)
cap.set(3, 720)
flag=0

detector = HandDetector(detectionCon=0.8, maxHands=2)
#keys=[]
keys=[["Q", "W", "E", "R", "T", "Y", "U", "I", "O"],
      ["P", "A", "S", "F", "G", "H", "J", "K","L"],
      [";", "Z", "X", "C", "V", "B", "N", "M", ","],
      [".", "/", "<-", "--", "<<", "cl"]]
finalText = ""

keyboard = Controller()


def drawAll(img, buttonList):
   for button in buttonList:
       x, y = button.pos
       w, h = button.size
       cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0)
       cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
       cv2.putText(img, button.text, (x + 20, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
   return img


# def drawAll(img, buttonList):
#     imgNew = np.zeros_like(img, np.uint8)
#     for button in buttonList:
#         x, y = button.pos
#         w, h = button.size
#         cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0)
#         cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]), (255, 0, 255), cv2.FILLED)
#         cv2.putText(img, button.text, (x + 20, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
#     out = img.copy()
#     alpha = 0.5
#     mask = imgNew.astype(bool)
#     print(mask.shape)
#     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1-alpha, 0)[mask]
#     return out


class Button():
    def __init__(self, pos, text, size=[50, 50]):
        self.pos = pos
        self.size = size
        self.text = text

buttonList=[]
for i in range(len(keys)):
    for x, key in enumerate(keys[i]):
        buttonList.append(Button([70 * x + 25, 70 * i + 50], key))


while True:
    success, img = cap.read()

    hands, img = detector.findHands(img, flipType=True)
    img = drawAll(img, buttonList)
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        centerPoint1 = hand1["center"]
        handType1= hand1["type"]


        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            if x< lmList1[8][0] < x +w and y<lmList1[8][1]<y+h:
                cv2.rectangle(img, (x-5, y-5), (x + w+5, y + h+5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
                l, info = detector.findDistance(lmList1[8][:2], lmList1[12][:2])
                print(l)

                #whenever we click
                if l<30:
                    if button.text=="<-":
                        keyboard.press(Key.enter)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
                        keyboard.release(Key.enter)
                        sleep(.3)
                    elif button.text=="--":
                        keyboard.press(Key.space)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
                        keyboard.release(Key.space)
                        sleep(.3)

                    elif button.text=="<<":
                        keyboard.press(Key.backspace)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
                        keyboard.release(Key.backspace)
                        sleep(.3)
                    elif button.text=="cl":

                        keyboard.press(Key.caps_lock)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
                        keyboard.release(Key.backspace)

                        sleep(.3)

                    else:
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
                        finalText += button.text
                        sleep(.3)

    cv2.rectangle(img, (60, 350), (600, 400), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (81, 399), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)


    cv2.imshow("Image", img)
    cv2.waitKey(1)





