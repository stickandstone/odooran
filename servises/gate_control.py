import sys
import time

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    from servises import test_relay as relay
else:
    from servises import relay


def action(gate_state) -> dict:
    """
    Подает сигнал на реле и возвращает сообщение с состоянием ворот.
    """
    # распаковка состояния
    position = gate_state['pos']
    t0 = gate_state['t0']
    gate_is_opening = gate_state['gio']
    t1 = time.time()
    # Можно представить движение ворот как движение точки по прямой.
    # закрыто |----#--------------| открыто
    # Если ворота открываются, то точка смещается вправо и значение увеличивается.
    # Иначе они закрываются, точнка смещается влево и значение уменьшается.
    if position != 0:
        if gate_is_opening:
            position = position + t0 - t1
        else:
            position = position + t1 - t0

    # Проверка крайних положений ворот, открыты или закрыты.
    if position <= 0:
        # закрыты
        message = 'Открываю ворота'
        position = 1
    elif position >= 25:
        # открыты
        message = 'Закрываю ворота'
        position = 24

    else:
        # Промежуточное состояние, ворота находится в движенни.
        # Если поступил сигнал их нужно остановить и продолжить движение
        # в другом направлении.
        relay.click()
        if gate_is_opening:
            message = 'Открываю ворота'
        else:
            message = 'Закрываю ворота'

    gate_is_opening = not gate_is_opening
    t0 = t1
    relay.click()

    # упаковка состояния в словарь
    gate_state['pos'] = position
    gate_state['t0'] = t0
    gate_state['gio'] = gate_is_opening
    gate_state['msg'] = message

    return(gate_state)
