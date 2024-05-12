import string
import csv
import re
import os
import msvcrt
import time
from csv import writer
import pandas as pd


class Contact:
    """
    Stores data for a contact

    Attributes:
        firstName (string): the first name for a person's contact. Required.
        lastName (string): the last name for a person's contact
        phoneNumber (string): the phone number for a person's contact
        address (string): the address for a person's contact
    """
    def __init__(self, firstN, lastN="null", phoneN="null", address="null"):
        self.firstName = firstN.lower()
        self.lastName = lastN.lower()
        if phoneN != "null":
            self.phoneNumber = re.findall("\d", phoneN)
        else:
            self.phoneNumber = phoneN
        self.address = address

    def toString(self) -> str:
        """
        Displays the contact object depending on the information given to the object

        Returns:
            String: returns a string containing all the information stored in the object's attributes
        """
        if self.phoneNumber != "null":
            tempNum = list(self.phoneNumber)
            countryCode = ""
            while len(tempNum) > 10:
                countryCode += tempNum.pop(0)

            first = "".join(str(element) for element in tempNum[0:3])
            second = "".join(str(element) for element in tempNum[3:6])
            third = "".join(str(element) for element in tempNum[6:10])

            if countryCode == "":
                countryCode = "1"
            num = f"+{countryCode}({first}) {second}-{third}"
        else:
            num = self.phoneNumber

        fName = self.firstName.capitalize()
        lName = self.lastName.capitalize()

        if fName == 'null':
            fName = ''

        if lName == 'null':
            lName = ''
            fName += ","
        else:
            lName += ","

        if num == 'null':
            num = ''

        if self.address == 'null':
            address = ''
        else:
            address = self.address
            if num != 'null':
                num += ","

        return f"{fName} {lName} {num} {address}"


maxLen = 0


def contactData() -> None:
    """
    Pulls information stored in the ContactsExp csv file, turns each row into a Contact object,
    and inserts the object into the trie
    """
    global maxLen
    with open('contactsExp.csv', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        header = next(reader)
        for i, row in enumerate(reader):
            tempName = row[0].split("  ")
            tempFname = tempName[1]
            tempLname = tempName[0]
            myStr = 'contact{}'.format(i + 1)
            myVars = globals()
            myVars[myStr] = Contact(tempFname, tempLname, row[1], row[2])
            CB.insert(myVars['contact{}'.format(i + 1)], False)
            if len(myVars['contact{}'.format(i + 1)].toString()) > maxLen:
                maxLen = len(myVars['contact{}'.format(i + 1)].toString())


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
        """
        Inserts given Contact into the prefix tree, and the csv file when specified

        Args:
             contact (Contact): contact to insert into the prefix tree
             save (bool): if True then add to csv file, if False do not
        """
        self.__insertHelper(contact.firstName, contact)
        if contact.lastName != "null":
            self.__insertHelper(contact.lastName, contact)
        if contact.phoneNumber != "null":
            self.__insertHelper(contact.phoneNumber, contact)
        if save:
            tempList = [f"{contact.lastName.capitalize()}  {contact.firstName.capitalize()}", ''.join(contact.phoneNumber), contact.address]
            with open('contactsExp.csv', 'a') as f_object:
                writer_object = writer(f_object, delimiter=",", quotechar="\"", quoting=csv.QUOTE_MINIMAL, lineterminator="\r")
                writer_object.writerow(tempList)
                f_object.close()

    def __insertHelper(self, wordNum: string, contact: Contact) -> None:
        """
        Helper function for inserting contacts into the prefix tree

        Args:
            wordNum (string): the name or phone number to insert into the prefix tree
            contact (Contact): contact to insert into the prefix tree
        """
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
        """
        Searches for a contact in the prefix tree

        Args:
            wordNum (string): the name or phone number to search for

        Returns:
            list: all Contacts that match the given prefix
        """
        results = []
        current = self.root
        for char in wordNum:
            if not current.children.get(char):
                break
            current = current.children[char]
        results.extend(self.__getChildren(current))
        return results

    def __getChildren(self, current: ContactNode) -> list:
        """
        Returns all contacts contained in the child nodes of the given node

        Args:
            current (ContactNode): the node to get all child nodes of

        Returns:
            list: list of Contacts which are stored in the child nodes of the current node
        """
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
        """
        Delete the given contact from the prefix tree and csv file

        Args:
            contact (Contact): the contact to delete
        """
        self.__deleteHelper(contact.firstName, contact)
        if contact.lastName != "null":
            self.__deleteHelper(contact.lastName, contact)
        if contact.phoneNumber != "null":
            self.__deleteHelper(contact.phoneNumber, contact)
        data = pd.read_csv("contactsExp.csv", header=None, names=["Name", "Phone Number", "Address"], sep=",")
        contactName = f"{contact.lastName.capitalize()}  {contact.firstName.capitalize()}"
        contactPhone = "".join(contact.phoneNumber)
        data = data.query("`Name` != @contactName and `Phone Number` != @contactPhone and `Address` != @contact.address")
        data.to_csv("contactsExp.csv", index=False, header=False)

    def __deleteHelper(self, wordNum: string, contact: Contact) -> None:
        """
        Helper method for delete

        Args:
            wordNum (string): the name or phone number to delete from the prefix tree
            contact (Contact): the contact to remove from the prefix tree
        """
        current = self.root
        for char in wordNum:
            if not current.children.get(char):
                break
            current = current.children[char]
        if current.endWordNum:
            current.contacts.remove(contact)

    def getContacts(self) -> list:
        """
        Get all the contacts in the prefix tree

        Returns:
            list: a list of all Contacts contained in the prefix tree
        """
        return self.__getChildren(self.root)


os.system('')


def inputSearch():
    """
    Text based GUI that takes in user search terms and outputs results in real time
    """
    os.system('cls')
    go_to_X2 = "\033[G"
    user = "".encode('ascii')
    userSearch = ''
    while user != b'\r':
        os.system('cls')
        results = CB.search(userSearch)

        go_to_X = f"\033[{len(results) + 3}A" + f"\033[{len(userSearch) + 3}G"
        borderSpacing = ''
        space1 = ''
        space2 = ''
        searchSpace = ''
        resultSpace = ''
        for i in range(maxLen):
            borderSpacing += '═'

        if maxLen % 2 != 0:
            space2 += ' '
        for i in range(int((maxLen - 48)/2)):
            space1 += ' '
            space2 += ' '

        for i in range(maxLen - len(userSearch)):
            searchSpace += ' '

        print(f"╒═{borderSpacing}═╕\n"
            + f"│ {space1}Input Search (press enter when contact is found){space2} │\n"
            + f"╞═{borderSpacing}═╡\n"
            + f"│ {userSearch}{searchSpace} │\n"
            + f"╞═{borderSpacing}═╡")
        for contact in results:
            resultSpace = ""
            if len(contact.toString()) < maxLen:
                for i in range(maxLen - len(contact.toString())):
                    resultSpace += ' '
            print('│ ' + contact.toString() + f'{resultSpace} │' )

        print(f"╘═{borderSpacing}═╛" + go_to_X, end='')
        print()
        user = (msvcrt.getch())

        if user == b'\x08':
            userSearch = userSearch[:-1]
        else:
            userSearch += user.decode('ascii')

    os.system('cls')


def inputDelete():
    """
    Using the same methodology as the search method, this program allows the user to delete a contact
    """
    global maxLen
    os.system('cls')
    go_to_X2 = "\033[G"
    user = "".encode('ascii')
    userSearch = ''
    while user != b'\r':
        os.system('cls')
        results = CB.search(userSearch)
        length = len(userSearch) + 3
        go_to_X = f"\033[{len(results) + 3}A" + f"\033[{length}G"
        borderSpacing = ''
        space1 = ''
        space2 = ''
        searchSpace = ''
        resultSpace = ''
        for i in range(maxLen):
            borderSpacing += '═'

        if maxLen % 2 != 0:
            space2 += ' '
        for i in range(int((maxLen - 54)/2)):
            space1 += ' '
            space2 += ' '

        for i in range(maxLen - len(userSearch)):
            searchSpace += ' '

        print(f"╒═{borderSpacing}═╕\n"
            + f"│ {space1}Search for Contact (press enter when contact is found){space2} │\n"
            + f"╞═{borderSpacing}═╡\n"
            + f"│ {userSearch}{searchSpace} │\n"
            + f"╞═{borderSpacing}═╡")
        for contact in results:
            resultSpace = ""
            if len(contact.toString()) < maxLen:
                for i in range(maxLen - len(contact.toString())):
                    resultSpace += ' '
            print('│ ' + contact.toString() + f'{resultSpace} │' )

        print(f"╘═{borderSpacing}═╛" + go_to_X, end='')
        print()
        user = (msvcrt.getch())

        if user == b'\x08':
            userSearch = userSearch[:-1]
        else:
            userSearch += user.decode('ascii')

    maxLen += 4
    os.system('cls')
    user = b'X'
    space1 = ''
    space2 = ''
    borderSpacing = ''
    searchSpace = ''

    for i in range(maxLen):
        borderSpacing += '═'

    for i in range(int((maxLen - 43) / 2)):
        space1 += ' '
        space2 += ' '
    for i in range((maxLen - 31) + 2):
        searchSpace += ' '

    borderSpacing2 = borderSpacing
    borderSpacing2 = borderSpacing2[:-3]
    while user == b'X':

        print(f"╒═{borderSpacing}═╕\n"
            + f"│ {space1}Select the contact you would like to delete {space2} │\n"
            + f"╞═{borderSpacing2}╤═══╡\n"
            + f"│ Enter your choice here -->{searchSpace}│ {user.decode('ascii')} │\n"
            + f"╞═{borderSpacing2}╧═══╡")


        for i, contact in enumerate(results):
            resultSpace = ""
            if len(contact.toString()) < maxLen:
                for j in range(maxLen - (len(contact.toString()) + 4)):
                    resultSpace += ' '
            print(f'│ ({i}) ' + contact.toString() + f'{resultSpace} │')
        print(f"╘═{borderSpacing}═╛" + go_to_X, end='')
        print()
        user = (msvcrt.getch())
        #try:
        CB.delete(results[int(user.decode('ascii'))])
        #except:
            #user = b'X'

    os.system('cls')
    print("╒═══════════════════════════════════════╕\n"
        + "│               Deleted                 │\n"
        + "╘═══════════════════════════════════════╛")
    time.sleep(2)

    os.system('cls')


def userInput():
    """
    GUI for the input of a contact
    """
    global maxLen
    user = b'X'
    FIRSTNAME = "null"
    LASTNAME = "null"
    PHONENUMBER = "null"
    ADDRESS = "null"
    
    while user != b'5':
        go_to_X = "\033[A" + "\033[74G"
        go_to_X2 = "\033[6A \033[G"

        print("╒══════════════════════════════════════════════════════════════════════════╕\n"
            + "│                                   Insert                                 │\n"
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

        if user == b'3':
            PHONENUMBER = phoneNumber()

        if user == b'4':
            ADDRESS = inputAddress()

    os.system('cls')

    #initializing all varibles needed for the confirmation code
    tempContact = Contact(FIRSTNAME, LASTNAME, PHONENUMBER, ADDRESS)
    length = len(tempContact.toString())
    spaceBorder = '═'
    spaceBorder2 = '═'
    spaceBorder3 = '═'
    spaces = ' '
    spaces2 = ' '
    spaces3 = ' '
    contactSpacing = ' '
    vert = 74

    # Testing for the length of the printed comment
    if length >= 73:
        vert = length + 2
        diff = length - 74
        for i in range(diff):
            spaceBorder += '═'
            spaces3 += ' '

        if diff % 2 == 0:
            diff = int(diff/2)
        else:
            diff = int(diff/2)
            spaces2 += ' '
            spaceBorder3 += '═'

        for i in range(diff):
            spaces += ' '
            spaces2 += ' '
            spaceBorder2 += '═'
            spaceBorder3 += '═'

        # Spacing was off a little bit, the code below fixes that
        spaceBorder += '══'
        spaceBorder2 += '═'
        spaceBorder3 += '═'
        spaces += ' '
        spaces2 += ' '
        spaces3 += '  '
    else:
        diff = 72 - length
        for i in range(diff):
            contactSpacing += ' '
    user2 = b'X'
    while user2 != b'1':
        go_to_X = f"\033[A" + f"\033[{vert}G"
        go_to_X2 = "\033[6A \033[G"

        print(f"╒══{spaceBorder}═══════════════════════════════════════════════════════════════════════╕\n"
            + f"│          {spaces}                 Confirm the contact     {spaces2}                     │\n"
             +f"╞══{spaceBorder}═══════════════════════════════════════════════════════════════════════╡\n"
             +f"│ {tempContact.toString()}{contactSpacing}│\n"
            + f"╞══{spaceBorder2}════════════════════════════════════╤══{spaceBorder3}═══════════════════════════════╡\n"
            + f"│1 - Yes {spaces}                              │ 2 - No {spaces2}                         │\n"
            + f"╞══{spaceBorder2}════════════════════════════════════╧══{spaceBorder3}═══════════════════════════╤═══╡\n"
            + f"│ Enter your choice here --> {spaces3}                                         │ {user2.decode('ascii')} │\n"
            + f"╘══{spaceBorder}═══════════════════════════════════════════════════════════════════╧═══╛" + go_to_X, end="")

        user2 = (msvcrt.getche())
        print(go_to_X2, end="")
        if user2 == b'2':
            break
        if user2 == b'1':
            # Saves the inserted contact
            if len(tempContact.toString()) > maxLen:
                maxLen = len(tempContact)
            CB.insert(tempContact, True)
    os.system('cls')


def firstName():
    """
    Takes user input for a new contact's first name.

    returns:
        String: The contact's first name
    """
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
    """
    Takes user input for a new contact's last name.

    returns:
        String: The contact's last name
    """
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


def phoneNumber():
    """
    Takes user input for a new contact's phone number.

    returns:
        String: The contact's phone number
    """
    os.system('cls')
    hori = 3
    number = ''
    choice = b''
    spacing = "                                                 "
    while choice != b'\r':
        go_to_X = "\033[A" + f"\033[{hori}G"
        go_to_X2 = "\033[6A \033[G"
        if choice == b'\x08':
            number = number[:-1]
            spacing += " "
            hori -= 1
        else:
            number += choice.decode('ascii')
            spacing = spacing[:-1]
            hori += 1

        print("╒══════════════════════════════════════════════════╕\n"
            + "│               Input Phone Number                 │\n"
            + "╞══════════════════════════════════════════════════╡\n"
           + f"│ {number} {spacing}│\n"
            + "╘══════════════════════════════════════════════════╛" + go_to_X, end="")
        choice = (msvcrt.getche())
        print(go_to_X2, end="")
    return number


def inputAddress():
    """
    Takes user input for a new contact's address.

    returns:
        String: The contact's address
    """
    os.system('cls')
    hori = 3
    address = ''
    choice = b''
    spacing = "                                                 "
    while choice != b'\r':
        go_to_X = "\033[A" + f"\033[{hori}G"
        go_to_X2 = "\033[6A \033[G"
        if choice == b'\x08':
            address = address[:-1]
            spacing += " "
            hori -= 1
        else:
            address += choice.decode('ascii')
            spacing = spacing[:-1]
            hori += 1

        print("╒══════════════════════════════════════════════════╕\n"
            + "│               Input Address                      │\n"
            + "╞══════════════════════════════════════════════════╡\n"
           + f"│ {address} {spacing}│\n"
            + "╘══════════════════════════════════════════════════╛" + go_to_X, end="")
        choice = (msvcrt.getche())
        print(go_to_X2, end="")
    return address


def main():
    """
    Calls all the other methods. It contains the main menu.
    """
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

        if user == b'2':
            inputDelete()
            os.system('cls')

        if user == b'3':
            inputSearch()
            os.system('cls')


CB = ContactBook()
contactData()
main()
os.system('cls')
