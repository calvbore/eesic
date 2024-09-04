import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, ClockCycles

@cocotb.test()
async def push_sliced_rand_data(dut):
    data = random.getrandbits(256)

    opcode = 0x5f

    dut.data_in.value = data

    for num in range(33):
        inst = opcode + num
        # print(hex(inst))
        # print(hex(data))
        dut.opcode.value = inst

        await Timer(1, "step")

        mask = ~((2**(8*(32-num)))-1)
        masked_data = data & mask
        assert masked_data == dut.masked_data.value
        assert (masked_data >> (8*(32-num))) == dut.data_out.value

        # print(hex(data))
        # print(hex(mask))
        # print(hex(masked_data))
        # print(hex(dut.data_out.value))

        # test gas output
        if inst == 0x5f:
            # print(dut.push_bytes.value)
            assert dut.gas.value    == 2
            assert dut.pc_nxt.value == 1
        else:
            assert dut.gas.value    == 3
            assert dut.pc_nxt.value == num

        assert dut.push_num.value == 1

@cocotb.test()
async def push_sliced_data(dut):
    data = (2**(256))-1

    opcode = 0x5f

    dut.data_in.value = data

    for num in range(33):
        inst = opcode + num
        # print(hex(inst))
        # print(hex(data))
        dut.opcode.value = inst

        await Timer(1, "step")

        mask = ~((2**(8*(32-num)))-1)
        masked_data = data & mask
        assert masked_data == dut.masked_data.value
        assert (masked_data >> (8*(32-num))) == dut.data_out.value


          

        