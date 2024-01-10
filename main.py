import string
import csv
import re
import os
import msvcrt



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
            contactList.append(myVars['contact{}'.format(i + 1)])


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

    def insert(self, contact: Contact) -> None:
        self.__insertHelper(contact.firstName, contact)
        self.__insertHelper(contact.lastName, contact)
        self.__insertHelper(contact.phoneNumber, contact)

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
        results.append(self.__getChildren(current))
        return results

    def __getChildren(self, current: ContactNode) -> list:
        temp = []
        for node in current.children.values():
            if node.endWordNum:
                temp.append(node.contacts)
            if len(node.children) > 0:
                temp.append(self.__getChildren(node))
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
def input_search():
    os.system('cls')
    go_to_X2 = "\033[G"
    search = ""
    temp = "press enter when you find the contact your looking for: "
    choice = "".encode('ascii')

    while(choice != b'\r'):
        temp += choice.decode('ascii')
        search += choice.decode('ascii')

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
        os.system('cls')
        print(go_to_X2, end="")
    os.system('cls')


