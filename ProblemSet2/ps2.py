# -*- coding: utf-8 -*-
# 6.00.2x Problem Set 2: Simulating robots

import math
import random

import ps2_visualize
import pylab

# For Python 2.7:
from ps2_verify_movement27 import testRobotMovement

# If you get a "Bad magic number" ImportError, you are not using 
# Python 2.7 and using most likely Python 2.6:


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.cleaned = []
        
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        clean = (int(pos.x),int(pos.y))
        if clean not in self.cleaned:
            self.cleaned.append(clean)
        return (int(pos.x),int(pos.y))
        
        

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return (m,n) in self.cleaned
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.cleaned)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return Position(random.choice(range(self.width)),random.choice(range(self.height)))

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        if pos.x < 0 or pos.y<0:
            return False
        if pos.x > self.width or pos.y > self.height:
            return False
        return int(pos.x) in range(self.width) and int(pos.y) in range(self.height)


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.posi = Position(random.choice(range((self.room.width))),random.choice(range((self.room.height))))
        self.dir = random.choice(range(360))
        

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return Position(self.posi.x,self.posi.y)
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.dir

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.posi = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.dir = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def __init__(self, room, speed):
        ## 继承 Robot 所有的属性
        Robot.__init__(self,room, speed)
        
        ##  room 的 cleaned 放上初始位置
        self.room.cleanTileAtPosition(self.getRobotPosition())
        
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        
        self.room      #  robot 所在 RectangularRoom
        self.speed
        self.getRobotPosition()    # robot 现在 position
        self.getRobotDirection()    # robot 现在 direction
        
        ##  移动到下一个位置
        # 如果碰壁，调整方向
        while self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed).x < 0 or self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed).y  < 0 or self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed).x > self.room.width or self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed).y > self.room.height:
            self.setRobotDirection(random.choice(range(360)))
        # 不碰壁，则移动到新的 Position
        else:
            self.setRobotPosition(self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed))
            self.room.cleanTileAtPosition(self.getRobotPosition())
        
        
        
        

# Uncomment this line to see your implementation of StandardRobot in action!
# testRobotMovement(StandardRobot, RectangularRoom)


# === Problem 3
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    total = []
    for n in range(num_trials):
        # ???  如何  确定机器人们是在同一个 room        答: 这样就可以定了，但一定要把 room 放在 for loop 下面，这样才能保证每次重置 clean
        room = RectangularRoom(width, height)
        #加入 num_robots 个机器人
        robots = []
        for i in range(num_robots):
            robots.append(robot_type(room,speed))
        time = 0
        # 当打扫面积不够时
        while float(room.getNumCleanedTiles())/float(room.getNumTiles()) < (min_coverage):
            time += 1
            for i in robots:
                i.updatePositionAndClean()
        total.append(time)
    mean = sum(total)/float(num_trials)
    return mean
    
    

# Uncomment this line to see how much your simulation takes on average
# print  runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot)


# === Problem 4
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def __init__(self, room, speed):
        ## 继承 Robot 所有的属性
        Robot.__init__(self,room, speed)
        
        ##  room 的 cleaned 放上初始位置
        self.room.cleanTileAtPosition(self.getRobotPosition())
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        
        self.room      #  robot 所在 RectangularRoom
        self.speed
        self.getRobotPosition()    # robot 现在 position
        self.getRobotDirection()    # robot 现在 direction
        
        ##  移动到下一个位置
        # 如果碰壁，调整方向
        while self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed).x < 0 or self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed).y  < 0 or self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed).x > self.room.width or self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed).y > self.room.height:
            self.setRobotDirection(random.choice(range(360)))
        # 不碰壁，则移动到新的 Position
        else:
            self.setRobotPosition(self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed))
            self.room.cleanTileAtPosition(self.getRobotPosition())
            self.setRobotDirection(random.choice(range(360)))             #  每走一步立刻变向


def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print "Plotting", num_robots, "robots..."
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.figure('Plot1')
    pylab.plot(num_robot_range, times1)                                             #  1. 注意，如果下面不写legend， 这里可以
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'),loc='upper right')            #  1. 注意，这里的 legent 用了 tuple 来写 legend 名称
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()



def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print "Plotting cleaning time for a room of width:", width, "by height:", height
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 50, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 50, RandomWalkRobot))
    pylab.figure('Plot2')
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'), loc='upper left')
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    


# === Problem 5
#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#
showPlot1('Time It Takes 1 - 10 Robots To Clean 80% Of A Room', 'Number of Robots', 'Time-steps')

#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#
showPlot2('Time It Takes Two Robots To Clean 80% Of Variously Shaped Rooms', 'Aspect Ratio', 'Time-steps')