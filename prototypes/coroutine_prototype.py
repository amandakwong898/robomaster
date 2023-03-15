"""
coroutine_prototype.py:

Implements a data class that holds all of the possible states for
the RoboMaster and a collection of coroutines that implement
a few of the possible states.

The client program randomly changes the Robomaster's state before
running the corresponding coroutine for that state.
"""

import random

# pylint: disable=too-few-public-methods
# This warning is diabled because the only purpose
# of this class is to hold data. This could be
# accomplished with an enum, but the RoboMaster
# does not support enums.
class RoboMasterState:
    """
    A data class that holds all of the possible states for the RoboMaster.

    PATROL: Patrols an area.
    CHASE: Chases another RoboMaster.
    ATTACK: Attacks another RoboMaster.
    FLEE: Runs away from another RoboMaster.
    IDLE: Waits an does nothing.
    CURRENT_STATE: The RoboMaster's current state. The default is IDLE.

    """
    PATROL = "PATROL"
    CHASE = "CHASE"
    ATTACK = "ATTACK"
    FLEE = "FLEE"
    IDLE = "IDLE"

    CURRENT_STATE = IDLE

def get_coroutine():
    """
    Returns a coroutine based on the RoboMaster's current state.

    When the current state is RoboMasterState.IDLE, it returns the idle coroutine.
    When the current state is RoboMasterState.PATROL, it returns the patrol coroutine.
  
    Parameters:
    none
  
    Returns:
    void
    """
    if RoboMasterState.CURRENT_STATE == RoboMasterState.PATROL:
        return patrol()

    return idle()

def idle():
    """
    Idles while the current state is RoboMasterState.IDLE.

    Parameters:
    none
  
    Returns:
    void
    """
    while RoboMasterState.CURRENT_STATE == RoboMasterState.IDLE:
        print(RoboMasterState.IDLE)
        yield
    print("Finished Idle")

def patrol():
    """
    Patrols while the current state is RoboMasterState.PATROL.

    Parameters:
    none
  
    Returns:
    void
    """
    while RoboMasterState.CURRENT_STATE == RoboMasterState.PATROL:
        print(RoboMasterState.PATROL)
        yield
    print("Finished Patrol")

def get_random_state():
    """
    Returns a random RoboMasterState.

    Parameters:
    none
  
    Returns:
    void
    """
    rand_int = random.randint(1, 10)

    if rand_int <= 5:
        return RoboMasterState.IDLE

    return RoboMasterState.PATROL

def start():
    """
    The entry-point method for the program.
    Randomly changes the Robomaster's state before running the corresponding
    coroutine for that state.
    """
    current_coroutine = idle()

    for _ in range(10):
        try:
            current_coroutine.__next__()
            RoboMasterState.CURRENT_STATE = get_random_state()
            # pylint: disable=broad-exception-caught
            # A StopIteration exception is always raised when exiting
            # a coroutine but the RoboMaster does not recognize it.
            # The solution to this problem is catching a
            # general exception.
        except Exception:
            current_coroutine = get_coroutine()

start()