import pyscreenshot as ImageGrab
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
    lower_red = np.array([0,0,30])
    upper_red = np.array([20,20,255])
    mask = cv2.inRange(image, lower_red, upper_red)
    res = cv2.bitwise_and(image, image, mask=mask)
    return res

def main():
    # time.sleep(5)
    # image = screenshot_to_image()
    image = file_to_image('combat.png')
    red_image = apply_red_filter(image)
    raw_image = red_image
    bilateral_filtered_image = cv2.bilateralFilter(raw_image, 5, 175, 175)
    cv2.imshow('Bilateral', bilateral_filtered_image)
    cv2.waitKey(0)

    edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)
    cv2.imshow('Edge', edge_detected_image)
    cv2.waitKey(0)

    _, contours, hierarchy = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_list = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
        area = cv2.contourArea(contour)
        if ((len(approx) > 8) & (len(approx) < 23) & (area > 30) ):
            contour_list.append(contour)
    print('see el', contour_list)
    cv2.drawContours(raw_image, contour_list,  -1, (255,0,0), 2)
    cv2.imshow('Objects Detected',raw_image)
    cv2.waitKey(0)
    output = red_image.copy()
    gray = cv2.cvtColor(red_image, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param2=8, minRadius=30, maxRadius=60)
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
    
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    
        # show the output image
        # cv2.imshow("gay", np.hstack([red_image, output]))
        cv2.waitKey(0)
    cv2.imshow('gray',output)

    k = cv2.waitKey(0)
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()