from enum import IntEnum

class RetroSteps(IntEnum):
    ICEBREAKER = 0
    REFLECT = 1
    GROUP = 2
    VOTE = 3
    DISCUSS = 4
    END = 5

    def next(step):
        if step == RetroSteps.END:
            return RetroSteps.END
        return RetroSteps(step + 1)