from typing import Union


class Pump:
    def __init__(self):
        self.status: bool = False
        self.current_volume: int = 0
        self.flow_speed: int = 0


class PumpsController:
    def __init__(self):
        self._pumps = self.basic_pump_initialization()
        self.synced_pumps_id = set()

    @staticmethod
    def basic_pump_initialization(pumps_num: int = 4) -> list:
        return [Pump() for _ in range(pumps_num)]

    def update(self):
        if len(self.get_sync_pumps_ids()) != 0 and \
                (self._all_sync_pumps_empty() or self._all_sync_pumps_filled_up()):
            for _id in self.get_sync_pumps_ids():
                self.set_pump_status(_id, True)

        for i in range(len(self._pumps)):
            if self._get_pump_status(i) == 0:
                continue
            val = self._get_pump_current_volume(i)
            val = 100 if val + self._pumps[i].flow_speed > 100 \
                else 0 if val + self._pumps[i].flow_speed < 0 \
                else val + self._pumps[i].flow_speed
            self._set_pump_current_volume(i, val)
            if val == 100:
                self.set_pump_flow_speed(i, abs(self._pumps[i].flow_speed))
                if i in self.get_sync_pumps_ids():
                    self.set_pump_status(i, False)
            elif val == 0:
                self.set_pump_flow_speed(i, -self._pumps[i].flow_speed)
                if i in self.get_sync_pumps_ids():
                    for _id in self.get_sync_pumps_ids():
                        self.set_pump_status(_id, False)

    def _all_sync_pumps_filled_up(self) -> bool:
        for _id in self.synced_pumps_id:
            if self._get_pump_current_volume(_id) != 100:
                return False
        return True

    def _all_sync_pumps_empty(self) -> bool:
        for _id in self.synced_pumps_id:
            if self._get_pump_current_volume(_id) != 0:
                return False
        return True

    def _get_pump_status(self, pump_id: int) -> bool:
        return self._pumps[pump_id].status

    def _get_pump_current_volume(self, pump_id: int) -> int:
        return self._pumps[pump_id].current_volume

    def _set_pump_current_volume(self, pump_id: int, volume: int) -> None:
        if not isinstance(volume, int):
            raise ValueError("current volume must be an integer")
        if not 0 <= volume <= 100:
            raise ValueError("current volume must be in the range from 0 to 100")
        self._pumps[pump_id].current_volume = volume

    def set_pump_flow_speed(self, pump_id: int, flow_speed: int) -> None:
        if not -100 <= flow_speed <= 100 or not isinstance(flow_speed, int):
            raise ValueError(
                "flow speed must be an integer in the range from -100 to 100")
        self._pumps[pump_id].flow_speed = flow_speed

    def set_pump_status(self, pump_id: int, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError('status must be a boolean')
        self._pumps[pump_id].status = value

    def set_pump_operating_mode(self, pump_id: int, mode: str) -> None:
        if mode not in ["async", "sync"]:
            raise ValueError('operating mode must be either "async" or "sync"')
        if mode == 'sync':
            self.synced_pumps_id.add(pump_id)
        elif pump_id in self.get_sync_pumps_ids():
            self.synced_pumps_id.remove(pump_id)

    def get_sync_pumps_ids(self) -> list:
        return list(self.synced_pumps_id)

    def get_pumps_count(self) -> int:
        return len(self._pumps)

    def get_pumps_ids(self) -> list:
        return [self._pumps.index(pump) for pump in self._pumps]

    def get_pumps_info(self):
        return [{str(self._pumps.index(pump)): {"pump_status": pump.status,
                           "pump_flow_speed": pump.flow_speed,
                           "pump_current_volume": pump.current_volume}} for pump in self._pumps.copy()]


def pumps_system_command_handler(system: PumpsController, _id: int, cmd: str, value: Union[str, int, bool]):
    if _id not in system.get_pumps_ids():
        return "Invalid pump id"
    try:
        match cmd:
            case '-m':
                system.set_pump_operating_mode(_id, value)
                return "Operating mode successfully changed"
            case "-f":
                system.set_pump_flow_speed(_id, value)
                return "Flow speed successfully changed"
            case "-s":
                system.set_pump_status(_id, value)
                return "Pump status successfully changed"
            case _:
                return "Unknown command"
    except Exception as e:
        return e.args[0]


if __name__ == "__main__":
    pumps_system = PumpsController()
    print(f"pumps_id = {pumps_system.get_pumps_ids()}")
    print(pumps_system.get_pumps_info(), pumps_system.get_sync_pumps_ids(), sep='\n')
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
        print(pumps_system.get_pumps_info(), pumps_system.get_sync_pumps_ids())
