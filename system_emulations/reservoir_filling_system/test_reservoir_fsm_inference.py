from aalpy import run_non_det_Lstar
from aalpy.oracles import RandomWalkEqOracle
from aalpy.learning_algs import run_Lstar

from system_emulations.test_locators import PATH_TO_RESULTS_DIR
from system_emulations.test_sul import MicrofluidicSystemSUL


def main():
    alphabet = ['fill', 'next', 'empty']

    sul = MicrofluidicSystemSUL()
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000,
                                   reset_prob=0.1)
    learned_model = run_non_det_Lstar(alphabet=alphabet, sul=sul,
                                      eq_oracle=eq_oracle)
    learned_model.save(PATH_TO_RESULTS_DIR.joinpath("Microfluidic_non_det_L"))

    sul = MicrofluidicSystemSUL()
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000,
                                   reset_prob=0.1)
    learned_model = run_Lstar(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle,
                              automaton_type='dfa')
    learned_model.save(PATH_TO_RESULTS_DIR.joinpath("Microfluidic_L_dfa"))

    sul = MicrofluidicSystemSUL()
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000,
                                   reset_prob=0.1)
    learned_model = run_Lstar(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle,
                              automaton_type='moore')
    learned_model.save(PATH_TO_RESULTS_DIR.joinpath("Microfluidic_L_moore"))

    sul = MicrofluidicSystemSUL()
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000,
                                   reset_prob=0.1)
    learned_model = run_Lstar(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle,
                              automaton_type='mealy')
    learned_model.save(PATH_TO_RESULTS_DIR.joinpath("Microfluidic_L_mealy"))


if __name__ == "__main__":
    if not PATH_TO_RESULTS_DIR.exists():
        PATH_TO_RESULTS_DIR.mkdir(parents=True)
    main()

