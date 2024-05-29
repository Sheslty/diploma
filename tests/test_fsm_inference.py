import socket
from aalpy.base import SUL
from aalpy.oracles import RandomWalkEqOracle
from aalpy.learning_algs import run_Lstar

def start_client(port):
    host = 'localhost'
    message = "Hello World"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        try:
            while True:
                client_socket.sendall(message.encode())
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode()}")
        except KeyboardInterrupt:
            print("Client shutting down...")
        finally:
            client_socket.close()
            print("Client disconnected.")


class SystemSUL(SUL):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM)

    # Инициализирует или сбрасывает систему в начальное состояние.
    # Это вызывается перед началом каждой новой серии входов в рамках тестирования или обучения.
    def pre(self):
        self.client_socket = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))


    # Получает входной символ, обрабатывает его и возвращает выход.
    # Этот метод должен моделировать, как система реагирует на каждый вход.
    def step(self, command):
        self.client_socket.sendall(command.encode())
        data = self.client_socket.recv(1024)
        print(f"Received: {data.decode()}")
        response = data.decode()
        return response


    # Очищает или завершает текущую сессию работы с системой.
    # Может использоваться для освобождения ресурсов или закрытия соединений.
    def post(self):
        self.client_socket.close()

if __name__ == "__main__":
    host = 'localhost'
    port = 57417
    # start_client(57409)
    #
    # exit()
    alphabet = ['l', 'ld', 'Mc', 'Mh', 'Mf', 'Md', 'SMt', 'SF', 'SH', 'ST', 's3', 's2', 's1', 's0', 'r'] # Определение алфавита
    sul = SystemSUL(host, port) # Создание SUL (System Under Learning)
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000, reset_prob=0.1) # Определение оракула эквивалентности
    learned_model = run_Lstar(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle, automaton_type='moore') # Запуск алгоритма L*
    print(learned_model) # Вывод изученного конечного автомата

