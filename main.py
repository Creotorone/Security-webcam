import cv2
import time
import glob
import os
from emailing import send_email
from datetime import datetime
from threading import Thread


scale = 30

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []

def clean_folder():
    print("Starting clean_folder")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("Finishing clean_folder")


while True:
    status = 0
    check, frame = video.read()
    height, width, channels = frame.shape

    centerX, centerY = int(height / 2), int(width / 2)
    radiusX, radiusY = int(scale * height / 100), int(scale * width / 100)
    minX, maxX = centerX - radiusX, centerX + radiusX
    minY, maxY = centerY - radiusY, centerY + radiusY

    cropped = frame[minX:maxX, minY:maxY]
    resized_cropped = cv2.resize(cropped, (width, height))

    gray_frame = cv2.cvtColor(resized_cropped, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21,21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    # cv2.imshow("My video", thresh_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(resized_cropped, (x, y), (x+w, y+h), (0, 255, 0), 3)

        now = datetime.now()

        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{now}.png", resized_cropped)
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]


    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(image_with_object, ))
        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        email_thread.start()

    print(status_list)

    cv2.imshow("Video", resized_cropped)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

clean_thread.start()

video.release()



