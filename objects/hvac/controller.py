import json
import logging
import socket
from multiprocessing import Process
from threading import Timer


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
        self._modes = self.config["modes"]

        self._mode = None
        self._locked = False
        self._fan_mode_turbo = False

        self._ventilation = WorkingVentilationElements()
        self._ventilation.sensors = self.default_sensors_settings
        self._last_ventilation_state = WorkingVentilationElements()

    def get_locked(self):
        return self._locked

    def get_humidifier(self):
        return self._ventilation.humidifier_on

    def get_conditioner(self):
        return self._ventilation.conditioner_on

    def get_ventilation(self):
        return self._ventilation.ventilation_on

    def get_fan_mode(self):
        return self._fan_mode_turbo

    def get_mode(self):
        return self._mode

    @property
    def default_sensors_settings(self):
        return VentilationSystemSensors(
            temperature=self._modes["default"]["temperature"],
            humidity=self._modes["default"]["humidity"],
            fan_speed=self._modes["default"]["fan_speed"]
        )

    def stop_working(self):
        if self._locked:
            raise Exception("ERR System is locked.")

        self._ventilation.ventilation_on = False
        self._ventilation.conditioner_on = False
        self._ventilation.humidifier_on = False

    def manage_ventilation(self):
        if self._locked:
            raise Exception("ERR System is locked.")
        self._ventilation.ventilation_on = not self._ventilation.ventilation_on

    def manage_conditioner(self):
        if self._locked:
            raise Exception("ERR System is locked.")

        self._ventilation.conditioner_on = not self._ventilation.conditioner_on
        if self._ventilation.conditioner_on and not self._ventilation.ventilation_on:
            self._ventilation.ventilation_on = True

    def manage_humidifier(self):
        if self._locked:
            raise Exception("ERR System is locked.")

        self._ventilation.humidifier_on = not self._ventilation.humidifier_on
        if self._ventilation.humidifier_on and not self._ventilation.ventilation_on:
            self._ventilation.ventilation_on = True

    def set_temperature(self, value: int):
        if self._locked:
            raise Exception("ERR System is locked.")
        if not isinstance(value, int):
            raise Exception("ERR Invalid value type.")

        self._mode = None
        self._ventilation.sensors.temperature = value

    def set_humidity(self, value: int):
        if self._locked:
            raise Exception("ERR System is locked.")
        if not isinstance(value, int):
            raise Exception("ERR Invalid value type.")
        if value not in range(0, 101):
            raise Exception("ERR Invalid value.")

        self._mode = None
        self._ventilation.sensors.humidity = value

    def set_fan_speed(self, value: int):
        if self._locked:
            raise Exception("ERR System is locked.")
        if not isinstance(value, int):
            raise Exception("ERR Invalid value type.")
        if value not in range(0, 101):
            raise Exception("ERR Invalid value.")

        self._ventilation.sensors.fan_speed = value

    def submode_turbo(self):
        if self._locked:
            raise Exception("ERR System is locked.")

        self._fan_mode_turbo = not self._fan_mode_turbo
        if self._fan_mode_turbo:
            self._last_ventilation_state = self._ventilation
            self.set_fan_speed(100)
        else:
            self._ventilation = self._last_ventilation_state

    def change_mode(self, mode_name):
        if self._locked:
            raise Exception("ERR System is locked.")
        if self._mode and self._mode != mode_name:
            raise Exception(f"ERR Other mode is already used.")

        if mode_name == self._mode:
            self._mode = None
            self._ventilation = self._last_ventilation_state

        else:
            params = self._modes["mode"][mode_name]
            self._last_ventilation_state = self._ventilation
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

    def lock(self):
        self._locked = not self._locked

    def reset(self):
        if self._locked:
            raise Exception("ERR System is locked.")
        self.__init__()

    def get_led_display(self):
        return self._ventilation.led_display

    def led_display(self):
        if self._locked:
            raise Exception("ERR System is locked.")
        self._ventilation.led_display = not self._ventilation.led_display
        self._last_ventilation_state.led_display = self._ventilation.led_display

    def info(self):
        return {"mode": self._mode,
                "is_locked": self._locked,
                "turbo_mode": self._fan_mode_turbo,
                "ventilation": self._ventilation.to_dict()}


def command_handler(system: VentilationSystem, cmd: str,
                    val: int = None) -> str:
    try:
        match cmd:
            case 's0':
                system.stop_working()
                return "OK System disabled."
            case 's1':
                system.manage_ventilation()
                return f"OK Ventilation {'enabled' if system.get_ventilation() else 'disabled'}."
            case 's2':
                system.manage_conditioner()
                return f"OK Air conditioning {'enabled' if system.get_conditioner() else 'disabled'}."
            case 's3':
                system.manage_humidifier()
                return f"OK Humidification system {'enabled' if system.get_humidifier() else 'disabled'}."
            case 'ST':
                system.set_temperature(val)
                return f"OK Temperature is set."
            case 'SH':
                system.set_humidity(val)
                return f"OK Humidity is set."
            case 'SF':
                system.set_fan_speed(val)
                return f"OK Fan speed is set."
            case 'SMt':
                system.submode_turbo()
                return f"OK Turbo mode {'enabled' if system.get_fan_mode() else 'disabled'}"
            case 'Mc':
                system.change_mode("cool")
                return f"OK Cool mode {'enabled' if system.get_mode() else 'disabled'}."
            case 'Md':
                system.change_mode("dry")
                return f"OK Dry mode {'enabled' if system.get_mode() else 'disabled'}."
            case 'Mh':
                system.change_mode('heat')
                return f"OK Heat mode {'enabled' if system.get_mode() else 'disabled'}."
            case 'Mf':
                system.change_mode('fan')
                return f"OK Fan mode {'enabled' if system.get_mode() else 'disabled'}."
            case 'l':
                system.lock()
                return f"OK Parameters {'locked' if system.get_locked() else 'unlocked'}."
            case 'r':
                system.reset()
                return "OK Parameters reset to default."
            case 'ld':
                system.led_display()
                return f"OK LED display {'enabled' if system.get_led_display() else 'disabled'}."
            case 'I':
                return str(system.info())
            case _:
                return "ERR Unknown command"
    except Exception as e:
        return e


def logger_init():
    fmt = '[%(asctime)s] [pid:%(process)-5d] [tid::%(thread)-5d] [module:%(module)s] [line:%(lineno)-3s] %(levelname)-8s %(message)s'
    logging.basicConfig(level=logging.DEBUG, filename="file.log",
                        filemode="a", format=fmt)

def handle_client(conn, addr):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                logging.info(f"Client {addr} disconnected")
                break
            logging.info(f"Received from {addr}: {data.decode()}")
            response = "Hi"
            conn.sendall(response.encode())
    logging.info(f"Connection with {addr} closed")

def start_server(timeout = 60):
    logger_init()
    ventilation_system = VentilationSystem()
    host = 'localhost'
    port = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        logging.info(f"Server started and listening on {host}:{server_socket.getsockname()[1]}")
        server_socket.listen()

        def shutdown_server():
            logging.info("No connections received. Server shutting down...")
            server_socket.close()
            exit(0)

        timer = Timer(timeout, shutdown_server)
        timer.start()

        while True:
            try:
                conn, addr = server_socket.accept()
                process = Process(target=handle_client, args=(conn, addr))
                process.start()
                conn.close()

                timer = Timer(timeout, shutdown_server)
                timer.start()
            except socket.error as e:
                logging.error(e)
                break


if __name__ == "__main__":
    start_server()
