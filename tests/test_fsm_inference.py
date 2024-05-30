import json
import socket

from aalpy.base import SUL
from aalpy.oracles import RandomWalkEqOracle
from aalpy.learning_algs import run_Lstar


class HVACSystemSUL(SUL):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.client_socket = None

    # Инициализирует или сбрасывает систему в начальное состояние.
    # Это вызывается перед началом каждой новой серии входов в рамках тестирования или обучения.
    def pre(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.client_socket.sendall('r'.encode())
        self.client_socket.close()

    # Получает входной символ, обрабатывает его и возвращает выход.
    # Этот метод должен моделировать, как система реагирует на каждый вход.
    def step(self, command):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        try:
            self.client_socket.sendall(command.encode())
            data = self.client_socket.recv(1024)
            response = data.decode().split()
            # print(f"{command = }, {data.decode() = }")

            if response[0] == "OK":
                self.client_socket.sendall("I".encode())
                data = self.client_socket.recv(1024)
                response = json.loads(data)
                # print(response)
                return data.decode()
            
        except Exception as e:
            print(e)
            print("Socket closed")

        finally:
            self.client_socket.close()

        return "ERR"

    # Очищает или завершает текущую сессию работы с системой.
    # Может использоваться для освобождения ресурсов или закрытия соединений.
    def post(self):
        pass


if __name__ == "__main__":
    host = 'localhost'
    port = 

    alphabet = ['l', 'ld', 'Mc', 'Mh', 'Mf', 'Md', 'SMt', 'SF', 'SH', 'ST',
                's3', 's2', 's1', 's0', 'r']  # Определение алфавита
    sul = HVACSystemSUL(host, port)  # Создание SUL (System Under Learning)
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000,
                                   reset_prob=0.1)  # Определение оракула эквивалентности
    learned_model = run_Lstar(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle,
                              automaton_type='mealy')  # Запуск алгоритма L*
    print(learned_model)  # Вывод изученного конечного автомата
