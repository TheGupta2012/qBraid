from abc import ABC, abstractmethod
from typing import Optional, List

class Gate(ABC):

    @abstractmethod
    def __init__(self, name: str, num_qubits: int, params: List = None, global_phase: Optional[float]=0.0, exponent: Optional[float]=1):
        self._name=name
        self._num_qubits=num_qubits
        self._params= [] if params == None else params 
        self._global_phase=global_phase
        self._exponent=exponent
    
    @property
    def name(self):
        return self._name

    @property
    def num_qubits(self):
        return self._num_qubits

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params: List):
        self._params = params

    @property
    def global_phase(self):
        return self._global_phase if hasattr(self,'_global_phase') else 0.0

    @global_phase.setter
    def global_phase(self, value: Optional[float]=0.0):
        self._global_phase = value

    def on(self, qubits):
        
        #avoid circular import
        from qbraid.circuits.instruction import Instruction
        return Instruction(self,qubits)

    def __call__(self, qubits):
        return self.on(qubits)

    def control(self, num_ctrls: Optional[int]=1):
        
        from .controlledgate import ControlledGate
        new_name = 'C'+self._name
        return ControlledGate(new_name, self._num_qubits+1, self._params, self._global_phase, self._exponent, num_ctrls)