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


# Default SRM version, can be overwritten in command line call
${SRM_VERSION}	2


*** Test Cases ***
SRMMV INTO SAME DIR
	[Documentation]	Moving a file to the same directory with a different name (should just rename file)
	SET CLIENT	srmcp
	SET PROTOCOL	${PROTOCOL}	${PORT}
	SET HOST	${HOST}
	SET EXTRA ARGUMENTS	-${SRM_VERSION} -retry_num=0
	${FILE_NAME}=	REPLACE STRING	${TEST NAME}	${SPACE}	${EMPTY}
	CREATE FILE	${LOCAL_FILE}${FILE_NAME}	This is a testfile for ${TEST NAME}
	COPY LOCAL FILE		${LOCAL_FILE}${FILE_NAME}	${REMOTE_FILE}${FILE_NAME}
	COMMAND SHOULD EXECUTE SUCCESSFULLY
	SET CLIENT	${CLIENT}
	SET HOST	${HOST}		${HOST}
	SET PROTOCOL	${PROTOCOL}	${PORT}		${PROTOCOL}	${PORT}
	COPY REMOTE TO REMOTE	${REMOTE_FILE}${FILE_NAME}	${REMOTE_FILE}${FILE_NAME}1
	COMMAND SHOULD EXECUTE SUCCESSFULLY
	
