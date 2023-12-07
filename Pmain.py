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
        self.endWord = False
        self.leafNode = False
        self.endNumber = False
        self.contacts = []


class ContactBook:
    # Trie data structure
    def __init__(self):
        self.root = ContactNode()

    def insert(self, contact: Contact) -> None:
        self.__insertName(contact.firstName)
        self.__insertName(contact.lastName)
        self.__insertPhoneNumber(contact.phoneNumber)

    def __insertName(self, name: string) -> None:
        current = self.root
        for letter in name:
            if not current.children.get(letter):
                current.children[letter] = ContactNode()
            current = current.children[letter]
        current.endWord = True
        current.leafNode = True # add logic to flip this off if another node is added after it
        # need to add the contact to contacts list in node

    def __insertPhoneNumber(self, phoneNumber: string) -> None:
        current = self.root
        for number in phoneNumber:
            if not current.children.get(number):
                current.children[number] = ContactNode()
            current = current.children[number]
        current.endNumber = True
        current.leafNode = True
        # need to add the contact to the contacts list in node
        # need to make sure that this doesn't conflict with the name trie. Either have 2 tries or all in one somehow

    def search(self, contact: Contact) -> list:
        pass

    def delete(self, contact: Contact) -> None:
        pass

    def getContacts(self) -> list:
        pass
        # like a toString method, but instead iterates through the trie to get all the contacts
