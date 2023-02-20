from enum import Enum

# --------------------------------------------------------
# LIBRARY CLASS
# --------------------------------------------------------
class ControlInterfaceTypes(Enum):
    '''
    The control interface types.
    '''
    BEST = 'Best'
    FIELD_DEVICE = 'FieldDevice'
    SMARTBLUE = 'SmartBlue'
    HART = 'HART'
    DTM = 'DTM'

selectedControlInterfaces = set(ControlInterfaceTypes)
print(selectedControlInterfaces)