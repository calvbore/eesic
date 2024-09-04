import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, ClockCycles

@cocotb.test()
async def test_exit_code(dut):
    opcode = 0x00

    dut.opcode.value = opcode

    await Timer(1, "step")

    assert dut.exit.value == 1
    assert dut.gas.value == 0

# copied and modified from push_cocotb.py
@cocotb.test()
async def push_push_data(dut):
    data = random.getrandbits(256)

    opcode = 0x5f

    dut.code_data.value = data

    for num in range(33):
        inst = opcode + num
        # print(hex(inst))
        # print(hex(data))
        dut.opcode.value = inst

        await Timer(1, "step")

        mask = ~((2**(8*(32-num)))-1)
        masked_data = data & mask;
        assert (masked_data >> (8*(32-num))) == dut.data_out.value[0]

        # print(dut.opcode.value)
        # print(dut.push.opcode.value)

        # print(dut.push.push_bytes.value)
        # print(dut.push.pc_nxt.value)

        # print(dut.push_pc.value)
        # print(dut.pc_nxt.value)

        # test gas output
        if inst == 0x5f:
            assert dut.gas.value    == 2
            assert dut.pc_nxt.value == 1
        else:
            assert dut.gas.value    == 3
            assert dut.pc_nxt.value == num

        assert dut.push_num.value == 1

        await Timer(1, "step")

# copied and modified from dup_cocotb.py
@cocotb.test()
async def test_dup_data(dut):
    data = [random.getrandbits(256) for _ in range(17)]

    # print(data)

    opcode = 0x80

    dut.stack_data.value = data

    for num in range(16):
        inst = opcode + num
        dut.opcode.value = inst

        await Timer(1, "step")

        # print(hex(inst))
        # print(hex(data[num]))
        # print(hex(dut.data_out.value))

        assert data[num] == dut.data_out.value[0]
        
        # test gas output
        assert dut.gas.value == 3

        assert dut.push_num.value == 1

        assert dut.pc_nxt.value == 1

# copied and modified from swap_cocotb.py
@cocotb.test()
async def test_data_swaps(dut):
    opcode = 0x90

    for num in range(16):
        data = [random.getrandbits(256) for _ in range(17)]
        dut.stack_data.value = data

        inst = opcode + num
        dut.opcode.value = inst

        await Timer(1, "step")

        # print(hex(data[0]))
        # print(hex(dut.data_out.value[num+1]))

        for i in range(17):
            if i == 0:
                assert data[num+1] == dut.data_out.value[0]
            elif i == num+1:
                assert data[0] == dut.data_out.value[num+1]
            else:
                assert data[i] == dut.data_out.value[i]

        # test gas output
        assert dut.gas.value == 3

        assert dut.push_num.value == num+2
        assert dut.pop_num.value  == num+2

        assert dut.pc_nxt.value == 1


@cocotb.test()
async def test_inst_switching(dut):
    codes =  [0x00]                        # exit code
    codes += [0x5f + n for n in range(33)] # push codes
    codes += [0x80 + n for n in range(16)] #  dup codes
    codes += [0x90 + n for n in range(16)] # swap codes

    # for c in codes:
    #     print(hex(c))

    stack_height = random.randint(0, 17)

    dut.stack_height.value = stack_height

    stack_data = [random.getrandbits(256) for _ in range(stack_height)] + [0]*(17-stack_height)
    code_data  = random.getrandbits(256)

    dut.stack_data.value = stack_data
    dut.code_data.value  = code_data

    for num in range(96):
        r = random.randint(0, len(codes)-1)
        opcode = codes[r]
        # print(hex(opcode))

        dut.opcode.value = opcode

        await Timer(1, "step")

        if opcode == 0x0:
            assert dut.exit.value == 1
            assert dut.gas.value == 0
        elif opcode >= 0x5f and opcode < 0x80:
            await assert_push_constraints(
                dut,
                opcode,
                code_data,
                stack_data,
                stack_height
            )
        elif opcode >= 0x80 and opcode < 0x90:
            await assert_dup_constraints(
                dut,
                opcode,
                code_data,
                stack_data,
                stack_height
            )
        elif opcode >= 0x90 and opcode < 0xa0:
            await assert_swap_constraints(
                dut,
                opcode,
                code_data,
                stack_data,
                stack_height
            )

        await Timer(1, "step")



async def assert_push_constraints(
    dut, 
    opcode, 
    code_data, 
    stack_data, 
    stack_height
):
    assert opcode >= 0x5f and opcode < 0x80
    num = opcode - 0x5f

    mask = ~((2**(8*(32-num)))-1)
    masked_data = code_data & mask
    assert (masked_data >> (8*(32-num))) == dut.data_out.value[0]

    if opcode == 0x5f:
        assert dut.gas.value    == 2
        assert dut.pc_nxt.value == 1
    else:
        assert dut.gas.value    == 3
        assert dut.pc_nxt.value == num

    assert dut.push_num.value == 1

async def assert_dup_constraints(
    dut, 
    opcode, 
    code_data, 
    stack_data, 
    stack_height
):
    assert opcode >= 0x80 and opcode < 0x90
    num = opcode - 0x80

    if stack_height < num+1:
        assert dut.exit.value == 1

    assert stack_data[num] == dut.data_out.value[0]

    # test gas output
    assert dut.gas.value == 3

    assert dut.push_num.value == 1

    assert dut.pc_nxt.value == 1
    
async def assert_swap_constraints(
    dut, 
    opcode, 
    code_data, 
    stack_data, 
    stack_height
):
    assert opcode >= 0x90
    num = opcode - 0x90

    if stack_height < num+2:
        assert dut.exit.value == 1

    for i in range(17):
        if i == 0:
            assert stack_data[num+1] == dut.data_out.value[0]
        elif i == num+1:
            assert stack_data[0] == dut.data_out.value[num+1]
        else:
            assert stack_data[i] == dut.data_out.value[i]

    # test gas output
    assert dut.gas.value == 3

    assert dut.push_num.value == num+2
    assert dut.pop_num.value  == num+2

    assert dut.pc_nxt.value == 1