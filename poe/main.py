import pyscreenshot as ImageGrab
from typing import List
from location import CharacterLocation, is_likely_duplicate, merge_locations
import ellipse
import time
import numpy as np
import cv2

def screenshot_to_image(bbox=None):
    img = ImageGrab.grab(bbox=bbox)
    img = np.array(img)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def file_to_image(fname):
    img = cv2.imread(fname)
    return img

def apply_red_filter(image):
    #bgr
    lower_red = np.array([0,0,30])
    upper_red = np.array([20,20,255])
    mask = cv2.inRange(image, lower_red, upper_red)
    res = cv2.bitwise_and(image, image, mask=mask)
    return res

def get_character_locations(image):
    red_image = apply_red_filter(image)
    raw_image = red_image
    bilateral_filtered_image = cv2.bilateralFilter(raw_image, 5, 175, 175)
    edge_detected_image = cv2.Canny(bilateral_filtered_image, 10, 50)
    cv2.imshow('Objects Detected',edge_detected_image)
    cv2.waitKey(0)
    _, contours, hierarchy = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    locations: List[CharacterLocation] = []
    for contour_points in contours:
        approx = cv2.approxPolyDP(contour_points, 0.01*cv2.arcLength(contour_points, True), True)
        area = cv2.contourArea(contour_points)
        if ((len(approx) > 8) & (len(approx) < 23) & (area > 30)) or 1:
            points = np.array([p[0] for p in contour_points])
            location = CharacterLocation(points) 
            min_x, max_x, min_y, max_y = location.extremes
            if min(max_x - min_x, max_y - min_y) > 15:
                for i, existing_location in enumerate(locations):
                    if is_likely_duplicate(location, existing_location):
                        location_to_use = location if len(location.points) > len(existing_location.points) else existing_location
                        locations[i] = location_to_use
                        break
                else:
                    locations.append(location)
    merged = merge_locations(locations)
    print([l.center for l in locations])
    return merged



def main():
    # image = screenshot_to_image()
    # cv2.imwrite('combat.png', image)
    image = file_to_image('combat.png')
    locations = get_character_locations(image)
    location_points = np.array([l.points for l in locations])
    raw_image = apply_red_filter(image)
    import random
    for p in location_points:
        b,g,r = [random.randint(0, 255) for i in range(3)]
        
        cv2.drawContours(image, [p],  -1, (b,g,r), 2)
    for l in locations:
        x, y = l.center
        cv2.rectangle(image, (x, y), (x, y), (0, 255, 0), 3)
    cv2.imshow('Objects Detected',image)
    cv2.waitKey(0)
    
if __name__ == "__main__":
    main()