class Practice:
    def __init__(self):
        self.yeet = []

    def yeeter(self):
        print("1:" + str(self.yeet))
        self.addYeet(self.yeet)
        print("2:" + str(self.yeet))

    def addYeet(self, yeet):
        yeet.append("Yeet!")
        return yeet


def main():
    p = Practice()
    p.yeeter()


main()
