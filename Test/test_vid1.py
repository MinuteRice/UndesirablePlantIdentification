import pytest
import cv2

def test_source():
    vid = cv2.VideoCapture('vid1.MOV')
    assert vid
