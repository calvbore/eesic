module dup (
    input wire  [7:0]   opcode,
    input wire  [9:0]   stack_height,
    input wire  [255:0] stack_data [0:15],
    output wire [255:0] data_out,
    output wire [4:0]   push_num,
    output wire [31:0]  gas,
    output wire         exit
);

// select stack item based on opcode
wire [3:0] item_sel = opcode[3:0];
// assign selected item to output
assign data_out = stack_data[item_sel]; // why does the selector have to be inverted?
assign push_num = 1;
assign gas      = 3;

// throw if stack smaller than index we want to dup
assign exit = stack_height < 10'(item_sel)+1 ? 1 : 0; 
    
endmodule