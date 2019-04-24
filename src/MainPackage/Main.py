
import numpy as np
import cv2

"""
Global Instances and Variables ------------->
"""
# initialize video instance with video full root
vid = cv2.VideoCapture('C:/Users\Test\PycharmProjects/UWIDS/vid3.MOV')

# define thresholds for Hue, Saturation, Value scale
hsvLowerThresh = [20, 10, 10] #50-20-20
hsvUpperThresh = [100, 255, 255] #100-255-255
vid_valid = False

"""
Main Function Below ----------------------->
"""

# main video processing function
def runMainProcess():
    global vid_valid
    # check that video file is valid/compatible
    if vid.read() == (False, None):
        print('Error Opening Video File!')
    else:
        vid_valid = True

    # start infinite loop for video frame processing if video file is valid
    while vid_valid:

        # read frame and convert it from BGR to HSV
        _,frame = vid.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # create numpy arrays from HSV lists
        lower = np.array(hsvLowerThresh)
        upper = np.array(hsvUpperThresh)
        # create a mask that identifies pixels of the original frame that are within the HSV range
        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # lay the mask over the original frame - this is used for calibration to visually inspect
        # vid_filtered = cv2.bitwise_and(frame, frame, mask=mask)

        # copy the mask because the operation will overwrite the original
        # find the contours of the mask using simplified extraction methods
        cnts,__ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # for each contour found in the frame, filter out any that have very large areas (desired crops)
        # and any contours that  have very small areas ( misc pixels that reside in the HSV range)
        for cnt in cnts:
            if cv2.contourArea(cnt) in range(5000,10000):
                # calculate a circle that encloses the contour areas
                (x,y),radius = cv2.minEnclosingCircle(cnt)
                center = (int(x),int(y))
                radius = int(radius)
                # draw the calculated circle inr red on the original frame
                cv2.circle(frame,center, radius,(7,7,255),5)
        # show the processed frame
        cv2.imshow('Processed Video', frame)
        # cv2.imshow('mask', mask)
        # wait for key q to be pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# run the function and releaset the video from que, and destroy all windows after function is finished
runMainProcess()
vid.release()
cv2.destroyAllWindows()
