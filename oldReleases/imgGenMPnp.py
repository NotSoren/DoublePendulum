import math
import numpy as np
from PIL import Image
import sys
import re
import multiprocessing
import time
#from termcolor import colored, cprint
import gc
import os
from multiprocessing import Pool

def LR(T1, T2, w1, w2):
    alpha2 = math.cos(T1 - T2)
    alpha1 = alpha2 / 2
    tmp = math.sin(T1 - T2)
    F1 = -w2**2 * tmp / 2 + 9.8 * math.sin(T1)
    F2 = w1**2 * tmp + 9.8 * math.sin(T2)
    a1 = (F1 - alpha1 * F2) / (1 - alpha1 * alpha2)
    a2 = (F2 - alpha2 * F1) / (1 - alpha1 * alpha2)
    return np.array([w1, w2, a1, a2])

def stepToPix(step):
    failed_colour = (255,255,255)
    #print(step,end=',')
    if step == -1:
        o = failed_colour
    elif step >= 10000*mult:
        o = (255, 255, 255)
    elif step > 1000*mult:
        o = [int(round(l*step/10000/mult)) for l in (0, 0, 255)]
    elif step > 100*mult:
        o = [int(round(l*step/1000/mult)) for l in (255, 0, 255)]
    elif step > 10*mult:
        o = [int(round(l*step/100/mult)) for l in (255, 0, 0)]
    elif step > 1*mult:
        o = [int(round(l*step/10/mult)) for l in (0, 255, 0)]
    else:
        o = [int(round(l*step/1/mult)) for l in (0, 255, 255)]
    return np.array(o)

def calcPix(i):
    i1 = int(i / im_dim) # y
    j1 = i % im_dim # x
    pi2 = 2 * math.pi
    step = 0
    h = 0.01
    a_1 = 0
    a_2 = 0
    Th_1 = (i1 / im_dim) * pi2
    Th_2 = (j1 / im_dim) * pi2
    i2 = i1 / im_dim
    j2 = j1 / im_dim
    
    cap = 10000*mult
    
    if (3*math.cos(Th_1) + math.cos(Th_2) < -2) | (.286<=j2<=.341) & (.265<=i2<=.372) | (.662<=j2<=.715) & (.667<=i2<=.742):
        return(-1)
    if (.335<i2<.67) & (.25<2<.66) | (.275<i2<.73) & (.375<j2<.625) | (.3<i2<.71) & (.325<j2<.68):
        return(-1)
    
    while abs((Th_1%(pi2)) - ((Th_2+math.pi)%(pi2))) > 0.03407:
        current_state = [Th_1, Th_2, a_1, a_2]
        k1 = LR(*current_state)
        k2 = LR(*(current_state + h * k1 / 2))
        k3 = LR(*(current_state + h * k2 / 2))
        k4 = LR(*(current_state + h * k3))
        
        R = 1 / 6 * h * (k1 + 2 * k2 + 2 * k3 + k4)
        
        Th_1 += R[0]
        Th_2 += R[1]
        a_1 += R[2]
        a_2 += R[3]
        step += 1
        if step >= cap:return(-1)
    return(step)


if __name__ == '__main__':
    
    args = sys.argv # Collecting arguments
    if len(args) >= 5:
        im_dim = int(re.sub('[^0-9]', '', args[1]))
        mult = float(re.sub('[^0-9.]', '', args[2]))
        thread_count = int(re.sub('[^0-9]', '', args[3]))
        output = int(re.sub('[^0-2]', '', args[4])[0])
    elif len(args) >= 4:
        im_dim = int(re.sub('[^0-9]', '', args[1]))
        mult = float(re.sub('[^0-9.]', '', args[2]))
        thread_count = int(re.sub('[^0-9]', '', args[3]))
        output = 1
    elif len(args) >= 3:
        im_dim = int(re.sub('[^0-9]', '', args[1]))
        mult = float(re.sub('[^0-9.]', '', args[2]))
        thread_count = multiprocessing.cpu_count()*4
        output = 1
    elif len(args) >= 2:
        im_dim = int(re.sub('[^0-9]', '', args[1]))
        mult = 1
        thread_count = multiprocessing.cpu_count()*4
        output = 1
    else:
        im_dim = 100
        mult = 1
        thread_count = multiprocessing.cpu_count()*4
        output = 1
    
    thread_count = min(thread_count,1010) #making sure to not use too many threads... I'm not sure if there's a concrete limit or if its determined by the OS or machine
    thread_count = min(thread_count,im_dim ** 2) #thread_count should always be less than the total number of pixels. 
    #print("threads:",thread_count)
    
    process_list = []
    for i in range(0, im_dim ** 2):process_list.append(i) # Creating 1d array for worker pool run through
    
    pixels = np.zeros((im_dim, im_dim, 3)) # creating empty 3d array for pixel data
    pixels = pixels.astype(int)
    
    total_start = time.time() # Starting timer
    
    with Pool(thread_count) as p: # Creating pool of worker threads
        process_list = p.map(calcPix, process_list) # Assigning threads to calculate step counts
        pixel_list = p.map(stepToPix, process_list) # Turning step counts into pixel values
        del(process_list)
    
    for i in range(0,len(pixel_list)): # Exporting those pixel values to pixels[][]
        pixels[int(i / im_dim)][i % im_dim] = pixel_list[i]
    
    del(pixel_list)
    
    #Saving converting pixels and saving image
    pixels = pixels.tolist()
    pixels = [item for sublist in pixels for item in sublist]
    pixels = [tuple(l) for l in pixels]
    im2 = Image.new("RGB", (im_dim, im_dim))
    im2.putdata(pixels)
    if output == 2:
        name = "doot"+str(im_dim)+"MT"+re.sub('[.]', '_', str(float(mult)))+".png"
    else:
        name = "outputs/doot"+str(im_dim)+"MT"+re.sub('[.]', '_', str(float(mult)))+".png" # creating image title
    
    if output != 0:im2.save(name)
    
    end = time.time()
    
    total = end-total_start
    print('time:',round((total)*1000)/1000,'s')
    print('each:',round((total/(im_dim**2))*1000)/1000,'s')
    gc.collect()
