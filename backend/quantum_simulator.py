from qubit_state import QubitState
from quantum_gates import QuantumGates

class QuantumSimulator:
    """
    A singleton class that simulates a single-qubit quantum system.

    Provides functionality for:
    - Applying standard and parametric quantum gates
    - Resetting the qubit to common preset states
    - Undoing operations with a history stack
    - Saving and loading custom qubit states by name
    - Retrieving the qubit's state vector and Bloch sphere coordinates

    This simulator wraps around a QubitState instance and offers a simplified
    interface for managing quantum state for the frontend.
    """
    _instance = None  # Singleton instance

    def __new__(cls):
        """
        Ensures that only one instance of the QuantumSimulator is created.
        :return: The single instance of the QuantumSimulator.
        """
        if cls._instance is None:
            cls._instance = super(QuantumSimulator, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """
        Initializes the QuantumSimulator instance with a qubit in the |0> state, 
        a history stack for undo operations, and a dictionary for saving states.
        """
        if self._initialized:
            return
        self.qubit = QubitState()
        self.history = []
        self.redo_stack = []
        self.saved_states = {}  # name -> (alpha, beta)
        self._initialized = True

    def reset(self, preset="zero"):
        """
        Resets the qubit to a specific preset state (e.g., |0>, |1>, etc.).
        :param preset: The name of the preset state (default is "zero").

        Supported states include: zero, one, plus, minus, i_plus, i_minus.
        """
        self.history.append((self.qubit.alpha, self.qubit.beta))
        self.redo_stack.clear()
        self.qubit.set_preset(preset)

    def apply_gate(self, gate_name, **kwargs):
        """
        Applies a specified quantum gate to the qubit state.
        :param gate_name: The name of the gate to apply (e.g., "hadamard", "pauli_x").
        :param kwargs: Additional arguments required by the gate (e.g., theta for rotation gates).

        Supported gates include: identity, pauli_x, pauli_y, pauli_z, hadamard, phase, t, 
        rotation_x, rotation_y, rotation_z.
        """
        self.history.append((self.qubit.alpha, self.qubit.beta))
        self.redo_stack.clear()
        gate = self._get_gate_by_name(gate_name, **kwargs)
        self.qubit.apply_gate(gate)

    def undo(self):
        """
        Undoes the last operation (either gate or reset) by restoring the previous qubit state.
        """
        if self.history:
            self.redo_stack.append((self.qubit.alpha, self.qubit.beta))
            alpha, beta = self.history.pop()
            self.qubit.alpha = alpha
            self.qubit.beta = beta
        else:
            print("No more undos available!")

    def redo(self):
        if self.redo_stack:
            self.history.append((self.qubit.alpha, self.qubit.beta))
            alpha, beta = self.redo_stack.pop()
            self.qubit.alpha = alpha
            self.qubit.beta = beta
        else:
            print("No more redos available!")

    def save_state(self, name):
        """
        Saves the current qubit state under a specific name.
        If a state with the same name already exists, a versioned name is used automatically (e.g., "state_1", "state_2").
        :param name: The name to save the current state under.
        """
        if name in self.saved_states:
            version = 1
            while f"{name}_{version}" in self.saved_states:
                version += 1
            name = f"{name}_{version}"
        self.saved_states[name] = (self.qubit.alpha, self.qubit.beta)
        self.last_state_name = name

    def load_state(self, name):
        """
        Loads a saved qubit state by its name.
        :param name: The name of the state to load.
        :raises ValueError: If the state with the provided name does not exist.
        """
        if name in self.saved_states:
            alpha, beta = self.saved_states[name]
            self.history.append((self.qubit.alpha, self.qubit.beta))
            self.qubit.alpha = alpha
            self.qubit.beta = beta
        else:
            print(f"No saved state named '{name}'")

    def get_state_vector(self):
        """
        Retrieves the current state vector of the qubit.
        :return: A numpy array representing the state vector [alpha, beta] of the qubit.
        """
        return self.qubit.get_state_vector()

    def get_bloch_coordinates(self):
        """
        Retrieves the current Bloch sphere coordinates of the qubit.
        :return: A tuple (theta, phi) representing the qubit's position on the Bloch sphere.
        """
        return self.qubit.get_bloch_vector()

    def _get_gate_by_name(self, gate_name, **kwargs):
        """
        Helper function to retrieve the appropriate quantum gate by name.
        :param gate_name: The name of the quantum gate to retrieve (e.g., "identity", "pauli_x").
        :param kwargs: Additional arguments for gates that require them (e.g., theta for rotation gates).
        :return: A QuantumGate object corresponding to the specified gate name.
        :raises ValueError: If the gate name is unknown.
        """
        gate_name = gate_name.lower()
        if gate_name == "identity":
            return QuantumGates.identity()
        elif gate_name == "pauli_x":
            return QuantumGates.pauli_x()
        elif gate_name == "pauli_y":
            return QuantumGates.pauli_y()
        elif gate_name == "pauli_z":
            return QuantumGates.pauli_z()
        elif gate_name == "hadamard":
            return QuantumGates.hadamard()
        elif gate_name == "phase":
            return QuantumGates.phase()
        elif gate_name == "t":
            return QuantumGates.t_gate()
        elif gate_name == "rotation_x":
            theta = kwargs.get("theta", 0)
            return QuantumGates.rotation_x(theta)
        elif gate_name == "rotation_y":
            theta = kwargs.get("theta", 0)
            return QuantumGates.rotation_y(theta)
        elif gate_name == "rotation_z":
            theta = kwargs.get("theta", 0)
            return QuantumGates.rotation_z(theta)
        else:
            raise ValueError(f"Unknown gate name: {gate_name}")
