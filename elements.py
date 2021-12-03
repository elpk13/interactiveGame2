from enum import Enum

class Object_Type(Enum):
    TREE = 0
    BISON = 1
    RABBIT = 2
    RACCOON = 3
    DEER = 4

class Object:
    def __init__(self,x,y,width,height, path=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.blocking = False
        self.path = path

class Bison(Object):
    def __init__(self,x,y,width,height,path):
        self.type = Object_Type.BISON
        super().init(x,y,width,height,path)

class Rabbit(Object):
    def __init__(self,x,y,width,height,path):
        self.type = Object_Type.RABBIT
        super().init(x,y,width,height,path)

class Raccoon(Object):
    def __init__(self,x,y,width,height,path):
        self.type = Object_Type.RACCOON
        super().init(x,y,width,height,path)

class Deer(Object):
    def __init__(self,x,y,width,height,path):
        self.type = Object_Type.DEER
        super().init(x,y,width,height,path)
