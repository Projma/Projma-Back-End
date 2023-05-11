from enum import Enum

class RetroSteps(Enum):
    ICEBREAKER = 0
    REFLECT = 1
    GROUP = 2
    VOTE = 3
    DISCUSS = 4

    def next(step):
        if step == RetroSteps.DISCUSS:
            return step
        return RetroSteps(step + 1)