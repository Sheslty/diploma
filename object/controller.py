import json
from pathlib import Path
import os


def delete_file(file_path: str) -> None:
    try:
        os.remove(file_path)
        print(f"Файл {file_path} успешно удален.")
    except Exception as e:
        print(f"Произошла ошибка при удалении файла: {e}")


def check_file_exists(file_path: str) -> bool:
    try:
        return Path(file_path).is_file()
    except Exception as e:
        print(e)
        return False


def read_json(filename: str) -> dict:
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError as e:
        print(e)


def save_json(data: dict, filename: str) -> None:
    try:
        with open(filename, "w") as f:
            json.dump(data, f)
    except FileNotFoundError as e:
        print(e)


class VentilationSystemSensors:
    def __init__(self, temperature: int | None = None,
                 fan_speed: int | None = None, humidity: int | None = None):
        self.temperature = temperature
        self.fan_speed = fan_speed
        self.humidity = humidity

    def to_dict(self):
        return {
            'temperature': self.temperature,
            'fan_speed': self.fan_speed,
            'humidity': self.humidity
        }


class WorkingVentilationElements:
    def __init__(self, ventilation: bool = False, conditioner: bool = False,
                 humidifier: bool = False,
                 led_display: bool = False,
                 sensors: VentilationSystemSensors = VentilationSystemSensors()):
        self.ventilation_on = ventilation
        self.conditioner_on = conditioner
        self.humidifier_on = humidifier
        self.led_display = led_display
        self.sensors = sensors

    def to_dict(self):
        return {
            'ventilation_on': self.ventilation_on,
            'conditioner_on': self.conditioner_on,
            'humidifier_on': self.humidifier_on,
            'led_display': self.led_display,
            'sensors': self.sensors.to_dict()
        }


class VentilationSystem:
    config_filename = "config.json"

    def __init__(self):
        self.config = read_json(self.config_filename)
        self.modes = self.config["modes"]

        self._mode = None
        self._locked = False
        self.fan_mode_turbo = False

        self._ventilation = WorkingVentilationElements()
        self._ventilation.sensors = self.default_sensors_settings
        self.last_ventilation_state = WorkingVentilationElements()

    @property
    def default_sensors_settings(self):
        return VentilationSystemSensors(
            temperature=self.modes["default"]["temperature"],
            humidity=self.modes["default"]["humidity"],
            fan_speed=self.modes["default"]["fan_speed"]
        )

    def stop_working(self):
        self._ventilation.ventilation_on = False
        self._ventilation.conditioner_on = False
        self._ventilation.humidifier_on = False
        print("OK System disabled.")

    def manage_ventilation(self):
        if self._locked:
            print("Err System is locked.")
            return
        self._ventilation.ventilation_on = True
        print("OK Ventilation turned on.")

    def manage_conditioner(self):
        if self._locked:
            print("Err System is locked.")
            return
        self._ventilation.conditioner_on = not self._ventilation.conditioner_on
        if self._ventilation.conditioner_on and not self._ventilation.ventilation_on:
            self._ventilation.ventilation_on = True
            print("Air conditioning enabled and ventilation turned on.")
        else:
            print(
                f"Air conditioning {'enabled' if self._ventilation.conditioner_on else 'disabled'}.")

    def manage_humidifier(self):
        if self._locked:
            print("Err System is locked.")
            return
        self._ventilation.humidifier_on = not self._ventilation.humidifier_on
        if self._ventilation.humidifier_on and not self._ventilation.ventilation_on:
            self._ventilation.ventilation_on = True
            print("Humidification system enabled and ventilation turned on.")
        else:
            print(
                f"Humidification system {'enabled' if self._ventilation.humidifier_on else 'disabled'}.")

    def set_temperature(self, value: int):
        if self._locked:
            print("Err System is locked.")
            return
        if not isinstance(value, int):
            print("Err Invalid value type.")
            return
        self._mode = None
        print(type(self._ventilation))
        self._ventilation.sensors.temperature = value
        print(f"OK Temperature is set.")

    def set_humidity(self, value: int):
        if self._locked:
            print("Err System is locked.")
            return
        if not isinstance(value, int):
            print("Err Invalid value type.")
            return
        if value not in range(0, 101):
            print("Err Invalid value.")
            return
        self._mode = None
        self._ventilation.sensors.humidity = value
        print(f"OK Humidity is set.")

    def set_fan_speed(self, value: int):
        if self._locked:
            print("Err System is locked.")
            return
        if not isinstance(value, int):
            print("Err Invalid value type.")
            return
        if value not in range(0, 101):
            print("Err Invalid value.")
            return
        self._ventilation.sensors.fan_speed = value
        print(f"OK Fan speed is set.")

    def submode_turbo(self):
        if self._locked:
            print("Err System is locked.")
            return
        self.fan_mode_turbo = not self.fan_mode_turbo
        if self.fan_mode_turbo:
            self.last_ventilation_state = self._ventilation
            self.set_fan_speed(100)
            print("OK Turbo mode Enabled")
        else:
            self._ventilation = self.last_ventilation_state
            print("OK Turbo mode disabled.")

    def change_mode(self, mode_name):
        if self._locked:
            print("Err System is locked.")
            return
        if self._mode and self._mode != mode_name:
            print(f"Err Other mode is already used.")
            return

        if mode_name == self._mode:
            self._mode = None
            self._ventilation = self.last_ventilation_state
            print(f"{mode_name.capitalize()} mode disabled.")
        else:
            try:
                params = self.modes["mode"][mode_name]
                self.last_ventilation_state = self._ventilation
                self._mode = mode_name
                if mode_name == "fan":
                    self._ventilation.humidifier_on = False
                    self._ventilation.conditioner_on = False
                else:
                    self._ventilation.sensors = VentilationSystemSensors(
                        temperature=params["temperature"],
                        fan_speed=params["humidity"],
                        humidity=params["fan"]
                    )
                print(f"{mode_name.capitalize()} mode enabled. ")
            except:
                pass

    def lock(self):
        self._locked = not self._locked
        print(f"OK Parameters {'locked' if self._locked else 'unlocked'}.")

    def reset(self):
        if self._locked:
            print("Err System is locked.")
            return
        self.__init__()
        print("OK Parameters reset to default.")

    def led_display(self):
        if self._locked:
            print("Err System is locked.")
            return
        self._ventilation.led_display = not self._ventilation.led_display
        self.last_ventilation_state.led_display = self._ventilation.led_display
        print(
            f"OK LED display {'enabled' if self._ventilation.led_display else 'disabled'}.")

    def info(self):
        return {"mode": self._mode,
                "is_locked": self._locked,
                "turbo_mode": self.fan_mode_turbo,
                "ventilation": self._ventilation.to_dict()}


def command_handler(ventilation_system: VentilationSystem, command: str,
                    value: int = None) -> None:
    match command:
        case 's0':
            ventilation_system.stop_working()
        case 's1':
            ventilation_system.manage_ventilation()
        case 's2':
            ventilation_system.manage_conditioner()
        case 's3':
            ventilation_system.manage_humidifier()
        case 'ST':
            ventilation_system.set_temperature(value)
        case 'SH':
            ventilation_system.set_humidity(value)
        case 'SF':
            ventilation_system.set_fan_speed(value)
        case 'SMt':
            ventilation_system.submode_turbo()
        case 'Mc':
            ventilation_system.change_mode("cool")
        case 'Md':
            ventilation_system.change_mode("dry")
        case 'Mh':
            ventilation_system.change_mode('heat')
        case 'Mf':
            ventilation_system.change_mode('fan')
        case 'l':
            ventilation_system.lock()
        case 'r':
            ventilation_system.reset()
        case 'ld':
            ventilation_system.led_display()
        case 'I':
            print(ventilation_system.info())
        case _:
            print("0 Unknown command")


def main():
    ventilation_system = VentilationSystem()

    while True:
        command = input("> ")
        inp_list = command.split()
        command = inp_list[0]
        value = int(inp_list[1]) if len(inp_list) == 2 else None
        command_handler(ventilation_system, command, value)


if __name__ == "__main__":
    main()
