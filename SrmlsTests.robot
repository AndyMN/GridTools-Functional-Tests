*** Settings ***

Variables	UserDefinedVariables.py
Resource	UserKeywords.robot

Library		String
Library		Collections
Library		DoorTesterLib.py	${HOST}
Library		ProtocolTesterLib.py

Suite Setup	TEST PROTOCOL DOOR	${PROTOCOL}	${PORT}


*** Variables ***

${CLIENT}	srmls
${PROTOCOL}	srm
${PORT}		&{PROTOCOL_PORTS}[${PROTOCOL}]

# Default SRM version, can be overwritten in command line call
${SRM_VERSION}	2


*** Test Cases ***
VALID PATH
	[Documentation]	Try to ls a valid directory path
	SET CLIENT	${CLIENT}
	SET PROTOCOL	${PROTOCOL}	${PORT}
	SET HOST	${HOST}
	SET EXTRA ARGUMENTS	-${SRM_VERSION} -retry_num=0
	GET REMOTE FILES LIST	${REMOTE_DIR}
	COMMAND SHOULD EXECUTE SUCCESSFULLY
	
INVALID PATH
	[Documentation]	Try to ls an invalid directory path
	SET CLIENT	${CLIENT}
	SET PROTOCOL	${PROTOCOL}	${PORT}
	SET HOST	${HOST}
	SET EXTRA ARGUMENTS	-${SRM_VERSION} -retry_num=0
	${FAKE_DIR}=	REPLACE STRING	${TEST NAME}	${SPACE}	${EMPTY}
	GET REMOTE FILES LIST	${REMOTE_DIR}${FAKE_DIR}
	ERROR SHOULD CONTAIN	SRM_INVALID_PATH
