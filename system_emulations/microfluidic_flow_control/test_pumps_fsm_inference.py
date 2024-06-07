from random import seed, choice
from aalpy.oracles import RandomWalkEqOracle
from aalpy.learning_algs import run_Lstar
from system_emulations.test_locators import PATH_TO_RESULTS_DIR
from system_emulations.test_sul import PumpsSystemSUL

seed()

def main():
    alphabet = ['change_flow_speed_pos', 'change_flow_speed_neg',
                'change_flow_speed_zero', 'change_mode_sync',
                'change_mode_async', 'turn_on', 'turn_off']
    cex_proc = choice(['rs', 'longest_prefix', 'longest_prefix',
                       'linear_fwd', 'linear_bwd',
                       'exponential_fwd', 'exponential_bwd'])
    closing_strat = choice(['longest_first', 'shortest_first', 'single'])

    sul = PumpsSystemSUL()
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000,
                                   reset_prob=0.1)
    learned_model = run_Lstar(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle,
                              automaton_type='dfa',
                              closing_strategy=closing_strat,
                              cex_processing=cex_proc,
                              e_set_suffix_closed=False,
                              all_prefixes_in_obs_table=False,
                              cache_and_non_det_check=True,
                              max_learning_rounds=10)

    learned_model.save(
        PATH_TO_RESULTS_DIR.joinpath("Pumps_L_dfa" + "_" + closing_strat + "_" + cex_proc))

    sul = PumpsSystemSUL()
    eq_oracle = RandomWalkEqOracle(alphabet=alphabet, sul=sul, num_steps=1000,
                                   reset_prob=0.1)
    learned_model = run_Lstar(alphabet=alphabet, sul=sul, eq_oracle=eq_oracle,
                              automaton_type='moore',
                              closing_strategy=closing_strat,
                              cex_processing=cex_proc,
                              e_set_suffix_closed=False,
                              all_prefixes_in_obs_table=False,
                              cache_and_non_det_check=True,
                              max_learning_rounds=10)

    learned_model.save(
        PATH_TO_RESULTS_DIR.joinpath("Pumps_L_moore" + "_" + closing_strat + "_" + cex_proc))


if __name__ == "__main__":
    if not PATH_TO_RESULTS_DIR.exists():
        PATH_TO_RESULTS_DIR.mkdir(parents=True)
    main()
