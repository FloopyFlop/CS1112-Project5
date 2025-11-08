# interval.py


class Interval:
    """
    An Interval has a left endpoint and a right endpoint.
    """


    def __init__(self, left=0, right=1):
        """
        Initializes an Interval object

        Parameters: 
        -----------

        left: numeric; left endpoint.  Default: 0
        
        right: numeric; right endpoint.  Default: 0.  Assume right > left.
        """
        self.left = left
        self.right = right


    def get_width(self):
        """
        Returns the width (numeric) of the interval 
        """
        return self.right - self.left
    

    def shift(self, s):
        """
        Shifts the interval by s units

        Parameter:
        -----------
        
        s: numeric; amount shifted (can be negative)
        """
        self.right += s
        self.left += s


    def is_in(self, other):
        """
        Returns True if self is entirely in the other Interval, otherwise False

        Parameter:
        -----------
        
        other, an instance of class Interval
        """
        return (self.left >= other.left) and (self.right <= other.right)


    def add(self, other):
        """
        Returns a new instance of Interval by adding Intervals component-wise

        Parameter:
        -----------
        
        other, an instance of class Interval
        """
        new_left = self.left + other.left
        new_right = self.right + other.right
        return Interval(new_left, new_right)


    def overlap(self, other):
        """
        If self and other overlap, returns the overlaping interval. Otherwise, 
        returns None

        Parameter:
        -----------
        
        other, another instance of class Interval
        """
        left = max(self.left, other.left)
        right = min(self.right, other.right)
        if right-left > 0:
            return Interval(left, right)
        return None


    def __str__(self):
        """
        Returns a string representation of the interval
        """
        return f"Interval [{self.left:.2f}, {self.right:.2f}]"