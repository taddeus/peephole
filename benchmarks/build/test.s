	.file	1 "test.c"

 # GNU C 2.7.2.3 [AL 1.1, MM 40, tma 0.1] SimpleScalar running sstrix compiled by GNU C

 # Cc1 defaults:
 # -mgas -mgpOPT

 # Cc1 arguments (-G value = 8, Cpu = default, ISA = 1):
 # -quiet -dumpbase -o

gcc2_compiled.:
__gnu_compiled_c:
	.text
	.align	2
	.globl	main

	.text

	.loc	1 3
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
	li	$2,0x00000002		# 2
	sw	$2,16($fp)
	li	$2,0x00000005		# 5
	sw	$2,20($fp)
	lw	$2,16($fp)
	lw	$3,20($fp)
	mult	$2,$3
	mflo	$2
	sw	$2,24($fp)
	lw	$2,16($fp)
	move	$4,$2
	sll	$3,$4,1
	addu	$3,$3,$2
	sll	$2,$3,1
	sw	$2,28($fp)
	li	$2,0x00000015		# 21
	sw	$2,32($fp)
	move	$2,$0
	j	$L1
$L1:
	move	$sp,$fp			# sp not trusted here
	lw	$31,44($sp)
	lw	$fp,40($sp)
	addu	$sp,$sp,48
	j	$31
	.end	main
