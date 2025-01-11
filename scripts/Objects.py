import pygame as pg

from scripts.utils import vector2

pg.init()

class circle():
    def __init__(self, Pos: vector2, Mass: float|int, Radius: float|int, Colour: tuple[int, int, int] = None, Velocity = vector2(0, 0)) -> 'circle':
        
        self.pos: 'vector2' = Pos
        self.velocity: 'vector2' = Velocity

        self.RADIUS: float|int = Radius
        self.MASS: float|int = Mass

        if Colour != None: self.COLOUR: tuple[int, int, int] = Colour
        else:
            from random import randint
            self.COLOUR: tuple[int, int, int] = (randint(30, 255), randint(30, 255), randint(30, 255))
    
    def WallCollesion(self, ScreenSize: tuple[int, int]) -> None:

        if (self.pos.X <= 0):
            self.pos.X = ScreenSize[0] - 1

        if (self.pos.X >= ScreenSize[0]):
            self.pos.X = 0 + 1

        if (self.pos.Y <= 0):
            self.pos.Y = ScreenSize[1] - 1

        if (self.pos.Y >= ScreenSize[1]):
            self.pos.Y = 0 + 1

    def CollisionResoultion(self, obj: 'circle') -> None:
        try:
            # Calculate masses and relative properties
            TotalMass: float | int = self.MASS + obj.MASS
            RelativeVelocity: vector2 = self.velocity - obj.velocity
            ImpactLine: vector2 = self.pos - obj.pos
            ImpactLineMagnitudeSquare = ImpactLine.magnitude() ** 2

            # Prevent zero division (if circles are exactly overlapping)
            if ImpactLineMagnitudeSquare == 0:
                ImpactLineMagnitudeSquare = 1e-6  # Small value to avoid division by zero

            # Calculate new velocities using elastic collision formula
            SelfNewVelocity: vector2 = self.velocity - (
                ((2 * obj.MASS) / TotalMass)
                * (RelativeVelocity.dot_product(ImpactLine) / ImpactLineMagnitudeSquare)
                * ImpactLine
            )

            self.velocity = SelfNewVelocity
            
            if type(obj) != static:
                ObjNewVelocity: vector2 = obj.velocity - (
                    ((2 * self.MASS) / TotalMass)
                    * ((-1 * RelativeVelocity).dot_product(-ImpactLine) / ImpactLineMagnitudeSquare)
                    * -ImpactLine
                )
                # Update velocities
                obj.velocity = ObjNewVelocity

            # --- Position correction to prevent overlap ---
            # Compute the overlap distance
            overlap = (self.RADIUS + obj.RADIUS) - ImpactLine.magnitude()

            if overlap > 0:  # If circles are overlapping
                correction = ImpactLine.normalize() * (overlap / 2)  # Divide correction equally
                self.pos += correction
                if type(obj) != static: obj.pos -= correction

        except ZeroDivisionError:
            self.velocity *= -1
            if type(obj) != static: obj.velocity *= -1

    def Update(self, SCREEN_SIZE):
        self.pos += self.velocity

        self.WallCollesion(SCREEN_SIZE)

        if self.velocity.X > 5: self.velocity.X = 5
        if self.velocity.Y > 5: self.velocity.Y = 5
        if self.velocity.X < -5: self.velocity.X = -5
        if self.velocity.Y < -5: self.velocity.Y = -5

class static():
    def __init__(self, Pos: vector2, Mass: float|int, Radius: float|int) -> 'circle':
        
        self.pos: 'vector2' = Pos
        self.velocity: 'vector2' = vector2(0 , 0)

        self.SETPOS = self.pos

        self.RADIUS: float|int = Radius
        self.MASS: float|int = Mass

        self.COLOUR: tuple[int] = (255, 255, 255)

    def CollisionResoultion(self, obj: 'circle') -> None:
        try:
            TotalMass: float | int = self.MASS + obj.MASS
            RelativeVelocity: vector2 = self.velocity - obj.velocity
            ImpactLine: vector2 = self.pos - obj.pos
            ImpactLineMagnitudeSquare = ImpactLine.magnitude() ** 2

            if ImpactLineMagnitudeSquare == 0:
                ImpactLineMagnitudeSquare = 1e-6

            ObjNewVelocity: vector2 = obj.velocity - (
                ((2 * self.MASS) / TotalMass)
                * ((-1 * RelativeVelocity).dot_product(-ImpactLine) / ImpactLineMagnitudeSquare)
                * -ImpactLine
            )

            obj.velocity = ObjNewVelocity

            overlap = (self.RADIUS + obj.RADIUS) - ImpactLine.magnitude()

            if overlap > 0:
                correction = ImpactLine.normalize() * (overlap / 2)
                obj.pos -= correction

        except ZeroDivisionError:
            obj.velocity *= -1

    def Update(self, SCREEN_SIZE):
        self.pos = self.SETPOS

def ApplyActiveForce(Force: int, Obj_List: tuple['circle', static], MousePos: tuple):
    ConstantPower = 25
    FieldRadius = 200

    Target = vector2(MousePos[0], MousePos[1])

    for Obj in Obj_List:
        if type(Obj) == static: continue

        DirectionToTarget = Target - Obj.pos

        Distance = DirectionToTarget.length()

        if Distance <= FieldRadius:

            DirectionToTarget = DirectionToTarget.normalize()

            ForceVector = DirectionToTarget * ConstantPower * Force

            Obj.velocity = ForceVector
    
def CollisionDetection(obj_list: list['circle', static], SCREENSIZE):

    gridSize = 100

    X_Axis_Box = round(SCREENSIZE[0] / gridSize)
    Y_Axis_Box = round(SCREENSIZE[1] / gridSize)
    Position_Dict = dict()

    for i in range(X_Axis_Box + 1):
        for j in range(Y_Axis_Box + 1):
            Position_Dict[(i * gridSize, j * gridSize)] = set()

    for obj in obj_list:
        X_Line = round(obj.pos.X / gridSize) * gridSize
        Y_Line = round(obj.pos.Y / gridSize) * gridSize

        if 0 <= X_Line <= SCREENSIZE[0] and 0 <= Y_Line <= SCREENSIZE[1]:
            Position_Dict[(X_Line, Y_Line)].add(obj)

        RADIUS_grid_size = round(obj.RADIUS / gridSize)

        for dx in [-RADIUS_grid_size, 0, RADIUS_grid_size]:
            for dy in [-RADIUS_grid_size, 0, RADIUS_grid_size]:
                X_Line = round(obj.pos.X / gridSize + dx) * gridSize
                Y_Line = round(obj.pos.Y / gridSize + dy) * gridSize

                if 0 <= X_Line <= SCREENSIZE[0] and 0 <= Y_Line <= SCREENSIZE[1]:
                    Position_Dict[(X_Line, Y_Line)].add(obj)

    for obj_Lists in Position_Dict.values():
        obj_Lists = tuple(obj_Lists)
        for index, obj in enumerate(obj_Lists):
            for otherObj in obj_Lists[index + 1:]:

                CenterDistance = (((obj.pos.X - otherObj.pos.X) ** 2) + ((obj.pos.Y - otherObj.pos.Y) ** 2)) ** 0.5
                RadiusTotal = obj.RADIUS + otherObj.RADIUS

                if CenterDistance <= RadiusTotal:
                    obj.CollisionResoultion(otherObj)

def GatherAll(Obj_List: list[circle, static], mousepos):
    for obj in Obj_List:
        if type(obj) == static: continue
        obj.pos = vector2(mousepos[0], mousepos[1])
    return Obj_List