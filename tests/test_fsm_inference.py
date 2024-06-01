from aalpy.base import SUL
from aalpy.oracles import RandomWalkEqOracle
from aalpy.learning_algs import run_Lstar
from objects.hvac.controller import VentilationSystemController, command_handler


class HVACSystemSUL(SUL):
    def __init__(self):
        super().__init__()
        self.hvac_system = VentilationSystemController()

    # Инициализирует или сбрасывает систему в начальное состояние.
    # Это вызывается перед началом каждой новой серии входов в рамках тестирования или обучения.
    def pre(self):
        command_handler(self.hvac_system, 'r')

    # Получает входной символ, обрабатывает его и возвращает выход.
    # Этот метод должен моделировать, как система реагирует на каждый вход.
    def step(self, command):
        response = command_handler(self.hvac_system, command) if command else command_handler(self.hvac_system, 'r')
        print(f"{command = }, {response = }")
        return response

    # Очищает или завершает текущую сессию работы с системой.
    # Может использоваться для освобождения ресурсов или закрытия соединений.
    def post(self):
        pass


if __name__ == "__main__":
    alphabet = ['l', 'ld', 'Mc', 'Mh', 'Mf', 'Md', 'SMt', 'SF', 'SH', 'ST',
                's3', 's2', 's1', 's0', 'r']  # Определение алфавита
    sul = HVACSystemSUL()  # Создание SUL (System Under Learning)
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000,
                                   reset_prob=0.1)  # Определение оракула эквивалентности
    learned_model = run_Lstar(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle,
                              automaton_type='dfa')  # Запуск алгоритма L*
    print(learned_model)  # Вывод изученного конечного автомата
