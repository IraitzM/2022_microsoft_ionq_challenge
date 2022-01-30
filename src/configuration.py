from qiskit import Aer
from azure.quantum.qiskit import AzureQuantumProvider

# iQuHack provider setting
provider = AzureQuantumProvider (
    resource_id = "/subscriptions/b1d7f7f8-743f-458e-b3a0-3e09734d716d/resourceGroups/aq-hackathons/providers/Microsoft.Quantum/Workspaces/aq-hackathon-01",
    location = "eastus"
)

# Backends
state_vect = Aer.get_backend('statevector_simulator')
simulator = provider.get_backend('ionq.simulator')
qpu_backend = provider.get_backend('ionq.qpu')

# Game levels
level_config = {
                '1': {'gates' : ['h', 'x'], 'actions' : 5}, 
                '2': {'gates' : ['h', 'z', 'y', 'x', 's'], 'actions' : 10}, 
                '3': {'gates' : ['h', 'z', 'y', 'x', 's','t', 'cx'], 'actions' : 20}
                }