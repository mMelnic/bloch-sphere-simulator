from qubit_state import QubitState
from quantum_gates import QuantumGates

class QuantumSimulator:
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QuantumSimulator, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.qubit = QubitState()
        self._initialized = True

    def reset(self, preset="zero"):
        self.qubit.set_preset(preset)

    def apply_gate(self, gate_name, **kwargs):
        gate = self._get_gate_by_name(gate_name, **kwargs)
        self.qubit.apply_gate(gate)

    def get_state_vector(self):
        return self.qubit.get_state_vector()

    def get_bloch_coordinates(self):
        return self.qubit.get_bloch_vector()

    def _get_gate_by_name(self, gate_name, **kwargs):
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
