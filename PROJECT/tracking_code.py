import sys
import os
import cv2
import numpy as np
import random
from matplotlib import pyplot as plt
import numpy as np
import pygame as pg
import csv

left_hand_coord_list = []
right_hand_coord_list = []
left_foot_coord_list = []
right_foot_coord_list = []
body_coord_list = []

def scale_points(points, center, scale):
    """
    points: list of (x, y)
    center: (cx, cy)
    scale: float
    returns: np.array of shape (N, 1, 2), dtype=int32 (OpenCV ready)
    """
    cx, cy = center
    new_points = []

    for x, y in points:
        new_x = cx + (x - cx) * scale
        new_y = cy + (y - cy) * scale
        new_points.append([int(new_x), int(new_y)])

    # Return in OpenCV polyline/contour format
    return np.array(new_points, dtype=np.int32).reshape((-1, 1, 2))

def polygon_centroid(points):
    """
    Computes the centre as the intersection of diagonals.
    Assumes points are (x,y) tuples.
    """

    n = len(points)

    # --- 2 points: midpoint ---
    if n == 2:
        (x1, y1), (x2, y2) = points
        return ( (x1 + x2) / 2.0, (y1 + y2) / 2.0 )

    # --- 3 points: treat as bounding box ---
    if n == 3:
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        return ( (min(xs)+max(xs))/2.0, (min(ys)+max(ys))/2.0 )

    # --- 4 points: intersection of diagonals ---
    # Ensure they are in order: UL, UR, BR, BL
    UL, UR, BR, BL = points

    # Diagonal midpoints are equal → intersection
    cx = (UL[0] + BR[0]) / 2.0
    cy = (UL[1] + BR[1]) / 2.0

    return (cx, cy)

def motion_track_and_extract_body_part_coord_lists():
    # use count
    video_name = 'Opt1-MarionetteMovements.mov'

    cap = cv2.VideoCapture(video_name)
    if not cap.isOpened():
        print('{} not opened'.format(video_name))
        sys.exit(1)
    time_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_counter = 0                                             # FRAME_COUNTER


    while(1):
        return_flag, frame = cap.read()  
        if not return_flag:
            print('Video Reach End')
            break
        # Main Content - Start
        frame_counter += 1
        # Main Content - End    
        if 0xff == ord('q'):
            break


    RED = 160
    GREEN = 200
    bgctr = frame_counter
    count = 0
    cap = cv2.VideoCapture(video_name)
    if not cap.isOpened():
        print('video not opened')
        sys.exit(1)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    i = 0

    while(i < 100):
        i = i + 1
        ret, monkeyframe = cap.read()
        if not ret:
            break
        # instead rcreate a black array in numpy
        bg = np.zeros((320,568,3),dtype=np.uint8) 

        # monkeyframe = cv2.resize(monkeyframe, (bg.shape[1], bg.shape[0]))

        for x in range(monkeyframe.shape[0]):

            for y in range(monkeyframe.shape[1]):

                
                ################  TODO  #################
                # replace the corresponding pixels in background with 
                # red pixels in monkey vid

                # # cget rgb values opencv uses BGR (so index 2 = red)
                r = monkeyframe[x, y, 2]  
                g = monkeyframe[x, y, 1]
                b = monkeyframe[x, y, 0]


                # # check if red is the dominant channel
                if (r > g) and (r > b) and (r > RED) and (g < GREEN):  # also apply a threshold
                    bg[x][y] = monkeyframe[x][y]


                # else:
                continue
                    
                #########################################


        # greyscale the image

        # erode image to remove unwatted tracks

        # dilate image to make found balls bigger



        # eroded_img = erosion(binary_img, se) 

        # greyscale the image
        gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)

        # threshold to binary (0 or 255)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

        # create a 3×3 structuring element for erosion / dilation
        SE = np.ones((3, 3), dtype=np.uint8)

        # erode image to remove unwanted tracks
        eroded = cv2.erode(binary.astype(np.uint8), SE, iterations=2)

        # dilate image to make found balls bigger
        dilated = cv2.dilate(eroded.astype(np.uint8), SE, iterations=0)

        inverted_image = cv2.bitwise_not(dilated)




        # Now dilated is an image which shows my attempt at segmentation

        # Setup SimpleBlobDetector parameters
        params = cv2.SimpleBlobDetector_Params()
        
        # Thresholds for binarization
        # params.minThreshold = 0
        # params.maxThreshold = 255
        
        # Filter by Area
        params.filterByArea = True
        params.minArea = 80
        
        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = 0.1
        
        # Filter by Convexity
        params.filterByConvexity = False
        params.minConvexity = 0.87
        
        # Filter by Inertia
        params.filterByInertia = False
        params.minInertiaRatio = 0.01
        
        # Create a detector with the parameters
        detector = cv2.SimpleBlobDetector_create(params)
        
        # Detect blobs
        keypoints = detector.detect(inverted_image)

        
        # Draw blobs as red circles
        output = cv2.drawKeypoints(inverted_image, keypoints, np.array([]), (0, 0, 255),
                                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        bg = cv2.bitwise_not(output)


        keypoints_sorted = sorted(keypoints, key=lambda kp: (kp.pt[1], kp.pt[0]))
        int_points = [(int(kp.pt[0]), int(kp.pt[1])) for kp in keypoints_sorted]


        # if(range(len(keypoints) == 4)):
            
        # y coord of middle point in detection box =

    
        # if(range(len(keypoints) == 3)):

        # if(range(len(keypoints) == 2)):


        # if the list has 2 elements then make upper_left and upper_right both equal to the higher point and lower_left and lower_right both equal to the lower point
        # --- Edge case: only 2 points ---
        # upper_left
        # upper_right
        # bottom_left
        # bottom_right

        if len(int_points) == 1:
            upper_left = int_points[0]
            upper_right = int_points[0]
            bottom_left = int_points[0]
            bottom_right = int_points[0]


        elif len(int_points) == 2:

            # sort by y (top first)
            top, bottom = sorted(int_points, key=lambda p: p[1])

            p1, p2 = int_points

            upper_left = top
            upper_right = top
            bottom_left = bottom
            bottom_right = bottom

        else:
            # Top two = smallest y
            top = int_points[:2]
            # Bottom two = largest y
            bottom = int_points[-2:]

            # Upper-left = smaller x of top
            upper_left = min(top, key=lambda p: p[0])
            # Upper-right = larger x of top
            upper_right = max(top, key=lambda p: p[0])

            # Bottom-left = smaller x of bottom
            bottom_left = min(bottom, key=lambda p: p[0])
            # Bottom-right = larger x of bottom
            bottom_right = max(bottom, key=lambda p: p[0])


        # draw a red box with these points
        box_pts = np.array([
            upper_left,
            upper_right,
            bottom_right,
            bottom_left
        ], dtype=np.int32)

        midpoint = box_pts.mean(axis=0)
        midpoint = midpoint.astype(int)

        scale_factor = 0.7

        scaled_box = scale_points(box_pts, midpoint, scale_factor)
        
        # get midpoint

        # Convert bg to single-channel if needed
        if len(bg.shape) == 3:
            # Take the first channel or convert to grayscale
            gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
        else:
            gray = bg.copy()

        # Make sure values are 0 or 1
        binary_bg = (gray > 0).astype(np.uint8)

        # Create mask from scaled_box
        mask = np.zeros_like(binary_bg, dtype=np.uint8)
        cv2.fillPoly(mask, [scaled_box], 1)

        # Keep only pixels inside the polygon
        pixels_inside = binary_bg * mask

        # Find coordinates of pixels that are 1
        ys, xs = np.nonzero(pixels_inside)  # safer than np.where

        if len(xs) > 0:
            centroid_x = int(xs.mean())
            centroid_y = int(ys.mean())
            centroid = (centroid_x, centroid_y)
            # print("Centroid:", centroid)
        else:
            centroid = None
            # print("No pixels with value 1 inside the box.")


        if centroid is not None:
            # centroid = (x, y)
            cv2.circle(bg, centroid, radius=4, color=(0,0,255), thickness=-1)

        cv2.polylines(bg, [scaled_box], isClosed=True, color=(0,0,255), thickness=2)


        cv2.imwrite('composite/composite%d.tif' % count, bg)


        #MAYBE: add code to see if tracking point is within a radius of the last point to see if its of the same bodypart

        left_hand_coord_list.append(upper_left)
        right_hand_coord_list.append(upper_right)
        left_foot_coord_list.append(bottom_left)
        right_foot_coord_list.append(bottom_right)
    
        if centroid is not None:
            body_coord_list.append(centroid) # if didnt scan make a 
        else:
            # get prev centroid
            prev_centroid = (0,0) # init it
            try:
                prev_centroid = body_coord_list[-1]
            except:
                prev_centroid = (200,100) # edge case if first frame cant find midpoint
            
            body_coord_list.append(prev_centroid)
        

        count += 1
        if 0xff == ord('q'):
            break

def save_coord_lists():
   
    with open("coords.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Left Hand Coords'])
        for coord in left_hand_coord_list:
            writer.writerow(coord)
        writer.writerow(['Right Hand Coords'])
        for coord in right_hand_coord_list:
            writer.writerow(coord)
        writer.writerow(['Left Foot Coords'])
        for coord in left_foot_coord_list:
            writer.writerow(coord)
        writer.writerow(['Right Foot Coords'])
        for coord in right_foot_coord_list:
            writer.writerow(coord)
        writer.writerow(['Body Coords'])
        for coord in body_coord_list:
            writer.writerow(coord)

def load_coord_lists():
    
    with open("coords.csv", 'r') as f:
        reader = csv.reader(f)
        
        next(reader)  # Skip header row
        
        current_list = left_hand_coord_list
        for row in reader:
            if row == ['Right Hand Coords']:
                current_list = right_hand_coord_list
            elif row == ['Left Foot Coords']:
                current_list = left_foot_coord_list
            elif row == ['Right Foot Coords']:
                current_list = right_foot_coord_list
            elif row == ['Body Coords']:
                current_list = body_coord_list
            else:
                current_list.append(tuple(map(int, row)))
    

