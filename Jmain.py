
import csv
import re
import os
import msvcrt

examples = []

os.system('cls')

class Contact:
    def __init__(self, firstN, lastN, phoneN, address = ""):
        self.firstName = firstN
        self.lastName = lastN
        self.phoneNumber = re.findall("\d", phoneN)
        self.address = address



    def toString(self) -> None:
        tempNum = list(self.phoneNumber)
        countryCode = ""
        while len(tempNum) > 10:
            countryCode += tempNum.pop(0)

        first = "".join(str(element) for element in tempNum[0:3])
        second = "".join(str(element) for element in tempNum[3:6])
        third = "".join(str(element) for element in tempNum[6:10])

        if(countryCode == ""):
            countryCode = "1"

        num = ("+" + countryCode + "(" + first + ") " + second + "-" + third)


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
tempList = []
for i in range(0, 10):
    tempList.append(contactList[i])

for i in range(0, 10):
    print(tempList[i].toString())






# Make sure that ANSI codes work
os.system('')

# We will move 1 line up and to the 32nd column





def input_search(list):
    os.system('cls')
    go_to_X2 = "\033[G"

    temp = "press enter when you find the contact your looking for: "
    choice = "".encode('ascii')

    while(choice != b'\r'):
        temp += choice.decode('ascii')
        print(temp)
        vert = 1
        for i in range(len(list)):
            print(list[i].toString())
            vert += 1
        hori = len(temp)
        go_to_X = f"\033[{vert}A" + f"\033[{hori}G"
        print(go_to_X, end="")

        # Read one character from STD input (getch = "Get char")
        # If you are on linux, then use getch.getch()
        choice = (msvcrt.getch())
        print(go_to_X2, end="")
    os.system('cls')

input_search(tempList)