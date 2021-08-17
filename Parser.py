import pyperclip

class AddressParser():
    def __init__(self, file=None):

        if file:
            self.file = file
        else:
            self.file = None

        self.split_address()


    def dump(self):
        print('Full Name: ', self.name)
        print('Address1: ', self.address)
        if self.address2 is not None:
            print('Address2: ', self.address2)
        print('City, State, Zip: ', end='')
        print(self.town, self.state, self.zip, sep= ', ')

    def clean_address(self, addr):
        split_address = [add.strip() for add in addr]
        split_address = filter(lambda x: x, split_address)

        for char in (',', '.', '"', "'", '\n', '\r'):
            split_address = [s.replace(char,'') for s in split_address]
        return split_address

    def split_address(self):
        if self.file:
            with open(self.file, 'r') as f:
                # remove template at top of file
                addr = f.readlines()[7:]
        else:
            # get address from clipboard if no file
            addr = pyperclip.paste().split('\n')

        name, address, *address2, townStateZip = self.clean_address(addr)

        if address2:
            assert len(address2) == 1
            self.address2 = address2[0]
        else:
            self.address2 = None

        *town, state, zip_code = townStateZip.split()

        self.name = name
        self.address = address
        self.town = ' '.join(town)
        self.state = state.upper()
        self.zip = zip_code

if __name__ == '__main__':
    p = AddressParser('file.txt')
    p.dump()
