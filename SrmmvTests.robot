*** Settings ***
Variables	UserDefinedVariables.py
Resource	UserKeywords.robot

Library		String
Library		OperatingSystem
Library		Collections
Library		DoorTesterLib.py	${HOST}
Library		ProtocolTesterLib.py	

Suite Setup	TEST PROTOCOL DOOR	${PROTOCOL}	${PORT}
Suite Teardown	REMOVE LOCAL AND REMOTE FILES WITH NAMES CONTAINING	testfile	testo



*** Variables ***

${CLIENT}	srmmv
${PROTOCOL}	srm
${PORT}		&{PROTOCOL_PORTS}[${PROTOCOL}]




*** Test Cases ***
SRMMV INTO SAME DIR
	SET CLIENT	srmcp
	SET PROTOCOL	${PROTOCOL}	${PORT}
	SET HOST	${HOST}
	${FILE_NAME}=	REPLACE STRING	${TEST NAME}	${SPACE}	${EMPTY}
	CREATE FILE	${LOCAL_FILE}${FILE_NAME}	This is a testfile for ${TEST NAME}
	COPY LOCAL FILE		${LOCAL_FILE}${FILE_NAME}	${REMOTE_FILE}${FILE_NAME}
	COMMAND SHOULD EXECUTE SUCCESSFULLY
	SET CLIENT	${CLIENT}
	COPY REMOTE TO REMOTE	${REMOTE_FILE}${FILE_NAME}	${REMOTE_FILE}${FILE_NAME}1
	COMMAND SHOULD EXECUTE SUCCESSFULLY
	
