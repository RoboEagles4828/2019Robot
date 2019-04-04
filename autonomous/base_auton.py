from magicbot import AutonomousStateMachine, state

from components.high.pathfinder.auto_drive import AutoDrive


class BaseAuton(AutonomousStateMachine):

    auto_drive: AutoDrive

    @state(first=True)
    def init(self):
        self.auto_drive.set("auton0")
        self.status = 0
        self.next_state("driving")

    @state
    def driving(self, initial_call):
        if initial_call:
            self.auto_drive.enable()
        status = self.auto_drive.getStatus()
        if status > self.status:
            self.auto_drive.disable()
            self.next_state("status_%d" % status)
            self.status = status
