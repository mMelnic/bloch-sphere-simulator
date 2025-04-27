import numpy as np

class QubitState:
    def __init__(self, alpha=1+0j, beta=0+0j):
        self.alpha = alpha
        self.beta = beta
        self.normalize()

    def normalize(self):
        norm = np.sqrt(abs(self.alpha)**2 + abs(self.beta)**2)
        if norm == 0:
            raise ValueError("Qubit has zero norm!")
        self.alpha /= norm
        self.beta /= norm

    def apply_gate(self, gate_matrix):
        vec = np.array([self.alpha, self.beta])
        result = np.dot(gate_matrix, vec)
        self.alpha, self.beta = result[0], result[1]
        self.normalize()

    def get_state_vector(self):
        return np.array([self.alpha, self.beta])

    def set_state(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.normalize()

    def set_preset(self, preset_name):
        if preset_name == "zero":
            self.set_state(1+0j, 0+0j)
        elif preset_name == "one":
            self.set_state(0+0j, 1+0j)
        elif preset_name == "plus":
            self.set_state(1/np.sqrt(2), 1/np.sqrt(2))
        elif preset_name == "minus":
            self.set_state(1/np.sqrt(2), -1/np.sqrt(2))
        elif preset_name == "i_plus":
            self.set_state(1/np.sqrt(2), 1j/np.sqrt(2))
        elif preset_name == "i_minus":
            self.set_state(1/np.sqrt(2), -1j/np.sqrt(2))
        else:
            raise ValueError(f"Unknown preset {preset_name}")

    def get_bloch_vector(self):
        # |ψ⟩ = cos(θ/2) |0⟩ + exp(iφ) sin(θ/2) |1⟩
        theta = 2 * np.arccos(np.abs(self.alpha))
        if abs(self.beta) > 1e-12:  # avoid division by zero
            phi = np.angle(self.beta) - np.angle(self.alpha)  # φ is the relative phase between α and β
        else:
            phi = 0
        return theta, phi