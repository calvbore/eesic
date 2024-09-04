import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, ClockCycles

async def reset(dut):
    dut.rst.value = 1
    await Timer(1, units="step")
    dut.rst.value = 0
    await Timer(1, units="step")

async def push_items_per_cycle(dut, items, cycles, pop_num=0):
    push_num = len(items)
    fill = [0]*(17 - push_num)
    push_list = items + fill

    dut.push_num.value = push_num
    dut.pop_num.value  = pop_num

    dut.data_in.value = push_list

    for cycle in range(cycles):
        height = dut.height.value

        dut.clk.value = 0
        await Timer(1, units="step")
        dut.clk.value = 1
        await Timer(1, units="step")

        assert dut.height.value == height + push_num - pop_num

    dut.clk.value = 0
    await Timer(1, units="step")

async def push_items_by_cycle(dut, items, pop_num=0):
    cycles = len(items)

    dut.push_num.value = 1
    dut.pop_num.value  = pop_num

    fill = [0]*16

    for cycle in cycles:
        push_list = [items[cycle]] + fill

        dut.data_in.value = push_list

        height = dut.height.value

        dut.clk.value = 0
        await Timer(1, units="step")
        dut.clk.value = 1
        await Timer(1, units="step")

        assert dut.height.value == height + 1 - pop_num

async def pop_items_per_cycle(dut, pop_num, cycles):
    dut.push_num.value = 0
    dut.pop_num.value  = pop_num

    for cycle in range(cycles):
        height = dut.height.value

        dut.clk.value = 0
        await Timer(1, units="step")
        dut.clk.value = 1
        await Timer(1, units="step")

        assert dut.height.value == height - pop_num

# test that the stack height is increasing by one for each single stack item pushed onto the stack
@cocotb.test()
async def test_stack_push_height(dut):
    await reset(dut)

    # dut.exit.value = 0

    dut.push_num.value = 1
    dut.pop_num.value  = 0

    push_list = [0]*17
    dut.data_in.value = push_list

    for cycle in range(100):
        dut.clk.value = 0
        await Timer(1, units="step")
        dut.clk.value = 1
        await Timer(1, units="step")
        assert cycle+1 == dut.height.value

# test that the stack height is decreasing by one for each single item popped off the stack
@cocotb.test()
async def test_stack_pop_height(dut):
    # do not reset so we can pop all the values from the last test
    # await reset(dut)

    # dut.exit.value = 0

    dut.push_num.value = 0
    dut.pop_num.value  = 1

    for cycle in range(100):
        dut.clk.value = 0
        await Timer(1, units="step")
        dut.clk.value = 1
        await Timer(1, units="step")
        assert 100-(cycle+1) == dut.height.value

# test that data is being pushed onto the stack properly
@cocotb.test()
async def test_stack_push_data(dut):
    # reset the stack
    await reset(dut)

    # dut.exit.value = 0

    for num in range(17):
        items = [random.getrandbits(256) for _ in range(num+1)]
        await push_items_per_cycle(dut, items, 1)
        # print(items)
        # print(dut.data_out.value[:num+1])

        assert items == dut.data_out.value[:num+1]

    assert dut.height.value == 153

# test that data is pushed correctly after properly popping values off the stack
@cocotb.test()
async def test_stack_push_pop_data(dut):
    # reset the stack
    await reset(dut)

    # dut.exit.value = 0

    for num in range(17):
        items = [random.getrandbits(256) for _ in range(num+1)]
        stack_data = dut.data_out.value

        pop = num-2
        if pop < 0:
            pop = 0
        # print(stack_data)
        await push_items_per_cycle(dut, items, 1, pop_num=pop)
        # print(items)

        assert items == dut.data_out.value[:num+1]
        pred_data = items + stack_data[pop:]
        # print(num)
        # print(pop)
        s = int(min(17, (((num+1)*(num+2))/2)-((pop*(pop+1)/2))))
        # print(s)
        # print(num, len(pred_data[:s]), pred_data[:s])
        # print(num, len(dut.data_out.value), dut.data_out.value[:s])
        assert pred_data[:s] == dut.data_out.value[:s]
