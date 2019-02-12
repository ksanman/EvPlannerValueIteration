class ActionSpace(object):
    Drive = 0
    Charge = 1

    def __init__(self, count, actions):
        """ Holds information about an action. 
            Each action should be enumerated as a property. 
            The total number of actions is passed in as a count. 

            Keyword arguments:

            count -- The total number of actions in the space. 
            actions -- An array of the enumeration of actions for RL agents to use. 
        """

        self.Count = count
        self.Actions = actions

class StartActionSpace(ActionSpace):
    def __init__(self):
        """ The Action Space for the start states
        """
        super(StartActionSpace, self).__init__(1, [0])

class ChargerActionSpace(ActionSpace):
    def __init__(self):
        """ The Action Space for the charger states
        """
        super(ChargerActionSpace, self).__init__(2, [0, 1])

class DestinationActionSpace(ActionSpace):
    def __init__(self):
        """ The Action Space for the destination states
        """
        super(DestinationActionSpace, self).__init__(0, [])
        