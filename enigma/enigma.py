import numpy as np


class Rotor:

    def __init__(self, name, order, turnover=1, position=0):
        self.name = name
        self.order = order
        self.turnover = turnover
        self.position = position

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def read(self):
        return self.order[self.position]

    def rotate(self):
        if self.position < len(self.order) - 1:
            self.position += 1
        else:
            self.position = 0
    def xForm(self, letter):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        origPos = alphabet.index(letter)
        newLetter = self.order[origPos + self.position]
        return newLetter

    def spew(self):
        spew = '{' + self.name + ', ' + self.order + ', ' + \
            str(self.position) + ' - ' + self.order[self.position] + '}'
        return spew

class Plugboard:
    
    def __init__(self, name, pairs):
        self.name = name
        self.pairs = pairs

    def xForm(self, letter):
        try:
            pair = self.pairs[0].index(letter)
            newLetter = self.pairs[1][pair]
        except:
            try:
                pair = self.pairs[1].index(letter)
                newLetter = self.pairs[0][pair]
            except:
                newLetter = letter
        return newLetter

class EnigmaMachine:

    def __init__(self, name):
        self.name = name
        self.rotors = []
        self.plugboard = None

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def append_rotor(self, rotor):
        self.rotors.append(rotor)

    def insert_rotor(self, idx, rotor):
        self.rotors.insert(idx, rotor)

    def remove_rotor(self, idx):
        self.rotors.pop(idx)

    def append_plugboard(self, plugboard):
        self.plugboard = plugboard
    
    def remove_plugboard(self):
        self.plugboard = None   

    def read(self):
        msg = ''
        for rotor in self.rotors:
            msg += rotor.read()
        return msg

    def spew(self):
        spew = 'Name: ' + self.name
        for (idx, rotor) in enumerate(self.rotors):
            spew += '\n'
            spew = spew + '    Rotor ' + str(idx) + ': ' + rotor.spew()
        return spew
    
    def encrypt(self, message):
        char = ''
        for element in message:
            char = self.plugboard.xForm(element)
            char = self.rotors[0].xForm(char)
            char = self.rotors[1].xForm(char)
            char = self.rotors[2].xForm(char)
            self.rotors[0].rotate()
            self.rotors[1].rotate()
            self.rotors[2].rotate()
            element = char
        return message


def main():
    # Initialize the machine.
    em = EnigmaMachine('Enigma I')
    #Test creating the plugboard. Plugboard should be changed to just a string
    plugPairs = []
    plugPairs.append(['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'Q'])
    plugPairs.append(['U', 'E', 'J', 'O', 'T', 'P', 'Z', 'W', 'N', 'S', 'R', 'V'])
    rows = len(plugPairs)
    cols = len(plugPairs[0])
    test = plugPairs[1].index('J')
    testBoard = Plugboard('TestBoard', plugPairs)
    #Test transforming a letter on the plugboard
    new = testBoard.xForm('E')
    em.append_rotor(Rotor('I', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'))
    em.append_rotor(Rotor('II', 'AJDKSIRUXBLHWTMCQGZNPYFVOE'))
    em.append_rotor(Rotor('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO'))
    em.append_plugboard(testBoard)
    new2 = em.rotors[0].xForm('A')
    # Test the rotors.
    print(em.spew())
    print(em.read())
    em.rotors[0].rotate()
    em.rotors[1].rotate()
    em.rotors[2].rotate()
    print(em.spew())
    print(em.read())
    # Test translate entire message
    testMsg = 'TEST'
    newMsg = em.encrypt(testMsg)

if __name__ == '__main__':
    main()
