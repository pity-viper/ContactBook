import csv

examples = []

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


def contactData() -> None:
    with open('contactsExp.csv', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for i, row in enumerate(reader):
            tempName = row[0].split("  ")
            tempFname = tempName[1]
            tempLname = tempName[0]
            curr = 'contact{}'.format(i+1)
            locals()[curr] = Contact(tempFname, tempLname, row[1], row[2])
            print(curr.toString())


class ContactBook:
    def __init__(self):
        self.root = self.getNode()

    def getNode(self):
        return ContactNode()



class ContactNode:
    def __init__(self):
        pass

contactData()
