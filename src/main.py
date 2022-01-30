import click
import random
import numpy as np
from configuration import level_config, simulator, state_vect
from qiskit import QuantumCircuit, execute

MAX_SHOTS = 50

def print_odds(state_vec):
    """
    Gets the states and odds

    Args:
        state_vec (array): Array containing the state vectors
    """
    array = np.asarray(state_vec)
    for i,v in enumerate(array):
        value = v.real**2 + v.imag**2
        if value > 0:
            print(f"Chances of ending in position {i} are {value}")

def apply_gate(circuit, gate, qubit, control = None):
    """A simple circuit that adds param defined gate to provided circuit

    Args:
        circuit (QuantumCircuit): The cirucit to which the gate needs to be applied to
        gate (str): The gate to be applied
        qubit (int): And the qubit to which it will be applied
        control (int, optional): For the CNOT gate so the controlling qubit is specified. Defaults to None.

    Returns:
        QuantumCircuit: Modified circuit
    """
    
    if gate == 'h':
        circuit.h(qubit)
    elif gate == 'x':
        circuit.x(qubit)
    elif gate == 'y':
        circuit.y(qubit)
    elif gate == 'z':
        circuit.z(qubit)
    elif gate == 's':
        circuit.s(qubit)
    elif gate == 't':
        circuit.t(qubit)
    elif gate == 'cx':
        circuit.cx(control, qubit) 
    
    return circuit

def get_random_circuit(level, n):
    """Gets a randomly generated circuit

    Args:
        level (str): String containing the number of the level to play
        n (int): Number of qubits to be used in the circuit

    Returns:
        dict: Dictionary with the set of possible states and the times each state was measured
    """
    # Define our circuit
    circuit = QuantumCircuit(n, n)
    circuit.name = f"Random {n}-qubit generator circuit"
    
    # Choose from available gates
    for _ in range(random.randint(0,level_config[level]['actions'])):
        gate = random.choice(level_config[level]['gates'])
        qubit = random.randint(0,n-1)
        if level == '3' and gate == 'cx':
            cbit = random.randint(0,n-1)
            while cbit == qubit:
                cbit = random.randint(0,n-1)
            circuit = apply_gate(circuit, gate, qubit, cbit)
        else:
            circuit = apply_gate(circuit, gate, qubit)
    
    # Measure output
    meas_array = []
    for i in range(n):
        meas_array += [i]
    circuit.measure(meas_array,meas_array)
    
    # Set the backend
    backend = level_config[level]['backend']
    qpu_job = backend.run(circuit, shots=MAX_SHOTS)

    # Wait until job is finished
    result = qpu_job.result()
    counts = result.get_counts()
    
    return counts, circuit.depth()

def score(target, obtained, diff):
    """Computes the final score for the player

    Args:
        target ([type]): [description]
        obtained ([type]): [description]
        diff (int): Diff in circuit depths
    """
    val = 0
    for i in target:
        val += abs(target[i] - obtained[i])
    
    if val == 0:
        print("Congratulations, you nailed it!")
    else:
        f_score = val/MAX_SHOTS + diff
        print(f"Final score: {f_score}")

def help(target, level):
    """ This function prints the helper text"""
    print(f'This is the obtained result {target} from the default {MAX_SHOTS} shots.')
    print(f"You can choose the sequence in which you would like to apply your gates, which for your level are: {level_config[level]['gates']}")
    if level != '3':
        print(" -> Please, specify them as (gate, qubit)")
    else:
        print(" -> Please, specify them as (gate, qubit) - add a third parameter when cx gat is used: (gate, qubit, control)")
    print("Enter state_vector() to check your odds.")
    print("Enter measure() to end your circuit and obtain your score. Good luck!")

@click.command()
@click.option('--level', type=click.Choice(['1', '2', '3']),prompt='Levels', help='Level you would like to play')
@click.option('--qubits', type=click.IntRange(1, 9), prompt='Qubits', help='Number of qubits to use')
def start_game(level, qubits):
    """
    A simple game that helps better understand how quantum circuits are built an what to expect from them
    
    """
    target, d_target = get_random_circuit(level, qubits)
    help(target, level)
    
    # Player circuit
    circuit = QuantumCircuit(qubits, qubits)
    circuit.name = f"Circuit"
    
    end = False
    while not end:
        val = input("Enter your choice: ")
        if val == "measure()":
            # Perform measurements
            meas_array = []
            for i in range(qubits):
                meas_array += [i]
            circuit.measure(meas_array,meas_array)
            
            end = True
            break
        elif val == "state_vector()":
            # Get the state vector
            sv = execute(circuit, state_vect).result().get_statevector(circuit)
            print_odds(sv)
        else:
            try:
                options = val.split(',')
                if len(options) > 2:
                    apply_gate(circuit, options[0], int(options[1]), int(options[2]))
                else:
                    apply_gate(circuit, options[0], int(options[1]))
            except Exception:
                print("Non valid entry")
                
    # Final measurement
    backend = level_config[level]['backend']
    qpu_job = backend.run(circuit, shots=MAX_SHOTS)

    # Wait until job is finished
    result = qpu_job.result()
    counts = result.get_counts()
    
    # Get score
    diff_depth = circuit.depth() - d_target
    score(target, counts, diff_depth)
        
if __name__ == '__main__':
    start_game()