class ListStateMachine:
    """ An object used to help make sure that only correct input is added to an array """

    def __init__(self, depth):
        """ depth - the depth of the array; for example, [1, 2, 3] would have a depth of 1, but [[1, 2], [3, 4]]
                    would have a depth of 2. Depth must be 1 or 2. If it is not 1, it will be set to 2 """
        self.array = []
        self.array2D = []
        self.string = ' -> '  # A String representation of the value of the array
        self.currentValue = 0  # Value of the number the that is currently being typed
        self.isComplete1 = False  # Whether the array is complete (has balanced opening and closing braces, etc.)
        self.isComplete2 = False  # Whether the array is complete (has balanced opening and closing braces, etc.)
        self.back = self.backStart  # The method to return to the previous state from the current state.
        if depth == 1:  # The depth of the array
            self.state = self.start1  # Use the one dimensional array states
        else:
            self.state = self.start2  # Use the two dimensional array states

    def backspace(self):
        """ Delete the most recent input """
        if self.string == ' -> ':
            return  # Don't delete anything if you're at the start
        lastIndex = len(self.string) - 1  # Keep track of the end of the string
        lastChar = self.string[lastIndex]  # Keep track of the last character
        if lastChar != '[' and lastChar != ',' and lastChar != ' ' and lastChar != ']':
            # If the last character is a number, reduce the value
            self.currentValue = self.array[len(self.array) - 1]
            self.currentValue = int(self.currentValue / 10)
            self.array[len(self.array) - 1] = self.currentValue
            # Get rid of the value if it is 0
            if self.currentValue == 0:
                self.array.pop()
        # Update the string to be one character shorter
        self.string = self.string[0:lastIndex]
        # Return the last character so other methods can use it
        return lastChar

    def start1(self, value):
        """ State where nothing has been entered yet """
        try:
            # Only accept an opening bracket to update the input
            if str(value) == '[':
                self.string += str(value)
                self.state = self.s1_1
                self.back = self.back1_1
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def backStart(self):
        """ Simply return the current input as a string """
        return self.string

    def s1_1(self, value):
        """ State where only the opening bracket has been entered
        or some numbers and a comma has been entered """
        try:
            # Expect a closing bracket for an empty list or a number
            if str(value) == ']':
                self.string += str(value)
                self.isComplete1 = True
                self.state = self.complete
            elif 0 <= int(value) <= 9:
                self.currentValue = int(value)
                self.array.append(self.currentValue)
                self.string += str(value)
                self.state = self.s1_2
                self.back = self.back1_2
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def back1_1(self):
        """ Go back to previous state from state 1 """
        self.backspace()
        if len(self.string) == 4:
            self.state = self.start1
            self.back = self.backStart
        else:
            self.state = self.s1_2
            self.back = self.back1_2
        return self.string

    def s1_2(self, value):
        """ State where a number has just been entered """
        try:
            # Expect a comma to lead to the next number, a closing bracket to finish the array, or more numbers
            if str(value) == ',':
                self.string += str(value)
                self.state = self.s1_1
            elif str(value) == ']':
                self.string += str(value)
                self.isComplete1 = True
                self.state = self.complete
                self.back = self.back1Last
            elif 0 <= int(value) <= 9:
                while self.string[len(self.string) - 1] == '0' and (self.string[len(self.string) - 2] == '[' or
                                                                    self.string[len(self.string) - 2] == ','):
                    self.string = self.string[0:len(self.string) - 1]
                self.currentValue *= 10
                self.currentValue += int(value)
                self.array.pop()
                self.array.append(self.currentValue)
                self.string += str(value)
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def back1_2(self):
        """ Go back to previous state from state 2 """
        self.backspace()
        lastChar = self.string[len(self.string) - 1]
        if lastChar == ',' or lastChar == '[':
            self.state = self.s1_1
            self.back = self.back1_1
        return self.string

    def complete(self, _):
        """ State where the closing bracket has been typed in """
        return self.string

    def back1Last(self):
        """ Go back to previous state from the complete array state """
        self.backspace()
        self.state = self.s1_2
        self.back = self.back1_2
        self.isComplete1 = False
        return self.string

    def start2(self, value):
        """ State of 2D Array where nothing has been entered yet """
        try:
            # Only accept an opening bracket as input
            if str(value) == '[':
                self.string += str(value)
                self.state = self.s2_1
                self.back = self.back2_1
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def s2_1(self, value):
        """ State where nothing but the first opening bracket or
        the opening bracket and full 1D arrays have been entered """
        try:
            # Expect another opening bracket or the final closing bracket
            if str(value) == '[':
                self.string += str(value)
                self.state = self.s2_2
                self.back = self.back2_2
            elif str(value) == ']':
                self.string += str(value)
                self.isComplete2 = True
                self.state = self.complete
                self.back = self.back2Last
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def back2_1(self):
        """ Go back to previous state from state 2.1 """
        deletedChar = self.backspace()
        if self.string == ' -> ':
            self.state = self.start2
            self.back = self.backStart
        elif deletedChar == ',':
            self.state = self.s2_6
            self.back = self.back2_6
        return self.string

    def s2_2(self, value):
        """ State where two opening brackets have been entered """
        try:
            if 0 <= int(value) <= 9:
                self.currentValue = int(value)
                self.array.append(self.currentValue)
                self.string += str(value)
                self.state = self.s2_3
                self.back = self.back2_3
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def back2_2(self):
        """ Go back to previous state from state 2.2 """
        self.backspace()
        self.state = self.s2_1
        self.back = self.back2_1
        return self.string

    def s2_3(self, value):
        """ State where two opening brackets and a number have been entered """
        try:
            # Expect a comma or another number
            if str(value) == ',':
                self.string += str(value)
                self.state = self.s2_4
                self.back = self.back2_4
            elif 0 <= int(value) <= 9:
                while self.string[len(self.string) - 1] == '0' and (self.string[len(self.string) - 2] == '[' or
                                                                    self.string[len(self.string) - 2] == ','):
                    self.string = self.string[0:len(self.string) - 1]
                self.currentValue *= 10
                self.currentValue += int(value)
                self.array.pop()
                self.array.append(self.currentValue)
                self.string += str(value)
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def back2_3(self):
        """ Go back to previous state from state 2.3 """
        self.backspace()
        lastChar = self.string[len(self.string) - 1]
        if lastChar == '[':
            self.state = self.s2_2
            self.back = self.back2_2
        return self.string

    def s2_4(self, value):
        """ State where Two opening brackets and a comma have been entered"""
        try:
            # Only accept a number as input
            if 0 <= int(value) <= 9:
                self.currentValue = int(value)
                self.array.append(self.currentValue)
                self.string += str(value)
                self.state = self.s2_5
                self.back = self.back2_5
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def back2_4(self):
        """ Go back to previous state from state 2.4 """
        self.backspace()
        self.state = self.s2_3
        self.back = self.back2_3
        return self.string

    def s2_5(self, value):
        """ State where two opening brackets, a number, and a comma have been entered """
        try:
            # Expect a closing bracket or another number
            if str(value) == ']':
                self.array2D.append(self.array)
                self.array = []
                self.string += str(value)
                self.state = self.s2_6
                self.back = self.back2_6
            elif 0 <= int(value) <= 9:
                while self.string[len(self.string) - 1] == '0' and (self.string[len(self.string) - 2] == '[' or
                                                                    self.string[len(self.string) - 2] == ','):
                    self.string = self.string[0:len(self.string) - 1]
                self.currentValue *= 10
                self.currentValue += int(value)
                self.array.pop()
                self.array.append(self.currentValue)
                self.string += str(value)
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def back2_5(self):
        """ Go back to previous state from state 2.5 """
        self.backspace()
        lastChar = self.string[len(self.string) - 1]
        if lastChar == ',':
            self.currentValue = self.array[len(self.array) - 1]
            self.state = self.s2_4
            self.back = self.back2_4
        return self.string

    def s2_6(self, value):
        """ State where a single closing bracket has been entered """
        try:
            # Get ready to start the next 1D array with a comma, or finish out the 2D array with a closing bracket
            if str(value) == ',':
                self.string += str(value)
                self.state = self.s2_1
                self.back = self.back2_1
            elif str(value) == ']':
                self.string += str(value)
                self.isComplete2 = True
                self.state = self.complete
                self.back = self.back2Last
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def back2_6(self):
        """ Go back to previous state from state 2.6 """
        self.backspace()
        self.array = self.array2D.pop()
        self.state = self.s2_5
        self.back = self.back2_5
        return self.string

    def back2Last(self):
        """ Go back to previous state from state 2.complete """
        self.backspace()
        lastChar = self.string[len(self.string) - 1]
        if lastChar == '[':
            self.state = self.s2_1
            self.back = self.back2_1
        else:
            self.state = self.s2_6
            self.back = self.back2_6
        self.isComplete2 = False
        return self.string
