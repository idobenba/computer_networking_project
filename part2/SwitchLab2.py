import Switch
import queue


class SwitchLab2(Switch):
    def __init__(self, address, number_of_io_ports, queue_type, isFluid=False):
        super().__init__(address, number_of_io_ports)


