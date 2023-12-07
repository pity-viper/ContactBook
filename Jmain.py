
import csv

examples = []



class Contact:
    def __init__(self, firstN, lastN, phoneN, address = ""):
        self.firstName = firstN
        self.lastName = lastN
        self.phoneNumber = phoneN
        self.address = address

    def toString(self) -> None:
        if self.address == "":
            return (self.firstName + " " + self.lastName + ", " + self.phoneNumber)
        else:
            return (self.firstName + " " + self.lastName + ", " + self.phoneNumber + ", Address: " + self.address)


contactList = []
def contactData() -> None:
    with open('contactsExp.csv', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for i, row in enumerate(reader):
            tempName = row[0].split("  ")
            tempFname = tempName[1]
            tempLname = tempName[0]
            myStr = 'contact{}'.format(i + 1)
            myVars = globals()
            myVars[myStr] = Contact(tempFname, tempLname, row[1], row[2])
            contactList.append(myVars['contact{}'.format(i+1)])

contactData()
for i in range(len(contactList)):
    print(contactList[i].toString())
print(len(contactList))

print(contact2.toString())
