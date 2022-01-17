1 ON SRQ THEN 20002 REM: FOR INSTRUCTIONS ON USING THIS PROGRAM, SEE LINE 10003 GO TO 1004 REM USER KEY #1: RUNS PROGRAM FROM BEGINNING WITH INSTRUCTIONS5 GO TO 1008 REM: USER KEY #2: DEVICE CLEAR9 WBYTE @20,95:10 GO TO 10012 REM: USER KEY #3: REQUEST WFM FROM INSTRUMENT13 WBYTE @A+64:14 RETURN99 REM: NOTE THAT INIT SENDS AN IFC100 INIT105 GOSUB 1000106 H=1108 T=1110 ON SRQ THEN 3000120 ON EOI THEN 4000130 SET KEY140 DIM X(512),Y(512),Q(10),P$(1)150 X=0160 Y=0175 E=0180 REM: PROCESS REQUEST QUEUE185 REM: THE QUEUE ALLOWS UP TO 9 SRQ'S TO BE RECEIVED AND SAVED FOR186 REM: PROCESSING IF THIS PROGRAM IS ALREADY PROCESSING A PREVIOUSLY187 REM: RECEIVED SRQ.195 PRINT "WAITING FOR GPIB INTERRUPT"200 IF H=T THEN 200210 GO TO Q(H) OF 270,215,290,230215 PRINT "ILLEGAL REQUEST"219 REM: REMOVE REQUEST FROM QUEUE220 Q(H)=0223 REM: DON'T LET SRQ INTERRUPT NEXT FEW LINES225 OFF SRQ230 H=H+1235 REM: SEE IF PAST QUEUE END;IF SO,WRAP AROUND TO BEGINNING240 IF H<=10 THEN 260250 H=1255 REM: TURN SRQ ENABLE BACK ON260 ON SRQ THEN 3000265 GO TO 195269 REM: POWER-ON SERVICE REQUEST ROUTINE270 PRINT "POWER-ON SERVICE REQUEST RECEIVED"275 PRINT280 GO TO 220289 REM: REQUEST TO SEND WAVEFORM290 PRINT "READY TO SEND WAVEFORM"295 PRINT300 GOSUB 500310 GOTO 220320 REM: TALKER-ONLY SERVICE REQUEST330 PRINT "TALKER-ONLY SEVICE REQUEST RECEIVED"340 PRINT "UNABLE TO PROCESS REQUEST: ISSUING DEVICE CLEAR"345 PRINT350 GO TO 8500 REM: #########################501 REM:502 REM: SUBROUTINE TO ASSIGN TALKER AND PICK UP WAVEFORM503 REM:504 REM: #########################505 REM: SEND TALK ADDRESS TO DEVICE506 REM: ADD 64 TO DEVICE ADDRESS (SET BIT 7 TO TALK DEVICE)510 WBYTE @A+64:515 PAGE519 REM: CALL ROUTINE TO DRAW GRATICULE520 GOSUB 6000550 REM: SET FIELD TO 0560 F=0564 REM: SET OUTPUT FLAG TO FALSE (0)565 O=0568 REM: SET COORDINATES OF FIRST PRINT FIELD OF SCREEN570 X1=0580 Y1=98.176585 REM: DEFINE LIMITS OF SCREEN586 VIEWPORT 0,130,0,100587 WINDOW 0,130,0,100590 REM: PICK UP A BYTE AND DECIDE WHETHER OR NOT TO PRINT IT600 MOVE X1,Y1605 RBYTE P606 IF E=0 THEN 609607 E=0608 RETURN609 REM: CHECK INPUT610 IF P<0 THEN 605620 IF P=10 THEN 605630 REM: CONVERT BYTE TO A CHARACTER635 P$=CHR(P)638 REM: IF;,THEN END OF WFM ID OR END OF A WAVEFORM640 IF P$=";" THEN 830645 REM: IF %, MEANS BEGINNING OF WAVEFORM POINT DATA650 IF P$="%" THEN 860655 REM: IF ANYTHING OTHER THAN COLON, GO ON TO SEE IF SHOULD PRINT IT660 IF P$<>":" THEN 710665 REM: HAVE ENCOUNTERED A COLON: END OF FIELD, INCREMENT FIELD COUNT670 F=F+1675 REM: SEE IF WE HAVE ENCOUNTERED TOO MANY FIELDS (SHOULD HAVE 16 MAX)680 IF F<16 THEN 700685 REM: RESET FIELD COUNT TO 1 IF HAVE EXCEEDED COUNT OF 16690 F=1695 REM: TURN OUTPUT FLAG ON (1)700 O=1705 REM: CHECK FIELD #S TO SEE IF SHOULD PRINT THIS FIELD710 IF F=1 THEN 760720 IF F=4 THEN 760730 IF F>5 AND F<9 THEN 760740 IF F>9 AND F<12 THEN 760745 REM: IF NO A FIELD TO BE PRINTED, GO BACK AND GET NEXT BYTE750 GO TO 605760 REM: SEE IF WE SHOULD PRINT THIS PART OF HE FIELD765 IF O=0 THEN 605766 REM: OUTPUT FLAG SET TRUE769 REM: DON'T WANT TO PRINT COLONS770 IF P$=":" THEN 605775 REM: PRINT CHARACTER AND SUPPRESS LINE FEED780 PRINT P$;785 IF P$<>"," THEN 605786 REM: COMMA MEANS END OF FILED. TURN OFF OUTPUT FLAG.790 O=0794 REM: CHECK TO SEE IF WE SHOULD GO TO NEXT LINE OF SCREEN795 REM: IF HAVE JUST FINISHED FIELD 1 OR 7, NEXT LINE796 IF F=1 THEN 800797 IF F=7 THEN 800798 GO TO 605800 REM: CHANGE YCOORD TO POINT TO NEX LINE810 Y1=Y1-2.816820 GO TO 600825 REM: HAVE COME TO END OF ID OR END OF WAVEFORM, RESET FIELD, OUTPUT830 F=0835 O=0838 REM: MOVE TO NEXT X PRINT FIELD840 X1=X1+26.88850 GO TO 580860 REM: PICK UP WAVEFORM DATA. FIRST GET HIGH BYTE COUNT865 RBYTE B1869 REM: GET LOW BYTE OF BYTE COUNT870 RBYTE B2872 REM: INITIALIZE CHECKSUM TO SUM OF HIGH AND LOW BYTES875 C=B1+B2879 REM: CONVERT TWO BYTES OF COUNT TO ONE NUMBER880 B=B1*256+B2-1885 REM: REDIMENSION WAVEFORM DATA ARRAYS886 DIM Y(B),X(B)890 REM: READ IN WAVEFORM DATA POINTS895 FOR I=1 TO B900 RBYTE Y(I)905 X(I)=I908 REM: ADD BYTE TO CHECKSUM TOTAL910 C=C+Y(I)920 NEXT I925 C=C-INT(C/256)*256930 REM: READ IN CHECKSUM FROM GPIB NOW935 RBYTE C1936 REM: VERIFY CHECKSUM940 IF C1+C<>256 THEN 990950 REM: IF CHECKSUM WAS OKAY, GO AHEAD AND DRAW WAVEFORM960 GOSUB 1350965 REM: GO BACK NOW AND SEE IF MORE WAVEFORMS BEING SENT970 GO TO 605990 PRINT "CHECKSUM INCORRECT"995 GO TO 8999 REM: #########################1000 REM: #########################1001 REM:1002 REM: INSTRUCTIONS FOR RUNNING THIS PROGRAM1003 REM:1004 REM: ------------------1005 PAGE1006 PRI "THIS IS A PROGRAM TO DEMONSTRATE THE GPIB OPTION OF THE 468."1007 PRINT1008 PRINT "INSTRUCTIONS:"1009 PRINT1010 PRINT "USER KEYS USED IN THIS PROGRAM:"1011 PRINT1012 PRINT "#1: STARTS THIS PROGRAM RUNNING"1013 PRINT1014 PRINT "#2: ISSUES A DEVICE CLEAR TO THE 468 AND RESTARTS PROGRAM"1015 PRINT1016 PRINT "#3: ASSIGNS INSTRUMENT AS TALKER (REQUESTS A WAVEFORM)"1017 PRINT1018 PRI "WHEN A WAVEFORM IS SENT THE FOLLOWING INFORMATION IS PRINTED:"1019 PRINT1020 PRINT "  VERSION NO.    CHANNEL, COUPLING"1021 PRINT "                 XMULTIPLIER, TRIGGER POINT, X UNITS"1022 PRINT "                 YMULTIPLIER, GROUND POINT, Y UNITS"1023 PRINT1024 PRINT "AFTER ALL WAVEFORMS HAVE BEEN DRAWN, YOU MUST PRESS <CR>"1025 PRINT "TO PAGE THE SCREEN AND GO BACK TO WAITING FOR THE NEXT"1026 PRINT "GPIB REQUEST."1027 PRINT1028 PRINT "MAKE SURE THE GPIB CABLE IS CONNECTED BEFORE SENDING A"1029 PRINT "WAVEFORM OR REQUESTING ONE USING THE 4051."1030 PRINT1031 PRINT "THIS PROGRAM CAN BE AUTOLOADED IF IT IS FILE #1 ON TAPE."1032 PRINT1033 PRINT "PRESS <CR> TO CONTINUE"1034 DIM I$(1)1035 INPUT I$1038 PAGE1040 PRINT "ENTER GPIB ADDRESS OF 468 (NUMBER BETWEEN 0 AND 30):";1045 INPUT A1050 IF A<0 THEN 10651055 IF A>30 THEN 10651060 RETURN1065 PRINT "ADDRESS IS OUTSIDE 0-30 RANGE. RE-ENTER ADDRESS:";1070 GO TO 10451350 REM: #########################1351 REM:1352 REM: ROUTINE TO PLOT WAVEFORM1353 REM:1354 REM: #########################1355 VIEWPORT 20,122.4,0,102.41358 REM: CHECK NUMBER OF WAVEFORM BYTES1360 IF B=256 THEN 13751363 REM: IF 512 POINTS, SET PLOT FOR 512 PTS1365 WINDOW 1,512,0,2551370 GO TO 13801374 REM: IF 256 POINTS, ONLY SET FOR 256 PTS1375 WINDOW 1,256,0,2551378 REM: MOVE TO ORIGIN OF PLOT1380 MOVE 0,01385 REM: DRAW WAVEFORM1390 DRAW X,Y1394 REM: RETURN CURSOR TO UPPER LEFT CORNER OF SCREEN1395 HOME1398 RETURN2000 REM: THIS IS HERE IN CASE AN SQR IS ASSERTED BEFORE THIS PROGRAM2001 REM: IS STARTED RUNNING2005 DIM Q(10)2010 GOSUB 10002015 H=12020 T=12025 GOSUB 30002030 GO TO 1103000 REM: #########################3001 REM:3002 REM: SRQ SERVICE ROUTINE3003 REM:3004 REM: #########################3005 REM: POLL DEVICES TO SEE WHICH INSTRUMENT REQUESTED SERVICE3010 POLL D,S;A3020 REM: ONLY 1 DEVICE ATTACHED, NO NEED TO CHECK DEVICE NUMBER (D)3021 REM: ADJUST STATUS SO IT IS A NUMBER BETWEEN 1 AND 43022 REM: STATUSES: PON = 65, TRANSMIT REQUEST = 195, TON = 1963025 IF S<64 THEN 31003030 S=S-643035 REM: NOW CHECK TO SEE IF IT IS TRANSMIT OR TON3040 IF S<100 THEN 30603045 REM: IF TRANSMIT OR TON, MUST ADJUST AGAIN (SUBTRACT 128)3050 S=S-1283055 REM: NOW SET TASK TO BE PROCESSED (ADD TO TASK QUEUE)3060 Q(T)=S3065 T=T+13070 IF T<=10 THEN 30803075 T=13080 IF H=T THEN 30903085 RETURN3090 REM: A QUEUE ERROR OCURRED, QUEUE IS FULL.3095 PRINT "QUEUE FULL-PROGRAM ABORTED"3099 GOTO 83100 REM: ILLEGAL STATUS BYTE PICKED UP3110 PRINT "ILLEGAL STATUS BYTE RECEIVED. STATUS=";S3115 PRINT "ISSUING DEVICE CLEAR"3120 GO TO 84000 REM: #########################4001 REM:4002 REM: EOI ROUTINE4003 REM:4004 REM: #########################4005 REM: SET FLAG TO SAY EOI ENCOUNTERED4006 REM: UNTALK AND UNLISTEN ALL DEVICES4007 WBYTE @63,95:4008 DIM C$(1)4010 E=14015 REM: WAIT FOR OPERATOR TO ENTER A KEY BEFORE RETURNING4020 INPUT C$4025 PAGE4030 RETURN6000 REM: #########################6001 REM:6002 REM: ROUTINE TO DRAW GRATICULE FOR WAVEFORM DISPLAY6003 REM:6004 REM: #########################6005 REM: DRAW GRATICULE IN LOWER RIGHT PORTION OF SCREEN6010 VIEWPORT 20,120,11.2,91.26015 REM: SET LIMITS OF GRAPHICS6020 WINDOW 0,511,101.4,920.66025 REM: POSITION CURSOR TO BEGIN DRAWING GRATICULE6030 MOVE 0,101.46040 DRAW 511,101.46050 DRAW 511,920.66060 DRAW 0,920.66070 DRAW 0,101.46080 AXIS 10.24,20.48,255,5116090 FOR I=1 TO 96100 AXIS 0,0,I*51.2,I*102.4+101.46110 NEXT I6120 VIEWPORT 30,130,0,1006130 WINDOW 0,511,0,10236140 HOME6150 RETURN