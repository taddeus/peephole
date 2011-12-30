	.file	1 "wiki.c"

 # GNU C 2.7.2.3 [AL 1.1, MM 40, tma 0.1] SimpleScalar running sstrix compiled by GNU C

 # Cc1 defaults:
 # -mgas -mgpOPT

 # Cc1 arguments (-G value = 8, Cpu = default, ISA = 1):
 # -quiet -dumpbase -O0 -o

gcc2_compiled.:
__gnu_compiled_c:
	.text
	.align	2
	.globl	main

	.text

	.loc	1 4
	.ent	main
main:
	.frame	$fp,48,$31		# vars= 24, regs= 2/0, args= 16, extra= 0
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	subu	$sp,$sp,48
	sw	$31,44($sp)
	sw	$fp,40($sp)
	move	$fp,$sp
	jal	__main
	li	$2,0x00000003		# 3
	sw	$2,16($fp)
	li	$2,0x00000005		# 5
	sw	$2,20($fp)
	li	$2,0x00000005		# 5
	sw	$2,24($fp)
	li	$2,0x00000064		# 100
	sw	$2,28($fp)
	lw	$2,16($fp)
	lw	$3,20($fp)
	slt	$2,$3,$2
	beq	$2,$0,$L2
	lw	$2,16($fp)
	lw	$3,20($fp)
	addu	$2,$2,$3
	sw	$2,36($fp)
	li	$2,0x00000002		# 2
	sw	$2,24($fp)
$L2:
	li	$2,0x00000004		# 4
	sw	$2,32($fp)
	lw	$2,20($fp)
	lw	$3,24($fp)
	mult	$2,$3
	mflo	$2
	lw	$4,32($fp)
	addu	$3,$2,$4
	move	$2,$3
	j	$L1
$L1:
	move	$sp,$fp			# sp not trusted here
	lw	$31,44($sp)
	lw	$fp,40($sp)
	addu	$sp,$sp,48
	j	$31
	.end	main
