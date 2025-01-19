from scripts.utils import vector2
from scripts.Objects import static

from itertools import product
from collections import defaultdict

def ApplyActiveForce(Program, MousePos: tuple):
    ConstantPower = 25
    FieldRadius = 200

    Target = vector2(MousePos[0], MousePos[1])

    for Obj in Program.Obj_Set:
        if type(Obj) == static: continue

        DirectionToTarget = Target - Obj.pos

        Distance = DirectionToTarget.length()

        if Distance <= FieldRadius:

            DirectionToTarget = DirectionToTarget.normalize()

            ForceVector = DirectionToTarget * ConstantPower * Program.ActiveForce

            Obj.velocity = ForceVector
    
def CollisionDetection(Program):

    Position_Dict: dict = defaultdict(set)

    for Obj in Program.Obj_Set:
        AdjX, AdjY = 0, 0

        X_Reminder = Obj.pos.X % Program.GridSize
        Y_Reminder = Obj.pos.Y % Program.GridSize

        if X_Reminder >= Program.GridSize // 2: AdjX = Program.GridSize
        if Y_Reminder >= Program.GridSize // 2: AdjY = Program.GridSize

        X_Line = Obj.pos.X - X_Reminder + AdjX
        Y_Line = Obj.pos.Y - Y_Reminder + AdjY

        Position_Dict[(X_Line, Y_Line)].add(Obj)

        RADIUS_grid_size = round(Obj.RADIUS / Program.GridSize)

        for dx, dy in product([-RADIUS_grid_size, 0, RADIUS_grid_size], repeat=2):
            X_Line = round(Obj.pos.X / Program.GridSize + dx) * Program.GridSize
            Y_Line = round(Obj.pos.Y / Program.GridSize + dy) * Program.GridSize

            if 0 <= X_Line <= Program.SCREENSIZE[0] and 0 <= Y_Line <= Program.SCREENSIZE[1]:
                Position_Dict[(X_Line, Y_Line)].add(Obj)

    for Obj_Sets in Position_Dict.values():
        for Obj, otherObj in product(Obj_Sets, repeat=2):

            if id(otherObj) == id(Obj): continue

            CenterDistance = Obj.pos.distance(otherObj.pos)
            RadiusTotal = Obj.RADIUS + otherObj.RADIUS

            if CenterDistance <= RadiusTotal:
                Obj.CollisionResoultion(otherObj)
        
    Position_Dict.clear()

def GatherAll(Program, MousePos: tuple[int, int]):
    for Obj in Program.Obj_Set:
        if type(Obj) == static: continue
        Obj.pos = vector2(MousePos[0], MousePos[1])

def testCollisionDetection(Program):
    for Obj in Program.Obj_Set:
        for otherObj in Program.Obj_Set:

            if Obj == otherObj: continue

            CenterDistance = Obj.pos.distance(otherObj.pos)
            RadiusTotal = Obj.RADIUS + otherObj.RADIUS

            if CenterDistance <= RadiusTotal:
                Obj.CollisionResoultion(otherObj)