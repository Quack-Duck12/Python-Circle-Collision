from scripts.utils import vector2

class static():
    def __init__(self, Pos: vector2, Mass: float|int, Radius: float|int):
        
        self.pos: 'vector2' = Pos
        self.velocity: 'vector2' = vector2(0 , 0)

        self.SETPOS = self.pos

        self.RADIUS: float|int = Radius
        self.MASS: float|int = Mass

        self.COLOUR: tuple[int] = (255, 255, 255)

        self.Dampining = 0.98

    def CollisionResoultion(self, obj) -> None:
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

            obj.velocity = ObjNewVelocity * self.Dampining

            overlap = (self.RADIUS + obj.RADIUS) - ImpactLine.magnitude()

            if overlap > 0:
                correction = ImpactLine.normalize() * (overlap / 2)
                obj.pos -= correction
                if type(obj) == static:
                    self.SETPOS = self.pos
                    obj.SETPOS = obj.pos

        except ZeroDivisionError:
            obj.velocity *= -1

    def WallCollesion(self, ScreenSize: tuple[int, int]) -> None:

        if (self.pos.X <= 0):
            self.pos.X = ScreenSize[0] - 1

        if (self.pos.X >= ScreenSize[0]):
            self.pos.X = 0 + 1

        if (self.pos.Y <= 0):
            self.pos.Y = ScreenSize[1] - 1

        if (self.pos.Y >= ScreenSize[1]):
            self.pos.Y = 0 + 1

    def Update(self, SCREEN_SIZE):
        self.pos = self.SETPOS
        self.WallCollesion(SCREEN_SIZE)

    def MaxVelocity(self, args): pass