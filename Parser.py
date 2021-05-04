import pyperclip as pc

class AddressParser(object):
    def __init__(self, file=None):
        if file is not None:
            self.file = file
        self.split_address()

    def dump(self):
        print(self.name)
        print(self.address)
        if self.address2 is not None:
            print(self.address2)
        print(self.town)
        print(self.state)
        print(self.zip)

    def split_address(self):
        if self.file:
            with open(self.file, 'r') as f:
                # remove template at top of file
                addr = f.readlines()[7:]
        else:
            # get address from clipboard if no file
            addr = pc.paste().split('\n')

        split_address = [add.strip() for add in addr]
        split_address = [s.replace(',','').replace('.','') for s in split_address]

        name, address, *address2, townStateZip = split_address

        if address2:
            assert len(address2) == 1
            address2 = address2[0]

        town, state, zip_code = townStateZip.split()

        self.name = name
        self.address = address
        self.town = town
        self.state = state
        self.zip = zip_code
        if address2:
            self.address2 = address2
        else:
            self.address2 = None

if __name__ == '__main__':
    p = AddressParser('file.txt')
    p.dump()
