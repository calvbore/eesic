from cocotb_test.simulator import run

def test_interp():
    run(
        verilog_sources=["../src/interpreter.sv"],
        includes=["../src"],
        toplevel="interpreter",
        module="interp_cocotb",
    )