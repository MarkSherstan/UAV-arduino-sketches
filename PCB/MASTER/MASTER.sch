EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr USLetter 11000 8500
encoding utf-8
Sheet 1 1
Title "MASTER"
Date "2020-05-07"
Rev "1"
Comp "Mark Sherstan"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L MCU_Module:Arduino_Nano_v3.x A1
U 1 1 5EB2E547
P 5200 4250
F 0 "A1" H 5200 3161 50  0000 C CNN
F 1 "Arduino_Nano_v3.x" H 5200 3070 50  0000 C CNN
F 2 "Module:Arduino_Nano" H 5200 4250 50  0001 C CIN
F 3 "http://www.mouser.com/pdfdocs/Gravitech_Arduino_Nano3_0.pdf" H 5200 4250 50  0001 C CNN
	1    5200 4250
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0101
U 1 1 5EB2FAD6
P 4700 5350
F 0 "#PWR0101" H 4700 5100 50  0001 C CNN
F 1 "GND" H 4705 5177 50  0000 C CNN
F 2 "" H 4700 5350 50  0001 C CNN
F 3 "" H 4700 5350 50  0001 C CNN
	1    4700 5350
	1    0    0    -1  
$EndComp
Wire Wire Line
	4700 5350 4700 5250
Wire Wire Line
	5300 5250 5750 5250
Wire Wire Line
	5750 5250 5750 5350
Wire Wire Line
	4700 5250 5200 5250
$Comp
L power:GND #PWR0102
U 1 1 5EB32798
P 5750 5350
F 0 "#PWR0102" H 5750 5100 50  0001 C CNN
F 1 "GND" H 5755 5177 50  0000 C CNN
F 2 "" H 5750 5350 50  0001 C CNN
F 3 "" H 5750 5350 50  0001 C CNN
	1    5750 5350
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0103
U 1 1 5EB32869
P 5400 3250
F 0 "#PWR0103" H 5400 3100 50  0001 C CNN
F 1 "+5V" H 5415 3423 50  0000 C CNN
F 2 "" H 5400 3250 50  0001 C CNN
F 3 "" H 5400 3250 50  0001 C CNN
	1    5400 3250
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0104
U 1 1 5EB33F05
P 5300 2950
F 0 "#PWR0104" H 5300 2800 50  0001 C CNN
F 1 "+3.3V" H 5315 3123 50  0000 C CNN
F 2 "" H 5300 2950 50  0001 C CNN
F 3 "" H 5300 2950 50  0001 C CNN
	1    5300 2950
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0105
U 1 1 5EB34843
P 5100 2700
F 0 "#PWR0105" H 5100 2550 50  0001 C CNN
F 1 "VCC" H 5117 2873 50  0000 C CNN
F 2 "" H 5100 2700 50  0001 C CNN
F 3 "" H 5100 2700 50  0001 C CNN
	1    5100 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	5100 2700 5100 3250
Wire Wire Line
	5300 2950 5300 3250
Text GLabel 4400 4350 0    50   Input ~ 0
CE
Text GLabel 4400 4450 0    50   Input ~ 0
CSN
Text GLabel 4400 4750 0    50   Input ~ 0
MOSI
Text GLabel 4400 4850 0    50   Input ~ 0
MISO
Text GLabel 4400 4950 0    50   Input ~ 0
SCK
Wire Wire Line
	4400 4350 4700 4350
Wire Wire Line
	4700 4450 4400 4450
Wire Wire Line
	4400 4750 4700 4750
Wire Wire Line
	4700 4850 4400 4850
Wire Wire Line
	4400 4950 4700 4950
$Comp
L RF:NRF24L01_Breakout U1
U 1 1 5EB37153
P 1750 4450
F 0 "U1" H 2130 4496 50  0000 L CNN
F 1 "NRF24L01_Breakout" H 2130 4405 50  0000 L CNN
F 2 "RF_Module:nRF24L01_Breakout" H 1900 5050 50  0001 L CIN
F 3 "http://www.nordicsemi.com/eng/content/download/2730/34105/file/nRF24L01_Product_Specification_v2_0.pdf" H 1750 4350 50  0001 C CNN
	1    1750 4450
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0106
U 1 1 5EB3CD7B
P 1750 5200
F 0 "#PWR0106" H 1750 4950 50  0001 C CNN
F 1 "GND" H 1755 5027 50  0000 C CNN
F 2 "" H 1750 5200 50  0001 C CNN
F 3 "" H 1750 5200 50  0001 C CNN
	1    1750 5200
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0107
U 1 1 5EB3DDC5
P 1750 3700
F 0 "#PWR0107" H 1750 3550 50  0001 C CNN
F 1 "+3.3V" H 1765 3873 50  0000 C CNN
F 2 "" H 1750 3700 50  0001 C CNN
F 3 "" H 1750 3700 50  0001 C CNN
	1    1750 3700
	1    0    0    -1  
$EndComp
Wire Wire Line
	1750 3850 1750 3700
Wire Wire Line
	1750 5200 1750 5050
Text GLabel 1050 4150 0    50   Input ~ 0
MOSI
Text GLabel 1050 4250 0    50   Input ~ 0
MISO
Text GLabel 1050 4350 0    50   Input ~ 0
SCK
Text GLabel 1050 4450 0    50   Input ~ 0
CSN
Text GLabel 1050 4650 0    50   Input ~ 0
CE
Wire Wire Line
	1050 4150 1250 4150
Wire Wire Line
	1250 4250 1050 4250
Wire Wire Line
	1050 4350 1250 4350
Wire Wire Line
	1250 4450 1050 4450
Wire Wire Line
	1050 4650 1250 4650
$Comp
L Device:R R1
U 1 1 5EB40232
P 1400 6900
F 0 "R1" V 1193 6900 50  0000 C CNN
F 1 "220 ohm" V 1284 6900 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 1330 6900 50  0001 C CNN
F 3 "https://www.digikey.ca/product-detail/en/panasonic-electronic-components/ERJ-PA3J221V/P220BZCT-ND/5036283" H 1400 6900 50  0001 C CNN
F 4 "P220BZCT-ND" V 1400 6900 50  0001 C CNN "Field4"
	1    1400 6900
	0    1    1    0   
$EndComp
$Comp
L Device:LED D1
U 1 1 5EB407E9
P 2050 6900
F 0 "D1" H 2043 6645 50  0000 C CNN
F 1 "R-LED" H 2043 6736 50  0000 C CNN
F 2 "LED_SMD:LED_0603_1608Metric_Pad1.05x0.95mm_HandSolder" H 2050 6900 50  0001 C CNN
F 3 "https://www.digikey.ca/product-detail/en/lite-on-inc/LTST-C191KRKT/160-1447-1-ND/386836" H 2050 6900 50  0001 C CNN
F 4 "160-1447-1-ND" H 2050 6900 50  0001 C CNN "Field4"
	1    2050 6900
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0108
U 1 1 5EB42F6B
P 2650 7050
F 0 "#PWR0108" H 2650 6800 50  0001 C CNN
F 1 "GND" H 2655 6877 50  0000 C CNN
F 2 "" H 2650 7050 50  0001 C CNN
F 3 "" H 2650 7050 50  0001 C CNN
	1    2650 7050
	1    0    0    -1  
$EndComp
Text GLabel 850  6900 0    50   Input ~ 0
D9
Text GLabel 850  7550 0    50   Input ~ 0
D10
Text GLabel 4400 4550 0    50   Input ~ 0
D9
Text GLabel 4400 4650 0    50   Input ~ 0
D10
Wire Wire Line
	4400 4550 4700 4550
Wire Wire Line
	4700 4650 4400 4650
Wire Wire Line
	850  6900 1250 6900
Wire Wire Line
	1550 6900 1900 6900
Wire Wire Line
	2200 6900 2650 6900
Wire Wire Line
	2650 6900 2650 7050
$Comp
L Device:R R2
U 1 1 5EB48633
P 1400 7550
F 0 "R2" V 1193 7550 50  0000 C CNN
F 1 "220 ohm" V 1284 7550 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad1.05x0.95mm_HandSolder" V 1330 7550 50  0001 C CNN
F 3 "https://www.digikey.ca/product-detail/en/panasonic-electronic-components/ERJ-PA3J221V/P220BZCT-ND/5036283" H 1400 7550 50  0001 C CNN
F 4 "P220BZCT-ND" V 1400 7550 50  0001 C CNN "Field4"
	1    1400 7550
	0    1    1    0   
$EndComp
$Comp
L Device:LED D2
U 1 1 5EB48639
P 2050 7550
F 0 "D2" H 2043 7295 50  0000 C CNN
F 1 "G-LED" H 2043 7386 50  0000 C CNN
F 2 "LED_SMD:LED_0603_1608Metric_Pad1.05x0.95mm_HandSolder" H 2050 7550 50  0001 C CNN
F 3 "https://www.digikey.ca/product-detail/en/lite-on-inc/LTST-C191GKT/160-1443-6-ND/1888655" H 2050 7550 50  0001 C CNN
F 4 "160-1443-6-ND" H 2050 7550 50  0001 C CNN "Field4"
	1    2050 7550
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0109
U 1 1 5EB4863F
P 2650 7700
F 0 "#PWR0109" H 2650 7450 50  0001 C CNN
F 1 "GND" H 2655 7527 50  0000 C CNN
F 2 "" H 2650 7700 50  0001 C CNN
F 3 "" H 2650 7700 50  0001 C CNN
	1    2650 7700
	1    0    0    -1  
$EndComp
Wire Wire Line
	1550 7550 1900 7550
Wire Wire Line
	2200 7550 2650 7550
Wire Wire Line
	2650 7550 2650 7700
Wire Wire Line
	850  7550 1250 7550
$Comp
L Connector_Generic:Conn_01x03 J2
U 1 1 5EB4B447
P 8950 3850
F 0 "J2" H 9030 3892 50  0000 L CNN
F 1 "Conn_01x03" H 9030 3801 50  0000 L CNN
F 2 "Connector_Molex:Molex_Micro-Fit_3.0_43650-0300_1x03_P3.00mm_Horizontal" H 8950 3850 50  0001 C CNN
F 3 "~" H 8950 3850 50  0001 C CNN
	1    8950 3850
	1    0    0    -1  
$EndComp
Text GLabel 4400 4050 0    50   Input ~ 0
D4
Wire Wire Line
	4400 4050 4700 4050
Text GLabel 8550 3950 0    50   Input ~ 0
D4
$Comp
L power:GND #PWR0110
U 1 1 5EB4D1CF
P 8050 3750
F 0 "#PWR0110" H 8050 3500 50  0001 C CNN
F 1 "GND" H 8055 3577 50  0000 C CNN
F 2 "" H 8050 3750 50  0001 C CNN
F 3 "" H 8050 3750 50  0001 C CNN
	1    8050 3750
	1    0    0    -1  
$EndComp
Wire Wire Line
	8050 3750 8750 3750
Wire Wire Line
	8250 3850 8750 3850
Wire Wire Line
	8550 3950 8750 3950
$Comp
L Connector_Generic:Conn_01x02 J1
U 1 1 5EB51CDD
P 1400 1450
F 0 "J1" H 1318 1125 50  0000 C CNN
F 1 "Conn_01x02" H 1318 1216 50  0000 C CNN
F 2 "Connector_Molex:Molex_Micro-Fit_3.0_43650-0200_1x02_P3.00mm_Horizontal" H 1400 1450 50  0001 C CNN
F 3 "~" H 1400 1450 50  0001 C CNN
	1    1400 1450
	-1   0    0    1   
$EndComp
$Comp
L Mechanical:MountingHole_Pad H1
U 1 1 5EB55153
P 4400 6900
F 0 "H1" H 4500 6949 50  0000 L CNN
F 1 "MountingHole_Pad" H 4500 6858 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3_ISO14580_Pad" H 4400 6900 50  0001 C CNN
F 3 "~" H 4400 6900 50  0001 C CNN
	1    4400 6900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0111
U 1 1 5EB55D99
P 4400 7150
F 0 "#PWR0111" H 4400 6900 50  0001 C CNN
F 1 "GND" H 4405 6977 50  0000 C CNN
F 2 "" H 4400 7150 50  0001 C CNN
F 3 "" H 4400 7150 50  0001 C CNN
	1    4400 7150
	1    0    0    -1  
$EndComp
Wire Wire Line
	4400 7150 4400 7000
$Comp
L Mechanical:MountingHole_Pad H3
U 1 1 5EB595D8
P 5400 6900
F 0 "H3" H 5500 6949 50  0000 L CNN
F 1 "MountingHole_Pad" H 5500 6858 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3_ISO14580_Pad" H 5400 6900 50  0001 C CNN
F 3 "~" H 5400 6900 50  0001 C CNN
	1    5400 6900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0112
U 1 1 5EB595DE
P 5400 7150
F 0 "#PWR0112" H 5400 6900 50  0001 C CNN
F 1 "GND" H 5405 6977 50  0000 C CNN
F 2 "" H 5400 7150 50  0001 C CNN
F 3 "" H 5400 7150 50  0001 C CNN
	1    5400 7150
	1    0    0    -1  
$EndComp
Wire Wire Line
	5400 7150 5400 7000
$Comp
L Mechanical:MountingHole_Pad H2
U 1 1 5EB5A561
P 4400 7550
F 0 "H2" H 4500 7599 50  0000 L CNN
F 1 "MountingHole_Pad" H 4500 7508 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3_ISO14580_Pad" H 4400 7550 50  0001 C CNN
F 3 "~" H 4400 7550 50  0001 C CNN
	1    4400 7550
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0113
U 1 1 5EB5A567
P 4400 7800
F 0 "#PWR0113" H 4400 7550 50  0001 C CNN
F 1 "GND" H 4405 7627 50  0000 C CNN
F 2 "" H 4400 7800 50  0001 C CNN
F 3 "" H 4400 7800 50  0001 C CNN
	1    4400 7800
	1    0    0    -1  
$EndComp
Wire Wire Line
	4400 7800 4400 7650
$Comp
L Mechanical:MountingHole_Pad H4
U 1 1 5EB5AD99
P 5400 7550
F 0 "H4" H 5500 7599 50  0000 L CNN
F 1 "MountingHole_Pad" H 5500 7508 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3_ISO14580_Pad" H 5400 7550 50  0001 C CNN
F 3 "~" H 5400 7550 50  0001 C CNN
	1    5400 7550
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0114
U 1 1 5EB5AD9F
P 5400 7800
F 0 "#PWR0114" H 5400 7550 50  0001 C CNN
F 1 "GND" H 5405 7627 50  0000 C CNN
F 2 "" H 5400 7800 50  0001 C CNN
F 3 "" H 5400 7800 50  0001 C CNN
	1    5400 7800
	1    0    0    -1  
$EndComp
Wire Wire Line
	5400 7800 5400 7650
Wire Wire Line
	1600 1450 1800 1450
Wire Wire Line
	2100 1350 2100 1450
$Comp
L power:+BATT #PWR0115
U 1 1 5EB72CEA
P 2100 1450
F 0 "#PWR0115" H 2100 1300 50  0001 C CNN
F 1 "+BATT" H 2115 1623 50  0000 C CNN
F 2 "" H 2100 1450 50  0001 C CNN
F 3 "" H 2100 1450 50  0001 C CNN
	1    2100 1450
	-1   0    0    1   
$EndComp
$Comp
L power:-BATT #PWR0116
U 1 1 5EB7373B
P 1800 1450
F 0 "#PWR0116" H 1800 1300 50  0001 C CNN
F 1 "-BATT" H 1815 1623 50  0000 C CNN
F 2 "" H 1800 1450 50  0001 C CNN
F 3 "" H 1800 1450 50  0001 C CNN
	1    1800 1450
	-1   0    0    1   
$EndComp
Wire Wire Line
	1600 1350 2100 1350
$Comp
L MASTER-Custom-Lib:LM2596-Breakout-Board U2
U 1 1 5EB8007E
P 5050 1300
F 0 "U2" V 5228 1371 50  0000 L CNN
F 1 "LM2596-Breakout-Board" V 4850 850 50  0000 L CNN
F 2 "LM2596-Breakout-Board:LM2596-Breakout-Board" H 5150 2250 50  0001 C CNN
F 3 "" H 5150 2250 50  0001 C CNN
	1    5050 1300
	0    -1   -1   0   
$EndComp
$Comp
L power:+BATT #PWR0117
U 1 1 5EB812D3
P 4500 1200
F 0 "#PWR0117" H 4500 1050 50  0001 C CNN
F 1 "+BATT" H 4515 1373 50  0000 C CNN
F 2 "" H 4500 1200 50  0001 C CNN
F 3 "" H 4500 1200 50  0001 C CNN
	1    4500 1200
	1    0    0    -1  
$EndComp
$Comp
L power:-BATT #PWR0118
U 1 1 5EB812D9
P 4250 1400
F 0 "#PWR0118" H 4250 1250 50  0001 C CNN
F 1 "-BATT" H 4265 1573 50  0000 C CNN
F 2 "" H 4250 1400 50  0001 C CNN
F 3 "" H 4250 1400 50  0001 C CNN
	1    4250 1400
	-1   0    0    1   
$EndComp
Wire Wire Line
	4250 1400 4650 1400
Wire Wire Line
	4650 1200 4500 1200
$Comp
L power:VCC #PWR0119
U 1 1 5EB8873B
P 5600 1200
F 0 "#PWR0119" H 5600 1050 50  0001 C CNN
F 1 "VCC" H 5617 1373 50  0000 C CNN
F 2 "" H 5600 1200 50  0001 C CNN
F 3 "" H 5600 1200 50  0001 C CNN
	1    5600 1200
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0120
U 1 1 5EB8947F
P 5800 1400
F 0 "#PWR0120" H 5800 1150 50  0001 C CNN
F 1 "GND" H 5805 1227 50  0000 C CNN
F 2 "" H 5800 1400 50  0001 C CNN
F 3 "" H 5800 1400 50  0001 C CNN
	1    5800 1400
	1    0    0    -1  
$EndComp
Wire Wire Line
	5600 1200 5400 1200
Wire Wire Line
	5400 1400 5800 1400
$Comp
L power:VCC #PWR0121
U 1 1 5EB93964
P 8250 3850
F 0 "#PWR0121" H 8250 3700 50  0001 C CNN
F 1 "VCC" H 8267 4023 50  0000 C CNN
F 2 "" H 8250 3850 50  0001 C CNN
F 3 "" H 8250 3850 50  0001 C CNN
	1    8250 3850
	-1   0    0    1   
$EndComp
Text GLabel 4400 3650 0    50   Input ~ 0
RX
Text GLabel 4400 3750 0    50   Input ~ 0
TX
Wire Wire Line
	4400 3750 4700 3750
Wire Wire Line
	4400 3650 4700 3650
Text GLabel 7400 6300 0    50   Input ~ 0
RX
Text GLabel 7400 6200 0    50   Input ~ 0
TX
$Comp
L Connector_Generic:Conn_01x02 J4
U 1 1 5EB3F66F
P 7700 1450
F 0 "J4" H 7618 1125 50  0000 C CNN
F 1 "Conn_01x02" H 7618 1216 50  0000 C CNN
F 2 "Connector_Molex:Molex_Micro-Fit_3.0_43650-0200_1x02_P3.00mm_Horizontal" H 7700 1450 50  0001 C CNN
F 3 "~" H 7700 1450 50  0001 C CNN
	1    7700 1450
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0122
U 1 1 5EB40110
P 8050 1450
F 0 "#PWR0122" H 8050 1200 50  0001 C CNN
F 1 "GND" H 8055 1277 50  0000 C CNN
F 2 "" H 8050 1450 50  0001 C CNN
F 3 "" H 8050 1450 50  0001 C CNN
	1    8050 1450
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0123
U 1 1 5EB40E7C
P 8300 1350
F 0 "#PWR0123" H 8300 1200 50  0001 C CNN
F 1 "VCC" H 8317 1523 50  0000 C CNN
F 2 "" H 8300 1350 50  0001 C CNN
F 3 "" H 8300 1350 50  0001 C CNN
	1    8300 1350
	-1   0    0    1   
$EndComp
Wire Wire Line
	7900 1350 8300 1350
Wire Wire Line
	7900 1450 8050 1450
$Comp
L Connector_Generic:Conn_01x02 J3
U 1 1 5EB45651
P 7850 6200
F 0 "J3" H 7768 5875 50  0000 C CNN
F 1 "Conn_01x02" H 7768 5966 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 7850 6200 50  0001 C CNN
F 3 "~" H 7850 6200 50  0001 C CNN
	1    7850 6200
	1    0    0    -1  
$EndComp
Wire Wire Line
	7400 6300 7650 6300
Wire Wire Line
	7650 6200 7400 6200
$Comp
L Connector_Generic:Conn_01x02 J5
U 1 1 5EB56929
P 8850 1450
F 0 "J5" H 8768 1125 50  0000 C CNN
F 1 "Conn_01x02" H 8768 1216 50  0000 C CNN
F 2 "Connector_Molex:Molex_Micro-Fit_3.0_43650-0200_1x02_P3.00mm_Horizontal" H 8850 1450 50  0001 C CNN
F 3 "~" H 8850 1450 50  0001 C CNN
	1    8850 1450
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0124
U 1 1 5EB5692F
P 9200 1450
F 0 "#PWR0124" H 9200 1200 50  0001 C CNN
F 1 "GND" H 9205 1277 50  0000 C CNN
F 2 "" H 9200 1450 50  0001 C CNN
F 3 "" H 9200 1450 50  0001 C CNN
	1    9200 1450
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR0125
U 1 1 5EB56935
P 9450 1350
F 0 "#PWR0125" H 9450 1200 50  0001 C CNN
F 1 "VCC" H 9467 1523 50  0000 C CNN
F 2 "" H 9450 1350 50  0001 C CNN
F 3 "" H 9450 1350 50  0001 C CNN
	1    9450 1350
	-1   0    0    1   
$EndComp
Wire Wire Line
	9050 1350 9450 1350
Wire Wire Line
	9050 1450 9200 1450
$Comp
L Connector_Generic:Conn_01x03 J6
U 1 1 5EB7503F
P 9300 6300
F 0 "J6" H 9380 6342 50  0000 L CNN
F 1 "Conn_01x03" H 9380 6251 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 9300 6300 50  0001 C CNN
F 3 "~" H 9300 6300 50  0001 C CNN
	1    9300 6300
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0126
U 1 1 5EB76185
P 8550 6200
F 0 "#PWR0126" H 8550 5950 50  0001 C CNN
F 1 "GND" H 8555 6027 50  0000 C CNN
F 2 "" H 8550 6200 50  0001 C CNN
F 3 "" H 8550 6200 50  0001 C CNN
	1    8550 6200
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0127
U 1 1 5EB76D83
P 8750 6300
F 0 "#PWR0127" H 8750 6150 50  0001 C CNN
F 1 "+5V" H 8765 6473 50  0000 C CNN
F 2 "" H 8750 6300 50  0001 C CNN
F 3 "" H 8750 6300 50  0001 C CNN
	1    8750 6300
	-1   0    0    1   
$EndComp
Text GLabel 4400 3950 0    50   Input ~ 0
D3
Wire Wire Line
	4400 3950 4700 3950
Text GLabel 9050 6400 0    50   Input ~ 0
D3
Wire Wire Line
	9100 6300 8750 6300
Wire Wire Line
	8550 6200 9100 6200
Wire Wire Line
	9100 6400 9050 6400
Text Notes 5050 6550 0    50   ~ 0
Mounting
Text Notes 1550 6450 0    50   ~ 0
Indicators
Text Notes 1450 3300 0    50   ~ 0
RF Communication
Text Notes 1500 950  0    50   ~ 0
Power In
Text Notes 8000 5900 0    50   ~ 0
Future Auxiliary Ports
Text Notes 4950 2350 0    50   ~ 0
Microcontroller
Text Notes 8550 3450 0    50   ~ 0
Servo
Text Notes 8300 950  0    50   ~ 0
Power Out
Text Notes 4700 900  0    50   ~ 0
Buck Regulator
$EndSCHEMATC
