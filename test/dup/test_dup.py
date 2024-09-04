from cocotb_test.simulator import run

def test_dup():
    run(
        verilog_sources=["../src/instructions/dup.sv"],
        toplevel="dup",
        module="dup_cocotb",
    )