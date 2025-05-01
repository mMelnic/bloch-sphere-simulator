import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
                             QLabel, QComboBox, QSlider, QLineEdit, QGridLayout)
from PyQt5.QtCore import Qt
from qutip import Bloch 
from quantum_simulator import QuantumSimulator
from qutip import Qobj

class QuantumGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.simulator = QuantumSimulator()
        self.setFixedSize(500, 400)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Bloch Sphere Quantum Simulator')
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #f0f0f0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3c3f58;
                border: none;
                border-radius: 8px;
                padding: 10px;
                color: white;
            }
            QPushButton:hover {
                background-color: #5a5f7a;
            }
            QPushButton:pressed {
                background-color: #2d2f45;
            }
            QComboBox, QLineEdit {
                background-color: #2b2e42;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 6px;
                color: white;
            }
            QComboBox:hover, QLineEdit:hover {
                border: 1px solid #666;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #444;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #6a6fc1;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QLabel {
                font-weight: bold;
                margin-bottom: 5px;
            }
        """)

        # Layouts
        main_layout = QVBoxLayout()
        control_layout = QHBoxLayout()
        gate_layout = QVBoxLayout()
        state_layout = QVBoxLayout()

        self.bloch = Bloch()
        self.bloch.show()

        # --- Gate Controls ---
        self.gate_combo = QComboBox()
        self.gate_combo.addItems([
            'identity', 'pauli_x', 'pauli_y', 'pauli_z', 
            'hadamard', 'phase', 't', 
            'rotation_x', 'rotation_y', 'rotation_z'
        ])
        gate_layout.addWidget(QLabel("Select Gate:"))
        gate_layout.addWidget(self.gate_combo)

        self.apply_gate_btn = QPushButton("Apply Gate")
        self.apply_gate_btn.clicked.connect(self.apply_gate)
        gate_layout.addWidget(self.apply_gate_btn)
        


        self.rotation_label = QLabel("Rotation Angle (for Rx, Ry, Rz): 0°")
        gate_layout.addWidget(self.rotation_label)

        self.rotation_slider = QSlider(Qt.Horizontal)
        self.rotation_slider.setRange(0, 360)
        self.rotation_slider.setValue(0)
        self.rotation_slider.valueChanged.connect(self.update_rotation_label)
        gate_layout.addWidget(self.rotation_slider)
     
        self.state_combo = QComboBox()
        self.state_combo.addItems(['zero', 'one', 'plus', 'minus', 'i_plus', 'i_minus'])
        state_layout.addWidget(QLabel("Reset to State:"))
        state_layout.addWidget(self.state_combo)

        self.reset_btn = QPushButton("Reset Qubit")
        self.reset_btn.clicked.connect(self.reset_qubit)
        state_layout.addWidget(self.reset_btn)

        self.undo_btn = QPushButton("Undo")
        self.undo_btn.clicked.connect(self.undo)
        state_layout.addWidget(self.undo_btn)
        
        self.redo_btn = QPushButton("Redo")
        self.redo_btn.clicked.connect(self.redo)
        state_layout.addWidget(self.redo_btn)

        self.save_input = QLineEdit()
        self.save_input.setPlaceholderText("Enter state name to save")
        self.save_btn = QPushButton("Save State")
        self.save_btn.clicked.connect(self.save_state)

        self.load_combo = QComboBox()
        self.load_btn = QPushButton("Load State")
        self.load_btn.clicked.connect(self.load_state)

        self.custom_btn = QPushButton("Custom...")
        self.custom_btn.clicked.connect(self.show_custom_popup)
        gate_layout.addWidget(self.custom_btn)

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

    def show_custom_popup(self):
        self.custom_popup = QWidget()
        self.custom_popup.setWindowTitle("Custom Gate Matrix")
        layout = QVBoxLayout()
    
        grid = QGridLayout()
        self.matrix_inputs = [[QLineEdit() for _ in range(2)] for _ in range(2)]
    
        # Fill grid with 2x2 editable fields
        for i in range(2):
            for j in range(2):
                self.matrix_inputs[i][j].setPlaceholderText("e.g. 1/sqrt(2)")
                if i == 1 and j == 1:
                    self.matrix_inputs[i][j].setPlaceholderText("e.g. -1/sqrt(2)")
                grid.addWidget(self.matrix_inputs[i][j], i, j)
    
        layout.addLayout(grid)
    
        apply_btn = QPushButton("Apply gate")
        apply_btn.clicked.connect(self.apply_custom_gate)
        layout.addWidget(apply_btn)
    
        self.custom_popup.setLayout(layout)
        self.custom_popup.setFixedSize(300, 150)
        self.custom_popup.show()

    def apply_custom_gate(self):
        try:
            matrix = []
            for i in range(2):
                row = []
                for j in range(2):
                    text = self.matrix_inputs[i][j].text()
                    value = complex(eval(text, {"sqrt": np.sqrt, "pi": np.pi, "__builtins__": {}}))
                    row.append(value)
                matrix.append(row)
    
            self.simulator.apply_gate("custom", matrix=matrix)
            self.update_bloch()

            self.custom_popup.close()
        except Exception as e:
            print(f"Error parsing matrix: {e}")

    def apply_gate(self):
        gate_name = self.gate_combo.currentText()
        kwargs = {}
        if 'rotation' in gate_name:
            theta = np.deg2rad(self.rotation_slider.value())
            kwargs['theta'] = theta
        try:
            self.simulator.apply_gate(gate_name, **kwargs)
            self.update_bloch()
        except Exception as e:
            print(f"Failed to apply gate: {e}")

    def redo(self):
        self.simulator.redo()
        self.update_bloch()
        

    def update_rotation_label(self):
        angle = self.rotation_slider.value()
        self.rotation_label.setText(f"Rotation Angle (for Rx, Ry, Rz): {angle}°")

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
            self.load_combo.addItem(self.simulator.last_state_name)
            self.save_input.clear()

    def load_state(self):
        name = self.load_combo.currentText()
        self.simulator.load_state(name)
        self.update_bloch()

    def update_bloch(self):
        theta, phi = self.simulator.get_bloch_coordinates()

        state_vector = np.array([np.cos(theta/2), np.sin(theta/2) * np.exp(1j * phi)])
        state_qobj = Qobj(state_vector)

        self.bloch.clear()
        self.bloch.add_states(state_qobj)
        self.bloch.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QuantumGUI()
    window.show()
    sys.exit(app.exec_())
