
import pygame.draw as show

class vector2():
    def __init__(self, Xpos: int | float, Ypos: int | float):
        
        self.X: int|float = Xpos
        self.Y: int|float = Ypos

    def Value(self):
        return (self.X, self.Y)

    def setX(self, Xpos: int | float):
        self.X: int|float = Xpos

    def setY(self, Ypos: int | float):
        self.Y: int|float = Ypos
    
    def setValue(self, Xpos: int | float, Ypos: int | float):
        self.X: int|float = Xpos
        self.Y: int|float = Ypos

    def __str__(self):
        return f"vector2{self.Value()}"

    def __add__(self, obj: 'vector2'):
        return vector2(self.X + obj.X, self.Y + obj.Y)
    def __sub__(self, obj: 'vector2'):
        return vector2(self.X - obj.X, self.Y - obj.Y)
    
    def __rmul__(self, obj: int|float):
        return vector2(self.X * obj, self.Y * obj)
    def __mul__(self, obj: int|float):
        return vector2(self.X * obj, self.Y * obj)
    
    def __truediv__(self, obj: int|float):
        if obj != 0:
            X = self.X / obj
            Y = self.Y /obj
            return(vector2(X, Y))
        else: 
           return(vector2(1, 1))

    def __exp__(self, obj: 'vector2'):
        return vector2(self.X ** obj.X, self.Y ** obj.Y)
    
    def dot_product(self, obj: 'vector2') -> int|float:
        return self.X * obj.X + self.Y * obj.Y
    
    def magnitude(self):
        return ((self.X ** 2) + (self.Y ** 2)) ** 0.5
    
    def normalize(self):
        magnitude = self.magnitude()
        return (self / magnitude)
    
    def __neg__(self):
        return vector2(-self.X, -self.Y)
    
    def length(self):
        return (self.X**2 + self.Y**2)**0.5
    
    def distance(self, obj: 'vector2'):
        return (((self.X - obj.X) ** 2) + ((self.Y - obj.Y) ** 2)) ** 0.5

def draw(Screen, objects):
    for object in objects:
        show.circle(Screen, object.COLOUR, object.pos.Value(), object.RADIUS,)

def Grids(self):
    from math import ceil
    GridSize = int((self.SCREENSIZE[0] * self.SCREENSIZE[1] // self.Balls) ** 0.5)
    
    X_Axis_Box = ceil(self.SCREENSIZE[0] / GridSize)
    Y_Axis_Box = ceil(self.SCREENSIZE[1] / GridSize)

    return GridSize

        
