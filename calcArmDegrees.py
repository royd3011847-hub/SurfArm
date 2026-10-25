import math

# Global arm lengths
JOINT1LEN = 10   # length of arm joint 1
JOINT2LEN = 10    # length of arm joint 2
JOINT1RANGE = [0, 180]

def circle_intersection(x, y):
    """
    Intersection points of a circle of radius JOINT2LEN centered at (x, y) and
    a circle of radius JOINT1LEN centered at the origin. Assumes (x, y) != (0, 0).
    Raises ValueError if the circles don't intersect.
    """
    r0 = JOINT1LEN
    r1 = JOINT2LEN

    d = math.hypot(x, y)  # distance between centers

    if d > r0 + r1 or d < abs(r0 - r1):
        raise ValueError(f"Circles don't intersect: distance is {d}")

    a = (d * d + r0 * r0 - r1 * r1) / (2 * d)   # dist from origin to midpoint of intersections
    h = math.sqrt(max(0.0, r0 * r0 - a * a))    # dist from midpoint to each intersection point

    # midpoint between the intersection points, along the line joining the centers
    mx = a * x / d
    my = a * y / d

    # perpendicular offset
    ox = h * (y / d)
    oy = h * (x / d)

    if ox >= 0:  # return the smaller x value
        rx = mx + ox
        ry = my - oy
    else:
        rx = mx - ox
        ry = my + oy
    
    

    return (rx, ry)
    
    
# function that takes 
# print(circle_intersection(6, 12))


def arm_degrees(x, y):
    
    
    #joint1 x and y endpoint
    joint1x, joint1y = circle_intersection(x, y)
    #joint2 x and y endpoint
    joint2x, joint2y = x, y
    
    joint1 = 0.0 # angle of joint attached to sub
    #find using arcsin
    joint1 = math.degrees(math.asin(joint1y/JOINT1LEN))
    # print("Joint1: "+str(joint1))
    if joint1 < 0:
        joint1 = 180 + joint1
    
    joint2 = 0.0 # angle of claw wrist joint
    #1. find the slope of joint 2 points and joint 1 points
    if joint2x-joint1x == 0:
        joint2 = 0
        return joint1, joint2
    slope = (joint2y-joint1y)/(joint2x-joint1x)
    # print("slope: " +str(slope))
    #2. find the degrees from the positive x axis to the 
    joint2 = math.degrees(math.atan(slope))
    if joint2 < 0:
        joint2 = 180 + joint2
    joint2 -= joint1
    # print("joint2: "+str(joint2))
    return joint1, joint2

print(arm_degrees(0, 19))