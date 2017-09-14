#!/usr/bin/python

import math
import sys

MOTOR_DISTANCE_MM = 1000
CIRCUMFERENCE_MM = 2*math.pi*16
STEPS_IN_REV = 200
MICROSTEPPING = 1
MM_PER_STEP = CIRCUMFERENCE_MM / (STEPS_IN_REV*MICROSTEPPING)

print 'mm per step:', MM_PER_STEP

cur_x = start_x = 500
cur_y = start_y = 500

possible_steps = ((0,0), (1,1), (1, 0), (1, -1), (0,1), (0,-1), (-1, 1), (-1, 0), (-1,-1))

def distance(x1, y1, x2, y2):
    d_x = math.pow(x1-x2, 2)
    d_y = math.pow(y1-y2, 2)
    return math.sqrt(d_x + d_y)

def step_coords_from_cartesian(x, y):
    s_x = distance(0, 0, x, y) / MM_PER_STEP
    s_y = distance(MOTOR_DISTANCE_MM, 0, x,y) / MM_PER_STEP
    return (s_x, s_y)

s_m = MOTOR_DISTANCE_MM / MM_PER_STEP
def cartesian_coords_from_steps(s_x, s_y):
    angle = math.acos( (s_x*s_x + s_m*s_m - s_y*s_y) / (2*s_x*s_m) )
    x = s_x * math.cos(angle) * MM_PER_STEP
    y = s_x * math.sin(angle) * MM_PER_STEP
    return (x,y)

def distance_from_line(x1, y1, x2, y2, x0, y0):
    top = abs( (y2-y1)*x0 - (x2-x1)*y0 + x2*y1 -y2*x1 )
    bottom = math.sqrt( math.pow(y2-y1, 2) + math.pow(x2-x1, 2) )
    if bottom < 0.0001: return 0
    return top/bottom

x_axis = []
y_axis = []

print 'starting x', cur_x, 'y', cur_y
a,b = step_coords_from_cartesian(cur_x, cur_y)
print a,b
c,d = cartesian_coords_from_steps(a,b)
print c,d
print

if abs(c-cur_x) > 1 or abs(d-cur_y) > 1:
    print 'invalid translation'
    sys.exit(1)

num_steps = 0

def draw_line_to(end_x, end_y):
    global cur_x, cur_y, num_steps, x_axis, y_axis
    start_x = cur_x
    start_y = cur_y

    if end_x == start_x and end_y == start_y: return

    for step in range(100000):
        cur_step_x, cur_step_y = step_coords_from_cartesian(cur_x, cur_y)
        best_step = None
        best_step_pos = None
        best_step_distance = None
        for step in possible_steps:
            next_step_x, next_step_y = (cur_step_x + step[0], cur_step_y + step[1])
            #print step
            #print 'next', next_step_x, next_step_y
            next_x, next_y = cartesian_coords_from_steps(next_step_x, next_step_y)
            #print 'next1', next_x, next_y
            d = distance_from_line(start_x, start_y, end_x, end_y, next_x, next_y)*10 + distance(end_x, end_y, next_x, next_y)
            #print 'distance', d, start_d
            if best_step is None or d < best_step_distance:
                best_step = step
                best_step_pos = (next_x, next_y)
                best_step_distance = d

        cur_x = best_step_pos[0]
        cur_y = best_step_pos[1]
        x_axis.append(cur_x)
        y_axis.append(cur_y)
        print 'step:', best_step, 'x', cur_x, 'y', cur_y, 'distance', best_step_distance

        if best_step == (0,0):
            break
        else:
            num_steps += 1

    assert abs(cur_x - end_x) < 1
    assert abs(cur_y - end_y) < 1
    cur_x = end_x
    cur_y = end_y


draw_line_to(300, 500)
draw_line_to(300, 300)
draw_line_to(500, 300)
draw_line_to(500, 500)

draw_line_to(300, 300)
cur_x = 300
cur_y = 500
draw_line_to(500,300)

import matplotlib.pyplot as plt
plt.plot(x_axis, y_axis)
plt.ylim([0,1000])
plt.xlim([0,1000])
plt.show()

print 'Done in %d steps' % num_steps
