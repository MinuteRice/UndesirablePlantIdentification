import argparse
import numpy as np
import cv2

# define command line argument
parse = argparse.ArgumentParser()
parse.add_argument("-v", "--video", required=True, help='Full path to video')
args = vars(parse.parse_args())

# initialize video instance with video full root
vid = cv2.VideoCapture(args["video"]) #'C:/Users\Test\PycharmProjects/UWIDS/vid3.MOV'

# define thresholds for Hue, Saturation, Value scale
hsvLowerThresh = [20, 10, 10] #50-20-20
hsvUpperThresh = [100, 255, 255] #100-255-255
frame_counter = 0

# video valid function
def vidValid(source):
    # check that video file is valid/compatible
    if source.read() == (False, None):
        print('Script Aborted: Error Opening Video File! Please Make Sure To Supply The Full Path For Argument --video')
    else:
        return True

# main video processing function
def runMainProcess():
    # start infinite loop for video frame processing
    while True:
        global frame_counter
        # read frame and add to frame counter
        _,frame = vid.read()
        frame_counter += 1

        # look for q or end of video to break loop
        c = cv2.waitKey(1)
        if 'q' == chr(c & 255) or frame_counter == int(vid.get(cv2.CAP_PROP_FRAME_COUNT)):
            break

        # convert frame from BGR to HSV
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

# if video is valid run main processing then release the video and destroy all windows
if vidValid(vid):
    runMainProcess()
vid.release()
cv2.destroyAllWindows()
