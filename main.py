import cv2
import numpy as np
import time
import subprocess
import glob
from PIL import Image as im

def getdim():
    global t_width, t_height
    out = subprocess.Popen(['tput', 'cols'], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()

    if stderr:
        t_width = 144
        t_height = 48
        print('tput not available, using fixed size')
        return

    t_width = int(stdout)

    out = subprocess.Popen(['tput', 'lines'], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()

    t_height = int(stdout)

cameralist = glob.glob("/dev/video*")
if not cameralist:
    print("You do not have a working camera")
    exit(1)
else:
    print("Which camera to use? default=0")
    for i in range(len(cameralist)):
        print(i, cameralist[i])
    choice = input()
    choice = 0 if not choice else int(choice)
    if choice not in range(len(cameralist)):
        print('invalid choice')
        exit(1)
    else:
        vid = cv2.VideoCapture(choice)

if not vid.isOpened():
    raise Exception("Could not open video device")

# symbols = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
symbols = '@#$%?*+;:,. '
print('inverted? Y/n')
if input() != 'n':
    symbols = symbols[::-1]
symlen = len(symbols)

try:
    while(True):
        ret, frame = vid.read()
        getdim()
      
        height = len(frame)
        width = len(frame[0])

        res = cv2.resize(frame, dsize=(t_width-1, t_height-1), interpolation=cv2.INTER_AREA)
        res = np.asarray(im.fromarray(res).convert('L'))
        output = ("\033[H\033[J") # clear screen
        for row in res:
            for pixel in row:
                ind = round((pixel / 255) * (symlen-1))
                ind = 0 if ind < 0 else ind
                output+=symbols [ ind ]
            output+="\n"
        print(output,end="")
        # Display the resulting frame
        # cv2.imshow('frame', edges)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    # After the loop release the cap object
    # Destroy all the windows
    print('releasing webcam')
    vid.release()
    cv2.destroyAllWindows()


  
