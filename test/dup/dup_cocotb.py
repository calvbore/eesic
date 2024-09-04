import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, ClockCycles

@cocotb.test()
async def test_dup_data(dut):
    data = [random.getrandbits(256) for _ in range(16)]

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

        assert data[num] == dut.data_out.value

@cocotb.test()
async def test_exit(dut):

    opcode = 0x80

    for num in range(16):
        inst = opcode + num
        dut.opcode.value = inst

        dut.stack_height.value = num+1
        await Timer(1, "step")
        assert dut.exit.value == 0

        dut.stack_height.value = num+2
        await Timer(1, "step")
        assert dut.exit.value == 1