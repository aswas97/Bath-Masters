from enigma import  PlugLead, Plugboard, Reflector, Rotor, Enigma
import copy
import itertools
import string

#simple cycle ober the refelctor types and decode for each and search for the crib
#since enigma is symetric we you dont need to adjust to decode an encrypted message.
#very basic


class Code1_decode_enigma:
    def __init__(self):
        self.cribs = "SECRETS"
        self.rotor_mappings = ["Beta","Gamma","V"]
        self.initial_positions = ["M","J","M"]
        self.ring_setting = [4,2,14]
        self.wiring = ["KI", "XN", "FL"]
        self.rotors = [Rotor(self.rotor_mappings, self.initial_positions,   self.ring_setting)]
        self.reflector = ["A","B","C"]
        
#simplpy cycle through generating the decoded message for each case and check for the crib            
    def decode(self,message):
        decoded = []
        for ref in self.reflector:
            reflector_test = Reflector(mapping = ref)
            rotors_copy = copy.deepcopy(self.rotors)
            enigma = Enigma(rotors_copy, reflector_test, self.wiring)
            decoded_message = enigma.mess_encode(message)
            if self.cribs in decoded_message:
                print("the refelctor is: ", ref)
                decoded.append(decoded_message)
        return decoded    
    
    
    
    
#the unkown here is that we dont know the initial positions
#simple itertools calculations for generating the positons 
#the positions is alwasy part of the alphabet so can do repeat = 3


class Code2_decode_enigma:
    def __init__(self):
        self.cribs = "UNIVERSITY"
        self.rotor_mappings = ["Beta","I","III"] 
        self.initial_positions = list(itertools.product(string.ascii_uppercase, repeat=3))
        self.ring_setting = [23,2,10]
        self.wiring = ["VH", "PT", "ZG", "BJ", "EY", "FS"]
        self.rotors = None
        self.reflector = Reflector("B")
        
#simplpy cycle through generating the decoded message for each case and check for the crib            
    def decode(self,message):
        decoded = []
        for pos_test in self.initial_positions:
            self.rotors = [Rotor(self.rotor_mappings, pos_test,   self.ring_setting)]    
            enigma = Enigma(self.rotors, self.reflector, self.wiring)
            decoded_message = enigma.mess_encode(message)
            if self.cribs in decoded_message:
                print("The initial position is: ", pos_test)
                decoded.append(decoded_message)
        return decoded  
    
    
    
    
#Using itertolls porducts allows for combinations when we have multiple missing as it generates an object with all /n
#The possible variables with multiple missing inputs
#We simply iterate over these and decode each.


class Code3_decode_enigma:
    def __init__(self):
        self.cribs = "THOUSANDS"
        self.rotor_options = list(itertools.product(["II","IV", "Beta", "Gamma"],  repeat=3))
        self.reflector_options = ["A","B","C"]
        self.ring_options =  list(itertools.product([2, 4, 6, 8, 20, 22, 24, 26],  repeat=3))
        self.options = list(itertools.product(self.rotor_options,self.reflector_options,self.ring_options))
        self.initial_positions = ["E","M","Y"]
        self.wiring = ["FH", "TS", "BE", "UQ", "KD", "AL"]
        self.rotors = None
        
        
#simplpy cycle through generating the decoded message for each case and check for the crib
    def decode(self,message):
        decoded = []
        for test in self.options:
            reflector = Reflector(test[1])
            rotor_mappings, ring_setting = test[0], test[2]
            self.rotors = [Rotor(rotor_mappings, self.initial_positions, ring_setting)]    
            
            enigma = Enigma(self.rotors, reflector, self.wiring)
            decoded_message = enigma.mess_encode(message)
            if self.cribs in decoded_message:
                print("The rotors used are: ", test[0],", the reflector used is: ", test[1] ,"and the ring settings used are: ", test[2])
                decoded.append(decoded_message)
        return decoded
    
    
    
    
    
class Code4_decode_enigma:
    
    #missing mappings for a number of wiring pairs - specifically 2.
    #Can brute force by finding the number of possible mappnigs
    #Since the know wires dont change we can fix these in the itertools function products
    #The itertools function will generate all posible choices when we give it the fixed inputs as well as the unknowns (the ?'s')
    #The output has various possible which include the crib, since there are only 10 we can deduce the solution by reading the decoded
    
    
    def __init__(self):
        self.cribs = "TUTOR" 
        self.initial_positions = ["S","W","U"]
        self.rotor_mappings =["V","III","IV"]
        self.ring_settings = [24,12,10]
        self.rotors = None
        self.wiring = ["WP", "RJ", "A?", "VF", "I?", "HN","CG","BS"]
        self.letters = ''.join(self.wiring)
        self.reflector = Reflector("A")
        self.rotors = [Rotor(self.rotor_mappings, self.initial_positions , self.ring_settings)]    
             
            
    def decode(self,message):
        
        map_choice = string.ascii_uppercase
        
        for i in self.letters:
            map_choice = map_choice.replace(i,"")
            
            
        wiring = list(itertools.product([self.wiring[0]],
                       [self.wiring[1]],
                       [''.join(map(str, i )) for i in list(itertools.product(["A"],map_choice))],
                       [self.wiring[3]],
                       [''.join(map(str, i )) for i in list(itertools.product(["I"],map_choice))],
                       [self.wiring[5]],[self.wiring[6]], [self.wiring[7]]))
        
        decoded = []
        
        for test in range(len(wiring)):
            rotors_copy = copy.deepcopy(self.rotors)
            enigma = Enigma(rotors_copy, self.reflector, wiring[test])
            decoded_message = enigma.mess_encode(message)
            
            if self.cribs in decoded_message:
                print("Decoded message: ", decoded_message, "given wires:", wiring[test])
                decoded.append(decoded_message)
                
        return decoded
    
    


#Swaps to the internal wiring of the reflector, made tghis difficult to scrack due to the large number of possible permutations the swaps would reult in.
    #Using the sheet information I narrowed down the crib to INSTAGRAM however initial tests yeileded no success for teh full crib so i reduced it down to half the size to try and get a partial match.

class Code5_decode_enigma:
    def __init__(self):
        self.crib = "INSTAGRAM"
        self.rotor_mappings = ["V","II","IV"]
        self.initial_positions = ["A","J","L"]
        self.ring_setting = [6,18,7]
        self.wiring = ["UG", "IE", "PO","NX", "WT"]
        self.rotors = [Rotor(self.rotor_mappings, self.initial_positions, self.ring_setting)]
        self.reflectors = {"A":['E','J','M','Z','A','L','Y','X','V','B','W','F','C','R','Q','U','O','N','T','S','P','I','K','H','G','D'],
                           "B":['Y','R','U','H','Q','S','L','D','P','X','N','G','O','K','M','I','E','B','F','Z','C','W','V','J','A','T'],
                           "C":['F','V','P','J','I','A','O','Y','E','D','R','Z','X','W','G','C','T','K','U','Q','S','B','N','M','H','L'],
                          }
        self.adjusted_refelctor = None
        
        
        
            
    def decode(self, message):
        decoded = []
        
        def swap1(message):
            #Iterate through reflectors on the first swap as unsure which is the standard refelctor
            #I set up a custom refelctor option for the testing here as we are making adjustmesnts to the reflector 
            for ref in list(self.reflectors.values()):
                reflector = ref.copy()
                for comb in itertools.combinations(reflector, 2):
                    comb_list = list(itertools.combinations(reflector, 2))
                    modified_reflector = reflector.copy()
                    
                    #the switching of the combinations is done here 
                    modified_reflector[reflector.index(comb[0])], modified_reflector[reflector.index(comb[1])] = modified_reflector[reflector.index(comb[1])], modified_reflector[reflector.index(comb[0])]

                    rotors_copy = copy.deepcopy(self.rotors)
                    test_reflector = Reflector(["CUSTOM"], custom=modified_reflector)
                    enigma = Enigma(rotors_copy, test_reflector, self.wiring)
                    decoded_message = enigma.mess_encode(message)
                    
                    #since unsure if the full crib wil be in the first swap we can iterator over a subset.
                    #chose 4 as nearly half, if less more likely t get false positives
                    for i in range(4,len(self.crib)):
                        strip_crib = self.crib[:i]
                        if strip_crib in decoded_message:
                            self.adjusted_refelctor = modified_reflector
                            print("Decoded message of: ",decoded_message," when swapping:", comb, "on refelctor: B")
                            
            #After doing the initial run through I managed to decode by eye part of the message after 1 swap.
            #Swapping ('Y', 'P') yeilded YOUCAPFOMLONMYIOGONINSTPGCAIATFELEBOFHSFFMANN
            # which using intuition I can assume the firts part of the srtring is "YOUCANFOLLOWMY"
            #Cannot confirm yet so lets earch for words "YOU" and "INSTA" next
                    

            
        def swap2(message, reflector):
            print("-----------------------------")
            print("Swap2")
            other_cribs = ["INSTA","YOU"]
            for comb in itertools.combinations(reflector, 2):

                comb_list = list(itertools.combinations(reflector, 2))
                modified_reflector = reflector.copy()
                modified_reflector[reflector.index(comb[0])], modified_reflector[reflector.index(comb[1])] = modified_reflector[reflector.index(comb[1])], modified_reflector[reflector.index(comb[0])]

                rotors_copy = copy.deepcopy(self.rotors)
                test_reflector = Reflector(["CUSTOM"], custom=modified_reflector)
                enigma = Enigma(rotors_copy, test_reflector, self.wiring)
                decoded_message = enigma.mess_encode(message)


                if all(word in decoded_message for word in other_cribs):
                    decoded.append(decoded_message)
                    self.adjusted_refelctor = modified_reflector
                    print("Decoded message of: ",decoded_message," with an addition swap of: ", comb)

            #Applying the next swap while also using "INSTA" and "YOU" as cribs tighens our search again.
            #"DOG"this time looking at the oucome I see "DOG" in the string which we can add to the crib list
            #USING an additon CRIB tightens our search which yeild an improvement if we switch ('R', 'Q') 
            
        
        def swap3(message, reflector):
            print("-----------------------------")
            print("Swap3")
            other_cribs = ["YOU","DOG","INSTAGRAM"]
            for comb in itertools.combinations(reflector, 2):

                comb_list = list(itertools.combinations(reflector, 2))
                modified_reflector = reflector.copy()
                modified_reflector[reflector.index(comb[0])], modified_reflector[reflector.index(comb[1])] = modified_reflector[reflector.index(comb[1])], modified_reflector[reflector.index(comb[0])]

                rotors_copy = copy.deepcopy(self.rotors)
                test_reflector = Reflector(["CUSTOM"], custom=modified_reflector)
                enigma = Enigma(rotors_copy, test_reflector, self.wiring)
                decoded_message = enigma.mess_encode(message)


                if all(word in decoded_message for word in other_cribs):
                    decoded.append(decoded_message)
                    self.adjusted_refelctor = modified_reflector
                    print("Decoded message of: ",decoded_message," with an addition swap of: ", comb)
                    
            #The string nearly makes sense and if we use the deduction we made earlier that "FOLLOW" is in the string we can add another crib
            #this again yeild an improvement when we swap ('I','A') and actually fully decodes the message
            #I know this as I search the page on instagram and could see it was a valid account.
                    
                    
        def swap4(message, reflector):
            print("-----------------------------")
            print("Swap4")
            other_cribs = ["YOU","FOLLOW","DOG","INSTAGRAM"]
            for comb in itertools.combinations(reflector, 2):

                comb_list = list(itertools.combinations(reflector, 2))
                modified_reflector = reflector.copy()
                modified_reflector[reflector.index(comb[0])], modified_reflector[reflector.index(comb[1])] = modified_reflector[reflector.index(comb[1])], modified_reflector[reflector.index(comb[0])]

                rotors_copy = copy.deepcopy(self.rotors)
                test_reflector = Reflector(["CUSTOM"], custom=modified_reflector)
                enigma = Enigma(rotors_copy, test_reflector, self.wiring)
                decoded_message = enigma.mess_encode(message)


                if all(word in decoded_message for word in other_cribs):
                    decoded.append(decoded_message)
                    self.adjusted_refelctor = modified_reflector
                    print("Decoded message of: ",decoded_message," with an addition swap of: ", comb)
                    
            # This highlights that ('I', 'A') is a chnage as this only has the M missing from "INSTAGRAM"
            # again now looking down the positive results it looks like 

        
        swap1(message)    
        swap2(message, self.adjusted_refelctor)
        swap3(message, self.adjusted_refelctor)   
        swap4(message, self.adjusted_refelctor)  


        return decoded
