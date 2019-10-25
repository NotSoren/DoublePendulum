 
import math
import numpy as np
from PIL import Image
import sys
import re
import time


args = sys.argv
if len(args) >= 2:
    im_dim = int(re.sub('[^0-9]', '', args[1]))
else:
    im_dim = 75

pixels = np.zeros((im_dim, im_dim, 3))
pixels = pixels.astype(int)

def LR(T1, T2, w1, w2):
    alpha2 = math.cos(T1 - T2)
    alpha1 = alpha2 / 2
    tmp = math.sin(T1 - T2)
    F1 = -w2**2 * tmp / 2 + 9.8 * math.sin(T1)
    F2 = w1**2 * tmp + 9.8 * math.sin(T2)
    t3 = 1 - alpha1 * alpha2
    
    a1 = (F1 - alpha1 * F2) / t3
    a2 = (F2 - alpha2 * F1) / t3
    return np.array([w1, w2, a1, a2])


left = 1
rangeTmp = range(im_dim)
pi2 = 2 * math.pi
for i in rangeTmp:
    for j in rangeTmp:
        print(i,j,end=" ")
        run = True
        step = 0
        h = 0.01
        
        a_1 = 0
        a_2 = 0
        """
        if (i == math.floor(im_dim / 2)) & (j != 0):
            run = False
        """
        
        Th_1 = (i / im_dim) * pi2
        Th_2 = (j / im_dim) * pi2
        
        if (3*math.cos(Th_1) + math.cos(Th_2) < -2)|(left==0):
            left += 1
            pixels[i][j] = (255, 255, 255)
            print(" Skipped")
            continue
        
        #start = time.time()
        while (abs((Th_1%(pi2)) - ((Th_2+math.pi)%(pi2))) > 0.03407):            
            current_state = np.array([Th_1, Th_2, a_1, a_2])
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
            # | (time.time()-start >= .5)
            if (step >= 100000):
                break
        #end = time.time()
        #print(" s:", step,"t:",end-start,"i:",left)
        print("s:", step,"i:",left)
        if step >= 100000:
            pixels[i][j] = (255, 255, 255)
        elif step > 10000:
            pixels[i][j] = [int(round(l*step/100000)) for l in (0, 0, 255)]
        elif step > 1000:
            pixels[i][j] = [int(round(l*step/10000)) for l in (255, 0, 255)]
        elif step > 100:
            pixels[i][j] = [int(round(l*step/1000)) for l in (255, 0, 0)]
        else:
            pixels[i][j] = [int(round(l*step/100)) for l in (0, 255, 0)]
        left += 1
        if run == False:
            pixels[i][j] = (255, 255, 255)
    pixel2 = pixels.tolist()
    pixel2 = [item for sublist in pixel2 for item in sublist]
    pixel2 = [tuple(l) for l in pixel2]
    im3 = Image.new("RGB", (im_dim, im_dim))
    im3.putdata(pixel2)
    im3.save("tmp1.png")

pixels = pixels.tolist()
pixels = [item for sublist in pixels for item in sublist]
pixels = [tuple(l) for l in pixels]
im2 = Image.new("RGB", (im_dim, im_dim))
im2.putdata(pixels)
name = "doot"+ str(im_dim)+"ST.png"
im2.save(name)
