	.file	1 "hello.c"

 # GNU C 2.7.2.3 [AL 1.1, MM 40, tma 0.1] SimpleScalar running sstrix compiled by GNU C

 # Cc1 defaults:
 # -mgas -mgpOPT

 # Cc1 arguments (-G value = 8, Cpu = default, ISA = 1):
 # -quiet -dumpbase -o

gcc2_compiled.:
__gnu_compiled_c:
	.sdata
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

	.loc	1 2
	.ent	main
main:
	.frame	$fp,56,$31		# vars= 32, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,56
	sw	$31,52($sp)
	sw	$fp,48($sp)
	move	$fp,$sp
	jal	__main
	li	$2,0x00000001		# 1
	sw	$2,16($fp)
	li	$2,0x00000005		# 5
	sw	$2,20($fp)
	l.d	$f0,$LC0
	s.d	$f0,24($fp)
	l.d	$f0,$LC1
	s.d	$f0,32($fp)
	li	$2,0x00000061		# 97
	sb	$2,40($fp)
	move	$2,$0
	j	$L1
$L1:
	move	$sp,$fp			# sp not trusted here
	lw	$31,52($sp)
	lw	$fp,48($sp)
	addu	$sp,$sp,56
	j	$31
	.end	main
