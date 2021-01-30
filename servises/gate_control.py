import sys
import time

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    from servises import test_relay as relay
else:
    from servises import relay


def action(gate_state) -> dict:
    """
    Turns the relay on and return the gate status value.
    """
    position = gate_state['pos']
    t0 = gate_state['t0']
    gate_is_opening = gate_state['gio']
    t1 = time.time()

    message = 'Открываю ворота' if gate_is_opening else 'Закрываю ворота'

    # You can think of the motion of the gate as the motion of a point in a straight line.
    # closed |----#--------------| open
    # If the gate opens, the point shifts to the right and the value increases.
    # Otherwise it is closed, the point moves to the left and the value decreases.

    if position != 0:
        if gate_is_opening:
            position = position + t0 - t1
        else:
            position = position + t1 - t0

    # Checking the end point of the gate. 0 is close, 25 is open.
    if position <= 0:
        position = 1
    elif position >= 25:
        position = 24
    else:
        relay.click()

    gate_is_opening = not gate_is_opening
    t0 = t1
    relay.click()

    gate_state['pos'] = position
    gate_state['t0'] = t0
    gate_state['gio'] = gate_is_opening
    gate_state['msg'] = message

    return(gate_state)
