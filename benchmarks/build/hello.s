	.file	1 "hello.c"

 # GNU C 2.7.2.3 [AL 1.1, MM 40, tma 0.1] SimpleScalar running sstrix compiled by GNU C

 # Cc1 defaults:
 # -mgas -mgpOPT

 # Cc1 arguments (-G value = 8, Cpu = default, ISA = 1):
 # -quiet -dumpbase -O0 -o

gcc2_compiled.:
__gnu_compiled_c:
	.sdata
	.align	2
$LC2:
	.ascii	"e: %d\n\000"
	.align	3
$LC0:
	.word	0x00000000		# 2
	.word	0x40000000
	.align	3
$LC1:
	.word	0x00000000		# 3.5
	.word	0x400c0000
	.text
	.align	2
	.globl	main

	.text

	.loc	1 3
	.ent	main
main:
	.frame	$fp,64,$31		# vars= 40, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,64
	sw	$31,60($sp)
	sw	$fp,56($sp)
	move	$fp,$sp
	jal	__main
	li	$2,0x00000001		# 1
	sw	$2,16($fp)
	li	$2,0x00000005		# 5
	sw	$2,20($fp)
	lw	$2,16($fp)
	lw	$3,20($fp)
	addu	$2,$2,$3
	sw	$2,24($fp)
	lw	$2,16($fp)
	addu	$3,$2,10
	sw	$3,28($fp)
	l.d	$f0,$LC0
	s.d	$f0,32($fp)
	l.d	$f0,$LC1
	s.d	$f0,40($fp)
	li	$2,0x00000061		# 97
	sb	$2,48($fp)
	la	$4,$LC2
	lw	$5,28($fp)
	jal	printf
	move	$2,$0
	j	$L1
$L1:
	move	$sp,$fp			# sp not trusted here
	lw	$31,60($sp)
	lw	$fp,56($sp)
	addu	$sp,$sp,64
	j	$31
	.end	main
