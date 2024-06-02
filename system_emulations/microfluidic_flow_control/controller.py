class Reservoir:
    def __init__(self, volume: int = 100, filled_in: bool = False):
        self._volume = volume
        self._filled_in = filled_in

    @property
    def volume(self):
        return self._volume

    @property
    def filled_in(self):
        return self._filled_in

    @filled_in.setter
    def filled_in(self, value: bool):
        self._filled_in = value


class MicrofluidicSystem:
    def __init__(self):
        self._reservoirs = [Reservoir(), Reservoir(), Reservoir()]
        self._current_reservoir_id = None

    def get_reservoirs_list(self):
        return self._reservoirs.copy()

    @property
    def current_reservoir_id(self):
        return self._current_reservoir_id

    def connect_to_reservoir(self):
        self._current_reservoir_id = (self._current_reservoir_id + 1) % 3 if self._current_reservoir_id else 0
        return "Connection to the next reservoir is successful"

    def fill_reservoir(self):
        if self._current_reservoir_id is None:
            return "None of the reservoirs are connected"
        if not self._reservoirs[self._current_reservoir_id].filled_in:
            self._reservoirs[self._current_reservoir_id].filled_in = True
            return "The reservoir is full"
        return "The reservoir is already full"

    def empty_reservoir(self):
        if self._current_reservoir_id is None:
            return "None of the reservoirs are connected"
        if self._reservoirs[self._current_reservoir_id].filled_in:
            self._reservoirs[self._current_reservoir_id].filled_in = False
            return "The reservoir is empty"
        return "The reservoir is already empty"


def microfluidic_system_command_handler(system: MicrofluidicSystem, command: str) -> str:
    match command:
        case "fill":
            return system.fill_reservoir()
        case "next":
            return system.connect_to_reservoir()
        case "empty":
            return system.empty_reservoir()
        case "info":
            return str(system.get_reservoirs_list()) + str(system.current_reservoir_id)
        case _:
            return "Unknown command"


if __name__ == "__main__":
    system = MicrofluidicSystem()

    while True:
        command = input(">")
        print(microfluidic_system_command_handler(system, command))
