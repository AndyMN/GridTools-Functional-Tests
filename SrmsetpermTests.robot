*** Settings ***
Variables	UserDefinedVariables.py
Resource	UserKeywords.robot

Library		String
Library		Collections
Library		DoorTesterLib.py	${HOST}
Library		ProtocolTesterLib.py
Suite Setup	TEST PROTOCOL DOOR	${PROTOCOL}	${PORT}
Suite Teardown	REMOVE REMOTE DIRECTORIES WITH NAMES CONTAINING	testo



*** Variables ***

${CLIENT}	srm-set-permissions
${PROTOCOL}	srm
${PORT}		&{PROTOCOL_PORTS}[${PROTOCOL}]




*** Test Cases ***
CHANGE DIR PERMISSIONS
	SET CLIENT	srmmkdir
	SET PROTOCOL	${PROTOCOL}	${PORT}
	SET HOST	${HOST}
	${DIR_NAME}=	REPLACE STRING	${TEST NAME}	${SPACE}	${EMPTY}
	CREATE REMOTE DIRECTORY		${REMOTE_DIR}${DIR_NAME}testo
	COMMAND SHOULD EXECUTE SUCCESSFULLY
	SET CLIENT	${CLIENT}
	CHANGE REMOTE PERMISSIONS	${REMOTE_DIR}${DIR_NAME}testo	perm_type=CHANGE	other=NONE
	COMMAND SHOULD EXECUTE SUCCESSFULLY
