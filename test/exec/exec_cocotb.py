import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, ClockCycles


# OPCODE CONSTRAINTS #

# PUSH #
async def assert_push_constraints(
    dut, 
    opcode, 
    code_data, 
    old_stack_data,
    old_stack_height
):
    assert opcode >= 0x5f and opcode < 0x80
    num = opcode - 0x5f

    mask = ~((2**(8*(32-num)))-1)
    masked_data = code_data & mask
    assert (masked_data >> (8*(32-num))) == dut.stack_data_out.value[0]
    assert old_stack_data[0] == dut.stack_data_out.value[1]

    assert old_stack_height+1 == dut.stack_height.value

    if opcode == 0x5f:
        assert dut.gas.value  == 2
        assert dut.pc_o.value == 1
    else:
        assert dut.gas.value  == 3
        assert dut.pc_o.value == num

    assert dut.push_num.value == 1

# DUP #
async def assert_dup_constraints(
    dut, 
    opcode, 
    old_stack_data, 
    old_stack_height
):
    assert opcode >= 0x80 and opcode < 0x90
    num = opcode - 0x80

    if int(old_stack_height) < num+1:
        assert dut.exit.value == 1
        assert old_stack_data == dut.stack_data_out.value
    else:
        assert old_stack_data[num] == dut.stack_data_out.value[0]

    # test gas output
    assert dut.gas.value == 3

    assert dut.push_num.value == 1

    assert dut.pc_o.value == 1
    
# SWAP #
async def assert_swap_constraints(
    dut, 
    opcode, 
    old_stack_data, 
    old_stack_height
):
    assert opcode >= 0x90
    num = opcode - 0x90

    if int(old_stack_height) < num+2:
        # print("exit: ", int(dut.stack_height.value))
        assert dut.exit.value == 1
        assert old_stack_data == dut.stack_data_out.value
    else:
        # print(int(dut.stack_height.value))
        for i in range(17):
            if i == 0:
                assert old_stack_data[num+1] == dut.stack_data_out.value[0]
            elif i == num+1:
                # print(int(dut.stack_height.value))
                # print(hex(old_stack_data[0]))
                # print(hex(dut.stack_data_in.value[0]))
                # print(hex(dut.stack_data_out.value[num+1]))
                assert old_stack_data[0] == dut.stack_data_out.value[num+1]
            else:
                assert old_stack_data[i] == dut.stack_data_out.value[i]

    # test gas output
    assert dut.gas.value == 3

    assert dut.push_num.value == num+2
    assert dut.pop_num.value  == num+2

    assert dut.pc_o.value == 1

# TESTS #

@cocotb.test()
async def test_codes(dut):
    codes =  [0x00]                        # exit code
    codes += [0x5f + n for n in range(33)] # push codes
    codes += [0x80 + n for n in range(16)] #  dup codes
    codes += [0x90 + n for n in range(16)] # swap codes


    dut.rst.value = 1
    await Timer(1, "step")
    dut.rst.value = 0
    await Timer(1, "step")


    code_data = random.getrandbits(256)

    dut.code_data.value  = code_data

    for num in range(96):
        r = random.randint(0, len(codes)-1)
        opcode = codes[r]
        # print(hex(opcode))

        # previous state of the stack
        old_stack_data = dut.stack_data_out.value
        old_stack_height = dut.stack_height.value

        dut.opcode.value = opcode

        dut.clk.value = 1
        await Timer(1, "step")
        dut.clk.value = 0
        await Timer(1, "step")

        if opcode == 0x0:
            assert dut.exit.value == 1
            assert dut.gas.value == 0
        elif opcode >= 0x5f and opcode < 0x80:
            await assert_push_constraints(
                dut,
                opcode,
                code_data,
                old_stack_data,
                old_stack_height
            )
        elif opcode >= 0x80 and opcode < 0x90:
            await assert_dup_constraints(
                dut,
                opcode,
                old_stack_data,
                old_stack_height
            )
        elif opcode >= 0x90 and opcode < 0xa0:
            await assert_swap_constraints(
                dut,
                opcode,
                old_stack_data,
                old_stack_height
            )

        # print(dut.exit.value)
        # dut.clk.value = 0
        # await Timer(1, "step")

# test sequential pushes are behaving properly
@cocotb.test()
async def test_push_to_stack(dut):
    codes = [0x5f + n for n in range(33)] # push codes

    dut.rst.value = 1
    await Timer(1, "step")
    dut.rst.value = 0
    await Timer(1, "step")

    for num in range(96):
        r = random.randint(0, len(codes)-1)
        opcode = codes[r]
        # print(hex(opcode))

        code_data = random.getrandbits(256)
        dut.code_data.value  = code_data

        # previous state of the stack
        old_stack_data = dut.stack_data_out.value
        old_stack_height = dut.stack_height.value

        dut.opcode.value = opcode

        dut.clk.value = 1
        await Timer(1, "step")
        dut.clk.value = 0
        await Timer(1, "step")

        # print(hex(code_data))
        # print(hex(dut.stack_data_out.value[0]))
        # print(dut.exit.value)
        await assert_push_constraints(
            dut,
            opcode,
            code_data,
            old_stack_data,
            old_stack_height
        )

# test dupes after pushes to the stack
@cocotb.test()
async def test_dup_on_stack(dut):
    push_codes = [0x5f + n for n in range(33)] # push codes
    dup_codes  = [0x80 + n for n in range(16)] #  dup codes

    dut.rst.value = 1
    await Timer(1, "step")
    dut.rst.value = 0
    await Timer(1, "step")

    for num in range(96):
        # push random on to stack
        r = random.randint(0, len(push_codes)-1)
        opcode = push_codes[r]
        # print(hex(opcode))

        code_data = random.getrandbits(256)
        dut.code_data.value  = code_data

        # previous state of the stack
        old_stack_data = dut.stack_data_out.value
        old_stack_height = dut.stack_height.value

        dut.opcode.value = opcode

        # cycle clock
        dut.clk.value = 1
        await Timer(1, "step")
        dut.clk.value = 0
        await Timer(1, "step")

        await assert_push_constraints(
            dut,
            opcode,
            code_data,
            old_stack_data,
            old_stack_height
        )

        # random duplicate stack element
        r = random.randint(0, len(dup_codes)-1)
        opcode = dup_codes[r]
        # print(hex(opcode))

        old_stack_data = dut.stack_data_out.value
        old_stack_height = dut.stack_height.value

        dut.opcode.value = opcode

        # cycle clock
        dut.clk.value = 1
        await Timer(1, "step")
        dut.clk.value = 0
        await Timer(1, "step")

        await assert_dup_constraints(
            dut,
            opcode,
            old_stack_data,
            old_stack_height
        )

# test swaps after pushing to stack
@cocotb.test()
async def test_swap_on_stack(dut):
    push_codes = [0x5f + n for n in range(33)] # push codes
    swap_codes = [0x90 + n for n in range(16)] # swap codes

    dut.rst.value = 1
    await Timer(1, "step")
    dut.rst.value = 0
    await Timer(1, "step")

    for num in range(96):
        # push random on to stack
        r = random.randint(0, len(push_codes)-1)
        opcode = push_codes[r]
        # print(hex(opcode))

        code_data = random.getrandbits(256)
        dut.code_data.value  = code_data

        # previous state of the stack
        old_stack_data = dut.stack_data_out.value
        old_stack_height = dut.stack_height.value

        dut.opcode.value = opcode

        # cycle clock
        dut.clk.value = 1
        await Timer(1, "step")
        dut.clk.value = 0
        await Timer(1, "step")

        await assert_push_constraints(
            dut,
            opcode,
            code_data,
            old_stack_data,
            old_stack_height
        )

        # random duplicate stack element
        r = random.randint(0, len(swap_codes)-1)
        opcode = swap_codes[r]
        # print(hex(opcode))

        old_stack_data = dut.stack_data_out.value
        old_stack_height = dut.stack_height.value

        dut.opcode.value = opcode

        # cycle clock
        dut.clk.value = 1
        await Timer(1, "step")
        dut.clk.value = 0
        await Timer(1, "step")

        await assert_swap_constraints(
            dut,
            opcode,
            old_stack_data,
            old_stack_height
        )