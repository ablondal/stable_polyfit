import cv2 as cv
import numpy as np
import sys
import queue
import os
from pathlib import Path

def regularize(img):
    visited = 1- (img[:,:,3] != 255)
    
    neighbours = [[-1,0],[1,0],[0,-1],[0,1]]
    
    # Initialize the queue with all transparent border pixels
    Q = queue.SimpleQueue()
    for x in range(img.shape[0]):
        if not visited[x,0]:
            visited[x,0] = 1
            Q.put((x,0))
        if not visited[x,-1]:
            visited[x,-1] = 1
            Q.put((x,img.shape[1]-1))
    for y in range(img.shape[1]):
        if not visited[0,y]:
            visited[0,y] = 1
            Q.put((0,y))
        if not visited[-1,y]:
            visited[-1,y] = 1
            Q.put((img.shape[0]-1,y))
    
    # Perform BFS on alpha pixel from out to in
    while not Q.empty():
        x, y = Q.get()
        for n in neighbours:
            nx = x + n[0]
            ny = y + n[1]
            if (nx >= 0 and nx < img.shape[0] and ny >= 0 and ny < img.shape[1] and not visited[nx, ny]):
                visited[nx,ny] = 1
                Q.put((nx,ny))
    
    new_img = np.zeros(img.shape)
    new_img = img[:,:,:]
    new_img[visited == 0] = [255, 255, 255, 255]
    
    # cv.imshow('image', img)
    # cv.imshow('new img', new_img)
    # k = cv.waitKey(0)
    # cv.destroyAllWindows()
    return new_img

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('Please provide file to vectorize as a command-line argument, and file to output to as well')

    imgfile = sys.argv[1]
    split_place = imgfile.rfind('.')
    tmpfile = imgfile[:split_place]+'_tmp'+imgfile[split_place:]
    outfile = sys.argv[2]

    # Unchanged here means that alpha is preserved
    img = cv.imread(imgfile, cv.IMREAD_UNCHANGED)

    print("Applying pre-Polyfit patches to image...")
    new_img = regularize(img)
    
    cv.imwrite(tmpfile, new_img)
    
    POLYFIT_CMD = 'polyfit.exe'
    
    cmd = f'{POLYFIT_CMD} {tmpfile} {outfile}'
    
    print("Running Polyfit...")
    os.system(cmd)

