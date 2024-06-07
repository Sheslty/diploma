from aalpy import run_non_det_Lstar
from aalpy.oracles import RandomWalkEqOracle
from aalpy.learning_algs import run_Lstar

from system_emulations.test_locators import PATH_TO_RESULTS_DIR
from system_emulations.test_sul import HVACSystemSUL


def main():
    alphabet = ['l', 'ld', 'Mc', 'Mh', 'Mf', 'Md', 'SMt', 'SF', 'SH', 'ST',
                's3', 's2', 's1', 's0', 'r']
    sul = HVACSystemSUL()
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000,
                                   reset_prob=0.1)
    learned_model = run_Lstar(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle,
                              automaton_type='dfa')
    learned_model.save(PATH_TO_RESULTS_DIR + "HVAC_L_dfa")

    sul = HVACSystemSUL()
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000,
                                   reset_prob=0.1)
    learned_model = run_non_det_Lstar(alphabet=alphabet, sul=sul,
                                      eq_oracle=eq_oracle)
    learned_model.save(PATH_TO_RESULTS_DIR + "HVAC_non_det_L")


if __name__ == "__main__":
    main()