class ActionSpace(object):
    Drive = 0
    Charge = 1

    def __init__(self, actions):
        """ Holds information about an action. 
            Each action should be enumerated as a property. 
            The total number of actions is passed in as a count. 

            Keyword arguments:

            actions -- An array of the enumeration of actions for RL agents to use. 
        """

        self.Count = len(actions)
        self.Actions = actions

class StartActionSpace(ActionSpace):
    def __init__(self):
        """ The Action Space for the start states
        """
        super(StartActionSpace, self).__init__([ActionSpace.Drive])

class ChargerActionSpace(ActionSpace):
    def __init__(self):
        """ The Action Space for the charging states
        """
        super(ChargerActionSpace, self).__init__([ActionSpace.Drive, ActionSpace.Charge])

class DestinationActionSpace(ActionSpace):
    def __init__(self):
        """ The Action Space for the destination states
        """
        super(DestinationActionSpace, self).__init__([])
        