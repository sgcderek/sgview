import argparse
import csv
import cv2
import math
import numpy as np
import os.path
import sys
import tempfile

# argparse stuff
parser = argparse.ArgumentParser(description='Creates 3D anaglyph image from stereo input',
                                 epilog='Accepted anaglyph types are: "red-cyan" "trioscopic"')
parser.add_argument("input",
                    help="path to input image")
parser.add_argument("-a","--anaglyph", type=str,
                    help="type of anaglyph")
args = parser.parse_args()

# check if input exists, load if yes, quit otherwise
path = args.input
if (os.path.isfile(path)):
    image = cv2.imread(path,1)
else:
    print(sys.argv[0] + ": error: specified input does not exist")
    quit()

# load color channels
if (os.path.isfile("sgv_types.csv")):
    anaglyphs = []
    with open('sgv_types.csv', 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            anaglyphs.append(row)
else:
    print(sys.argv[0] + ": error: could not find sgv_types.csv")
    quit()
    
# find specified type, if none use first in csv
if args.anaglyph == None:
    selected = anaglyphs[0]
else:
    selected = None
    for anaglyph in anaglyphs:
        if args.anaglyph == anaglyph[0]:
            selected = anaglyph

# print out selected anaglyph and copy colors           
if selected == None:
    print(sys.argv[0] + ": error: specified anaglyph not found")
    quit()
else:
    print(sys.argv[0] + ": info: using anaglyph",selected[0])
    mask = [(float(selected[6]),float(selected[5]),float(selected[4])),(float(selected[3]),float(selected[2]),float(selected[1]))]

if (os.path.isfile(path+".csv")):
    # read corner coordinates from file if present
    print(sys.argv[0] + ": info: coordinate file FOUND, will transform")
    coords = []
    with open(path+".csv", 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            row = [eval(i) for i in row]
            coords.append(row)
            
    # find longest vertical and horizontal side to be used as final image dimensions
    imwidth = int(max(math.dist(coords[0],coords[3]),math.dist(coords[1],coords[2]),math.dist(coords[4],coords[7]),math.dist(coords[5],coords[6])))
    imheight = int(max(math.dist(coords[0],coords[1]),math.dist(coords[2],coords[3]),math.dist(coords[4],coords[5]),math.dist(coords[6],coords[7])))
    
    # perspective transfrom function using given coordinates
    rcoords = np.float32([coords[0], coords[1],
                       coords[2], coords[3]])
    lcoords = np.float32([coords[4], coords[5],
                       coords[6], coords[7]])
    fcoords = np.float32([[0,0], [0,imheight],
                       [imwidth-1,imheight-1], [imwidth-1,0]])
    lmatrix = cv2.getPerspectiveTransform(lcoords,fcoords)
    rmatrix = cv2.getPerspectiveTransform(rcoords,fcoords)
    left = cv2.warpPerspective(image,lmatrix,(imwidth,imheight))
    right = cv2.warpPerspective(image,rmatrix,(imwidth,imheight))
else:
    # split input into left/right images down the middle if no coords found
    print(sys.argv[0] + ": info: coordinate file NOT found, will split")
    height,width,_ = image.shape
    left  = image[:, :width // 2  ]
    right = image[:,  width // 2 :]

# apply color correction
left  = left * mask[0]
right = right * mask[1]
image = (left + right)

# write final image to %TEMP% folder
cv2.imwrite(tempfile.gettempdir()+"/sgview.png", image)
