import subprocess
import csv
import time
import os
import matplotlib.pyplot as plt
import pandas as pd

def prueba(output_dir, architecture, cpu_type, l1d_size, l1i_size, l2_size, l1d_assoc, l1i_assoc, l2_assoc, cacheline_size, l1d_repl_policy, bp_type):
    script_path = './proyecto2.sh'
    command = f"bash {script_path} {output_dir} {architecture} {cpu_type} {l1d_size} {l1i_size} {l2_size} {l1d_assoc} {l1i_assoc} {l2_assoc} {cacheline_size} {l1d_repl_policy} {bp_type}"

    start_time = time.time()
    subprocess.run(command, shell=True)
    execution_time = time.time() - start_time

    print(f"Execution time: {execution_time:.2f} seconds")

def run_simulations(architecture):
    cpu_types = ['MinorCPU', 'AtomicSimpleCPU']
    cache_sizes = ['32kB', '64kB', '128kB']
    replacement_policies = ['LRURP', 'RandomRP']
    branch_predictors = ['BiModeBP', 'LTAGE', 'TAGE']



    script_path = './proyecto2.sh'
    output_base_path = f'./Outputs/{architecture}'
    os.makedirs(output_base_path, exist_ok=True)
    csv_path = os.path.join(output_base_path, 'simulation_results.csv')

    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['run_number', 'cpu_type', 'l1d_size', 'l1i_size', 'l2_size', 'replacement_policy', 'branch_predictor', 'execution_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        run_number = 1
        for cpu_type in cpu_types:
            for cache_size in cache_sizes:
                for bp in branch_predictors:
                    for rp in replacement_policies:
                        start_time = time.time()
                        output_dir = f"{output_base_path}/m5out_{run_number}"
                        command = f"bash {script_path} {output_dir} {architecture} {cpu_type} {cache_size} {cache_size} {cache_size} 2 2 1 64 {rp} {bp}"
                        subprocess.run(command, shell=True)
                        execution_time = time.time() - start_time
                        writer.writerow({
                            'run_number': run_number, 'cpu_type': cpu_type, 'l1d_size': cache_size, 'l1i_size': cache_size, 'l2_size': cache_size,
                            'replacement_policy': rp, 'branch_predictor': bp, 'execution_time': execution_time
                        })
                        run_number += 1

    print(f"Simulations completed and results saved to {csv_path}.")

def plot_results(architecture):
    output_base_path = f'./Outputs/{architecture}'
    csv_path = os.path.join(output_base_path, 'simulation_results.csv')
    plot_path = os.path.join(output_base_path, 'execution_time_profiles.png')
    data = pd.read_csv(csv_path)
    
    unique_cache_sizes = data['l1d_size'].unique()
    unique_replacement_policies = data['replacement_policy'].unique()
    unique_branch_predictors = data['branch_predictor'].unique()
    unique_cpu_types = data['cpu_type'].unique()
    
    num_subplots = len(unique_cache_sizes) * len(unique_replacement_policies)
    rows = len(unique_cache_sizes)
    cols = len(unique_replacement_policies)
    
    fig, axs = plt.subplots(rows, cols, figsize=(cols*6, rows*4), sharex=True, sharey=True)
    fig.suptitle('Execution Time Profiles', fontsize=16)
    
    for i, cache_size in enumerate(unique_cache_sizes):
        for j, rp in enumerate(unique_replacement_policies):
            ax = axs[i, j]
            for bp in unique_branch_predictors:
                for cpu in unique_cpu_types:
                    subset = data[(data['l1d_size'] == cache_size) & 
                                  (data['replacement_policy'] == rp) &
                                  (data['branch_predictor'] == bp) &
                                  (data['cpu_type'] == cpu)]
                    ax.plot(subset['run_number'], subset['execution_time'], marker='o', label=f'{cpu} - {bp}')
            
            ax.set_title(f'Cache Size: {cache_size}, Replacement Policy: {rp}')
            ax.set_xlabel('Run Number')
            ax.set_ylabel('Execution Time (s)')
            ax.grid(True)
            ax.legend()
    
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.show()
    
    print(f"Plot saved to {plot_path}.")

if __name__ == "__main__":
    arch = "ARM"
    prueba(output_dir='./output', architecture='ARM', cpu_type='MinorCPU', l1d_size='64kB', l1i_size='64kB', l2_size='128kB',
           l1d_assoc=2, l1i_assoc=2, l2_assoc=1, cacheline_size=64, l1d_repl_policy='LRURP', bp_type='TAGE')
    # run_simulations(arch)
    # plot_results(arch)