import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, ClockCycles

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

@cocotb.test()
async def test_exit(dut):
    opcode = 0x90

    for num in range(16):
        inst = opcode + num
        dut.opcode.value = inst

        dut.stack_height.value = num+1
        await Timer(1, "step")
        assert dut.exit.value == 1

        dut.stack_height.value = num+2
        await Timer(1, "step")
        assert dut.exit.value == 0