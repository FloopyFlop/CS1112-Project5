# robot.py


from shapes import draw_disk
import matplotlib.pyplot as plt
import copy


class Robot:
    """
    A robot has an ID, a maximum weight it can pick up, a total amount of time
    when it is operating, an initial location, and a list of items it has picked. 
    A robot moves in the cardinal directions only--north, east, south, west (NESW)
    --and moves one unit distance in each time step.

    Attributes:
    ------------

    _id_: int; the robot's identifier

    _max_weight: number; maximum weight that the robot can pick up at each pickup

    _total_time: int; the total number of time steps the robot is on (moving, picking)

    _init_loc: list; the initial location of the robot, represented as a list of two
    numbers (the x and y coordinates)

    _items_picked: list; each element of the list is an Item that the robot has 
    picked up. The list is initially empty
    """


    def __init__(self, id_, max_weight, total_time, init_loc):
        """
        Initializes a `Robot` object

        Parameters:
        ------------

        id_: int; robot's identifier

        max_weight: number; maximum weight that the robot is able to pick up

        total_time: int; total number of time steps the robot can be on, positive

        init_loc: list; a length-2 list of the initial location (x- and y-coord)
        of the robot
        """
        # Initialize all attributes as described in the class docstring
        self._id_ = id_
        self._max_weight = max_weight
        self._total_time = total_time
        self._init_loc = init_loc
        # Initialize the list of items picked as empty
        self._items_picked = []
        


    def get_id(self):
        """
        Returns (int) the `_id_` of the robot.
        """
        # Return the robot's id
        return self._id_
        


    def get_items_picked(self):
        """
        Returns a deep copy of `_items_picked`.
        """
        # Return a deep copy of the items picked list
        return copy.deepcopy(self._items_picked)
        
   

    def total_operation_time(self):
        """
        Returns the total operation time of the robot immediately after
        completing its most recent Item pick-up. The return type is int.

        You may find it useful to leverage the `_items_picked_` attribute. If
        no item has been picked up, return 0 as the total operation time.
        """
        # Check if any items have been picked up
        if len(self._items_picked) == 0:
            # No items picked, so total operation time is 0
            return 0
        else:
            # Get the last item in the items_picked list
            last_item = self._items_picked[-1]
            # Return the right endpoint of the last item's picked_window
            # This is when the robot finished picking up the last item
            return last_item.picked_window.right
        
    

    def latest_resting_loc(self):
        """
        Returns the latest resting location of the robot. This should be a
        length 2 list representing a location (one x-coord and one y-coord).

        You may find it useful to leverage the `_items_picked_` attribute.

        If no item has been picked up, the robot's latest resting location
        is just its initial location; otherwise, the robot's latest resting
        location is where it picked up the most recent item.
        """
        # Check if any items have been picked up
        if len(self._items_picked) == 0:
            # No items picked, return initial location
            return self._init_loc
        else:
            # Return the location of the last item picked
            last_item = self._items_picked[-1]
            return last_item.loc
        
    

    def draw(self, loc):
        """
        Draw a blue circle of diameter 1 to represent the robot at a given
        location `loc`. Label the circle at the center with the robot's `_id_`.

        Assumes figure window is already open.

        Parameter:
        -----------

        loc: list; a length 2 list storing the x- and y-coordinates at which
        the robot should be drawn.
        """
        # Draw a blue disk with diameter 1 (radius 0.5) at the given location
        draw_disk(loc[0], loc[1], 0.5, 'b')
        # Add the robot's id as text at the center
        plt.text(loc[0], loc[1], str(self._id_), horizontalalignment="center")
        


    def travel_steps(self, curr, dest):
        """
        Returns a valid list of locations that form a path between two locations,
        `curr` and `dest`. Each location in the list corresponds to one time step.
        The first location in the returned list should be `curr`, the robot's
        current location; the last location in the list should be `dest`, the
        robot's destination.  The return type is list; each element inside the
        list is a length 2 list storing an x-coordinate and a y-coordinate.

        While there are multiple ways to construct the path, one simple solution
        is to have the robot first move along the x-direction, then along the
        y-direction.

        Parameters:
        -----------

        curr: list; a length 2 list storing the robot's current x-y coordinate

        dest: list; a length 2 list storing the robot's destiny x-y coordinate

        If `curr` and `dest` refer to the same location, return a length 1 list
        storing this shared location.

        """
        # Initialize the path with the current location
        path = [curr]

        # Extract current and destination coordinates
        curr_x = curr[0]
        curr_y = curr[1]
        dest_x = dest[0]
        dest_y = dest[1]

        # Move along the x-direction first
        # Determine the direction of movement in x
        if dest_x > curr_x:
            # Move right (increase x)
            for x in range(curr_x + 1, dest_x + 1):
                path.append([x, curr_y])
        elif dest_x < curr_x:
            # Move left (decrease x)
            for x in range(curr_x - 1, dest_x - 1, -1):
                path.append([x, curr_y])

        # Move along the y-direction
        # Determine the direction of movement in y
        if dest_y > curr_y:
            # Move up (increase y)
            for y in range(curr_y + 1, dest_y + 1):
                path.append([dest_x, y])
        elif dest_y < curr_y:
            # Move down (decrease y)
            for y in range(curr_y - 1, dest_y - 1, -1):
                path.append([dest_x, y])

        return path
        


    def pick(self, item, do_pick=True, num_arms=0):
        """
        Returns True if the robot is able to pick up the item, False otherwise.

        If the robot is able to pick up the item, execute the pick-up if `do_pick`
        evaluates to True.

        The robot is able to pick up `item` when the following are true:
        1. the robot's physical characteristics allows it to pick up `item`
        2. the robot can travel to `item` and fully pick it up in time
        3. `item` has not yet been scheduled for pickup

        If the pick-up is executed, we need to:
        1. Update `item`'s picked_window
        2. Update `Robot`'s `_items_picked` attribute
        No attributes should be updated if the pick-up is not executed.

        Parameters:
        -----------

        item: Item; the item to be picked up by the robot

        do_pick: Boolean; indicates if the robot should execute the pick should
        it be possible. Default is True.

        num_arms: int; the number of arms the robot has. Default is 0.

        """
        # Condition 1: does the robot's physical chacteristics allow it to pick up
        # the item? Hint: you wrote a relevant function in the Item class.
        # Check if the item can be picked up given the robot's max weight and arms
        physical_ok = item.valid_pickup(self._max_weight, num_arms)

        # Condition 2: can the robot travel to the item and pick it up within the
        # given total simulation time `_total_time`?
        # Hint: you may find the total_operation_time(), latest_resting_loc(),
        # and travel_steps() methods useful.
        # Calculate the time needed to travel from current location to the item
        current_loc = self.latest_resting_loc()
        travel_path = self.travel_steps(current_loc, item.loc)
        # Time to travel is the length of the path minus 1
        # (since the first position is the current location)
        travel_time = len(travel_path) - 1
        # Time when robot arrives at the item
        arrival_time = self.total_operation_time() + travel_time
        # Time when robot finishes picking up the item
        finish_time = arrival_time + item.duration
        # Check if the robot can complete the pickup within the total time
        time_ok = finish_time <= self._total_time

        # Condition 3: is the item not already scheduled for pick-up?
        # Hint: `item` has a relevant attribute that you may need.
        # Check if the item's picked_window is None (not yet scheduled)
        not_scheduled = item.picked_window is None

        # If all three conditions above are met, set `success` to True.
        # Check if all three conditions are satisfied
        success = physical_ok and time_ok and not_scheduled

        # If the robot is able to pick up the item and `do_pick` is True,
        # we execute the pick-up by
        # (1) Updating the item's `picked_window`
        # (2) Updating the robot's `_items_picked`
        if success and do_pick:
            # Update the item's pickup status with the arrival time
            item.update_pickup_status(arrival_time)
            # Add the item to the robot's list of picked items
            self._items_picked.append(item)

        # Return `success`
        return success


    def get_location(self, t):
        """
        Provided method that computes the location of the robot at a queried
        time step t, where t >= 0.

        This method calls the total_operation_time(), latest_resting_loc(), and
        travel_steps() methods that you implemented and assumes correctness in
        those methods. 

        Read but DO NOT modify the code.
        """
        # If t is larger than the total operation time of the robot so far
        if t >= self.total_operation_time():
            return self.latest_resting_loc()
        # Determine which item the robot is handling at the queried time step
        index = 0
        while index < len(self._items_picked) and t > self._items_picked[index].picked_window.right:
            index += 1
        # If the robot is in the middle of picking up an item
        if t >= self._items_picked[index].picked_window.left:
            return self._items_picked[index].loc
        # Otherwise, the robot is in the middle of traveling
        if index == 0:
            curr = self._init_loc
            time_offset = t
        else:
            curr = self._items_picked[index - 1].loc
            time_offset = t - self._items_picked[index - 1].picked_window.right
        dest = self._items_picked[index].loc
        steps = self.travel_steps(curr, dest)
        return steps[time_offset]
    