from magicbot import AutonomousStateMachine, state

from components.high.pathfinder.auto_drive import AutoDrive


class BaseAuton(AutonomousStateMachine):

    auto_drive: AutoDrive

    @state(first=True)
    def init(self):
        self.auto_drive.setTrajectories("auton0")
        self.status = 0
        self.next_state("driving")

    @state
    def driving(self, initial_call):
        if initial_call:
            self.auto_drive.enable()
        if self.auto_drive.isFinished():
            self.auto_drive.disable()
            self.auto_drive.next()
            self.next_state("status_%d" % self.status)
            self.status += 1
