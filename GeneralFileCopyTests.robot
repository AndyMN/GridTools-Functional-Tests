
*** Settings ***
Variables   UserDefinedVariables.py
Resource    UserKeywords.robot

Library		OperatingSystem
Library		Collections

Library		ProtocolTesterLib.py
Library		DoorTesterLib.py	${HOST}
Library		FileTesterLib.py


Suite Setup	CHECK IF DOORS ARE OPEN		${PROTOCOL_PORTS}
Suite Teardown	REMOVE LOCAL AND REMOTE FILES WITH NAMES CONTAINING	testfile	testo
Test Template	COPY FILE WITH CLIENT AND PROTOCOL


*** Test Cases ***
SRMCP	srmcp	srm	${LOCAL_FILE}	${REMOTE_FILE}
DCCP	dccp	gsidcap	${LOCAL_FILE}	${REMOTE_FILE}	EXTRA_ARGUMENTS=-A
GLOBUS	globus-url-copy	gsiftp	${LOCAL_FILE}	${REMOTE_FILE}
ARCCP	arccp	srm	${LOCAL_FILE}	${REMOTE_FILE}


*** Keywords ***

COPY FILE WITH CLIENT AND PROTOCOL
	[Documentation]	General test case structure for copying a file with a specific client using a specific protocol
	[Arguments]	${CLIENT}	${PROTOCOL}	${LOCAL_FILE}	${REMOTE_FILE}	${EXTRA_ARGUMENTS}=${EMPTY}     ${PROTOCOL_PORT}=-1
	CREATE FILE	${LOCAL_FILE}${TEST NAME}	This is a testfile for ${TEST NAME}
	SET CLIENT	${CLIENT}
	${PORT}=    SET VARIABLE  ${PROTOCOL_PORT}
	${PORT}=    RUN KEYWORD IF  ${PROTOCOL_PORT} < 0    GET FROM DICTIONARY     ${PROTOCOL_PORTS}  ${PROTOCOL}
	SET PROTOCOL	${PROTOCOL}	${PORT}
	SET EXTRA ARGUMENTS	${EXTRA_ARGUMENTS}
	SET HOST	${HOST}
	COPY LOCAL FILE	${LOCAL_FILE}${TEST NAME}	${REMOTE_FILE}${TEST NAME}
	COMMAND SHOULD EXECUTE SUCCESSFULLY
	COPY REMOTE FILE	${REMOTE_FILE}${TEST NAME}	${LOCAL_FILE}${TEST NAME}1
	COMMAND SHOULD EXECUTE SUCCESSFULLY
	FILES SHOULD BE THE SAME	${LOCAL_FILE}${TEST NAME}	${LOCAL_FILE}${TEST NAME}1



