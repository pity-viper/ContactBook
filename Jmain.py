
import csv
import re

examples = []



class Contact:
    def __init__(self, firstN, lastN, phoneN, address = ""):
        self.firstName = firstN
        self.lastName = lastN
        self.phoneNumber = self.processNum(phoneN)
        self.address = address

    def processNum(self, number):
        return re.findall("\d", txt)

    def toString(self) -> None:
        tempNum = list(self.phoneNumber)
        countryCode = ""
        while len(tempNum) > 10:
            countryCode += num.pop(0)

        first = "".join(str(element) for element in tempNum[0:3])
        second = "".join(str(element) for element in tempNum[3:6])
        third = "".join(str(element) for element in tempNum[6:10])

        num = ("+" + countryCode + " (" + first + ") " + second + "-" + third)


        if self.address == "":
            return (self.firstName + " " + self.lastName + ", " + num)
        else:
            return (self.firstName + " " + self.lastName + ", " + num + ", Address: " + self.address)


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
