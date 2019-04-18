import pygame, math
import numpy as np
import os
from pygame import gfxdraw

# global variable for the screen dimensions
screen_dim = (800,400)
x_half = int(round(screen_dim[1] / 2))

# global math variables
pi2 = math.pi * 2

# updating the array of parameters
def LR(T1, T2, w1, w2):
    alpha1 = math.cos(T1 - T2) / 2
    alpha2 = math.cos(T1 - T2)
    #alpha2 = math.cos(T1 - T2)
    #alpha1 = alpha2 / 2
    tmp = math.sin(T1 - T2)
    F1 = -w2**2 * tmp / 2 + 9.8 * math.sin(T1)
    F2 = w1**2 * tmp + 9.8 * math.sin(T2)
    a1 = (F1 - alpha1 * F2) / (1 - alpha1 * alpha2)
    a2 = (F2 - alpha2 * F1) / (1 - alpha1 * alpha2)
    return np.array([w1, w2, a1, a2])

# define a main function
def main():
    clock = pygame.time.Clock()
    # denominator of h is the frame rate in fps
    h = 1/240

    input_path = "outputs/doot1000MT1.png"

    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Double Pendulum")

    # create a surface on screen that has the size of screen_dim
    screen = pygame.display.set_mode(screen_dim)

    # get the theta map
    theta_map = pygame.image.load(os.path.join(input_path))
    theta_map = pygame.transform.scale(theta_map, (screen_dim[1], screen_dim[1]))
    theta_map = pygame.transform.rotate(theta_map, 90)
    theta_map = pygame.transform.flip(theta_map, True, False)
    theta_map.convert()

    # draw it
    screen.blit(theta_map, (screen_dim[1], 0))

    # flip
    pygame.display.flip()


    # define a variable to control the main loop
    running = True

    # initial drawing of the pendulum
    #screen.fill((255,255,255))

    a_1 = 0
    a_2 = 0

    Th_1 = math.pi / 2
    Th_2 = math.pi / 2

    pen_scr_length = x_half * (3/8)

    x_1 = x_half + int(round(math.sin(Th_1)*pen_scr_length))
    y_1 = x_half + int(round(-math.cos(Th_1)*pen_scr_length))

    x_2 = x_half + int(round(math.sin(Th_1)*pen_scr_length + math.sin(Th_2)*pen_scr_length))
    y_2 = x_half + int(round(-math.cos(Th_1)*pen_scr_length - math.cos(Th_2)*pen_scr_length))

    pygame.draw.circle(screen, (0, 0, 0), (x_half, x_half), 4)
    pygame.draw.line(screen, (0, 0, 0), (x_half, x_half), (x_1, y_1), 2)
    pygame.draw.circle(screen, (0, 0, 0), (x_1, y_1), 4)
    pygame.draw.line(screen, (0, 0, 0), (x_1, y_1), (x_2, y_2), 2)
    pygame.draw.circle(screen, (0, 0, 0), (x_2, y_2), 4)

    current_mouse = pygame.mouse.get_pos()

    # main loop
    while running:

        # check to see if the mouse has been moved
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos != current_mouse:
            screen.blit(theta_map, (screen_dim[1], 0))
            Th_1 = ((mouse_pos[0] - screen_dim[1]) / screen_dim[1]) * pi2
            Th_2 = ((mouse_pos[1] - screen_dim[1]) / screen_dim[1]) * pi2

            a_1 = 0
            a_2 = 0

            current_mouse = mouse_pos

        # draw trail
        trail_x = int(round(((Th_1) * screen_dim[1] / pi2)%400 + screen_dim[1]))
        trail_y = int(round(((Th_2) * screen_dim[1] / pi2) + screen_dim[1]))

        trail_y = trail_y % 400

        pygame.draw.rect(screen, (0, 200, 0),(trail_x-1, trail_y-1, 3, 3))

        pygame.draw.rect(screen,(255, 255, 255),(0,0,screen_dim[1],screen_dim[1]))
        clock.tick(1/h)
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        # update function for pendulum
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

        x_1 = x_half + int(round(math.sin(Th_1)*pen_scr_length))
        y_1 = x_half + int(round(-math.cos(Th_1)*pen_scr_length))

        x_2 = x_half + int(round(math.sin(Th_1)*pen_scr_length + math.sin(Th_2)*pen_scr_length))
        y_2 = x_half + int(round(-math.cos(Th_1)*pen_scr_length - math.cos(Th_2)*pen_scr_length))

        pygame.gfxdraw.aacircle(screen, x_half, x_half, 4, (0, 0, 0))
        pygame.draw.aaline(screen, (0, 0, 0), (x_half, x_half), (x_1, y_1), True)
        pygame.gfxdraw.aacircle(screen, x_1, y_1, 4, (0, 0, 0))
        pygame.draw.aaline(screen, (0, 0, 0), (x_1, y_1), (x_2, y_2), True)
        pygame.gfxdraw.aacircle(screen, x_2, y_2, 4, (0, 0, 0))
        #screen.blit(theta_map, (screen_dim[1], 0))

        pygame.display.flip()



# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
