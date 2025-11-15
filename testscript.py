# testscript.py
"""
Demonstration and tests for Project 5 classes
"""


from interval import Interval
from item import Item
from robot import Robot
import matplotlib.pyplot as plt


## Test class Interval
in1 = Interval(3, 9)              # Instantiate an Interval with endpoints 3 and 9
print(in1)
print(in1.left)                   # Should be 3. The attributes are "public," so it 
                                  #   is possible to access the attribute left directly.
in2 = Interval()                  # Instantiate an Interval with default end points
print(in2)
o = in1.overlap(Interval(5, 15))  # o references an Interval with endpoints 5 and 9.
print(o)
print(f"{o.get_width()=}")        # Should be 4, the width of the Interval referenced by o


## Test class Item
i1 = Item(1, 'basket', 2, [3, 4], 0, 3)
print(f"{i1.id_=}")                        # Should be 1
print(f"{i1.loc=}")                        # Should be [3, 4]

# Test valid_pickup method
# Test case 1: Robot can pick up the item (weight ok, arms ok)
print(f"{i1.valid_pickup(4, 2)=}")         # Should be True
# Test case 2: Robot cannot pick up the item (weight too low)
print(f"{i1.valid_pickup(1, 0)=}")         # Should be False
# Test case 3: Robot cannot pick up the item (not enough arms)
i2 = Item(2, 'table', 5, [2, 2], 2, 2)
print(f"{i2.valid_pickup(10, 1)=}")        # Should be False (needs 2 arms, has 1)
# Test case 4: Robot can pick up the item (exact match)
print(f"{i2.valid_pickup(5, 2)=}")         # Should be True

# Test update_pickup_status method
# Test case 1: Update pickup status starting at time 2
print(f"{i1.update_pickup_status(2)=}")    # Should return None
print(f"{i1.picked_window.left=}")         # Should be 2
print(f"{i1.picked_window.right=}")        # Should be 5 (2 + 3 duration)
print(f"{i1.picked_window.get_width()=}") # Should be 3
# Test case 2: Update pickup status starting at time 0
i3 = Item(3, 'pen', 0.1, [1, 1], 0, 1)
i3.update_pickup_status(0)
print(f"{i3.picked_window.left=}")         # Should be 0
print(f"{i3.picked_window.right=}")        # Should be 1

# Test draw method
# Test case 1: Item should be drawn at time 3 (not yet fully picked up)
plt.figure(1)
i1.draw(3)                                  # Should draw red rectangle with "1"
# Test case 2: Item should not be drawn at time 5 (fully picked up)
plt.figure(2)
i1.draw(5)                                  # Should not draw anything
# Test case 3: Item should be drawn when not scheduled
i4 = Item(4, 'notebook', 1, [5, 5], 0, 2)
plt.figure(3)
i4.draw(0)                                  # Should draw red rectangle with "4"



## Test class Robot
# Create test items
item1 = Item(1, 'apples', 12, [3, 3], 1, 1)
item2 = Item(4, 'rubber duck', 1, [5, 5], 0, 3)
item3 = Item(6, 'paperclip', 0.1, [9, 1], 0, 3)

# Test Robot __init__ and getter methods
# Test case 1: Create a robot and test get_id
robot1 = Robot(1, 4, 20, [4, 4])
print(f"{robot1.get_id()=}")                # Should be 1
# Test case 2: Test get_items_picked on a new robot
print(f"{robot1.get_items_picked()=}")      # Should be []
# Test case 3: Create another robot
robot2 = Robot(3, 10, 20, [1, 2])
print(f"{robot2.get_id()=}")                # Should be 3

# Test total_operation_time and latest_resting_loc
# Test case 1: Robot with no items picked
print(f"{robot1.total_operation_time()=}") # Should be 0
print(f"{robot1.latest_resting_loc()=}")   # Should be [4, 4]

# Test travel_steps method
# Test case 1: Move from [4, 4] to [5, 5] (move right then up)
path1 = robot1.travel_steps([4, 4], [5, 5])
print(f"{path1=}")                          # Should be [[4, 4], [5, 4], [5, 5]]
# Test case 2: Move from [1, 2] to [3, 3] (move right then up)
path2 = robot2.travel_steps([1, 2], [3, 3])
print(f"{path2=}")                          # Should be [[1, 2], [2, 2], [3, 2], [3, 3]]
# Test case 3: Same location
path3 = robot1.travel_steps([5, 5], [5, 5])
print(f"{path3=}")                          # Should be [[5, 5]]
# Test case 4: Move left and down
path4 = robot1.travel_steps([5, 5], [3, 3])
print(f"{path4=}")                          # Should move left then down

# Test draw method
# Test case 1: Draw robot at location [4, 4]
plt.figure(4)
robot1.draw([4, 4])                         # Should draw blue circle with "1"
# Test case 2: Draw robot at location [1, 2]
plt.figure(5)
robot2.draw([1, 2])                         # Should draw blue circle with "3"

# Test pick method
# Test case 1: Robot 1 cannot pick up item1 (apples need 1 arm, robot has 0)
result1 = robot1.pick(item1, do_pick=True, num_arms=0)
print(f"{result1=}")                        # Should be False
# Test case 2: Robot 1 can pick up item2 (rubber duck)
result2 = robot1.pick(item2, do_pick=True, num_arms=0)
print(f"{result2=}")                        # Should be True
print(f"{robot1.total_operation_time()=}") # Should be 5 (2 steps travel + 3 pickup)
print(f"{robot1.latest_resting_loc()=}")   # Should be [5, 5]
# Test case 3: Robot 1 can pick up item3 (paperclip)
result3 = robot1.pick(item3, do_pick=True, num_arms=0)
print(f"{result3=}")                        # Should be True
print(f"{robot1.total_operation_time()=}") # Should be 16 (previous 5 + 8 travel + 3 pickup)
# Test case 4: Test that item2 cannot be picked up again (already scheduled)
result4 = robot2.pick(item2, do_pick=True, num_arms=0)
print(f"{result4=}")                        # Should be False
# Test case 5: Test get_items_picked after picking items
items_picked = robot1.get_items_picked()
print(f"{len(items_picked)=}")              # Should be 2
print(f"{items_picked[0].name=}")           # Should be 'rubber duck'
print(f"{items_picked[1].name=}")           # Should be 'paperclip'

# Test get_location method (provided method)
# Test case 1: Get location at time 0
loc_t0 = robot1.get_location(0)
print(f"{loc_t0=}")                         # Should be [4, 4] (initial location)
# Test case 2: Get location at time 1 (traveling to first item)
loc_t1 = robot1.get_location(1)
print(f"{loc_t1=}")                         # Should be [5, 4]
# Test case 3: Get location at time 2 (arriving at first item)
loc_t2 = robot1.get_location(2)
print(f"{loc_t2=}")                         # Should be [5, 5]
# Test case 4: Get location at time 13 (after picking up both items)
loc_t13 = robot1.get_location(13)
print(f"{loc_t13=}")                        # Should be [9, 1]

