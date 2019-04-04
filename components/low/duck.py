import wpilib

class Duck:
#kehan wuz here x jackie
    duck_solenoid: wpilib.DoubleSolenoid
    duck_servo_0: wpilib.Servo
    duck_servo_1: wpilib.Servo

    def __init__(self):
        with open(sys.path[0] +
                  ("/../" if os.getcwd()[-5:-1] == "test" else "/") +
                  "config/duck.json") as f:
            self.config = json.load(f)
        self.pos_servo = False
        self.pos_sol = False

    def setBill(self, pos): #bill is both of the servo
        self.pos_servo = pos
    
    def setPusher(self, pos): #sol is sol
        self.pos_sol = pos

    def execute(self): #True is OPEN = < 
        if self.pos_servo: 
            self.duck_servo_0.set(self.config["bill"]["pos_0_open"])
            self.duck_servo_1.set(self.config["bill"]["pos_1_open"])
        else: 
            self.duck_servo_0.set(self.config["bill"]["pos_0_close"])
            self.duck_servo_1.set(self.config["bill"]["pos_1_close"])
        if self.pos_sol:
            self.duck_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
        else:
            self.duck_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)



