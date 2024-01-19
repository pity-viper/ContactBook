import string
import re
import csv


class Contact:
    """
    Stores a person's information as a Contact

    Attributes:
        firstName (string): the person's first name
        lastName (string): the person's last name, or null if unspecified
        phoneNumber (string): the person's phone number, or null if unspecified
        address: (string): the person's address, or null if unspecified
    """
    def __init__(self, firstN, lastN="null", phoneN="null", address="null"):
        self.firstName = firstN.lower()
        self.lastName = lastN.lower()
        if phoneN != "null":
            self.phoneNumber = re.findall("\d", phoneN)
        else:
            self.phoneNumber = phoneN
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
        if self.phoneNumber != "null":
            num = f"+{countryCode}({first}) {second}-{third}"
        else:
            num = self.phoneNumber

        fName = self.firstName.capitalize()
        lName = self.lastName.capitalize()
        if self.address == "":
            return f"{fName} {lName}, {num}"
        else:
            return f"{fName} {lName}, {num}, Address: {self.address}"


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
        if contact.lastName != "null":
            self.__insertHelper(contact.lastName, contact)
        if contact.phoneNumber != "null":
            self.__insertHelper(contact.phoneNumber, contact)
        if save:
            with open('contactExp.csv', 'w') as file:
                file.write(f"{contact.lastName}  {contact.firstName}, {contact.phoneNumber}, {contact.address}")
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
        if contact.lastName != "null":
            self.__deleteHelper(contact.lastName, contact)
        if contact.phoneNumber != "null":
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


def contactData() -> None:
    with open('contactsExp.csv', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for i, row in enumerate(reader):
            tempName = row[0].split("  ")
            tempFname = tempName[1]
            tempLname = tempName[0]
            """if tempLname == "null":
                tempLname = ""
                """
            myStr = 'contact{}'.format(i + 1)
            myVars = globals()
            myVars[myStr] = Contact(tempFname, tempLname, row[1], row[2])
            #contactList.append(myVars['contact{}'.format(i + 1)])
            CB.insert(myVars['contact{}'.format(i + 1)])


CB = ContactBook()
