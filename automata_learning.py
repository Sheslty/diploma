import random
import sys
from aalpy.base import SUL
from aalpy.oracles import RandomWalkEqOracle
from aalpy.learning_algs import run_Lstar
from subprocess import run, PIPE

random.seed()

class SystemSUL(SUL):
    def __init__(self, script_path: str, config_path: str):
        super().__init__()
        self.script_path = script_path
        self.config_name = config_path
        self.config_flag = '--config'
        self.stdout_flag = '--stdout'

    # Инициализирует или сбрасывает систему в начальное состояние.
    # Это вызывается перед началом каждой новой серии входов в рамках тестирования или обучения.
    def pre(self):
        upper_limit = 2000
        bottom_limit = 1000
        self.params = [random.randint(-10, 10), round(random.random() * (upper_limit + bottom_limit) - bottom_limit, 2)]

    # Получает входной символ, обрабатывает его и возвращает выход.
    # Этот метод должен моделировать, как система реагирует на каждый вход.
    def step(self, command):
        run_args = [
            sys.executable,
            self.script_path,
            self.config_flag, self.config_name,
            self.stdout_flag,
        ]
        if not command:
            return
        result: str
        if 'reboot' in command:
            run_args.append(command)
            result = run(run_args, stdout=PIPE).stdout.decode('utf-8')
        else:
            run_args.append(command)
            run_args.extend(str(param) for param in self.params)
            result = run(run_args, stdout=PIPE).stdout.decode('utf-8')
        return result

    # Очищает или завершает текущую сессию работы с системой.
    # Может использоваться для освобождения ресурсов или закрытия соединений.
    def post(self):
        pass

if __name__ == "__main__":
    alphabet = ['--speed', '--height', '--reboot'] # Определение алфавита
    sul = SystemSUL("object/system.py", "object/config.json") # Создание SUL (System Under Learning)
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000, reset_prob=0.1) # Определение оракула эквивалентности
    learned_model = run_Lstar(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle, automaton_type='moore') # Запуск алгоритма L*
    print(learned_model) # Вывод изученного конечного автомата
