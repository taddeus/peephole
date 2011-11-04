/*	EVERBODY:	Please read "APOLOGY" below. -rick 01/06/86
 *
 *	"DHRYSTONE" Benchmark Program
 *
 *	Version:	C/1.1, 12/01/84
 *
 *	Date:		PROGRAM updated 01/06/86, RESULTS updated 02/17/86
 *
 *	Author:		Reinhold P. Weicker,  CACM Vol 27, No 10, 10/84 pg. 1013
 *			Translated from ADA by Rick Richardson
 *			Every method to preserve ADA-likeness has been used,
 *			at the expense of C-ness.
 *
 *	Compile:	cc -O dry.c -o drynr			: No registers
 *			cc -O -DREG=register dry.c -o dryr	: Registers
 *
 *	Defines:	Defines are provided for old C compiler's
 *			which don't have enums, and can't assign structures.
 *			The time(2) function is library dependant; Most
 *			return the time in seconds, but beware of some, like
 *			Aztec C, which return other units.
 *			The LOOPS define is initially set for 50000 loops.
 *			If you have a machine with large integers and is
 *			very fast, please change this number to 500000 to
 *			get better accuracy.  Please select the way to
 *			measure the execution time using the TIME define.
 *			For single user machines, time(2) is adequate. For
 *			multi-user machines where you cannot get single-user
 *			access, use the times(2) function.  If you have
 *			neither, use a stopwatch in the dead of night.
 *			Use a "printf" at the point marked "start timer"
 *			to begin your timings. DO NOT use the UNIX "time(1)"
 *			command, as this will measure the total time to
 *			run this program, which will (erroneously) include
 *			the time to malloc(3) storage and to compute the
 *			time it takes to do nothing.
 *
 *	Run:		drynr; dryr
 *
 *	Results:	If you get any new machine/OS results, please send to:
 *
 *				{ihnp4,vax135,..}!houxm!castor!pcrat!rick
 *
 *			and thanks to all that do.  Space prevents listing
 *			the names of those who have provided some of these
 *			results.  I'll be forwarding these results to
 *			Rheinhold Weicker.
 *
 *	Note:		I order the list in increasing performance of the
 *			"with registers" benchmark.  If the compiler doesn't
 *			provide register variables, then the benchmark
 *			is the same for both REG and NOREG.
 *
 *	PLEASE:		Send complete information about the machine type,
 *			clock speed, OS and C manufacturer/version.  If
 *			the machine is modified, tell me what was done.
 *			On UNIX, execute uname -a and cc -V to get this info.
 *
 *	80x8x NOTE:	80x8x benchers: please try to do all memory models
 *			for a particular compiler.
 *
 *	APOLOGY (1/30/86):
 *		Well, I goofed things up!  As pointed out by Haakon Bugge,
 *		the line of code marked "GOOF" below was missing from the
 *		Dhrystone distribution for the last several months.  It
 *		*WAS* in a backup copy I made last winter, so no doubt it
 *		was victimized by sleepy fingers operating vi!
 *
 *		The effect of the line missing is that the reported benchmarks
 *		are 15% too fast (at least on a 80286).  Now, this creates
 *		a dilema - do I throw out ALL the data so far collected
 *		and use only results from this (corrected) version, or
 *		do I just keep collecting data for the old version?
 *
 *		Since the data collected so far *is* valid as long as it
 *		is compared with like data, I have decided to keep
 *		TWO lists- one for the old benchmark, and one for the
 *		new.  This also gives me an opportunity to correct one
 *		other error I made in the instructions for this benchmark.
 *		My experience with C compilers has been mostly with
 *		UNIX 'pcc' derived compilers, where the 'optimizer' simply
 *		fixes sloppy code generation (peephole optimization).
 *		But today, there exist C compiler optimizers that will actually
 *		perform optimization in the Computer Science sense of the word,
 *		by removing, for example, assignments to a variable whose
 *		value is never used.  Dhrystone, unfortunately, provides
 *		lots of opportunities for this sort of optimization.
 *
 *		I request that benchmarkers re-run this new, corrected
 *		version of Dhrystone, turning off or bypassing optimizers
 *		which perform more than peephole optimization.  Please
 *		indicate the version of Dhrystone used when reporting the
 *		results to me.
 *		
 * RESULTS BEGIN HERE
 *
 *----------------DHRYSTONE VERSION 1.1 RESULTS BEGIN--------------------------
 *
 * MACHINE	MICROPROCESSOR	OPERATING	COMPILER	DHRYSTONES/SEC.
 * TYPE				SYSTEM				NO REG	REGS
 * --------------------------	------------	-----------	---------------
 * IBM PC/AT    80286-7.5Mhz    Venix/286 SVR2  cc              1159    1254 *15
 *
 *
 *----------------DHRYSTONE VERSION 1.0 RESULTS BEGIN--------------------------
 *
 * MACHINE	MICROPROCESSOR	OPERATING	COMPILER	DHRYSTONES/SEC.
 * TYPE				SYSTEM				NO REG	REGS
 * --------------------------	------------	-----------	---------------
 * Commodore 64	6510-1MHz	C64 ROM		C Power 2.8	  36	  36
 * HP-110	8086-5.33Mhz	MSDOS 2.11	Lattice 2.14	 284	 284
 * IBM PC/XT	8088-4.77Mhz	PC/IX		cc		 271	 294
 * CCC 3205	?		Xelos(SVR2) 	cc		 279	 296
 * Perq-II	2901 bitslice	Accent S5c 	cc (CMU)	 301	 301
 * IBM PC/XT	8088-4.77Mhz	COHERENT 2.3.43	MarkWilliams cc  296	 317
 * Cosmos	68000-8Mhz	UniSoft		cc		 305	 322
 * IBM PC/XT	8088-4.77Mhz	Venix/86 2.0	cc		 297	 324
 * DEC PRO 350  11/23           Venix/PRO SVR2  cc               299     325
 * IBM PC	8088-4.77Mhz	MSDOS 2.0	b16cc 2.0	 310	 340
 * PDP11/23	11/23           Venix (V7)      cc               320     358
 * Commodore Amiga		?		Lattice 3.02	 368	 371
 * PC/XT        8088-4.77Mhz    Venix/86 SYS V  cc               339     377
 * IBM PC	8088-4.77Mhz	MSDOS 2.0	CI-C86 2.20M	 390	 390
 * IBM PC/XT	8088-4.77Mhz	PCDOS 2.1	Wizard 2.1	 367	 403
 * IBM PC/XT	8088-4.77Mhz	PCDOS 3.1	Lattice 2.15	 403	 403 @
 * Colex DM-6	68010-8Mhz	Unisoft SYSV	cc		 378	 410
 * IBM PC	8088-4.77Mhz	PCDOS 3.1	Datalight 1.10	 416	 416
 * IBM PC	NEC V20-4.77Mhz	MSDOS 3.1	MS 3.1 		 387	 420
 * IBM PC/XT	8088-4.77Mhz	PCDOS 2.1	Microsoft 3.0	 390	 427
 * IBM PC	NEC V20-4.77Mhz	MSDOS 3.1	MS 3.1 (186) 	 393	 427
 * PDP-11/34	-		UNIX V7M	cc		 387	 438
 * IBM PC	8088, 4.77mhz	PC-DOS 2.1	Aztec C v3.2d	 423	 454
 * Tandy 1000	V20, 4.77mhz	MS-DOS 2.11	Aztec C v3.2d	 423	 458
 * Tandy TRS-16B 68000-6Mhz	Xenix 1.3.5	cc		 438	 458
 * PDP-11/34	-		RSTS/E		decus c		 438	 495
 * Onyx C8002	Z8000-4Mhz	IS/1 1.1 (V7)	cc		 476	 511
 * CCC 3230			Xelos (SysV.2)	cc		 507	 565
 * Tandy TRS-16B 68000-6Mhz	Xenix 1.3.5	Green Hills	 609	 617
 * DEC PRO 380  11/73           Venix/PRO SVR2  cc               577     628
 * FHL QT+	68000-10Mhz	Os9/68000	version 1.3	 603	 649 FH
 * Apollo DN550	68010-?Mhz	AegisSR9/IX	cc 3.12		 666	 666
 * HP-110	8086-5.33Mhz	MSDOS 2.11	Aztec-C		 641	 676 
 * ATT PC6300	8086-8Mhz	MSDOS 2.11	b16cc 2.0	 632	 684
 * IBM PC/AT	80286-6Mhz	PCDOS 3.0	CI-C86 2.1	 666	 684
 * Tandy 6000	68000-8Mhz	Xenix 3.0	cc		 694	 694
 * IBM PC/AT	80286-6Mhz	Xenix 3.0	cc		 684	 704 MM
 * Macintosh	68000-7.8Mhz 2M	Mac Rom		Mac C 32 bit int 694	 704
 * Macintosh	68000-7.7Mhz	-		MegaMax C 2.0	 661	 709
 * IBM PC/AT	80286-6Mhz	Xenix 3.0	cc		 704	 714 LM
 * Codata 3300	68000-8Mhz	UniPlus+ (v7)	cc		 678	 725
 * WICAT MB	68000-8Mhz	System V	WICAT C 4.1	 585	 731 ~
 * Cadmus 9000	68010-10Mhz	UNIX		cc		 714	 735
 * AT&T 6300    8086-8Mhz       Venix/86 SVR2   cc               668     743
 * Cadmus 9790	68010-10Mhz 1MB	SVR0,Cadmus3.7	cc		 720	 747
 * NEC PC9801F	8086-8Mhz	PCDOS 2.11	Lattice 2.15	 768	  -  @
 * ATT PC6300	8086-8Mhz	MSDOS 2.11	CI-C86 2.20M	 769	 769
 * Burroughs XE550 68010-10Mhz	Centix 2.10	cc		 769	 769 CT1
 * EAGLE/TURBO  8086-8Mhz       Venix/86 SVR2   cc               696     779
 * ALTOS 586	8086-10Mhz	Xenix 3.0b	cc 		 724	 793
 * DEC 11/73	J-11 micro	Ultrix-11 V3.0	System V	 735	 793
 * ATT 3B2/300	WE32000-?Mhz	UNIX 5.0.2	cc		 735	 806
 * Apollo DN320	68010-?Mhz	AegisSR9/IX	cc 3.12		 806	 806
 * IRIS-2400	68010-10Mhz	UNIX System V	cc		 772	 829
 * Atari 520ST  68000-8Mhz      TOS             DigResearch      839     846
 * IBM PC/AT	80286-6Mhz	PCDOS 3.0	MS 3.0(large)	 833	 847 LM
 * WICAT MB	68000-8Mhz	System V	WICAT C 4.1	 675	 853 S~
 * VAX 11/750	-		Ultrix 1.1	4.2BSD cc	 781	 862
 * CCC  7350A	68000-8MHz	UniSoft V.2	cc		 821	 875
 * VAX 11/750	-		UNIX 4.2bsd	cc		 862	 877
 * Fast Mac	68000-7.7Mhz	-		MegaMax C 2.0	 839	 904 +
 * IBM PC/XT	8086-9.54Mhz	PCDOS 3.1	Microsoft 3.0	 833	 909 C1
 * DEC 11/44			Ultrix-11 V3.0	System V	 862	 909
 * Macintosh	68000-7.8Mhz 2M	Mac Rom		Mac C 16 bit int 877	 909 S
 * CCC 3210	?		Xelos R01(SVR2)	cc		 849	 924
 * CCC 3220	?               Ed. 7 v2.3      cc		 892	 925
 * IBM PC/AT	80286-6Mhz	Xenix 3.0	cc -i		 909	 925
 * AT&T 6300	8086, 8mhz	MS-DOS 2.11	Aztec C v3.2d	 862	 943
 * IBM PC/AT	80286-6Mhz	Xenix 3.0	cc		 892	 961
 * VAX 11/750	w/FPA		Eunice 3.2	cc		 914	 976
 * IBM PC/XT	8086-9.54Mhz	PCDOS 3.1	Wizard 2.1	 892	 980 C1
 * IBM PC/XT	8086-9.54Mhz	PCDOS 3.1	Lattice 2.15	 980	 980 C1
 * Plexus P35	68000-10Mhz	UNIX System III cc		 984	 980
 * PDP-11/73	KDJ11-AA 15Mhz	UNIX V7M 2.1	cc		 862     981
 * VAX 11/750	w/FPA		UNIX 4.3bsd	cc		 994	 997
 * IRIS-1400	68010-10Mhz	UNIX System V	cc		 909	1000
 * IBM PC/AT	80286-6Mhz	Venix/86 2.1	cc		 961	1000
 * IBM PC/AT	80286-6Mhz	PCDOS 3.0	b16cc 2.0	 943	1063
 * Zilog S8000/11 Z8001-5.5Mhz	Zeus 3.2	cc		1011	1084
 * NSC ICM-3216 NSC 32016-10Mhz	UNIX SVR2	cc		1041	1084
 * IBM PC/AT	80286-6Mhz	PCDOS 3.0	MS 3.0(small)	1063	1086
 * VAX 11/750	w/FPA		VMS		VAX-11 C 2.0	 958	1091
 * Stride	68000-10Mhz	System-V/68	cc		1041	1111
 * Plexus P/60  MC68000-12.5Mhz	UNIX SYSIII	Plexus		1111	1111
 * ATT PC7300	68010-10Mhz	UNIX 5.2	cc		1041	1111
 * CCC 3230	?		Xelos R01(SVR2)	cc		1040	1126
 * Stride	68000-12Mhz	System-V/68	cc		1063	1136
 * IBM PC/AT    80286-6Mhz      Venix/286 SVR2  cc              1056    1149
 * Plexus P/60  MC68000-12.5Mhz	UNIX SYSIII	Plexus		1111	1163 T
 * IBM PC/AT	80286-6Mhz	PCDOS 3.0	Datalight 1.10	1190	1190
 * ATT PC6300+	80286-6Mhz	MSDOS 3.1	b16cc 2.0	1111	1219
 * IBM PC/AT	80286-6Mhz	PCDOS 3.1	Wizard 2.1	1136	1219
 * Sun2/120	68010-10Mhz	Sun 4.2BSD	cc		1136	1219
 * IBM PC/AT	80286-6Mhz	PCDOS 3.0	CI-C86 2.20M	1219	1219
 * WICAT PB	68000-8Mhz	System V	WICAT C 4.1	 998	1226 ~
 * MASSCOMP 500	68010-10MHz	RTU V3.0	cc (V3.2)	1156	1238
 * Alliant FX/8 IP (68012-12Mhz) Concentrix	cc -ip;exec -i 	1170	1243 FX
 * Cyb DataMate	68010-12.5Mhz	Uniplus 5.0	Unisoft cc	1162	1250
 * PDP 11/70	-		UNIX 5.2	cc		1162	1250
 * IBM PC/AT	80286-6Mhz	PCDOS 3.1	Lattice 2.15	1250	1250
 * IBM PC/AT	80286-7.5Mhz	Venix/86 2.1	cc		1190	1315 *15
 * Sun2/120	68010-10Mhz	Standalone	cc		1219	1315
 * Intel 380	80286-8Mhz	Xenix R3.0up1	cc		1250	1315 *16
 * Sequent Balance 8000	NS32032-10MHz	Dynix 2.0	cc	1250	1315 N12
 * IBM PC/DSI-32 32032-10Mhz	MSDOS 3.1	GreenHills 2.14	1282	1315 C3
 * ATT 3B2/400	WE32100-?Mhz	UNIX 5.2	cc		1315	1315
 * CCC 3250XP	-		Xelos R01(SVR2)	cc		1215	1318
 * IBM PC/RT 032 RISC(801?)?Mhz BSD 4.2         cc              1248    1333 RT
 * DG MV4000	-		AOS/VS 5.00	cc		1333	1333
 * IBM PC/AT	80286-8Mhz	Venix/86 2.1	cc		1275	1380 *16
 * IBM PC/AT	80286-6Mhz	MSDOS 3.0	Microsoft 3.0	1250	1388
 * ATT PC6300+	80286-6Mhz	MSDOS 3.1	CI-C86 2.20M	1428	1428
 * COMPAQ/286   80286-8Mhz      Venix/286 SVR2  cc              1326    1443
 * IBM PC/AT    80286-7.5Mhz    Venix/286 SVR2  cc              1333    1449 *15
 * WICAT PB	68000-8Mhz	System V	WICAT C 4.1	1169	1464 S~
 * Tandy II/6000 68000-8Mhz	Xenix 3.0	cc      	1384	1477
 * WICAT MB	68000-12.5Mhz	System V	WICAT C 4.1	1246	1537 ~
 * IBM PC/AT    80286-9Mhz      SCO Xenix V     cc              1540    1556 *18
 * Cyb DataMate	68010-12.5Mhz	Uniplus 5.0	Unisoft cc	1470	1562 S
 * VAX 11/780	-		UNIX 5.2	cc		1515	1562
 * MicroVAX-II	-		-		-		1562	1612
 * VAX 11/780	-		UNIX 4.3bsd	cc		1646	1662
 * Apollo DN660	-		AegisSR9/IX	cc 3.12		1666	1666
 * ATT 3B20	-		UNIX 5.2	cc		1515	1724
 * NEC PC-98XA	80286-8Mhz	PCDOS 3.1	Lattice 2.15	1724	1724 @
 * HP9000-500	B series CPU	HP-UX 4.02	cc		1724	-
 * IBM PC/STD	80286-8Mhz	MSDOS 3.0 	Microsoft 3.0	1724	1785 C2
 * WICAT MB	68000-12.5Mhz	System V	WICAT C 4.1	1450	1814 S~
 * WICAT PB	68000-12.5Mhz	System V	WICAT C 4.1	1530	1898 ~
 * DEC-2065	KL10-Model B	TOPS-20 6.1FT5	Port. C Comp.	1937	1946
 * Gould PN6005	-		UTX 1.1(4.2BSD)	cc		1675	1964
 * DEC2060	KL-10		TOPS-20		cc		2000	2000 &
 * VAX 11/785	-		UNIX 5.2	cc		2083	2083
 * VAX 11/785	-		VMS		VAX-11 C 2.0	2083	2083
 * VAX 11/785	-		UNIX SVR2	cc		2123	2083
 * VAX 11/785   -               ULTRIX-32 1.1   cc		2083    2091 
 * VAX 11/785	-		UNIX 4.3bsd	cc		2135	2136
 * WICAT PB	68000-12.5Mhz	System V	WICAT C 4.1	1780	2233 S~
 * Pyramid 90x	-		OSx 2.3		cc		2272	2272
 * Pyramid 90x	FPA,cache,4Mb	OSx 2.5		cc no -O	2777	2777
 * Pyramid 90x	w/cache		OSx 2.5		cc w/-O		3333	3333
 * IBM-4341-II	-		VM/SP3		Waterloo C 1.2  3333	3333
 * IRIS-2400T	68020-16.67Mhz	UNIX System V	cc		3105	3401
 * Celerity C-1200 ?		UNIX 4.2BSD	cc		3485	3468
 * SUN 3/75	68020-16.67Mhz	SUN 4.2 V3	cc		3333	3571
 * IBM-4341	Model 12	UTS 5.0		?		3685	3685
 * SUN-3/160    68020-16.67Mhz  Sun 4.2 V3.0A   cc		3381    3764
 * Sun 3/180	68020-16.67Mhz	Sun 4.2		cc		3333	3846
 * IBM-4341	Model 12	UTS 5.0		?		3910	3910 MN
 * MC 5400	68020-16.67MHz	RTU V3.0	cc (V4.0)	3952	4054
 * NCR Tower32  68020-16.67Mhz  SYS 5.0 Rel 2.0 cc              3846	4545
 * Gould PN9080	-		UTX-32 1.1c	cc		-	4629
 * MC 5600/5700	68020-16.67MHz	RTU V3.0	cc (V4.0)	4504	4746 %
 * Gould 1460-342 ECL proc      UTX/32 11/c   c           342   677G1
* VX 800			UIX .3bd	c		724	088 * AX 600-		MS	VAX11  2.	712	742
* Aliat F/8 E		oncntrx	c -c;exc - 	652	655FX
* CI PWER6/3		CS(S+4.)	c		700	800 * CI OWE 6/2		OWE 6 NIXV	c		836	498 * CI OWE 6/2		.2 el.1.2	cc	893	944
* Serr (CI Pwer6)	4.2SD	cc	934   000
 *CRA-X-P/1	  105hz	OS .14Cra C       020   020
 *IBM308	-	UTS5.0Rel1	c	     1666  1250
  CRY-1	   80hz	TSS	Cry C2.0   1210  1388
  IB-303	-	VMCMSHPO3.4Watrlo C .2 388   388
 *Amdhl 70 /8 	UT/V .2     ccv1.3     1550  1550
  CRY-XMP/8	  10MhzCTS		Cay  2.    1525  1757
* Adah 58	-	UTS5.0Rel1.2cc 1.5      307   307
 *Amdhl 860 		TS/ 5.      c v.23     2970  2970 *
* NTE
*  *  Crytalchagedfro 'sock tolised alu.
       hisMacntoh ws ugraed rom128 to512 insuc a ay hat *     th ne 38K o memory is not slowed down by video generator accesses.
 *   %   Single processor; MC == MASSCOMP
 *   &   A version 7 C compiler written at New Mexico Tech.
 *   @   vanilla Lattice compiler used with MicroPro standard library
 *   S   Shorts used instead of ints
 *   T	 with Chris Torek's patches (whatever they are).
 *   ~   For WICAT Systems: MB=MultiBus, PB=Proprietary Bus
 *   LM  Large Memory Model. (Otherwise, all 80x8x results are small model)
 *   MM  Medium Memory Model. (Otherwise, all 80x8x results are small model)
 *   C1  Univation PC TURBO Co-processor; 9.54Mhz 8086, 640K RAM
 *   C2  Seattle Telecom STD-286 board
 *   C3  Definicon DSI-32 coprocessor
 *   C?  Unknown co-processor board?
 *   CT1 Convergent Technologies MegaFrame, 1 processor.
 *   MN  Using Mike Newtons 'optimizer' (see net.sources).
 *   G1  This Gould machine has 2 processors and was able to run 2 dhrystone
 *       Benchmarks in parallel with no slowdown.
 *   FH  FHC == Frank Hogg Labs (Hazelwood Uniquad 2 in an FHL box).
 *   FX  The Alliant FX/8 is a system consisting of 1-8 CEs (computation
 *	 engines) and 1-12 IPs (interactive processors). Note N8 applies.
 *   RT  This is one of the RT's that CMU has been using for awhile.  I'm
 *	 not sure that this is identical to the machine that IBM is selling
 *	 to the public.
 *   Nnn This machine has multiple processors, allowing "nn" copies of the
 *	 benchmark to run in the same time as 1 copy.
 *   ?   I don't trust results marked with '?'.  These were sent to me with
 *       either incomplete info, or with times that just don't make sense.
 *	 ?? means I think the performance is too poor, ?! means too good.
 *       If anybody can confirm these figures, please respond.
 *
 *  ABBREVIATIONS
 *	CCC	Concurrent Computer Corp. (was Perkin-Elmer)
 *	MC	Masscomp
 *
 *--------------------------------RESULTS END----------------------------------
 *
 *	The following program contains statements of a high-level programming
 *	language (C) in a distribution considered representative:
 *
 *	assignments			53%
 *	control statements		32%
 *	procedure, function calls	15%
 *
 *	100 statements are dynamically executed.  The program is balanced with
 *	respect to the three aspects:
 *		- statement type
 *		- operand type (for simple data types)
 *		- operand access
 *			operand global, local, parameter, or constant.
 *
 *	The combination of these three aspects is balanced only approximately.
 *
 *	The program does not compute anything meaningfull, but it is
 *	syntactically and semantically correct.
 *
 */

/* Accuracy of timings and human fatigue controlled by next two lines */
/*#define LOOPS	50000		/* Use this for slow or 16 bit machines */
#define LOOPS	5000		/* Use this for faster machines */

/* Compiler dependent options */
#undef	NOENUM			/* Define if compiler has no enum's */
#undef	NOSTRUCTASSIGN		/* Define if compiler can't assign structures */

/* define only one of the next two defines */
#define TIMES			/* Use times(2) time function */
/*#define TIME			/* Use time(2) time function */

/* define the granularity of your times(2) function (when used) */
/*#define HZ	60		/* times(2) returns 1/60 second (most) */
#define HZ	100		/* times(2) returns 1/100 second (WECo) */

/* for compatibility with goofed up version */
/*#define GOOF			/* Define if you want the goofed up version */

#ifdef GOOF
char	Version[] = "1.0";
#else
char	Version[] = "1.1";
#endif

#ifdef	NOSTRUCTASSIGN
#define	structassign(d, s)	memcpy(&(d), &(s), sizeof(d))
#else
#define	structassign(d, s)	d = s
#endif

#ifdef	NOENUM
#define	Ident1	1
#define	Ident2	2
#define	Ident3	3
#define	Ident4	4
#define	Ident5	5
typedef int	Enumeration;
#else
typedef enum	{Ident1, Ident2, Ident3, Ident4, Ident5} Enumeration;
#endif

typedef int	OneToThirty;
typedef int	OneToFifty;
typedef char	CapitalLetter;
typedef char	String30[31];
typedef int	Array1Dim[51];
typedef int	Array2Dim[51][51];

struct	Record
{
	struct Record		*PtrComp;
	Enumeration		Discr;
	Enumeration		EnumComp;
	OneToFifty		IntComp;
	String30		StringComp;
};

typedef struct Record 	RecordType;
typedef RecordType *	RecordPtr;
typedef int		boolean;

#define	NULL		0
#define	TRUE		1
#define	FALSE		0

#ifndef REG
#define	REG
#endif

extern Enumeration	Func1();
extern boolean		Func2();

#ifdef TIMES
#include <sys/types.h>
#include <sys/times.h>
#endif

main()
{
	Proc0();
	exit(0);
}

/*
 * Package 1
 */
int		IntGlob;
boolean		BoolGlob;
char		Char1Glob;
char		Char2Glob;
Array1Dim	Array1Glob;
Array2Dim	Array2Glob;
RecordPtr	PtrGlb;
RecordPtr	PtrGlbNext;

Proc0()
{
	OneToFifty		IntLoc1;
	REG OneToFifty		IntLoc2;
	OneToFifty		IntLoc3;
	REG char		CharLoc;
	REG char		CharIndex;
	Enumeration	 	EnumLoc;
	String30		String1Loc;
	String30		String2Loc;
	extern char		*malloc();

#ifdef TIME
	long			time();
	long			starttime;
	long			benchtime;
	long			nulltime;
	register unsigned int	i;

	starttime = time( (long *) 0);
	for (i = 0; i < LOOPS; ++i);
	nulltime = time( (long *) 0) - starttime; /* Computes o'head of loop */
#endif
#ifdef TIMES
	time_t			starttime;
	time_t			benchtime;
	time_t			nulltime;
	struct tms		tms;
	register unsigned int	i;

	times(&tms); starttime = tms.tms_utime;
	for (i = 0; i < LOOPS; ++i);
	times(&tms);
	nulltime = tms.tms_utime - starttime; /* Computes overhead of looping */
#endif

	PtrGlbNext = (RecordPtr) malloc(sizeof(RecordType));
	PtrGlb = (RecordPtr) malloc(sizeof(RecordType));
	PtrGlb->PtrComp = PtrGlbNext;
	PtrGlb->Discr = Ident1;
	PtrGlb->EnumComp = Ident3;
	PtrGlb->IntComp = 40;
	strcpy(PtrGlb->StringComp, "DHRYSTONE PROGRAM, SOME STRING");
#ifndef	GOOF
	strcpy(String1Loc, "DHRYSTONE PROGRAM, 1'ST STRING");	/*GOOF*/
#endif
	Array2Glob[8][7] = 10;	/* Was missing in published program */

/*****************
-- Start Timer --
*****************/
#ifdef TIME
	starttime = time( (long *) 0);
#endif
#ifdef TIMES
	times(&tms); starttime = tms.tms_utime;
#endif
	for (i = 0; i < LOOPS; ++i)
	{

		Proc5();
		Proc4();
		IntLoc1 = 2;
		IntLoc2 = 3;
		strcpy(String2Loc, "DHRYSTONE PROGRAM, 2'ND STRING");
		EnumLoc = Ident2;
		BoolGlob = ! Func2(String1Loc, String2Loc);
		while (IntLoc1 < IntLoc2)
		{
			IntLoc3 = 5 * IntLoc1 - IntLoc2;
			Proc7(IntLoc1, IntLoc2, &IntLoc3);
			++IntLoc1;
		}
		Proc8(Array1Glob, Array2Glob, IntLoc1, IntLoc3);
		Proc1(PtrGlb);
		for (CharIndex = 'A'; CharIndex <= Char2Glob; ++CharIndex)
			if (EnumLoc == Func1(CharIndex, 'C'))
				Proc6(Ident1, &EnumLoc);
		IntLoc3 = IntLoc2 * IntLoc1;
		IntLoc2 = IntLoc3 / IntLoc1;
		IntLoc2 = 7 * (IntLoc3 - IntLoc2) - IntLoc1;
		Proc2(&IntLoc1);
	}

/*****************
-- Stop Timer --
*****************/

#ifdef TIME
	benchtime = time( (long *) 0) - starttime - nulltime;
	printf("Dhrystone(%s) time for %ld passes = %ld\n",
		Version,
		(long) LOOPS, benchtime);
	printf("This machine benchmarks at %ld dhrystones/second\n",
		((long) LOOPS) / benchtime);
#endif
#ifdef TIMES
	times(&tms);
	benchtime = tms.tms_utime - starttime - nulltime;
	printf("Dhrystone(%s) time for %ld passes = %ld\n",
		Version,
		(long) LOOPS, benchtime/HZ);
	printf("This machine benchmarks at %ld dhrystones/second\n",
		((long) LOOPS) * HZ / benchtime);
#endif

}

Proc1(PtrParIn)
REG RecordPtr	PtrParIn;
{
#define	NextRecord	(*(PtrParIn->PtrComp))

	structassign(NextRecord, *PtrGlb);
	PtrParIn->IntComp = 5;
	NextRecord.IntComp = PtrParIn->IntComp;
	NextRecord.PtrComp = PtrParIn->PtrComp;
	Proc3(NextRecord.PtrComp);
	if (NextRecord.Discr == Ident1)
	{
		NextRecord.IntComp = 6;
		Proc6(PtrParIn->EnumComp, &NextRecord.EnumComp);
		NextRecord.PtrComp = PtrGlb->PtrComp;
		Proc7(NextRecord.IntComp, 10, &NextRecord.IntComp);
	}
	else
		structassign(*PtrParIn, NextRecord);

#undef	NextRecord
}

Proc2(IntParIO)
OneToFifty	*IntParIO;
{
	REG OneToFifty		IntLoc;
	REG Enumeration		EnumLoc;

	IntLoc = *IntParIO + 10;
	for(;;)
	{
		if (Char1Glob == 'A')
		{
			--IntLoc;
			*IntParIO = IntLoc - IntGlob;
			EnumLoc = Ident1;
		}
		if (EnumLoc == Ident1)
			break;
	}
}

Proc3(PtrParOut)
RecordPtr	*PtrParOut;
{
	if (PtrGlb != NULL)
		*PtrParOut = PtrGlb->PtrComp;
	else
		IntGlob = 100;
	Proc7(10, IntGlob, &PtrGlb->IntComp);
}

Proc4()
{
	REG boolean	BoolLoc;

	BoolLoc = Char1Glob == 'A';
	BoolLoc |= BoolGlob;
	Char2Glob = 'B';
}

Proc5()
{
	Char1Glob = 'A';
	BoolGlob = FALSE;
}

extern boolean Func3();

Proc6(EnumParIn, EnumParOut)
REG Enumeration	EnumParIn;
REG Enumeration	*EnumParOut;
{
	*EnumParOut = EnumParIn;
	if (! Func3(EnumParIn) )
		*EnumParOut = Ident4;
	switch (EnumParIn)
	{
	case Ident1:	*EnumParOut = Ident1; break;
	case Ident2:	if (IntGlob > 100) *EnumParOut = Ident1;
			else *EnumParOut = Ident4;
			break;
	case Ident3:	*EnumParOut = Ident2; break;
	case Ident4:	break;
	case Ident5:	*EnumParOut = Ident3;
	}
}

Proc7(IntParI1, IntParI2, IntParOut)
OneToFifty	IntParI1;
OneToFifty	IntParI2;
OneToFifty	*IntParOut;
{
	REG OneToFifty	IntLoc;

	IntLoc = IntParI1 + 2;
	*IntParOut = IntParI2 + IntLoc;
}

Proc8(Array1Par, Array2Par, IntParI1, IntParI2)
Array1Dim	Array1Par;
Array2Dim	Array2Par;
OneToFifty	IntParI1;
OneToFifty	IntParI2;
{
	REG OneToFifty	IntLoc;
	REG OneToFifty	IntIndex;

	IntLoc = IntParI1 + 5;
	Array1Par[IntLoc] = IntParI2;
	Array1Par[IntLoc+1] = Array1Par[IntLoc];
	Array1Par[IntLoc+30] = IntLoc;
	for (IntIndex = IntLoc; IntIndex <= (IntLoc+1); ++IntIndex)
		Array2Par[IntLoc][IntIndex] = IntLoc;
	++Array2Par[IntLoc][IntLoc-1];
	Array2Par[IntLoc+20][IntLoc] = Array1Par[IntLoc];
	IntGlob = 5;
}

Enumeration Func1(CharPar1, CharPar2)
CapitalLetter	CharPar1;
CapitalLetter	CharPar2;
{
	REG CapitalLetter	CharLoc1;
	REG CapitalLetter	CharLoc2;

	CharLoc1 = CharPar1;
	CharLoc2 = CharLoc1;
	if (CharLoc2 != CharPar2)
		return (Ident1);
	else
		return (Ident2);
}

boolean Func2(StrParI1, StrParI2)
String30	StrParI1;
String30	StrParI2;
{
	REG OneToThirty		IntLoc;
	REG CapitalLetter	CharLoc;

	IntLoc = 1;
	while (IntLoc <= 1)
		if (Func1(StrParI1[IntLoc], StrParI2[IntLoc+1]) == Ident1)
		{
			CharLoc = 'A';
			++IntLoc;
		}
	if (CharLoc >= 'W' && CharLoc <= 'Z')
		IntLoc = 7;
	if (CharLoc == 'X')
		return(TRUE);
	else
	{
		if (strcmp(StrParI1, StrParI2) > 0)
		{
			IntLoc += 7;
			return (TRUE);
		}
		else
			return (FALSE);
	}
}

boolean Func3(EnumParIn)
REG Enumeration	EnumParIn;
{
	REG Enumeration	EnumLoc;

	EnumLoc = EnumParIn;
	if (EnumLoc == Ident3) return (TRUE);
	return (FALSE);
}

#ifdef	NOSTRUCTASSIGN
memcpy(d, s, l)
register char	*d;
register char	*s;
register int	l;
{
	while (l--) *d++ = *s++;
}
#endif

#if 0
IntLoc;
		}
	if (CharLoc >= 'W' && CharLoc <= 'Z')
		IntLoc = 7;
	if (CharLoc == 'X')
		return(TRUE);
	else
	{
		if (strcmp(StrParI1, StrParI2) > 0)
		{
			IntLoc += 7;
			return (TRUE);
		}
		else
			return (FALSE);
	}
}
#endif
