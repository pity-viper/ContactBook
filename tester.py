from Pmain import Contact

choice = input("What do you want to test?:\n")
if choice == "Contact-1":
    fullContact = Contact("John", "Smith", "123456789", "12345 Main Street")
    print("Contact with first name, last name, phone number, and address:")
    print(fullContact.toString())
if choice == "Contact-2":
    nameOnlyContact = Contact("John", "Smith")
    print("Contact with first name and last name:")
    print(nameOnlyContact.toString())
if choice == "Contact-3":
    firstNameOnlyContact = Contact("John")
    print("Contact with first name:")
    print(firstNameOnlyContact.toString())


