# actions class will be implemented here

class ActionSet(object):

    def __init__(self) -> None:
        pass


class CooperativeFourDirection(ActionSet):

    def __init__(self) -> None:
        super().__init__()
        self.actions = ['r', 'l', 'u', 'd', 'wait']
        self.actionsDict = {'r': [1, 0, 1],
                        'l': [-1, 0, 1],
                        'u': [0, 1, 1],
                        'd': [0, -1, 1],
                        'wait': [0, 0, 0.25]}