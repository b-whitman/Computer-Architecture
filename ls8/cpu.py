"""CPU functionality."""

import sys

HLT  = 0b00000001
LDI  = 0b10000010
PRN  = 0b01000111
MUL  = 0b10100010
PUSH = 0b01000101
POP  = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.fl = 0

    def load(self):
        """Load a program into memory."""

        address = 0
        
        program = []

        if len(sys.argv) < 2:
            print("missing filename argument")
            sys.exit(1)

        file_path = sys.argv[1]
        with open(file_path) as f:

            for line in f:
                split_line = line.split('#')[0]
                stripped_split_line = split_line.strip()

                if stripped_split_line != "":
                    command = int(stripped_split_line, 2)

                    program.append(command)

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, mar):
        if mar < len(self.ram):
            number_to_read = self.ram[mar]
        else:
            number_to_read = None    
        return number_to_read

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:

            ir = self.pc
            command = self.ram[ir]

            # print(command)

            operand_a = self.ram_read(ir+1)
            operand_b = self.ram_read(ir+2)

            if command == LDI:
                register_address = operand_a
                num_to_save = operand_b
                self.reg[register_address] = num_to_save

            elif command == PRN:
                register_address = operand_a
                number_to_print = self.reg[register_address]
                print(number_to_print)
            
            elif command == MUL:
                self.alu('MUL', operand_a, operand_b)

            elif command == PUSH:
                # Decrement self.reg[7]
                self.reg[7] -= 1
                # Copy value in given register to address pointed to by self.reg[7]
                register_address = operand_a
                value = self.reg[register_address]
                sp = self.reg[7]
                self.ram[sp] = value

            elif command == POP:
                # Copy value from RAM at SP to given register
                register_address = operand_a
                sp = self.reg[7]
                value = self.ram[sp]
                self.reg[register_address] = value
                # Increment SP
                self.reg[7] += 1

            elif command == HLT:
                running = False

            number_of_operands = command >> 6
            self.pc += (1 + number_of_operands)
