from scripts.utils import vector2
from .Static import static

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
        #print("COLLISION")
            # Calculate masses and relative properties
        TotalMass: float | int = self.MASS + obj.MASS
        RelativeVelocity: vector2 = self.velocity - obj.velocity
        ImpactLine: vector2 = self.pos - obj.pos
        ImpactLineMagnitudeSquare = ImpactLine.magnitude() ** 2

                # Prevent zero division (if circles are exactly overlapping)
        if ImpactLineMagnitudeSquare == 0:
            ImpactLineMagnitudeSquare = 1e-6  # Small value to avoid division by zero

        if type(obj) == circle:
                # Calculate new velocities using elastic collision formula
            SelfNewVelocity: vector2 = self.velocity - (
                ((2 * obj.MASS) / TotalMass)
                * (RelativeVelocity.dot_product(ImpactLine) / ImpactLineMagnitudeSquare)
                * ImpactLine
                )

            self.velocity = SelfNewVelocity
                
            ObjNewVelocity: vector2 = obj.velocity - (
                ((2 * self.MASS) / TotalMass)
                * ((-1 * RelativeVelocity).dot_product(-ImpactLine) / ImpactLineMagnitudeSquare)
                * -ImpactLine
                )
                    # Update velocities
            obj.velocity = ObjNewVelocity
        else:
            self.velocity *= -1
            self.pos += self.velocity

            # --- Position correction to prevent overlap ---
            # Compute the overlap distance
        overlap = (self.RADIUS + obj.RADIUS) - ImpactLine.magnitude()

        if overlap > 0:  # If circles are overlapping
            correction = ImpactLine.normalize() * (overlap / 2)  # Divide correction equally
            self.pos += correction
            if type(obj) != static: obj.pos -= correction

    def Update(self, SCREEN_SIZE, ):
        self.pos += self.velocity

        self.WallCollesion(SCREEN_SIZE)

    def MaxVelocity(self, MaxVelocity: int):
        if abs(self.velocity.X) > MaxVelocity:
            if self.velocity.X < 0: self.velocity.X = -MaxVelocity
            else: self.velocity.X = MaxVelocity
        if abs(self.velocity.Y) > MaxVelocity:
            if self.velocity.Y < 0: self.velocity.Y = -MaxVelocity
            else: self.velocity.Y = MaxVelocity
