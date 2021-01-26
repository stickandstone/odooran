import sys
import time

if len(sys.argv) > 1 and sys.argv[1] == 'test':
    from servises import test_relay as relay
else:
    from servises import relay


def action(t0, position, gate_is_opening) -> str:
    """
    Подает сигнал на реле и возвращает сообщение с состоянием ворот.
    """
    t1 = time.time()
    # Можно представить движение ворот как движение по прямой.
    # закрыто |----#--------------| открыто
    # Если ворота открываются, то точка смещается вправо.
    # Иначе они закрываются и точнка смещается влево.
    if position != 0:
        if gate_is_opening:
            position = t0 - t1
        else:
            position = t1 - t0

    # Проверка крайних положений ворот, открыты или закрыты.
    if position <= 0:
        message = 'Открываю ворота'
        position = 1
    elif position >= 25:
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

    return(t0, position, gate_is_opening, message)
