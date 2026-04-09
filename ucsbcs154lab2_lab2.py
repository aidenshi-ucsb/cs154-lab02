import pyrtl

### DECLARE WIRE VECTORS, INPUT, MEMBLOCK ###
rf = pyrtl.MemBlock(bitwidth=32, addrwidth=5)
instr = pyrtl.Input(bitwidth=32)

rs = pyrtl.WireVector(bitwidth=5, name='rs')
rt = pyrtl.WireVector(bitwidth=5, name='rt')
rd = pyrtl.WireVector(bitwidth=5, name='rd')
sh = pyrtl.WireVector(bitwidth=5, name='sh')
funct = pyrtl.WireVector(bitwidth=6, name='funct')

data0 = pyrtl.WireVector(bitwidth=32, name='data0')
data1 = pyrtl.WireVector(bitwidth=32, name='data1')

alu_out = pyrtl.WireVector(bitwidth=32, name='alu_out')

### DECODE INSTRUCTION AND RETRIEVE RF DATA ###
rs <<= instr[21:26]
rt <<= instr[16:21]
rd <<= instr[11:16]
sh <<= instr[6:11]
funct <<= instr[0:6]

data0 <<= rf[rs]
data1 <<= rf[rt]


### ADD ALU LOGIC HERE ###
with pyrtl.conditional_assignment:
    with funct == 0x20:
        alu_out |= data0 + data1
    with funct == 0x22:
        alu_out |= data0 - data1
    with funct == 0x24:
        alu_out |= data0 & data1
    with funct == 0x25:
        alu_out |= data0 | data1
    with funct == 0x26:
        alu_out |= data0 ^ data1
    with funct == 0x00:
        alu_out |= pyrtl.shift_left_logical(data1, sh)
    with funct == 0x02:
        alu_out |= pyrtl.shift_right_logical(data1, sh)
    with funct == 0x03:
        alu_out |= pyrtl.shift_right_arithmetic(data1, sh)
    with funct == 0x2a:
        alu_out |= pyrtl.signed_lt(data0, data1)
    with pyrtl.otherwise:
        alu_out |= 0

### WRITEBACK ###
rf[rd] <<= alu_out
