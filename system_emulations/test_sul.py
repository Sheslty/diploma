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
        valid_value = randint(0, 100)
        invalid_value = randint(101, 1000)
        match letter:
            case "change flow speed from 1 to 100":
                return pumps_system_command_handler(self.system, _id, '-f', valid_value)
            case "change flow speed from -100 to -1":
                return pumps_system_command_handler(self.system, _id, '-f', -valid_value)
            case "change flow speed from 101 to inf":
                return pumps_system_command_handler(self.system, _id, '-f', invalid_value)
            case "change flow speed from -inf to -101":
                return pumps_system_command_handler(self.system, _id, '-f', -invalid_value)
            case "change flow speed zero":
                return pumps_system_command_handler(self.system, _id, '-f', 0)
            case "change mode sync":
                return pumps_system_command_handler(self.system, _id, '-m', 'sync')
            case "change mode async":
                return pumps_system_command_handler(self.system, _id, '-m', 'async')
            case "turn on":
                return pumps_system_command_handler(self.system, _id, '-s', True)
            case "turn off":
                return pumps_system_command_handler(self.system, _id, '-s', False)
            case _:
                return "Unknown command"

    def post(self):
        self.system.update()
