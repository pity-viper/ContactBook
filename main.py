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
        self.children = {k:[] for k in string.ascii_lowercase}
        self.endWord = False
        self.endNode = False


class ContactBook:
    # Trie data structure
    def __init__(self):
        self.root = ContactNode()

    def insert(self, contact: Contact) -> None:
        pass

    def search(self, contact: Contact) -> None:
        pass

    def delete(self, contact: Contact) -> None:
        pass
