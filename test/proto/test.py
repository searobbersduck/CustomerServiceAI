import message_pb2

print('begin proto test\n')

person = message_pb2.Person()
print(person.IsInitialized())
person.id = 1234
person.name = 'john'
person.email = 'john@gmail.com'
phone = person.phones.add()
phone.number = '1232341324'
phone.type = message_pb2.Person.HOME

print(person.IsInitialized())

print(person.__str__())

addressbook = message_pb2.AddressBook()
person1 = addressbook.people.add()
person1.CopyFrom(person)

print('====> addressbook: ')
print(addressbook)

with open('addressbook', 'wb') as f:
    f.write(addressbook.SerializeToString())

addressbook1 = message_pb2.AddressBook()
with open('addressbook', 'rb') as f:
    addressbook1.ParseFromString(f.read())

print('====> addressbook1: ')
print(addressbook1)