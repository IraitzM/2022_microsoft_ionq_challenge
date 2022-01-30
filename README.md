# Propposal for the IonQ + Microsoft Joint Challenge @ MIT iQuHACK 2022!

<p align="left">
  <a href="https://azure.microsoft.com/en-us/solutions/quantum-computing/" target="_blank"><img src="https://user-images.githubusercontent.com/10100490/151488491-609828a4-cd1f-4076-b5b2-a8d9fc2d0fa4.png" width="30%"/> </a>
  <a href="https://ionq.com/" target="_blank"><img src="https://user-images.githubusercontent.com/10100490/151488159-da95eb05-9277-4abe-b1ba-b49871d563ed.svg" width="20%" style="padding: 1%;padding-left: 5%"/></a>
  <a href="https://iquhack.mit.edu/" target="_blank"><img src="https://user-images.githubusercontent.com/10100490/151647370-d161d5b5-119c-4db9-898e-cfb1745a8310.png" width="8%" style="padding-left: 5%"/> </a>
  
</p>


# Circuit guessing game

Welcome to **Q-guess**!

The game is pretty simple. Once the player chooses the level he/she wants to play at and the complexity (number of qubits), a random circuit is generated and a set of counts for 50 shots shown. He/she will have to design a sequence of gates applied to each qubit so that the ending counts match the presented one. First levels will only use simulators but for the third level, real devices will be used so that it helps build an intuituin as well around NISQ devices and their implications.

# Levels

First level: Only H and X gates are used.

Second level: Z and Y gates are added as well as S and T (rotations around Z).

Third level: CNOT gates will be added to previous levels. Also, noise starts to make its magic (computing times may be longer given the queue for the device)

# Scores

A zero is the perfect match to the randomly generated circuit while gates used and distance to the target counts will add to the score. The one that get closer to zero wins!

# Running the game

Simply clone the repo and install the required dependencies:
```
pip install -r requirements.txt
```

And hit:

```
python src/main.py
```
