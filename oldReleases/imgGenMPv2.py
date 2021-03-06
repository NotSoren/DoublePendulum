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
        print('  ',end='')
        return

    cap = 10000*mult
    while abs((Th_1%(pi2)) - ((Th_2+math.pi)%(pi2))) > 0.03407:            
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
if __name__ == '__main__':
    total_start = time.time()
    args = sys.argv
    if len(args) >= 4:
        im_dim = int(re.sub('[^0-9]', '', args[1]))
        mult = float(re.sub('[^0-9.]', '', args[2]))
        threadCount = int(re.sub('[^0-9]', '', args[3]))
        print(threadCount)
    elif len(args) >= 3:
        im_dim = int(re.sub('[^0-9]', '', args[1]))
        mult = float(re.sub('[^0-9.]', '', args[2]))
        threadCount = multiprocessing.cpu_count()*2
        print(threadCount)
    elif len(args) >= 2:
        im_dim = int(re.sub('[^0-9]', '', args[1]))
        mult = 1 
        threadCount = multiprocessing.cpu_count()*2
        print(threadCount)
    else:
        im_dim = 100
        mult = 1
        threadCount = multiprocessing.cpu_count()*2
        print(threadCount)

    pixels = np.zeros((im_dim, im_dim, 3))
    pixels = pixels.astype(int)

    left = 1
    pi2 = 2 * math.pi

    # Declaring variables to be treated as pointers for multiprocessing. Yes, it's ugly. Get over it. 
    for i in range(1,25):
        #print(i)
        exec("t"+str(i)+" = multiprocessing.Value('i')")
        exec("t0"+str(i)+" = multiprocessing.Value('i')")

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
            if (j <= xmax - 16) & (threadCount >= 16):
                p1 = multiprocessing.Process(target=calcPix, args=(i,j,pixels,t1,t2,t3)) # Creating processes
                p2 = multiprocessing.Process(target=calcPix, args=(i,j+1,pixels,t4,t5,t6)) 
                p3 = multiprocessing.Process(target=calcPix, args=(i,j+2,pixels,t7,t8,t9))
                p4 = multiprocessing.Process(target=calcPix, args=(i,j+3,pixels,t10,t11,t12))
                p5 = multiprocessing.Process(target=calcPix, args=(i,j+4,pixels,t13,t14,t15)) 
                p6 = multiprocessing.Process(target=calcPix, args=(i,j+5,pixels,t16,t17,t18))
                p7 = multiprocessing.Process(target=calcPix, args=(i,j+6,pixels,t19,t20,t21))
                p8 = multiprocessing.Process(target=calcPix, args=(i,j+7,pixels,t22,t23,t24))
                p9 = multiprocessing.Process(target=calcPix, args=(i,j+8,pixels,t01,t02,t03)) # Creating processes
                p10 = multiprocessing.Process(target=calcPix, args=(i,j+9,pixels,t04,t05,t06)) 
                p11 = multiprocessing.Process(target=calcPix, args=(i,j+10,pixels,t07,t08,t09))
                p12 = multiprocessing.Process(target=calcPix, args=(i,j+11,pixels,t010,t011,t012))
                p13 = multiprocessing.Process(target=calcPix, args=(i,j+12,pixels,t013,t014,t015)) 
                p14 = multiprocessing.Process(target=calcPix, args=(i,j+13,pixels,t016,t017,t018))
                p15 = multiprocessing.Process(target=calcPix, args=(i,j+14,pixels,t019,t020,t021))
                p16 = multiprocessing.Process(target=calcPix, args=(i,j+15,pixels,t022,t023,t024))
                
                p1.start() # Starting Processes
                p2.start()
                p3.start()
                p4.start()
                p5.start()
                p6.start()
                p7.start()
                p8.start()
                p9.start()
                p10.start()
                p11.start()
                p12.start()
                p13.start()
                p14.start()
                p15.start()
                p16.start()
                
                p1.join()
                p2.join()
                p3.join()
                p4.join()
                p5.join()
                p6.join()
                p7.join()
                p8.join()
                p9.join()
                p10.join()
                p11.join()
                p12.join()
                p13.join()
                p14.join()
                p15.join()
                p16.join()

                pixels[i][j] = [t1.value,t2.value,t3.value]
                pixels[i][j+1] = [t4.value,t5.value,t6.value]
                pixels[i][j+2] = [t7.value,t8.value,t9.value]
                pixels[i][j+3] = [t10.value,t11.value,t12.value]
                pixels[i][j+4] = [t13.value,t14.value,t15.value]
                pixels[i][j+5] = [t16.value,t17.value,t18.value]
                pixels[i][j+6] = [t19.value,t20.value,t21.value]
                pixels[i][j+7] = [t22.value,t23.value,t24.value]
                pixels[i][j+8] = [t01.value,t02.value,t03.value]
                pixels[i][j+9] = [t04.value,t05.value,t06.value]
                pixels[i][j+10] = [t07.value,t08.value,t09.value]
                pixels[i][j+11] = [t010.value,t011.value,t012.value]
                pixels[i][j+12] = [t013.value,t014.value,t015.value]
                pixels[i][j+13] = [t016.value,t017.value,t018.value]
                pixels[i][j+14] = [t019.value,t020.value,t021.value]
                pixels[i][j+15] = [t022.value,t023.value,t024.value]
                j+=15
            elif (j <= xmax - 8) & (threadCount >= 8):
                p1 = multiprocessing.Process(target=calcPix, args=(i,j,pixels,t1,t2,t3)) # Creating processes
                p2 = multiprocessing.Process(target=calcPix, args=(i,j+1,pixels,t4,t5,t6)) 
                p3 = multiprocessing.Process(target=calcPix, args=(i,j+2,pixels,t7,t8,t9))
                p4 = multiprocessing.Process(target=calcPix, args=(i,j+3,pixels,t10,t11,t12))
                p5 = multiprocessing.Process(target=calcPix, args=(i,j+4,pixels,t13,t14,t15)) 
                p6 = multiprocessing.Process(target=calcPix, args=(i,j+5,pixels,t16,t17,t18))
                p7 = multiprocessing.Process(target=calcPix, args=(i,j+6,pixels,t19,t20,t21))
                p8 = multiprocessing.Process(target=calcPix, args=(i,j+7,pixels,t22,t23,t24))
                
                p1.start() # Starting Processes
                p2.start()
                p3.start()
                p4.start()
                p5.start()
                p6.start()
                p7.start()
                p8.start()

                p1.join() # Waiting for processes to finish
                p2.join()
                p3.join()
                p4.join()
                p5.join()
                p6.join()
                p7.join()
                p8.join()

                pixels[i][j] = [t1.value,t2.value,t3.value]
                pixels[i][j+1] = [t4.value,t5.value,t6.value]
                pixels[i][j+2] = [t7.value,t8.value,t9.value]
                pixels[i][j+3] = [t10.value,t11.value,t12.value]
                pixels[i][j+4] = [t13.value,t14.value,t15.value]
                pixels[i][j+5] = [t16.value,t17.value,t18.value]
                pixels[i][j+6] = [t19.value,t20.value,t21.value]
                pixels[i][j+7] = [t22.value,t23.value,t24.value]
                j+=7
            elif (j <= xmax - 4) & (threadCount >= 4):
                p1 = multiprocessing.Process(target=calcPix, args=(i,j,pixels,t1,t2,t3)) # Creating processes
                p2 = multiprocessing.Process(target=calcPix, args=(i,j+1,pixels,t4,t5,t6)) 
                p3 = multiprocessing.Process(target=calcPix, args=(i,j+2,pixels,t7,t8,t9))
                p4 = multiprocessing.Process(target=calcPix, args=(i,j+3,pixels,t10,t11,t12))
                
                p1.start() # Starting Processes
                p2.start()
                p3.start()
                p4.start()
                
                p1.join() # Waiting for processes to finish
                p2.join()
                p3.join()
                p4.join()
                
                pixels[i][j] = [t1.value,t2.value,t3.value]
                pixels[i][j+1] = [t4.value,t5.value,t6.value]
                pixels[i][j+2] = [t7.value,t8.value,t9.value]
                pixels[i][j+3] = [t10.value,t11.value,t12.value]
                
                j+=3
            elif (j <= im_dim - 2) & (threadCount >= 2):
                p1 = multiprocessing.Process(target=calcPix, args=(i,j,pixels,t1,t2,t3)) # Creating processes
                p2 = multiprocessing.Process(target=calcPix, args=(i,j+1,pixels,t4,t5,t6))
                
                p1.start() # Starting processes
                p2.start()
                
                p1.join() # Waiting for processes to finish. 
                p2.join()

                pixels[i][j] = [t1.value,t2.value,t3.value]
                pixels[i][j+1] = [t4.value,t5.value,t6.value]
                
                j+=1
            else: 
                """
                I used a process here instead of just doing the work in the main process because it allows for 
                better logging and consistency. Also because I don't want to rewrite the calcPix func to work 
                inside the main process. Sue me. 
                """
                p1 = multiprocessing.Process(target=calcPix, args=(i,j,pixels,t1,t2,t3)) # Creating process
                #print(j,end=": ")
                p1.start() # Starting process
                
                p1.join() # Waiting for process to finish
                
                pixels[i][j] = [t1.value,t2.value,t3.value]
                #print("done")
            end = time.time()
            j+=1
        print(round((end-start)*100)/100)
        """
        Comment out the next 5 lines to disable outputting to tmp2.png every line. This is recommended unless
        you're running the below command at the same time. That only works on linux, btw. 
        feh --force-aliasing -ZR 1 -g 800x800 tmp2.png
        """
        
        pixel2 = pixels.tolist()
        pixel2 = [item for sublist in pixel2 for item in sublist]
        pixel2 = [tuple(l) for l in pixel2]
        im3 = Image.new("RGB", (im_dim, im_dim))
        im3.putdata(pixel2)
        im3.save("outputs/tmp2.png")
        
        i+=1

    pixels = pixels.tolist()
    pixels = [item for sublist in pixels for item in sublist]
    pixels = [tuple(l) for l in pixels]
    im2 = Image.new("RGB", (im_dim, im_dim))
    im2.putdata(pixels)
    name = "outputs/doot"+str(im_dim)+"MT"+re.sub('[.]', '_', str(mult))+".png"
    #name = "outputs/doot"+str(im_dim)+"MT.png"
    im2.save(name)
    end = time.time()
    print('time:',round((end-total_start)*1000)/1000,'s')
    gc.collect()
