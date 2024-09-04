from cocotb_test.simulator import run

def test_stack():
    run(
        verilog_sources=["../src/stack.sv"],
        toplevel="stack",
        module="stack_cocotb",
    )
