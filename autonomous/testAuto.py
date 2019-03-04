from magicbot import AutonomousStateMachine, timed_state, state
import wpilib

from components.low.drivetrain import DriveTrain

class TestAuto(AutonomousStateMachine):
    MODE_NAME = 'Test Auto'
    DISABLED = False
    DEFAULT = True

    drive: DriveTrain

    @timed_state(duration=3, first=True)
    def drive_forward(self):
        self.drive.setSpeedsFromJoystick(0, .3, 0)
