from flask import Blueprint, render_template, request, redirect, url_for 

mips_blueprint = Blueprint("mips_blueprint", __name__, static_folder="static", template_folder="templates")


# GLOBAL VARIABLES 
# a dictionary that contains the relevant r instructions as well as their func code 
r_instructions_dict = {
    "ADD": "100000",
    "SUB": "100010",
    "SLL": "000000", 
    "SRL": "000010", 
    "AND": "100100", 
    "NOR": "100111", 
    "OR":  "100101", 
    "SLT": "101010"
}

# a dictionary that contains the relevant i instructions as well as their opcode 
i_instructions_dict = {
    "ADDI": "8", 
    "LW": "23", 
    "SW": "2b"
}

# a dictionary that contains the binary values of the registers 
registers = {
    "$zero": "00000", 
    "$t0": "01000", 
    "$t1": "01001", 
    "$t2": "01010", 
    "$t3": "01011", 
    "$t4": "01100", 
    "$t5": "01101", 
    "$t6": "01110", 
    "$t7": "11111", 
    "$t8": "11000", 
    "$t9": "11001", 
    "$s0": "10000", 
    "$s1": "10001", 
    "$s2": "10010", 
    "$s3": "10011", 
    "$s4": "10100",
    "$s5": "10101", 
    "$s6": "10110", 
    "$s7": "10111" 
}




@mips_blueprint.route("/mips", methods=["GET", "POST"])
def mips(): 

    # initialize global variables within view function
    global r_instructions_dict
    global i_instructions_dict
    test = "" 

    
    if request.method == "POST": 
       
        output = "" 
        mips_instruction = request.form.get('mips_instruction')
     
        # creates an array with elements separated by the commas 
        # ADD $s1, $s2, $s2 -> ["ADD", '$s1', '$s2', '$s2']
        index = mips_instruction.find(" ")
        instr_type = mips_instruction[0:index]
        mips_instruction = mips_instruction[index+1:]
        var_array = "" 
       

        if (instr_type.upper() in r_instructions_dict or instr_type.upper() in i_instructions_dict): 
            # commas 
            var_array = mips_instruction.split(',') 
            print(var_array)

        elif instr_type.upper() == "J": 
            # if instruction is j instruction, there will not be any commas in the instruction
            var_array = mips_instruction



        #check if the first element of the var_array is in any specific type of instructions 
        if instr_type.upper() in r_instructions_dict: 
            output = handle_r(var_array, instr_type.upper())
            
        
        elif instr_type.upper() in i_instructions_dict: 
            output = handle_i(var_array, instr_type.upper())

        elif instr_type.upper() == "J":
            output = handle_j(var_array, instr_type.upper()) 

        else: 
            # invalid instruction 
            return redirect("/error")

        test = convert_binary_to_hex(output)
    
    return render_template("mips.html",input=request.form.get('mips_instruction'),test=test)






# global methods 

# returns a string with the binary format of the r instruction 
def handle_r(var_array, instr_type): 

    # define variables 
    global r_instructions_dict
    global registers
    inst_type = instr_type
    print(inst_type)
    instruction_en = "000000"

    # r instructions opcode all start with 0 
    if ( inst_type == "ADD" or inst_type == "SUB" or inst_type == "SLT" or inst_type == "AND" or inst_type == "OR" or inst_type == "NOR"):
        if (var_array[1] in registers): 
            instruction_en += registers[var_array[1]]
        else: 
            instruction_en += '{0:05b}'.format(int(var_array[1][1:]))
        
        if (var_array[2] in registers): 
            instruction_en += registers[var_array[2]]
        else: 
            instruction_en += '{0:05b}'.format(int(var_array[2][1:]))

        if var_array[0] in registers: 
            instruction_en += registers[var_array[0]]
        else: 
            instruction_en += '{0:05b}'.format(int(var_array[0][1:]))

        # no shamt since add is not a shift function 
        instruction_en += "00000"

        if inst_type == "ADD": 
            instruction_en += r_instructions_dict['ADD']
        elif inst_type == "SUB": 
            print("b")
            instruction_en += r_instructions_dict['SUB']
        elif inst_type == "SLT": 
            instruction_en += r_instructions_dict['SLT']
        elif inst_type == "AND": 
            instruction_en += r_instructions_dict['AND']
        elif inst_type == "OR": 
            instruction_en += r_instructions_dict['OR']
        else: 
            instruction_en += r_instructions_dict["NOR"]


    elif ( inst_type == "SLL" or inst_type == "SRL" ): 
        
        # for all shift instructions the source register will always be set to zero 
        instruction_en += "00000" 

        # include rt instruction
        if var_array[1] in registers: 
            instruction_en += registers[var_array[1]]
        else: 
            instruction_en += '{0:05b}'.format(int(var_array[1][1:]))

        # include rd instruction 
        if var_array[0] in registers: 
            instruction_en += registers[var_array[0]]
        else: 
            instruction_en += '{0:05b}'.format(int(var_array[0][1:]))

        # include shamt instruction 
        instruction_en += '{0:05b}'.format(int(var_array[2]))

        # include funct code 
        if inst_type == "SRL": 
            instruction_en += r_instructions_dict["SRL"]
        else: 
            instruction_en += r_instructions_dict["SLL"]

    return instruction_en
        








def handle_i(var_array, instr_type): 
    global i_instructions_dict
    global registers 
    instruction_en = "" 

    # store and load instructions 
    if (instr_type == "SW" or instr_type == "LW"): 
        if instr_type == "SW": 
            instruction_en += "101011"
        else: 
            instruction_en += "010111"

        target_register = var_array[0]
        offset_index = var_array[1].find("(")
        offset = var_array[1][0:offset_index]
        source_register = var_array[1][offset_index+1:]
        print(source_register)
        source_register = source_register[:-1]
        print(source_register)

        # encode source register into the instruction
        if source_register in registers: 
            instruction_en += registers[source_register]
        else:
            instruction_en += '{0:05b}'.format(int(source_register[1:])) 

        # encode target register into the instruction
        if target_register in registers: 
            instruction_en += registers[target_register]
        else: 
            instruction_en += '{0:05b}'.format(int(target_register[1:])) 

        # encode the immediate offset into the instruction 
        instruction_en += '{0:016b}'.format(int(offset))
        
    elif (instr_type == "ADDI"): 

        # opcode for the ADDI instruction
        instruction_en += "001000"

        source_register = var_array[1]
        target_register = var_array[0]
        immediate = var_array[2]

        if source_register in registers: 
            instruction_en += registers[source_register]
        else: 
            instruction_en += '{0:05b}'.format(int(source_register[1:])) 

        if target_register in registers: 
            instruction_en += registers[target_register]
        else: 
            instruction_en += '{0:05b}'.format(int(target_register[1:])) 

        # if the immediate value is not negative 
        if immediate[0] != "-": 
            instruction_en += '{0:016b}'.format(int(immediate))
        else: 
            # function that will convert the 16 bit number to its equivalent 2s complement 
            instruction_en += twos_complement(immediate) 
        
    return instruction_en




    





def handle_j(var_array, instr_type):
    global i_instructions_dict
    global registers 

    instruction_en = "000010"

    # get pc + 4 instruction 
    pc_add_four = "0000"
    instruction_en += pc_add_four

    # include address provided by the user + the 2nd two bits that are not included 
    instruction_en += var_array + "00"
    return instruction_en 



    
   








def convert_binary_to_hex(binary_string): 
    print(binary_string)
    hex_string = ""
    components = []

    for i in range(8): 
        components.append(0)
    

    components[0] = binary_string[0:4]
    components[1] = binary_string[4:8]
    components[2] = binary_string[8:12]
    components[3] = binary_string[12:16]
    components[4] = binary_string[16:20]
    components[5] = binary_string[20:24]
    components[6] = binary_string[24:28]
    components[7] = binary_string[28:]


    for i in range(8): 
        hex_string += '{0:01x}'.format(int(components[i],2)) + " "
    print(hex_string)


    return hex_string


# function that will convert a negative number to its corresponding 2s complement
def twos_complement(number): 
    # slice the string so that we can ignore the negative number in the front 
    number = number[1:]
    carry = "0000000000000001"
    # convert the immediate magnitude to its binary values
    binary = '{0:016b}'.format(int(number))
    invert_binary = ""

    for b in binary: 
        if b == "0": 
            invert_binary += "1"
        else: 
            invert_binary += "0"

    value = str(bin(int(invert_binary, 2) + int(carry, 2)))

    # string returns a leading 0b so we need to exclude it
    value = value[2:]

    # get the leading zeroes
    while len(value) != 16:
        value = "1" + value 
   
    return value
