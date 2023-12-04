class Contact:
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

class ContactBook:
    def __init__(self):
        self.root = self.getNode()

    def getNode(self):
        return ContactNode()



class ContactNode:
    def __init__(self):
        pass