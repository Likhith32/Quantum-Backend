from qiskit import QuantumCircuit
from qiskit_aer import Aer
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # allow React frontend to connect

def quantum_random_bits(n_bits=256):
    result_bits = ""

    backend = Aer.get_backend("qasm_simulator")

    for _ in range(n_bits):
        qc = QuantumCircuit(1, 1)
        qc.h(0)           # Hadamard → superposition
        qc.measure(0, 0)  # Collapse qubit

        # run circuit (instead of execute)
        job = backend.run(qc, shots=1)
        counts = job.result().get_counts()
        bit = "0" if "0" in counts else "1"
        result_bits += bit

    return result_bits

@app.route("/qrng")
def get_qrng_key():
    bits = quantum_random_bits(256)  # 256-bit key
    hex_key = hex(int(bits, 2))[2:].upper()
    return jsonify({"qrng_key": hex_key})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

