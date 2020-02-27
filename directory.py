import random


class File(object):
    '''A File class'''

    def __init__(self, name, size):
        '''(File, str, int) -> None
        Create a new File with name and size.
        Generate and assign a rgb color to File'''

        self.name = name
        self.size = size

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.color = (r, g, b)


class Folder(File):
    '''A Folder class which inherits from File'''

    def __init__(self, name, size):
        '''(Folder, str, int) -> None
        Create a new Folder with name, size,
        and an empty list of files. (Empty Folder)'''

        File.__init__(self, name, size)
        self.files = []
