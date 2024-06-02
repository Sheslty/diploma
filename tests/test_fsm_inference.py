from aalpy import run_non_det_Lstar
from aalpy.base import SUL
from aalpy.oracles import RandomWalkEqOracle
from aalpy.learning_algs import run_Lstar, run_KV
from systems.hvac.controller import VentilationSystemController, command_handler
from systems.microfluidic_flow_control.controller import MicrofluidicSystem, microfluidic_system_command_handler


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
        return response

    # Очищает или завершает текущую сессию работы с системой.
    # Может использоваться для освобождения ресурсов или закрытия соединений.
    def post(self):
        pass


class MicrofluidicSystemSUL(SUL):
    def __init__(self):
        super().__init__()
        self.microfluidic_system = None

    def pre(self):
        self.microfluidic_system = MicrofluidicSystem()

    def step(self, command):
        return microfluidic_system_command_handler(self.microfluidic_system, command)

    def post(self):
        pass


def fsm_hvac_system_model():
    alphabet = ['l', 'ld', 'Mc', 'Mh', 'Mf', 'Md', 'SMt', 'SF', 'SH', 'ST',
                's3', 's2', 's1', 's0', 'r']
    sul = HVACSystemSUL()
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000,
                                   reset_prob=0.1)
    learned_model = run_Lstar(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle,
                           automaton_type='dfa')
    learned_model.save("HVACLearnedModel")


def fsm_microfluidic_system_model():
    alphabet = ['fill', 'next', 'empty']
    sul = MicrofluidicSystemSUL()
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000,
                                   reset_prob=0.1)
    learned_model = run_non_det_Lstar(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle)
    learned_model.save("Microfluidic_non_det_Lstar")

    sul = MicrofluidicSystemSUL()
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000,
                                   reset_prob=0.1)
    learned_model = run_Lstar(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle, automaton_type='dfa')
    learned_model.save("Microfluidic_Lstar_dfa")

    sul = MicrofluidicSystemSUL()
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000,
                                   reset_prob=0.1)
    learned_model = run_Lstar(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle, automaton_type='moore')
    learned_model.save("Microfluidic_Lstar_moore")

    sul = MicrofluidicSystemSUL()
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000,
                                   reset_prob=0.1)
    learned_model = run_Lstar(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle, automaton_type='mealy')
    learned_model.save("Microfluidic_Lstar_mealy")

    sul = MicrofluidicSystemSUL()
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000,
                                   reset_prob=0.1)
    learned_model = run_KV(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle, automaton_type='moore')
    learned_model.save("Microfluidic_KV_moore")


    sul = MicrofluidicSystemSUL()
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000,
                                   reset_prob=0.1)
    learned_model = run_KV(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle, automaton_type='mealy')
    learned_model.save("Microfluidic_KV_mealy")


if __name__ == "__main__":
    #fsm_hvac_system_model()
    fsm_microfluidic_system_model()
