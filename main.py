import string
import csv
import re
import os
import msvcrt



class Contact:
    def __init__(self, firstN, lastN, phoneN, address = ""):
        self.firstName = firstN.lower()
        self.lastName = lastN.lower()
        self.phoneNumber = re.findall("\d", phoneN)
        self.address = address



    def toString(self) -> string:
        tempNum = list(self.phoneNumber)
        countryCode = ""
        while len(tempNum) > 10:
            countryCode += tempNum.pop(0)

        first = "".join(str(element) for element in tempNum[0:3])
        second = "".join(str(element) for element in tempNum[3:6])
        third = "".join(str(element) for element in tempNum[6:10])

        if(countryCode == ""):
            countryCode = "1"

        #num = ("+" + countryCode + "(" + first + ") " + second + "-" + third)
        num = f"+{countryCode}({first}) {second}-{third}"

        fName = self.firstName.capitalize()
        lName = self.lastName.capitalize()
        if self.address == "":
            #return (self.firstName + " " + self.lastName + ", " + num)
            return f"{fName} {lName}, {num}"
        else:
            #return (self.firstName + " " + self.lastName + ", " + num + ", Address: " + self.address)
            return f"{fName} {lName}, {num}, Address: {self.address}"


contactList = []
def contactData() -> None:
    with open('contactsExp.csv', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for i, row in enumerate(reader):
            tempName = row[0].split("  ")
            tempFname = tempName[1]
            tempLname = tempName[0]
            if tempLname == "null":
                tempLname = ""
            myStr = 'contact{}'.format(i + 1)
            myVars = globals()
            myVars[myStr] = Contact(tempFname, tempLname, row[1], row[2])
            #contactList.append(myVars['contact{}'.format(i + 1)])
            CB.insert(myVars['contact{}'.format(i + 1)])


class ContactNode:
    """
    Node object in a prefix tree

    Attributes:
        children (dict): maps letters to a list of ContactNodes
        endWordNum (bool): if this node is the end of a word or phone number
        leafNode (bool): if this is the last node in the chain
        contacts (list): all Contacts associated with this node
    """
    def __init__(self):
        self.children = {}
        self.endWordNum = False
        self.leafNode = False
        self.contacts = []


class ContactBook:
    """
    Prefix Tree data structure that stores Contacts using ContactNodes

    Attributes:
        root (ContactNode): the root node of the prefix tree
    """
    def __init__(self):
        self.root = ContactNode()

    def insert(self, contact: Contact, save: bool) -> None:
        self.__insertHelper(contact.firstName, contact)
        self.__insertHelper(contact.lastName, contact)
        self.__insertHelper(contact.phoneNumber, contact)
        if save:
            if contact.lastName == "":
                lName = "null"
            else:
                lName = contact.lastName
            with open('contactExp.csv', 'w') as file:
                file.write(f"{lName}  {contact.firstName}, {contact.phoneNumber}, {contact.address}")
                file.write('n')

    def __insertHelper(self, wordNum: string, contact: Contact) -> None:
        current = self.root
        for char in wordNum:
            if not current.children.get(char):
                current.children[char] = ContactNode()
                if current.leafNode:
                    current.leafNode = False
            current = current.children[char]
        current.endWordNum = True
        current.leafNode = True
        current.contacts.append(contact)

    def search(self, wordNum: string) -> list:
        results = []
        current = self.root
        for char in wordNum:
            if not current.children.get(char):
                break
            current = current.children[char]
        results.extend(self.__getChildren(current))
        return results

    def __getChildren(self, current: ContactNode) -> list:
        temp = []
        if current.endWordNum:
            temp.extend(current.contacts)
        for node in current.children.values():
            if node.endWordNum:
                temp.extend(node.contacts)
            if len(node.children) > 0:
                temp.extend(self.__getChildren(node))
        return temp

    def delete(self, contact: Contact) -> None:
        self.__deleteHelper(contact.firstName, contact)
        self.__deleteHelper(contact.lastName, contact)
        self.__deleteHelper(contact.phoneNumber, contact)

    def __deleteHelper(self, wordNum: string, contact: Contact) -> None:
        current = self.root
        for char in wordNum:
            if not current.children.get(char):
                break
            current = current.children[char]
        if current.endWordNum:
            current.contacts.remove(contact)

    def getContacts(self) -> list:
        return self.__getChildren(self.root)


os.system('')


def inputSearch():
    os.system('cls')
    go_to_X2 = "\033[G"
    userSearch = ""
    temp = "press enter when you find the contact your looking for: "
    choice = "".encode('ascii')

    while(choice != b'\r'):
        if choice == b'\x08':
            temp = temp[:-1]
            userSearch = userSearch[:-1]
        else:
            temp += choice.decode('ascii')
            userSearch += choice.decode('ascii')
        results = CB.search(userSearch)
        print(temp)
        hori = len(temp)
        vert = 1
        print(type(results))
        for contact in results:
            #print(type(contact))
            #print(contact)
            print(contact.toString())
            vert += 1
        go_to_X = f"\033[{vert}A" + f"\033[{hori}G"
        print(go_to_X, end="")

        # Read one character from STD input (getch = "Get char")
        # If you are on linux, then use getch.getch()
        choice = (msvcrt.getch())
        os.system('cls')
        print(go_to_X2, end="")
    os.system('cls')

def userInput():
    user = b'X'
    FIRSTNAME = ""
    LASTNAME = ""
    PHONENUMBER = ""
    ADDRESS = ""
    while user != b'5':
        go_to_X = f"\033[A" + f"\033[74G"
        go_to_X2 = "\033[6A \033[G"

        print("╒══════════════════════════════════════════════════════════════════════════╕\n"
            + "│                                     Insert                               │\n"
            + "╞══════════════╤═══════════════╤══════════════════╤═════════════╤══════════╡\n"
            + "│1 - First Name│ 2 - Last Name │ 3 - Phone Number │ 4 - Address │ 5 - Exit │\n"
            + "╞══════════════╧═══════════════╧══════════════════╧═════════════╧══════╤═══╡\n"
           + f"│ Enter your choice here -->                                           │ {user.decode('ascii')} │\n"
            + "╘══════════════════════════════════════════════════════════════════════╧═══╛" + go_to_X, end="")

        user = (msvcrt.getche())
        print(go_to_X2, end="")

        if user == b'1':
            FIRSTNAME = firstName()

        if user == b'2':
            LASTNAME = lastName()


def firstName():
    os.system('cls')
    hori = 3
    name = ''
    choice = b''
    spacing = "                                              "
    while choice != b'\r':
        go_to_X = "\033[A" + f"\033[{hori}G"
        go_to_X2 = "\033[6A \033[G"
        if choice == b'\x08':
            name = name[:-1]
            spacing += " "
            hori -= 1
        else:
            name += choice.decode('ascii')
            spacing = spacing[:-1]
            hori += 1

        print("╒═══════════════════════════════════════════════╕\n"
            + "│               Input First Name                │\n"
            + "╞═══════════════════════════════════════════════╡\n"
           + f"│ {name} {spacing}│\n"
            + "╘═══════════════════════════════════════════════╛" + go_to_X, end="")
        choice = (msvcrt.getche())
        print(go_to_X2, end="")
        return name

def lastName():
    os.system('cls')
    hori = 3
    name = ''
    choice = b''
    spacing = "                                              "
    while choice != b'\r':
        go_to_X = "\033[A" + f"\033[{hori}G"
        go_to_X2 = "\033[6A \033[G"
        if choice == b'\x08':
            name = name[:-1]
            spacing += " "
            hori -= 1
        else:
            name += choice.decode('ascii')
            spacing = spacing[:-1]
            hori += 1

        print("╒═══════════════════════════════════════════════╕\n"
            + "│               Input Last Name                 │\n"
            + "╞═══════════════════════════════════════════════╡\n"
           + f"│ {name} {spacing}│\n"
            + "╘═══════════════════════════════════════════════╛" + go_to_X, end="")
        choice = (msvcrt.getche())
        print(go_to_X2, end="")
        return name


def main():
    os.system('cls')
    user = b'X'
    while user != b'4':
        go_to_X = "\033[F" + "\033[47G"
        go_to_X2 = "\033[5A \033[G"

        print("╒══════════╤════════════╤════════════╤══════════╕\n"
            + "│1 - Insert│ 2 - Delete │ 3 - Search │ 4 - Exit │\n"
            + "╞══════════╧════════════╧════════════╧══════╤═══╡\n"
           + f"│ Enter your choice here -->                │ {user.decode('ascii')} │\n"
            + "╘═══════════════════════════════════════════╧═══╛" + go_to_X, end="")
        user =  msvcrt.getche()
        print(go_to_X2, end='')

        if user == b'1':
            userInput()
            os.system('cls')

CB = ContactBook()
main()
