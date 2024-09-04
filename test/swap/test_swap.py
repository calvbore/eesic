from cocotb_test.simulator import run

def test_swap():
    run(
        verilog_sources=["../src/instructions/swap.sv"],
        toplevel="swap",
        module="swap_cocotb",
    )