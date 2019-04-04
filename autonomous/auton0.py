from magicbot import state, timed_state
from autonomous.base_auton import BaseAuton


class Auton0(BaseAuton):

    MODE_NAME = "Auton0"

    @state
    def status_1(self):
        pass
