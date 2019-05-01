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

def LR(T1, T2, w1, w2):
    alpha2 = math.cos(T1 - T2)
    alpha1 = alpha2 / 2
    tmp = math.sin(T1 - T2)
    F1 = -w2**2 * tmp / 2 + 9.8 * math.sin(T1)
    F2 = w1**2 * tmp + 9.8 * math.sin(T2)
    a1 = (F1 - alpha1 * F2) / (1 - alpha1 * alpha2)
    a2 = (F2 - alpha2 * F1) / (1 - alpha1 * alpha2)
    #gc.collect()
    return np.array([w1, w2, a1, a2])

def calcPix(i1,j1,pixels,out1,out2,out3):
    pi2 = 2 * math.pi
    step = 0
    h = 0.01
    a_1 = 0
    a_2 = 0

    Th_1 = (i1 / im_dim) * pi2
    Th_2 = (j1 / im_dim) * pi2
    i2 = i1 / im_dim 
    j2 = j1 / im_dim
    
    if (3*math.cos(Th_1) + 1.2*math.cos(Th_2) < -1.82) | (.286<=j2<=.341) & (.265<=i2<=.372) | (.662<=j2<=.715) & (.667<=i2<=.742):
        out1.value = 255
        out2.value = 255
        out3.value = 255
        #print(colored(format(j1),"yellow"),end=" ")
        print('__',end='')
        return

    cap = 10000*mult
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
        if step >= cap:
            break
    #print(i1,j1,"s:", step)
    if step >= 10000*mult:
        pixels[i1][j1] = (255, 255, 255)
        #print(j1,end=" ")
        print('  ',end='')
    elif step > 1000*mult:
        pixels[i1][j1] = [int(round(l*step/10000/mult)) for l in (0, 0, 255)]
        #print(colored(format(j1),'blue'),end=" ")
        print('░░',end='')
    elif step > 100*mult:
        pixels[i1][j1] = [int(round(l*step/1000/mult)) for l in (255, 0, 255)]
        #print(colored(format(j1),'magenta'),end=" ")
        print('▒▒',end='')
    elif step > 10*mult:
        pixels[i1][j1] = [int(round(l*step/100/mult)) for l in (255, 0, 0)]
        #print(colored(format(j1),'red'),end=" ")
        print('▓▓',end='')
    else:
        pixels[i1][j1] = [int(round(l*step/10/mult)) for l in (0, 255, 0)]
        #print(colored(format(j1),'green'),end=" ")
        print('██',end='')
    out1.value = pixels[i1][j1][0]
    out2.value = pixels[i1][j1][1]
    out3.value = pixels[i1][j1][2]
    
args = sys.argv
if len(args) >= 4:
    im_dim = int(re.sub('[^0-9]', '', args[1]))
    mult = float(re.sub('[^0-9.]', '', args[2]))
    threadCount = int(re.sub('[^0-9]', '', args[3]))
elif len(args) >= 3:
    im_dim = int(re.sub('[^0-9]', '', args[1]))
    mult = float(re.sub('[^0-9.]', '', args[2]))
    threadCount = multiprocessing.cpu_count()*2
elif len(args) >= 2:
    im_dim = int(re.sub('[^0-9]', '', args[1]))
    mult = 1 
    threadCount = multiprocessing.cpu_count()*2
else:
    im_dim = 100
    mult = 1
    threadCount = multiprocessing.cpu_count()*2

threadCount = min(im_dim, threadCount) 
print(threadCount)

pixels = np.zeros((im_dim, im_dim, 3))
pixels = pixels.astype(int)

left = 1
pi2 = 2 * math.pi

# Declaring variables to be treated as pointers for multiprocessing. 
for i in range(1,threadCount*3+1):
    exec("t"+str(i)+" = multiprocessing.Value('i')")

xmin = 0
xmax = im_dim
ymin = 0
ymax = im_dim

print("Running between X=",xmin,xmax)
print("Running between Y=",ymin,ymax)

i=ymin
while i <= ymax - 1:
    print(i,end=":")
    if i < 100:
        print(" ",end="")
        if i < 10:
            print(" ",end="")
    j=xmin
    start = time.time()
    while j <= xmax - 1:
        threads = min(threadCount,(xmax - j))
        for q in range(1,threads+1): # generate process targets
            exec("p"+str(q)+" = multiprocessing.Process(target=calcPix, args=(i,j+"+str(q-1)+",pixels,t"+str((q-1)*3+1)+",t"+str((q-1)*3+2)+",t"+str((q-1)*3+3)+"))")
        
        for q in range(1,threads+1): # start processes
            exec("p"+str(q)+".start()")
        for q in range(1,threads+1): # join processes
            exec("p"+str(q)+".join()")
            
        for q in range(1,threads+1): # save pixel values
            exec("pixels[i][j+"+str(q-1)+"] = [t"+str((q-1)*3+1)+".value,t"+str((q-1)*3+2)+".value,t"+str((q-1)*3+3)+".value]")
        j+=threads
        end = time.time()
    print(round((end-start)*100)/100)
    i+=1
    """
    Comment out the next 5 lines to disable outputting to tmp2.png every line. This is recommended unless
    you're running the below command at the same time. That only works on linux, btw. 
    feh --force-aliasing -ZR 1 -g 800x800 tmp2.png
    """
    """
    pixel2 = pixels.tolist()
    pixel2 = [item for sublist in pixel2 for item in sublist]
    pixel2 = [tuple(l) for l in pixel2]
    im3 = Image.new("RGB", (im_dim, im_dim))
    im3.putdata(pixel2)
    im3.save("outputs/tmp2.png")
    """

pixels = pixels.tolist()
pixels = [item for sublist in pixels for item in sublist]
pixels = [tuple(l) for l in pixels]
im2 = Image.new("RGB", (im_dim, im_dim))
im2.putdata(pixels)
name = "outputs/doot"+str(im_dim)+"MT"+re.sub('[.]', '_', str(mult))+".png"
#name = "outputs/doot"+str(im_dim)+"MT.png"
im2.save(name)
 
gc.collect()
