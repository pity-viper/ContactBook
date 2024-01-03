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
    def __init__(self):
        #self.children = {k:None for k in string.ascii_lowercase}
        self.children = {}
        self.endWordNum = False
        self.leafNode = False
        #self.endNumber = False
        self.contacts = []


class ContactBook:
    # Trie data structure
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
        pass

    def getContacts(self) -> list:
        pass
        # like a toString method, but instead iterates through the trie to get all the contacts
