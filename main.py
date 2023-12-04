class contact:
    def __init__(self, firstN, lastN, phoneN, addres = ""):
        self.firstName = firstN
        self.lastName = lastN
        self.phoneNumber = phoneN
        self.address = addres

    def toString(self):
        if self.address == "":
            print(self.firstName + self.lastName + ", " + self.phoneNumber)
        else:
            print(self.firstName + self.lastName + ", " + self.phoneNumber + ", Address: " + self.address)

class contactBook:
    def __init__