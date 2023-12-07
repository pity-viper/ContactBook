import string


class Contact:
    def __init__(self, firstN, lastN, phoneN, address = ""):
        self.firstName = firstN
        self.lastName = lastN
        self.phoneNumber = phoneN
        self.address = address

    def toString(self):
        if self.address == "":
            print(self.firstName + self.lastName + ", " + self.phoneNumber)
        else:
            print(self.firstName + self.lastName + ", " + self.phoneNumber + ", Address: " + self.address)


class ContactNode:
    def __init__(self):
        #self.children = {k:None for k in string.ascii_lowercase}
        self.children = {}
        self.endWord = False
        self.endNode = False
        self.contacts = []


class ContactBook:
    # Trie data structure
    def __init__(self):
        self.root = ContactNode()

    def insert(self, contact: Contact) -> None:
        current = self.root
        self._insertName(current, contact.firstName)
        self._insertName(current, contact.lastName)
        self._insertPhoneNumber(current, contact.phoneNumber)

    def _insertName(self, current: ContactNode, name: string) -> None:
        for letter in name:
            if not current.children.get(letter):
                current.children[letter] = ContactNode()
            current = current.children[letter]
        current.endWord = True
        current.endNode = True
        # need to add the contact to contacts list in node

    def _insertPhoneNumber(self, current: ContactNode, phoneNumber: string) -> None:
        pass
    def search(self, contact: Contact) -> list:
        pass

    def delete(self, contact: Contact) -> None:
        pass
