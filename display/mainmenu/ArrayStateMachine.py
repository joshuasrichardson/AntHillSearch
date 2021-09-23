class ArrayStateMachine:

    def __init__(self, depth):
        self.array = []
        self.array2D = []
        self.string = ' -> '
        self.currentValue = 0
        self.isComplete1 = False
        self.isComplete2 = False
        if depth == 1:
            self.state = self.start1
        else:
            self.state = self.start2

    def start1(self, value):
        try:
            if str(value) == '[':
                self.string += str(value)
                self.state = self.s1_1
            elif str(value) == ' ':
                self.string += str(value)
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def s1_1(self, value):
        try:
            if str(value) == ' ':
                self.string += str(value)
            elif str(value) == ']':
                self.string += str(value)
                self.isComplete1 = True
                self.state = self.complete
            elif 0 <= int(value) <= 9:
                self.currentValue = int(value)
                self.string += str(value)
                self.state = self.s1_2
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def s1_2(self, value):
        try:
            if str(value) == ',':
                self.array.append(self.currentValue)
                self.string += str(value)
                self.state = self.s1_1
            elif str(value) == ' ':
                self.string += str(value)
            elif str(value) == ']':
                self.array.append(self.currentValue)
                self.string += str(value)
                self.isComplete1 = True
                self.state = self.complete
            elif 0 <= int(value) <= 9:
                self.currentValue *= 10
                self.currentValue += int(value)
                self.string += str(value)
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def complete(self, value):
        return self.string

    def start2(self, value):
        try:
            if str(value) == '[':
                self.string += str(value)
                self.state = self.s2_1
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def s2_1(self, value):
        try:
            if str(value) == '[':
                self.string += str(value)
                self.state = self.s2_2
            elif str(value) == ']':
                self.string += str(value)
                self.isComplete2 = True
                self.state = self.complete
            elif str(value) == ' ':
                self.string += str(value)
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def s2_2(self, value):
        try:
            if str(value) == ' ':
                self.string += str(value)
            elif 0 <= int(value) <= 9:
                self.currentValue = int(value)
                self.string += str(value)
                self.state = self.s2_3
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def s2_3(self, value):
        try:
            if str(value) == ',':
                self.array.append(self.currentValue)
                self.string += str(value)
                self.state = self.s2_4
            elif str(value) == ' ':
                self.string += str(value)
            elif 0 <= int(value) <= 9:
                self.currentValue *= 10
                self.currentValue += int(value)
                self.string += str(value)
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def s2_4(self, value):
        try:
            if str(value) == ' ':
                self.string += str(value)
            elif 0 <= int(value) <= 9:
                self.currentValue = int(value)
                self.string += str(value)
                self.state = self.s2_5
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def s2_5(self, value):
        try:
            if str(value) == ' ':
                self.string += str(value)
            elif str(value) == ']':
                self.array.append(self.currentValue)
                self.array2D.append(self.array)
                self.array = []
                self.string += str(value)
                self.state = self.s2_6
            elif 0 <= int(value) <= 9:
                self.currentValue *= 10
                self.currentValue += int(value)
                self.string += str(value)
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def s2_6(self, value):
        try:
            if str(value) == ',':
                self.string += str(value)
                self.state = self.s2_1
            elif str(value) == ' ':
                self.string += str(value)
            elif str(value) == ']':
                self.string += str(value)
                self.isComplete2 = True
                self.state = self.complete
        except ValueError:
            print("Invalid input was skipped.")
        return self.string
