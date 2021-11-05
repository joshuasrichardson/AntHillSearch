class ArrayStateMachine:

    def __init__(self, depth):
        self.array = []
        self.array2D = []
        self.string = ' -> '
        self.currentValue = 0
        self.isComplete1 = False
        self.isComplete2 = False
        self.back = self.backStart
        if depth == 1:
            self.state = self.start1
        else:
            self.state = self.start2

    def backspace(self):
        if self.string == ' -> ':
            return
        lastIndex = len(self.string) - 1
        lastChar = self.string[lastIndex]
        if lastChar != '[' and lastChar != ',' and lastChar != ' ' and lastChar != ']':
            self.currentValue = self.array[len(self.array) - 1]
            self.currentValue = int(self.currentValue / 10)
            self.array[len(self.array) - 1] = self.currentValue
            if self.currentValue == 0:
                self.array.pop()
        self.string = self.string[0:lastIndex]
        return lastChar

    def start1(self, value):
        try:
            if str(value) == '[':
                self.string += str(value)
                self.state = self.s1_1
                self.back = self.back1_1
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def backStart(self):
        return self.string

    def s1_1(self, value):
        try:
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
        self.backspace()
        if len(self.string) == 4:
            self.state = self.start1
            self.back = self.backStart
        else:
            self.state = self.s1_2
            self.back = self.back1_2
        return self.string

    def s1_2(self, value):
        try:
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
        self.backspace()
        lastChar = self.string[len(self.string) - 1]
        if lastChar == ',' or lastChar == '[':
            self.state = self.s1_1
            self.back = self.back1_1
        return self.string

    def complete(self, value):
        return self.string

    def back1Last(self):
        self.backspace()
        self.state = self.s1_2
        self.back = self.back1_2
        self.isComplete1 = False
        return self.string

    def start2(self, value):
        try:
            if str(value) == '[':
                self.string += str(value)
                self.state = self.s2_1
                self.back = self.back2_1
        except ValueError:
            print("Invalid input was skipped.")
        return self.string

    def s2_1(self, value):
        try:
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
        deletedChar = self.backspace()
        if self.string == ' -> ':
            self.state = self.start2
            self.back = self.backStart
        elif deletedChar == ',':
            self.state = self.s2_6
            self.back = self.back2_6
        return self.string

    def s2_2(self, value):
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
        self.backspace()
        self.state = self.s2_1
        self.back = self.back2_1
        return self.string

    def s2_3(self, value):
        try:
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
        self.backspace()
        lastChar = self.string[len(self.string) - 1]
        if lastChar == '[':
            self.state = self.s2_2
            self.back = self.back2_2
        return self.string

    def s2_4(self, value):
        try:
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
        self.backspace()
        self.state = self.s2_3
        self.back = self.back2_3
        return self.string

    def s2_5(self, value):
        try:
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
        self.backspace()
        lastChar = self.string[len(self.string) - 1]
        if lastChar == ',':
            self.currentValue = self.array[len(self.array) - 1]
            self.state = self.s2_4
            self.back = self.back2_4
        return self.string

    def s2_6(self, value):
        try:
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
        self.backspace()
        self.array = self.array2D.pop()
        self.state = self.s2_5
        self.back = self.back2_5
        return self.string

    def back2Last(self):
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
