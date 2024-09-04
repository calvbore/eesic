from cocotb_test.simulator import run

def test_interp():
    run(
        verilog_sources=["../src/execution.sv"],
        includes=["../src"],
        toplevel="execution",
        module="exec_cocotb",
    )