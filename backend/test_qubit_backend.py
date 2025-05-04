import numpy as np
from qubit_state import QubitState
from quantum_gates import QuantumGates

def almost_equal_complex(a, b, tol=1e-6):
    return np.abs(a - b) < tol

def test_initialization():
    q = QubitState()
    state = q.get_state_vector()
    assert almost_equal_complex(state[0], 1)
    assert almost_equal_complex(state[1], 0)

def test_apply_hadamard():
    q = QubitState()
    q.apply_gate(QuantumGates.hadamard())
    state = q.get_state_vector()
    expected = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
    assert np.allclose(state, expected, atol=1e-6)

def test_apply_pauli_x():
    q = QubitState()
    q.apply_gate(QuantumGates.pauli_x())
    state = q.get_state_vector()
    expected = np.array([0, 1])
    assert np.allclose(state, expected, atol=1e-6)

def test_set_preset_plus():
    q = QubitState()
    q.set_preset("plus")
    state = q.get_state_vector()
    expected = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
    assert np.allclose(state, expected, atol=1e-6)

def test_apply_rotation_x():
    q = QubitState()
    q.apply_gate(QuantumGates.rotation_x(np.pi))
    state = q.get_state_vector()
    expected = np.array([0, -1j])  # rotation by π around X maps |0> -> -i|1>
    # ignore global phase
    norm_phase = np.exp(-1j * np.angle(state[1]))
    state = state * norm_phase
    expected = expected * norm_phase
    assert np.allclose(state, expected, atol=1e-6)

def test_bloch_vector_zero_state():
    q = QubitState()
    theta, phi = q.get_bloch_vector()
    assert np.isclose(theta, 0, atol=1e-6)
    assert np.isclose(phi, 0, atol=1e-6)

def test_bloch_vector_plus_state():
    q = QubitState()
    q.apply_gate(QuantumGates.hadamard())
    theta, phi = q.get_bloch_vector()
    assert np.isclose(theta, np.pi/2, atol=1e-6)
    assert np.isclose(phi, 0, atol=1e-6)

def test_normalization():
    q = QubitState(alpha=3+4j, beta=1+2j)
    norm = abs(q.alpha)**2 + abs(q.beta)**2
    assert np.isclose(norm, 1.0, atol=1e-6)