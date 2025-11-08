# For dynamic graphics, first use this command in the Spyder Python Console:
#     %matplotlib qt


from robot import Robot
from item import Item
import numpy as np
import matplotlib.pyplot as plt


def run_robots(data_filename):
    """

    Create an allocation of robots to pickup items given a data file in the
    necessary format.

    Parameter:
    -----------
    
    data_filename: string; the name of the data file.
    """
    with open(data_filename, 'r') as fid:
        # Process the first line of the file
        line = fid.readline()  
        sim_info = line.strip().split(',')
        sim_time = int(sim_info[0])
        horiz_dim = float(sim_info[1])
        vert_dim = float(sim_info[2])
        room_size = np.array([horiz_dim, vert_dim])

        # Process the remaining lines of the file
        
        ##############################################################
        # TASK 1: Add code below to create a list of Robots and a 
        # list of Items.
        ##############################################################

        robots = []  # list of robots
        items = []   # list of items
        for line in fid:
            # `line` is a string, the next line of text in the file
            # Split `line` into a list of strings, with comma as separator
            tokens = line.strip().split(',')

            # Check if this line is for a Robot or an Item
            if tokens[0].strip() == 'Robot':
                # Parse robot data: Robot, ID, max_weight, [x, y]
                # Format: Robot, 1, 4, [4,4]
                # After splitting by comma: ['Robot', ' 1', ' 4', ' [4', '4]']
                robot_id = int(tokens[1].strip())
                max_weight = float(tokens[2].strip())
                # Parse the location which is split across tokens[3] and tokens[4]
                # tokens[3] contains '[x' and tokens[4] contains 'y]'
                x_str = tokens[3].strip().replace('[', '')
                y_str = tokens[4].strip().replace(']', '')
                init_loc = [float(x_str), float(y_str)]
                # Create a Robot object and add to the robots list
                robot = Robot(robot_id, max_weight, sim_time, init_loc)
                robots.append(robot)

            elif tokens[0].strip() == 'Item':
                # Parse item data: Item, ID, name, weight, [x, y], arms, duration
                item_id = int(tokens[1].strip())
                name = tokens[2].strip()
                weight = float(tokens[3].strip())
                # Parse the location string which is in format [x,y]
                # The location may span multiple tokens depending on spacing
                # Find the token with '[' and reconstruct the location
                loc_str = ''
                loc_start_idx = 4
                for i in range(4, len(tokens)):
                    if '[' in tokens[i]:
                        loc_start_idx = i
                        break
                for i in range(loc_start_idx, len(tokens)):
                    loc_str += tokens[i].strip()
                    if ']' in tokens[i]:
                        # The next two tokens after location are arms and duration
                        arm_requirement = int(tokens[i + 1].strip())
                        duration = int(tokens[i + 2].strip())
                        break
                # Remove brackets and split by comma
                loc_str = loc_str.replace('[', '').replace(']', '')
                loc_parts = loc_str.split(',')
                loc = [float(loc_parts[0].strip()), float(loc_parts[1].strip())]
                # Create an Item object and add to the items list
                item = Item(item_id, name, weight, loc, arm_requirement, duration)
                items.append(item)

        ##############################################################
        # End of TASK 1
        ##############################################################
       
    # Do a task allocation
    items_remaining = simple_allocation(robots, items)

    # Animate the simulation
    animate(robots, items, sim_time, room_size)

    # Print descriptive output
    output_results(robots, items_remaining)
    

def simple_allocation(robots, items):
    """
    Given a list of items and a list of robots, allocate item pickups to the robots.

    Algorithm: for each `Item` in `items`, look for the first `Robot` in `robots`
    that is capable of picking it up. Pick up the `Item` with this first `Robot`.

    Returns: list; a list of remaining `Item`s that did not get picked up.

    Parameters:
    -----------

    robots: list; non-empty list of unique `Robot` references

    items: list; non-empty list of unique `Item` references
    """
    ##############################################################
    # TASK 2: Implement this function
    ##############################################################
    # Create a list to store items that were not picked up
    items_remaining = []

    # Iterate through each item in the items list
    for item in items:
        # Flag to track if the item was picked up
        picked_up = False

        # Try each robot in order to see if it can pick up the item
        for robot in robots:
            # Attempt to pick up the item with this robot
            # Note: num_arms defaults to 0 for standard robots
            if robot.pick(item, do_pick=True, num_arms=0):
                # If successful, mark the item as picked up and move to next item
                picked_up = True
                break

        # If no robot could pick up the item, add it to the remaining list
        if not picked_up:
            items_remaining.append(item)

    # Return the list of items that were not picked up
    return items_remaining

    ##############################################################
    # End of TASK 2
    ##############################################################


def animate(robots, items, sim_time, room_size):
    """
    Animate the robots and items in space for `sim_time` timesteps.  At each time 
    step, call the `draw` method for each `Item` and for each `Robot`. 

    For drawing a Robot at its correct location at each time step, you will find 
    the get_location() method helpful.

    Parameters
    ----------
    
    robots : list; list of `Robot` references

    items : list; list of `Item` references
    
    sim_time : int; number of timesteps
    
    roomsize : list; length-2 list that represents the dimensions of the room
    """
    plt.close('all')
    plt.figure()
    plt.pause(1)
    for t in range(0, sim_time + 1):
        # Clear axis
        plt.cla()
        plt.axis('equal')
        plt.axis('off')
        # Draw the room
        plt.axis([0, room_size[0] + 1, 0, room_size[1] + 1])
        plt.title(f"Time = {t}")

        ##################################################################
        # TASK 3: Add code for drawing the items and robots at time step t
        ##################################################################
        # Draw all items at time step t
        for item in items:
            # Each item's draw method handles whether it should be drawn at time t
            item.draw(t)

        # Draw all robots at time step t
        for robot in robots:
            # Get the robot's location at time step t
            robot_loc = robot.get_location(t)
            # Draw the robot at its current location
            robot.draw(robot_loc)

        ##################################################################
        # End of TASK 3
        ##################################################################
        
        b= 1  # blink time of 1 second for animation
        plt.pause(b)


def output_results(robots, items_remaining):
    """
    Prints the results of task allocation. Show the stats and tasks for each 
    `Robot` in `robots`:
    (1) Print the number of `Item`s picked and the total timesteps taken
    (2) Print out each `Item` picked and the time period taken to navigate to
    the object and pick it.

    Also print out each `Item` that the robots were not able to pick up.

    See the print format in the project description.
    
    Parameters:
    ------------
    
    robots: list; each element is a `Robot` in the simulation

    items_remaining: list; each element is an `Item` that the robots were not
    able to pick up.
    """

    ##############################################################
    # TASK 4: Implement this method
    ##############################################################
    # Print separator line
    print("-------------------------------")

    # Print information for each robot
    for robot in robots:
        # Get the list of items picked by this robot
        items_picked = robot.get_items_picked()

        # Only print if the robot picked at least one item
        if len(items_picked) > 0:
            # Print robot stats: ID, number of items, and total operation time
            robot_id = robot.get_id()
            num_items = len(items_picked)
            total_time = robot.total_operation_time()
            print(f"Robot {robot_id} picked {num_items} items in {total_time} timesteps")

            # Print information for each item picked by this robot
            for item in items_picked:
                # Get the item's name, ID, and pickup window
                item_name = item.name
                item_id = item.id_
                # The item was assigned when the robot arrived at its location
                assigned_time = item.picked_window.left
                # The item was fully picked up at the end of the pickup window
                picked_time = item.picked_window.right
                print(f"{item_name} (ID {item_id}): Assigned at time {assigned_time}, picked up at time {picked_time}")

    # Print separator line
    print("-------------------------------")

    # Print information about items that were not picked up
    if len(items_remaining) > 0:
        print("The robots were not able to pick up:")
        for item in items_remaining:
            print(f"{item.name} (ID {item.id_})")
    else:
        print("All items were picked up!")

    # Print final separator line
    print("-------------------------------")

    ##############################################################
    # End of TASK 4
    ##############################################################


if __name__ == '__main__':
    run_robots("room1.txt")