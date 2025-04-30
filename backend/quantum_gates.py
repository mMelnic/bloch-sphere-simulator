import numpy as np

class QuantumGates:
    @staticmethod
    def identity():
        return np.array([[1, 0], [0, 1]], dtype=complex)

    @staticmethod
    def pauli_x():
        return np.array([[0, 1], [1, 0]], dtype=complex)

    @staticmethod
    def pauli_y():
        return np.array([[0, -1j], [1j, 0]], dtype=complex)

    @staticmethod
    def pauli_z():
        return np.array([[1, 0], [0, -1]], dtype=complex)

    @staticmethod
    def hadamard():
        return (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)

    @staticmethod
    def phase():
        return np.array([[1, 0], [0, 1j]], dtype=complex)

    @staticmethod
    def t_gate():
        return np.array([[1, 0], [0, np.exp(1j*np.pi/4)]], dtype=complex)

    @staticmethod
    def rotation_x(theta):
        return np.array([[np.cos(theta/2), -1j*np.sin(theta/2)],
                         [-1j*np.sin(theta/2), np.cos(theta/2)]], dtype=complex)

    @staticmethod
    def rotation_y(theta):
        return np.array([[np.cos(theta/2), -np.sin(theta/2)],
                         [np.sin(theta/2), np.cos(theta/2)]], dtype=complex)

    @staticmethod
    def rotation_z(theta):
        return np.array([[np.exp(-1j*theta/2), 0],
                         [0, np.exp(1j*theta/2)]], dtype=complex)
    
    @staticmethod
    def custom_gate(matrix):
        if matrix is None:
            raise ValueError("Custom gate must include 'matrix' parameter.")
        try:
            matrix = np.array(matrix, dtype=complex)
        except Exception as e:
            raise ValueError(f"Invalid matrix format: {e}")
        if matrix.shape != (2, 2):
            raise ValueError("Custom gate matrix must be 2x2.")
        if not np.allclose(matrix.conj().T @ matrix, np.eye(2), atol=1e-8):
            raise ValueError("Custom gate matrix must be unitary.")
        return matrix