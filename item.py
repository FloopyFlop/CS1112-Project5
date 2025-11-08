# item.py


from interval import Interval
from shapes import draw_rect
import matplotlib.pyplot as plt


class Item:
    """
    An Item has an id_, a name, a weight, a location, the number of arms 
    required to lift it, the amount of time required to pick it up, and 
    a time window when pick-up is scheduled.
    """


    def __init__(self, id_, name, weight, loc, arm_requirement, duration):
        """
        Initializes an Item object
        
        Parameters:
        -----------
        
        id_: The item's identifier, an int
        
        name: The item's name, a string
        
        weight: The item's weight, a float
        
        loc: Location of the item, a list of length 2 (x coordinate followed
             by a y coordinate)
        
        arm_requirement: Number of arms required to pick up the item, an int
        
        duration: Time units necessary to fully pick up the item, an int
        """
        self.id_ = id_
        self.name = name
        self.weight = weight
        self.loc = loc
        self.arm_requirement = arm_requirement
        self.duration = duration
        self.picked_window = None
        

    def valid_pickup(self, max_load, num_arms):
        """
        Returns True if a robot with a max picking capability of `max_load`
        and `num_arms` number of arms is able to pick up the item; returns
        False otherwise.

        Parameters:
        ____________

        max_load: (int) the maxium weight that the picking robot can hold

        num_arms: (int) the number of arms of the picking robot
        """
        # Check if the robot can carry the item's weight
        weight_ok = self.weight <= max_load
        # Check if the robot has enough arms to pick up the item
        arms_ok = num_arms >= self.arm_requirement
        # Return True only if both conditions are satisfied
        return weight_ok and arms_ok
        


    def update_pickup_status(self, pickup_time):
        """
        Updates attribute `picked_window` to be an Interval indicating the
        time window that the item is scheduled to be picked.

        The end point of `picked_window` should be `pickup_time` plus the
        duration required to pick up the item.

        Returns None.

        Parameter:
        ____________

        pickup_time: (int) the time at which the robot reaches the item's
            location and begins to pick it up
        """
        # Calculate the end time of the pickup window
        end_time = pickup_time + self.duration
        # Create an Interval from pickup_time to end_time
        self.picked_window = Interval(pickup_time, end_time)
        


    def draw(self, t):
        """
        Draws a red square of side length 1 centered over the item's location
        at timestep `t` if and only if the item is not yet fully picked up at
        time `t`.  Label the square at the center with the item's `id_`.

        An item is fully picked up at the end of its `picked_window` and so
        should not be drawn at that time value.

        Assumes figure window is already open.

        Parameter:
        _____________

        t: (int, non-negative) the timestep
        """
        # Check if the item should be drawn at time t
        # Item should be drawn if it hasn't been picked up yet, or if pickup is not complete
        should_draw = False

        if self.picked_window is None:
            # Item has not been scheduled for pickup, so draw it
            should_draw = True
        elif t < self.picked_window.right:
            # Item is scheduled but not yet fully picked up, so draw it
            should_draw = True

        # Draw the item if needed
        if should_draw:
            # Calculate the lower left corner of the rectangle
            # Rectangle has side length 1 and is centered at the item's location
            lower_left_x = self.loc[0] - 0.5
            lower_left_y = self.loc[1] - 0.5
            # Draw a red rectangle with side length 1
            draw_rect(lower_left_x, lower_left_y, 1, 1, 'r')
            # Add the item's id as text at the center
            plt.text(self.loc[0], self.loc[1], str(self.id_), horizontalalignment="center")
        

