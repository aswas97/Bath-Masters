# Enigma Machine Simulation

This project is a Python simulation of the Enigma machine, a type of enciphering machine used by the German military during World War II. The simulation includes classes that represent the core components of the Enigma machine: the plugboard, the rotors, and the reflector.

## Description

The Enigma machine was an advanced cipher machine, which provided billions of ways to encode a message. This simulation includes the following components:

- `PlugLead`: Represents a cable used in the plugboard to swap pairs of letters in the Enigma machine.
- `Plugboard`: Represents the plugboard itself, which is used to swap pairs of letters before and after the main rotor encryption.
- `Rotor`: Represents one of the rotors in the Enigma machine, which performs substitution cipher based on its configuration.
- `Reflector`: Represents the reflector in the Enigma machine, which reflects the signal back through the rotors after substitution.
- `Enigma`: Represents the entire Enigma machine, which includes the rotors, the reflector, and the plugboard.

## Installation

No installation is necessary for this simulation. Simply download the `.py` file and run it in a Python environment. Ensure that you have Python installed on your system.

## Usage

To use the Enigma machine simulation, you need to create instances of the components and configure them according to the desired settings.

### Example

```python
from enigma import PlugLead, Plugboard, Rotor, Reflector, Enigma

# Create plug leads
plug_lead = PlugLead('AG')

# Create and configure the plugboard
plugboard = Plugboard()
plugboard.add(plug_lead)

# Create rotors with their initial settings
rotor = Rotor(['I', 'II', 'III'], ['A', 'B', 'C'], [1, 1, 1])

# Create a reflector
reflector = Reflector(['B'])

# Assemble the Enigma machine
enigma = Enigma(rotor, reflector, ['AG', 'CT'])

# Encode a message
encoded_message = enigma.mess_encode('HELLOWORLD')
print(encoded_message)
