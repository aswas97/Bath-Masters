import math
import string


class PlugLead:
    def __init__(self, mapping):
        if len(mapping) != 2:
            raise ValueError("The Mapping input should contain exactly two characters")
        self.__mapping = mapping

    def encode(self, char):
        if char == self.__mapping[0]:
            return self.__mapping[1]
        elif char == self.__mapping[1]:
            return self.__mapping[0]
        else:
            return char
        
# A class for storing plugboard wirings, takes in a str of lenth 2 and adds it to the connections list, these are called in the enigma before and after rotor adjustments like in the real enigma.
#Like the real engima machine it has a limitation of 10 wires meaning 10 pairs of letters with zero intersection.
#A potential extension would be to remove this constraint and have more wires avaiable.
        
class Plugboard:
    def __init__(self):
        self.connections = []
        self.lead_count = 0
        
    def add(self,lead):
        if self.is_full():
            raise ValueError("Enigma only allows for 10 leads.")
            return
        else:
            self.connections.append(lead)
            self.lead_count += 1

    def is_full(self):
        return self.lead_count > 10
        
    def encode(self, char):
        #encode a pair of charatcers showing the forward and reverse of the mapping 
        for lead in self.connections:
            encoded_char = lead.encode(char)
            
            if encoded_char != char:  
                return encoded_char
        return char  


    
#The Rotor class is set up to take in the rotor mapping keys, initial positions and ring settings these are standard inputs of enigma.
#These varaibles are all specific to the rotors so makes sense to initalise in the same class
#I have used dictionaries extensively in my code as it alows for easy indexing and serching hence the manipulation to dictionaries
class Rotor:
    def __init__(self, mapping, start_positions,ring_setting):
        self.all_rotors = {"I": ['E','K','M','F','L','G','D','Q','V','Z','N','T','O','W','Y','H','X','U','S','P','A','I','B','R','C','J'],
                       "II": ['A','J','D','K','S','I','R','U','X','B','L','H','W','T','M','C','Q','G','Z','N','P','Y','F','V','O','E'],
                       "III": ['B','D','F','H','J','L','C','P','R','T','X','V','Z','N','Y','E','I','W','G','A','K','M','U','S','Q', 'O'],
                       "Gamma":['F','S','O','K','A','N','U','E','R','H','M','B','T','I','Y','C','W','L','Q','P','Z','X','V','G','J','D'],
                       "Beta":['L','E','Y','J','V','C','N','I','X','W','P','B','Q','M','D','R','T','A','K','Z','G','F','U','H','O','S'],
                       "IV":['E','S','O','V','P','Z','J','A','Y','Q','U','I','R','H','X','L','N','F','T','G','K','D','C','M','W','B'],
                       "V":['V','Z','B','R','G','I','T','Y','U','P','S','D','N','H','L','X','A','W','M','J','Q','O','F','E','C','K'],
                       "VI":['J','P','G','V','O','U','M','F','Y','Q','B','E','N','H','Z','R','D','K','A','S','X','L','I','C','T','W']
                      }
        self.notch = {"I": "Q", "II": "E", "III": "V", "IV": "J", "V": "Z","Beta":".", "Gamma":"."}
        
        
        #Some validation checks for the input variables to ensure they are within bounds/ valid entries
        #An extention here could be to have the option for inputting a non standard rotor.
        if self.are_mappings_valid(mapping):
            raise ValueError("An invalid rotor has been selected for use, this must be in the set [I, II, III, IV, V, VI,VII, VIII, Beta, Gamma]")
        
        if self.are_start_positions_valid(start_positions):
            raise ValueError("An invalid start position has been entered, values must be between in the set [A, B, C..., Z], with inclusive bound. This is case sensitive.")
        
        if self.are_ring_settings_valid(ring_setting):
            raise ValueError("An invalid ring setting has been entered, values must be between in the set [1, 2, 3..., 26], with inclusive bounds")
            
        #If validation successfull manipulate the data to a more usefull state
        self.mapping = {key:self.all_rotors.get(key) for key in mapping}        
        self.positions = dict(zip(mapping, [ord(x) - 65 for x in start_positions]))
        self.ring = dict(zip(mapping, [chr(x + 64) for x in ring_setting])) 
        
        #These rotors have a second notch and slo have the condition that they rotate the next rotor when they turn onto there notch
        #This was easy to implement using a simple offset of 1, this is implemented below 
        self.notch["VI"] = ["Z","M"]
        self.notch["VII"] = ["Z","M"]
        self.notch["VIII"] = ["Z","M"]
        
        
    #Functions for Rotor, ring settings and initial position input validation
    def are_mappings_valid(self,mapping):
        valid_rotors = list(self.all_rotors.keys())
        return not(all([i in valid_rotors for i in mapping]))
    
    def are_start_positions_valid(self,start_positions):
        return not(all([i < chr(ord("Z")+1) and i > chr(64)  for i in start_positions]))
    
    def are_ring_settings_valid(self,ring_setting):
        return not(all([i < 27 and i > 0  for i in ring_setting]))
        
        

    
#set up a Reflector class to store standard reflectors and initialse the requested reflector option
#Added a custom reflector condition for use in the decoding section of the project, this allows for a varing reflector to be used ie. in decoder question 5 where adjustments to the refelctor are required
class Reflector:
    def __init__(self,mapping, custom=None):
        self.reflectors = {"A":['E','J','M','Z','A','L','Y','X','V','B','W','F','C','R','Q','U','O','N','T','S','P','I','K','H','G','D'],
                           "B":['Y','R','U','H','Q','S','L','D','P','X','N','G','O','K','M','I','E','B','F','Z','C','W','V','J','A','T'],
                           "C":['F','V','P','J','I','A','O','Y','E','D','R','Z','X','W','G','C','T','K','U','Q','S','B','N','M','H','L']
                          }
        if custom != None:
            self.reflectors["CUSTOM"] = custom
            
        if self.are_mappings_valid(mapping):
            raise ValueError("An invalid reflector has been selected for use, this must be in the set [A, B, C]")
            
        self.mapping = self.reflectors[mapping[0]]
    
    
    #A function for returning the output of a reflector
    def reflection_output(self,character):
        return self.mapping[ord(character)-65]
    
    #Reflector input validation
    def are_mappings_valid(self,mapping):
        valid_rotors = list(self.reflectors.keys())
        return not(all([i in valid_rotors for i in mapping]))

    


#The enigma class takes in Rotor, Reflector and a list of wirings and handles all of the enigma calculations

#I have opted for an approach which generates the positional adjustments based on the required number of key strokes in the input message.
#It is in this part where we handle the rotation after each key stroke, double stepping and coditional stepping requirements (Beta, Gama dont have a notch and thus dont rotate the next rotor)
#This is housed in the generate_instuction fuction.

#From here we can cycle through these adjustemnts and apply the otehr constraints ring setting adjustemnets 

class Enigma:
    def __init__(self, rotors ,reflector, wiring):
        self.rotors = rotors
        self.base = string.ascii_uppercase
        self.reflector = reflector
        self.ring = rotors[0].ring
        self.message_rotation = None
        self.rotor_keys = list(rotors[0].mapping.keys())
        self.rotor_path = self.rotor_keys[::-1] + ["reflector"] + self.rotor_keys
        self.notch = rotors[0].notch
        self.wiring = wiring
        self.plugboard = Plugboard()
        for i in self.wiring:
            self.plugboard.add(PlugLead(i))
        
        
#The function generate_instuction is responsible for generating the rotational adjustments for each character in the message. These are determined by the number of strokes, rotor notches and rotor specifc criteria (see comentary at the top of Class).
#The output of this fuction is a nested list with tuples of shape 2 in each index entry. Index 0 of each tuple is the character of the message the positional adjustemt related to and index 1 of the tuple is a dictionary of rotors with each valuye being the rotor positional offset for that character in the message. EXAMPLE: [('A', {'I': 17, 'II': 5, 'III': 22}), ('A', {'I': 17, 'II': 5, 'III': 23}),...]
    def generate_instuction(self, message, notch):
        
        notch_assignment = self.notch
        rotations = []
        positions = self.rotors[0].positions
        reversed_rotator_order = self.rotor_keys[::-1]

        
        #Function for handling if the next rotor should be rotatated or not, i.e are we at the notch of that rotor or not.
        #If position = notch we rotate the next rotor and check if that is on a notch.
        def rotation_instruction(rotor_name):
            if chr(positions[rotor_name]+65) in notches:
                positions[rotor_name] = (positions[rotor_name] +  1) % 26
                return True  
            else:
                positions[rotor_name] = (positions[rotor_name] +  1) % 26
                return False  
        
        
        #Check the case of 1 rotor
        if len(self.rotor_keys)==1:
            for _ in message:
                positions[reversed_rotator_order[0]] += 1
                rotations.append(positions.copy())
        


#If we have 2 or more rotors then we need to consider the double step condition on the 2nd rotor if the notches of these rotors align.
#The double step condition is by default set to False and is only activated when the notch alignment occurrs on the two most right rotors.
#Cycle through the length of the message means we generate the positional adjustment for each character in the message to encode/decode.
#Cycle through the reversed rotors as furthest is the fast rotor.
#rotate_next_rotor is default set to True as the furthest rotor (fast rotor) rotates on every key stroke.
        if len(self.rotor_keys)>=2:
            for index,_ in enumerate(message):
                rotate_next_rotor = True    
                double_step = False
                 
       
                for rotor_name in reversed_rotator_order: # e.g [III,II,I]
                    notches = notch_assignment[rotor_name]
                    
                    #Event that we use 4 or more rotors we restrict the movement of the the last
                    if len(self.rotor_keys)>= 4 and rotor_name == self.rotor_keys[0]:
                        break
                    
                    if rotate_next_rotor:
                        rotate_next_rotor = rotation_instruction(rotor_name)
                        continue
                    
                    #Double notch condition: want to check if we are looking at the second rotor and that it is on its notch and that the first is not a notchless rotor. 
                    if rotor_name == reversed_rotator_order[1] and reversed_rotator_order[0] not in ["Beta","Gamma"] and chr(positions[rotor_name]+65) in notches:
                        double_step = chr(positions[rotor_name]+65) in notches
                        
                    #if the above condition is met we can rotate the rotor again
                    if double_step and len(self.rotor_keys)>= 3 and chr(positions[rotor_name]+65) in notches:
                        rotate_next_rotor = rotation_instruction(rotor_name)

                rotations.append(positions.copy())

        #Generate the output variable as a list of adjustments as described in the Class description above
        message_rotation = list(zip(message, rotations))
        self.message_rotation = message_rotation


    
#char_encode is a function for encoding/ decoding a specific character, the character variable here is an index element of the above functions output. e.g  ('A', {'I': 17, 'II': 5, 'III': 22})
#In this function we apply the the neccessary adjustments brought on by the rings settings, rotors and reflectors.     
    def char_encode(self,rotor_path, rotors,reflector, character):
        ring = rotors[0].ring
        rotors =  rotors[0].mapping
        character[0] = self.plugboard.encode(character[0])
        

        for index, rotor in enumerate(rotor_path):
            #Reflector output
            if rotor == "reflector":
                character[0] = reflector.reflection_output(character[0])
                continue
            
            #Forward path through the rotors
            elif index < len(self.rotor_keys):
                ring_adjustment = ord(ring[rotor]) - 65
                adjustment = character[1][rotor] - ring_adjustment 
                inp = (self.base.index(character[0]) + adjustment ) % 26
                rotor_out = rotors[rotor][inp]
                character[0] = self.base[(ord(rotor_out) - 65 - adjustment ) % 26]
                continue
            
            #Backwards path through the rotors
            else:
                ring_adjustment = ord(ring[rotor])
                adjustment = character[1][rotor] - ring_adjustment
                inp = rotors[rotor].index(chr(((ord(character[0]) + adjustment ) % 26) + 65))
                rotor_out = self.base[inp]
                character[0] = self.base[(ord(rotor_out) - adjustment ) % 26]
                continue
                
        character[0] = self.plugboard.encode(character[0])
        
        return character[0]    
    
    
#A function in the class which when called with a message will generate the message positional adjustmnets via generate_instuction.
#Takes in a message string, generates the message path using generate_instuction and then cycles though the message path this function creates, encoding that specific character  
    def mess_encode(self,message):
        notch_values = self.rotors[0].notch
        self.generate_instuction(message, notch_values)
        encoded = ""
        for char in self.message_rotation:
            character = list(char)
            encoded += self.char_encode(self.rotor_path, self.rotors,self.reflector,character)
             
        return encoded
        
