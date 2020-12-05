"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.registers[7] = 0xF4
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

            operand_a = self.ram_read(ir+1)
            operand_b = self.ram_read(ir+2)

            if command == LDI:
                register_address = operand_a
                num_to_save = operand_b
                self.ram_write(register_address, num_to_save)
                self.pc += 2

            elif command == PRN:
                register_address = operand_a
                number_to_print = self.ram[register_address]
                print(number_to_print)
                self.pc += 1

            elif command == HLT:
                running = False

            self.pc += 1
