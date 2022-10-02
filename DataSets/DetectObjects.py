from ShapeDetector import ShapeDetector
import argparse
import imutils
import cv2
import numpy as np

def crop_object_fromContour(orig, c):
  (x, y, w, h) = cv2.boundingRect(c)
  object_img = orig[y:y+h, x:x+w]
  return object_img

def removing_backgroundMask(masked):
    # thresholding
    gray_masked = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    t_val, alpha_thresh = cv2.threshold(gray_masked, 10, 255, cv2.THRESH_BINARY)
    # getting b,g,r channel
    b,g,r = cv2.split(masked)
    #merging rbg and also the alpha_thresh
    masked_filtered = cv2.merge([r, g, b, alpha_thresh], 4)
    #returing
    return masked_filtered

def masking(image, c, background):
    h = image.shape[0]
    w = image.shape[1]
    #all black area masking
    mask = np.zeros([h,w], np.uint8)
    #draw contours
    white_color = (255, 255, 255)
    #for specific image
    cv2.drawContours(mask, [c], -1, white_color, cv2.FILLED)
    #for background
    cv2.drawContours(background, [c], -1, white_color, cv2.FILLED)
    #masking
    inv_mask = 255-mask
    masked = cv2.bitwise_and(image, image, mask=mask)
    #cropping
    cropped_masked = crop_object_fromContour(masked, c) 
    #removing_backgroundMask
    filtered_masked = removing_backgroundMask(cropped_masked)

    return filtered_masked

def save_info(file_name, dataList):
    #convert this to textfile
    with open(file_name, 'w',encoding = 'utf-8') as f:
        for data in dataList:
            f_name, posX, posY, shape = data
            f.write(f"{f_name};{posX};{posY};{shape}\n")

def extract_objects(image_fname):
    #data list
    data_list = list()
    # reading an image
    image = cv2.imread(image_fname)
    resized = imutils.resize(image, width=300)
    ratio = image.shape[0]/float(resized.shape[0])

    #gray scale and blurring
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (1, 1), 1)
    # using canny edge to show the edges
    edged = cv2.Canny(blurred, 50, 255)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    # getting the contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # shape detector
    sd = ShapeDetector()

    #
    background_mask = np.zeros(image.shape[0:2], np.uint8)
    # looping on all contours found
    for i,c in enumerate(cnts):
    # if its small then ignore
        if(cv2.contourArea(c)<100):
            continue

        #get moments
        M = cv2.moments(c)
        # finding the center position
        cX = int((M["m10"]/M["m00"]) * ratio)
        cY = int((M["m01"]/M["m00"]) * ratio)
        #detecting shape
        shape = sd.detect(c)

        # dependent on c ratio move up to the original
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")

        # masking
        filtered_masked = masking(image, c, background_mask)
        #output saving
        f_name = f"Image{i}.png"
        cv2.imwrite(f"DataTemp/Objs/{f_name}", filtered_masked)
        #data encoding
        instances = (f_name, cX, cY, shape)
        data_list.append(instances)
        

    # for background
    background_mask_inv = 255-background_mask
    background_masked = cv2.bitwise_and(image, image, mask=background_mask_inv)
    cv2.imwrite(f"DataTemp/Background.jpg", background_masked)
    #saving data
    save_info(f"DataTemp/DataList.txt", data_list)

#must masked background

# calling the method
extract_objects("ImageTest/referenceImage.png")
print("Done")
