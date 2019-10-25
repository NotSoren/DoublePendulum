import math
import numpy as np
from PIL import Image
import sys
import re

def LR(T1, T2, w1, w2):
    alpha1 = math.cos(T1 - T2) / 2
    alpha2 = math.cos(T1 - T2)

    F1 = -w2**2 * math.sin(T1 - T2) / 2 + 9.8 * math.sin(T1)
    F2 = w1**2 * math.sin(T1 - T2) + 9.8 * math.sin(T2)

    a1 = (F1 - alpha1 * F2) / (1 - alpha1 * alpha2)
    a2 = (F2 - alpha2 * F1) / (1 - alpha1 * alpha2)

    return np.array([w1, w2, a1, a2])

args = sys.argv
if len(args) >= 2:
    im_dim = int(re.sub('[^0-9]', '', args[1]))
else:
    im_dim = 75

pixels = np.zeros((im_dim, im_dim, 3))
pixels = pixels.astype(int)

left = 0

for i in range(im_dim):
    for j in range(im_dim):

        step = 0

        h = 0.01

        a_1 = 0
        a_2 = 0

        Th_1 = (i / im_dim) * 2 * math.pi
        Th_2 = (j / im_dim) * 2 * math.pi
        if (3*math.cos(Th_1) + math.cos(Th_2) < -2)|(left==0):
            left += 1
            pixels[i][j] = (255, 255, 255)
            continue

        while abs((Th_1%(2*math.pi)) - ((Th_2+math.pi)%(2*math.pi))) > 0.03407:

            current_state = np.array([Th_1, Th_2, a_1, a_2])

            k1 = LR(*current_state)
            k2 = LR(*(current_state + h * k1 / 2))
            k3 = LR(*(current_state + h * k2 / 2))
            k4 = LR(*(current_state + h * k3))

            R = 1.0 / 6.0 * h * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

            Th_1 += R[0]
            Th_2 += R[1]
            a_1 += R[2]
            a_2 += R[3]

            step += 1

            if step >= 10000:
                break

        print(i,j,"s:",step,"i:",left)
        left += 1
        if step >= 10000:
            pixels[i][j] = (255, 255, 255)
        elif step > 1000:
            pixels[i][j] = [int(round(l*step/10000)) for l in (0, 0, 255)]
        elif step > 100:
            pixels[i][j] = [int(round(l*step/1000)) for l in (255, 0, 255)]
        elif step > 10:
            pixels[i][j] = [int(round(l*step/100)) for l in (255, 0, 0)]
        else:
            pixels[i][j] = [int(round(l*step/10)) for l in (0, 255, 0)]
    pixel2 = pixels.tolist()
    pixel2 = [item for sublist in pixel2 for item in sublist]
    pixel2 = [tuple(l) for l in pixel2]
    im3 = Image.new("RGB", (im_dim, im_dim))
    im3.putdata(pixel2)
    im3.save("tmp0.png")

pixels = pixels.tolist()
pixels = [item for sublist in pixels for item in sublist]
pixels = [tuple(l) for l in pixels]
im2 = Image.new("RGB", (im_dim, im_dim))
im2.putdata(pixels)
name = "doot"+ str(im_dim)+"OC.png"
im2.save(name)
