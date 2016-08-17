*** Settings ***
Variables	UserDefinedVariables.py
Resource	UserKeywords.robot

Library		DoorTesterLib.py	${HOST}
Library		ProtocolTesterLib.py	





*** Variables ***

${CLIENT}	dccp
${PROTOCOL}	gsidcap
${PORT}		&{PROTOCOL_PORTS}[${PROTOCOL}]



*** Test Cases ***
PRESTAGE ON DIR
	SET CLIENT	${CLIENT}
	SET PROTOCOL	${PROTOCOL}	${PORT}
	SET HOST	${HOST}
	SET EXTRA ARGUMENTS	-P
	PERFORM ARBITRARY COMMAND ON REMOTE DIR	${REMOTE_DIR}
	ERROR SHOULD CONTAIN	dc_stage fail

