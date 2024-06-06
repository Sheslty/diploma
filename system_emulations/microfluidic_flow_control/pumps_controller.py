from typing import Union

class Pump:
    def __init__(self):
        self.status: bool = False
        self.current_volume: int = 0
        self.flow_speed: int = 0

    @property
    def status(self):
        return self.status

    @status.setter
    def status(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError('status must be a boolean')
        self.status = value

    @property
    def current_volume(self):
        return self.current_volume

    @current_volume.setter
    def current_volume(self, value: int):
        if not isinstance(value, int):
            raise ValueError("current_volume must be an integer")
        if 0 < value < 100:
            raise ValueError("current_volume must be in the range from 0 to 100")
        self.current_volume = value

    @property
    def flow_speed(self):
        return self.flow_speed

    @flow_speed.setter
    def flow_speed(self, value: int):
        if not isinstance(value, int):
            raise ValueError("flow_speed must be an integer")
        if -100 < value < 100:
            raise ValueError("flow_speed must be in the range from -100 to 100")
        self.flow_speed = value


class PumpsController:
    def __init__(self):
        self._pumps = self.basic_pump_initialization()
        self.synced_pumps_id = set()

    @staticmethod
    def basic_pump_initialization(pumps_num: int = 4) -> list:
        return [Pump() for _ in range(pumps_num)]

    # Переделать под новую структуру класса насоса
    def update(self):
        if self.all_sync_pumps_empty() or self.all_sync_pumps_filled_up():
            for _id in self.get_sync_pumps_ids():
                self.set_pump_status(_id, True)

        for pump in self._pumps:
            if pump.status == 0:
                continue
            val = pump.current_volume
            val = 100 if val + pump.flow_speed > 100 \
                else 0 if val + pump.flow_speed < 0 \
                else val + pump.flow_speed
            pump.current_volume = val
            if val == 100:
                pump.flow_speed = abs(pump.flow_speed)
                if pump.operating_mode == "sync":
                    pump.status = 0
            elif val == 0:
                pump.flow_speed = -pump.flow_speed
                if pump.operating_mode == "sync":
                    for _id in self.get_sync_pumps_ids():
                        self.set_pump_status(_id, False)

    # Переделать под новую структуру класса насоса
    def all_sync_pumps_filled_up(self) -> bool:
        for pump in self._pumps:
            if pump.current_volume != 100 and pump.operating_mode == 'sync':
                return False
        return True

    # Переделать под новую структуру класса насоса
    def all_sync_pumps_empty(self) -> bool:
        for pump in self._pumps:
            if pump.current_volume != 0 and pump.operating_mode == 'sync':
                return False
        return True

    def set_pump_flow_speed(self, pump_id: int, flow_speed: int):
        self._pumps[pump_id].flow_speed = flow_speed

    def set_pump_status(self, pump_id: int, value: bool):
        self._pumps[pump_id].status = value

    def set_pump_operating_mode(self, pump_id: int, mode: str):
        if mode not in ["async", "sync"]:
            raise ValueError('operating_mode must be either "async" or "sync"')
        if mode == 'sync':
            self.synced_pumps_id.add(pump_id)
        elif pump_id in self.get_sync_pumps_ids():
            self.synced_pumps_id.remove(pump_id)

    def get_sync_pumps_ids(self) -> list:
        return list(self.synced_pumps_id)

    def get_pumps_count(self):
        return len(self._pumps)

    def get_pumps_ids(self):
        return [self._pumps.index(pump) for pump in self._pumps]

    def get_pumps(self):
        return self._pumps.copy()


def pumps_system_command_handler(system: PumpsController, _id: int, cmd: str, value: Union[str, int, bool]):
    if _id not in system.get_pumps_ids():
        return "Invalid id"
    try:
        match cmd:
            case '-m':
                system.set_pump_operating_mode(_id, value)
                return "Operating mode has been successfully changed on the selected pump"
            case "-f":
                if not isinstance(value, int):
                    return "Invalid speed value"
                system.set_pump_flow_speed(_id, value)
                return "Flow speed successfully changed"
            case "-s":
                if not isinstance(value, bool):
                    return "Invalid speed value"
                system.set_pump_status(_id, value)
                return "Pump status successfully changed"
            case _:
                return "Unknown command"

    except Exception as e:
        return e.args[0]


if __name__ == "__main__":
    pumps_system = PumpsController()
    print(f"pumps_id = {pumps_system.get_pumps_ids()}")
    while True:
        _id, command_flag, value = input("> ").split()
        try:
            _id = int(_id)
        except ValueError as e:
            print(e)
            continue
        try:
            value = int(value)
        except ValueError as e:
            print(e)

        print(pumps_system_command_handler(pumps_system, _id, command_flag, value))
        pumps_system.update()
        print(pumps_system.get_pumps())
