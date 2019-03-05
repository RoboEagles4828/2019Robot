import logging
import wpilib
import ctre
import navx

class Lift:

    navx: navx.AHRS
    lift_front: ctre.WPI_TalonSRX
    lift_back: ctre.WPI_TalonSRX
    lift_drive_left: ctre.WPI_VictorSPX
    lift_drive_right: ctre.WPI_VictorSPX
    lift_prox_front: wpilib.DigitalInput
    lift_prox_back: wpilib.DigitalInput
    lift_limit_front_top: wpilib.DigitalInput
    lift_limit_front_bottom: wpilib.DigitalInput
    lift_limit_rear_top: wpilib.DigitalInput
    lift_limit_rear_bottom: wpilib.DigitalInput
    

    back_ratio = 3/4

    def __init__(self):
        self.logger = logging.getLogger("Lift")
        self.front_speed = 0
        self.back_speed = 0
        self.drive_speed = 0

    def disable(self):
        self.front_speed = 0
        self.back_speed = 0
        self.drive_speed = 0

    def setDriveSpeed(self, speed):
        self.drive_speed = speed

    def setFrontSpeed(self, speed):
        self.front_speed = speed

    def setBackSpeed(self, speed):
        self.back_speed = speed
    def get_limit_front_top(self):
        return not self.lift_limit_front_top.get()
    def get_limit_front_bottom(self):
        return not self.lift_limit_front_bottom.get()
    def get_limit_rear_top(self):
        return not self.lift_limit_rear_top.get()
    def get_limit_rear_bottom(self):
        return not self.lift_limit_rear_bottom.get()
    def setLiftSpeed(self, speed):
        self.setFrontSpeed(speed)
        self.setBackSpeed(self.back_ratio * speed)

    def getProxFront(self):
        return not self.lift_prox_front.get()

    def getProxBack(self):
        return not self.lift_prox_back.get()

    def debugNavx(self):
        return self.navx.getPitch()
    

    def execute(self):
        if (not self.get_limit_front_bottom() and self.front_speed >0) or (not self.get_limit_front_top() and self.front_speed<0):
            self.lift_front.set(self.front_speed)
        else:
            self.lift_front.set(0)
        if (not self.get_limit_rear_bottom() and self.back_speed >0) or (not self.get_limit_rear_top() and self.back_speed<0):
            self.lift_back.set(self.back_speed)
        else:
            self.lift_back.set(0)
        
        

        self.lift_drive_left.set(self.drive_speed)
        self.lift_drive_right.set(self.drive_speed)
        
    
