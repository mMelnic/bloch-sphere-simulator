import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
                             QLabel, QComboBox, QSlider, QLineEdit)
from PyQt5.QtCore import Qt
from qutip import Bloch 
from quantum_simulator import QuantumSimulator
from qutip import Qobj

class QuantumGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.simulator = QuantumSimulator()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Bloch Sphere Quantum Simulator')

        # Layouts
        main_layout = QVBoxLayout()
        control_layout = QHBoxLayout()
        gate_layout = QVBoxLayout()
        state_layout = QVBoxLayout()

        self.bloch = Bloch()  
        self.bloch.show()

        # Gate controls
        self.gate_combo = QComboBox()
        self.gate_combo.addItems(['identity', 'pauli_x', 'pauli_y', 'pauli_z', 'hadamard',
                                  'phase', 't', 'rotation_x', 'rotation_y', 'rotation_z'])
        gate_layout.addWidget(QLabel("Select Gate:"))
        gate_layout.addWidget(self.gate_combo)

        self.apply_gate_btn = QPushButton("Apply Gate")
        self.apply_gate_btn.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px;")
        self.apply_gate_btn.clicked.connect(self.apply_gate)
        gate_layout.addWidget(self.apply_gate_btn)

        self.rotation_slider = QSlider(Qt.Horizontal)
        self.rotation_slider.setRange(0, 360)
        self.rotation_slider.setValue(0)
        gate_layout.addWidget(QLabel("Rotation Angle (for Rx, Ry, Rz):"))
        gate_layout.addWidget(self.rotation_slider)

        # State controls
        self.state_combo = QComboBox()
        self.state_combo.addItems(['zero', 'one', 'plus', 'minus', 'i_plus', 'i_minus'])
        state_layout.addWidget(QLabel("Reset to State:"))
        state_layout.addWidget(self.state_combo)

        self.reset_btn = QPushButton("Reset Qubit")
        self.reset_btn.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px;")
        self.reset_btn.clicked.connect(self.reset_qubit)
        state_layout.addWidget(self.reset_btn)

        self.undo_btn = QPushButton("Undo")
        self.undo_btn.setStyleSheet("background-color: #9E9E9E; color: white; font-size: 14px; padding: 10px;")
        self.undo_btn.clicked.connect(self.undo)
        state_layout.addWidget(self.undo_btn)

        # Save/Load controls
        self.save_input = QLineEdit()
        self.save_input.setPlaceholderText("Enter state name to save")
        self.save_btn = QPushButton("Save State")
        self.save_btn.setStyleSheet("background-color: #2196F3; color: white; font-size: 14px; padding: 10px;")
        self.save_btn.clicked.connect(self.save_state)

        self.load_combo = QComboBox()
        self.load_btn = QPushButton("Load State")
        self.load_btn.setStyleSheet("background-color: #2196F3; color: white; font-size: 14px; padding: 10px;")
        self.load_btn.clicked.connect(self.load_state)

        state_layout.addWidget(self.save_input)
        state_layout.addWidget(self.save_btn)
        state_layout.addWidget(QLabel("Saved States:"))
        state_layout.addWidget(self.load_combo)
        state_layout.addWidget(self.load_btn)

        control_layout.addLayout(gate_layout)
        control_layout.addLayout(state_layout)
        main_layout.addLayout(control_layout)

        self.setLayout(main_layout)
        self.update_bloch()

    def apply_gate(self):
        gate_name = self.gate_combo.currentText()
        kwargs = {}
        if 'rotation' in gate_name:
            theta = np.deg2rad(self.rotation_slider.value())
            kwargs['theta'] = theta
        self.simulator.apply_gate(gate_name, **kwargs)
        self.update_bloch()

    def reset_qubit(self):
        preset = self.state_combo.currentText()
        self.simulator.reset(preset)
        self.update_bloch()

    def undo(self):
        self.simulator.undo()
        self.update_bloch()

    def save_state(self):
        name = self.save_input.text()
        if name:
            self.simulator.save_state(name)
            self.load_combo.addItem(name)
            self.save_input.clear()

    def load_state(self):
        name = self.load_combo.currentText()
        self.simulator.load_state(name)
        self.update_bloch()

    def update_bloch(self):
        theta, phi = self.simulator.get_bloch_coordinates()

    # Update the Bloch sphere with the current quantum state
        state_vector = np.array([np.cos(theta/2), np.sin(theta/2) * np.exp(1j * phi)])

        state_qobj = Qobj(state_vector)

    # Clear the previous visualization
        self.bloch.clear()  
        self.bloch.add_states(state_qobj) 
        self.bloch.show() 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QuantumGUI()
    window.show()
    sys.exit(app.exec_())