`include "instructions/dup.sv"
`include "instructions/push.sv"
`include "instructions/swap.sv"

module interpreter(
    input wire          clk,
    input wire  [7:0]   opcode,
    input wire  [9:0]   stack_height,
    input wire  [255:0] code_data,
    input wire  [255:0] stack_data [0:16],
    output reg  [255:0] data_out   [0:16],
    output reg  [4:0]   push_num,
    output reg  [4:0]   pop_num,
    output reg  [15:0]  pc_nxt, // how much to move the pc by in next cycle
    output reg  [31:0]  gas,
    output wire         exit
);

// STOP wire
reg rvrt;
// @TODO: add negedge clk reset for rvrt


// PUSH wires
wire [255:0] push_data_out;
wire [4:0]   push_push_n; // always 1
wire [5:0]   push_pc;
wire [31:0]  push_gas;

push push(
    .opcode(opcode),
    .data_in(code_data),
    .data_out(push_data_out),
    .push_num(push_push_n), // always 1
    .pc_nxt(push_pc),
    .gas(push_gas)
);


// DUP wires
wire [255:0] dup_data_out;
wire [4:0]   dup_push_n; // always 1
wire [31:0]  dup_gas;
wire         dup_exit;

dup dup(
    .opcode(opcode),
    .stack_height(stack_height),
    .stack_data(stack_data[0:15]),
    .data_out(dup_data_out),
    .push_num(dup_push_n), // always 1
    .gas(dup_gas),
    .exit(dup_exit)
);


// SWAP wires
wire [255:0] swap_data_out [0:16];
wire [4:0]   swap_push_n;
wire [4:0]   swap_pop_n;
wire [31:0]  swap_gas;
wire         swap_exit;

swap swap(
    .opcode(opcode),
    .stack_height(stack_height),
    .stack_data(stack_data),
    .data_out(swap_data_out),
    .push_num(swap_push_n),
    .pop_num(swap_pop_n),
    .gas(swap_gas),
    .exit(swap_exit)
);


// switch between instruction outputs based on opcode
always @(*) begin
    casez (opcode)
        // STOP
        8'h00: begin
            rvrt        = 1;
            gas         = 0;
        end
        // PUSH0 - PUSH32
        8'h5f, 8'h6?, 8'h7?: begin
            data_out[0] = push_data_out;
            push_num    = push_push_n; // always 1
            pop_num     = 0;
            pc_nxt      = 16'(push_pc);
            gas         = push_gas;
            rvrt        = 0;
        end
        // DUP1 - DUP16
        8'h8?: begin
            data_out[0] = dup_data_out;
            push_num    = dup_push_n; // always 1
            pop_num     = 0;
            pc_nxt      = 1;
            gas         = dup_gas;
            rvrt        = dup_exit;
        end
        // SWAP1 - SWAP16
        8'h9?: begin
            data_out    = swap_data_out;
            push_num    = swap_push_n;
            pop_num     = swap_pop_n;
            pc_nxt      = 1;
            gas         = swap_gas;
            rvrt        = swap_exit;
        end
        default: ;
    endcase
end

assign exit = rvrt;

endmodule