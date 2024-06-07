from aalpy.base import SUL
from system_emulations.split_system.split_system_controller import SplitSystemController, split_system_command_handler
from system_emulations.reservoir_filling_system.reservoir_controller import ReservoirSystem, reservoir_system_command_handler
from system_emulations.pump_transfer_system.pumps_controller import \
    PumpsController, pumps_system_command_handler
from random import seed, randint

seed()

class MicrofluidicSystemSUL(SUL):
    def __init__(self):
        super().__init__()
        self.microfluidic_system = None

    def pre(self):
        self.microfluidic_system = ReservoirSystem()

    def step(self, command):
        return reservoir_system_command_handler(self.microfluidic_system, command)

    def post(self):
        pass


class HVACSystemSUL(SUL):
    def __init__(self):
        super().__init__()
        self.hvac_system = SplitSystemController()

    def pre(self):
        split_system_command_handler(self.hvac_system, 'r')

    def step(self, command):
        response = split_system_command_handler(self.hvac_system, command) if command else split_system_command_handler(self.hvac_system, 'r')
        return response

    def post(self):
        pass


class PumpsSystemSUL(SUL):
    def __init__(self):
        super().__init__()
        self.system = None

    def pre(self):
        self.system = PumpsController()

    def step(self, letter):
        _id = randint(0, 3)
        value = randint(1, 100)
        match letter:
            case "change_flow_speed_pos":
                return pumps_system_command_handler(self.system, _id, '-f', value)
            case "change_flow_speed_neg":
                return pumps_system_command_handler(self.system, _id, '-f', -value)
            case "change_flow_speed_zero":
                return pumps_system_command_handler(self.system, _id, '-f', 0)

            case "change_mode_sync":
                return pumps_system_command_handler(self.system, _id, '-m', 'sync')

            case "change_mode_async":
                return pumps_system_command_handler(self.system, _id, '-m', 'async')

            case "turn_on":
                return pumps_system_command_handler(self.system, _id, '-s', True)
            case "turn_off":
                return pumps_system_command_handler(self.system, _id, '-s', False)
            case _:
                return "Unknown command"

    def post(self):
        self.system.update()
