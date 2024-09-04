module stack (
    input wire          clk,
    input wire          rst,
    input wire          exit,
    input wire  [4:0]   push_num,
    input wire  [4:0]   pop_num, // should never be larger than the stack height
    input wire  [255:0] data_in  [0:16], // able to put 17 items on the stack (support for swap instructions)
    output wire [255:0] data_out [0:16], // access to 17 stack items
    output wire [9:0]   height // access to stack height so opcodes can revert if there aren't enough items
);
parameter STACK_DEPTH = 1024;

reg [9:0] pointer;
reg [255:0] stack_word [0:STACK_DEPTH-1];

always @(posedge clk or posedge rst) begin
    if (rst) begin
        // reset stack pointer pointer and all words
        pointer <= 0;
        for (integer i=0; i<STACK_DEPTH; i++) stack_word[i] = 0;
    end else if (exit) begin
        // dump the stack_word array to some kind of external manager and clear stack
        // load the previous context's stack state and pointer/height
        // @TODO
    end else begin
        // increment height of the stack
        pointer <= pointer + 10'(push_num) - 10'(pop_num);

        // push new words onto the stack
        for (integer i=0; i<=16; i=i+1) begin
            if (i<push_num) stack_word[32'(pointer)+(32'(push_num)-i)-32'(pop_num)] <= data_in[i];
        end
    end
end

// output read data for the most recent 17 items on the stack
genvar j;
for (j=0; j<=16; j=j+1) begin
    assign data_out[j] = stack_word[pointer-j];
end
// output the stack height
assign height = pointer;
    
endmodule