@R0
D=M
@R5
M=D
@R1
D=M
@R5
D=D-M
@R1M
D;JGT

(STARTR2)
	@R2
	D=M
	@R5
	D=D-M
	@R2M
	D;JGT

(STARTR3)
	@R3
	D=M
	@R5
	D=D-M
	@R3M
	D;JGT

(STARTR4)
	@R4
	D=M
	@R5
	D=D-M
	@R4M
	D;JGT
	@END
	0;JMP

(R1M)
	@R1
	D=M
	@R5
	M=D
	@STARTR2
	0;JMP
(R2M)
	@R2
	D=M
	@R5
	M=D
	@STARTR3
	0;JMP
(R3M)
	@R3
	D=M
	@R5
	M=D
	@STARTR4
	0;JMP
(R4M)
	@R4
	D=M
	@R5
	M=D
	@END
	0;JMP
(END)
	@END
	0;JMP



