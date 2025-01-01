#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 12:24:26 2024

@author: mdkfahim30
"""

import cv2
import numpy as np
import os

dim = (1920, 1080)


downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")


cap = cv2.VideoCapture(0)

captured_frames = []

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("tor code thik kor halarpohala")
        break
    

    frame_resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow('Webcam Feed', frame_resized)
    

    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        captured_frames.append(frame_resized)
        print("Frame captured for panorama.")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


if len(captured_frames) >= 2:
    stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
    ret, pano = stitcher.stitch(captured_frames)
    
    if ret == cv2.Stitcher_OK:

        panorama_path = os.path.join(downloads_path, 'panorama.jpg')
        cv2.imwrite(panorama_path, pano)
        print(f"Panorama saved at: {panorama_path}")
        

        cv2.imshow('Panorama', pano)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(f"Stitching failed with error code: {ret}")
else:
    print("Not enough frames captured for stitching.")
