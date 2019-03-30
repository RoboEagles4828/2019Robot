import pathfinder as pf
from pathfinder.followers import EncoderFollower

class PathFollow:
    left: EncoderFollower
    right: EncoderFollower

    def __init__(self, trajectory, max_velocity, encoder_position):
        modifier = pf.modifiers.TankModifier(trajectory).modify(0.5)

        self.left = EncoderFollower(modifier.getLeftTrajectory())
        self.right = EncoderFollower(modifier.getRightTrajectory())

        # Encoder Position is the current, cumulative position of your encoder. If
        # you're using an SRX, this will be the 'getEncPosition' function.
        # 1000 is the amount of encoder ticks per full revolution
        # Wheel Diameter is the diameter of your wheels (or pulley for a track system) in meters
        self.left.configureEncoder(encoder_position, 1000, 0.2032)

        # The first argument is the proportional gain. Usually this will be quite high
        # The second argument is the integral gain. This is unused for motion profiling
        # The third argument is the derivative gain. Tweak this if you are unhappy with the tracking of the trajectory
        # The fourth argument is the velocity ratio. This is 1 over the maximum velocity you provided in the
        #      trajectory configuration (it translates m/s to a -1 to 1 scale that your motors can read)
        # The fifth argument is your acceleration gain. Tweak this if you want to get to a higher or lower speed quicker
        self.left.configurePIDVA(1.0, 0.0, 0.0, 1 / max_velocity, 0)
        self.right.configurePIDVA(1.0, 0.0, 0.0, 1 / max_velocity, 0)

    def follow(self):
        pass

    def execute(self):
        self.left.calculate(encoder_position)
