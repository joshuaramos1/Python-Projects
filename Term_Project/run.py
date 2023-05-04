import subprocess

"""
 * @file run.py
 * @brief An Apocalyptic Simulator that highlights the computational advantages
 *        of the LRTA* algorithm in a multi-agent, adversarial,  
 *        dynamic environement.
 *
 * @author Joshua Ramos <joshuara@andrew.cmu.edu>
 * @author Sarah Stapleton <sstaplet@andrew.cmu.edu>
 * @author Anna Yu <annay@andrew.cmu.edu>
 *
"""



def main():

    num_trials = 1 # Change this to run more than one trial

    num_successful = 0
    success_stats = [0, 0]
    for i in range(num_trials):
        sim = subprocess.check_output('python simulation.py')
        out_list = sim.decode("utf-8").split()
        new_list = list(map(int, out_list))
        success = new_list[0]
        avg_plan_time_in_ns = new_list[1]
        avg_plan_time = avg_plan_time_in_ns/(10**6)
        avg_sim_time = new_list[2]
        # Successful Run
        if success == 1:
            num_successful += 1
            success_stats[0] += avg_plan_time
            success_stats[1] += avg_sim_time
    num_unsuccessful = num_trials - num_successful
    if (success_stats[0] != 0):
        success_stats[0] = success_stats[0]/num_successful
    if (success_stats[1] != 0):
        success_stats[1] = success_stats[1]/num_successful
    print("Successful Trials: ", num_successful)
    print("Average plan time (ms) of successful trials: ", success_stats[0])
    print("Average total simulation time (s) of successful trials: ", success_stats[1])
    print("\n")
    print("Unsuccessful Trials: ", num_unsuccessful)
    print("\n")
    success_rate = (num_successful/num_trials)*100
    print("Success Rate: ", success_rate)
        

if __name__ == '__main__':
    main()
