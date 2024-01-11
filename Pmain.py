import string


class Contact:
    def __init__(self, firstN, lastN, phoneN, address = ""):
        self.firstName = firstN
        self.lastName = lastN
        self.phoneNumber = phoneN
        self.address = address

    def toString(self):
        if self.address == "":
            print(self.firstName + " " + self.lastName + ", " + self.phoneNumber)
        else:
            print(self.firstName + " " + self.lastName + ", " + self.phoneNumber + ", Address: " + self.address)


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
