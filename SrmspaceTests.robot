*** Settings ***
Variables	UserDefinedVariables.py
Resource	UserKeywords.robot

Library		String
Library		OperatingSystem
Library		DoorTesterLib.py	${HOST}
Library		ProtocolTesterLib.py

Suite Setup	TEST PROTOCOL DOOR	${PROTOCOL}	${PORT}
Suite Teardown	REMOVE LOCAL AND REMOTE FILES WITH NAMES CONTAINING	testfile	testo



*** Variables ***
${CLIENT}	srm-get-space-tokens
${PROTOCOL}	srm
${PORT}		&{PROTOCOL_PORTS}[${PROTOCOL}]

${SPACE_DESC}	robot-g2-testspace

# Default SRM version, can be overwritten in command line call
${SRM_VERSION}	2


*** Test Cases ***
GET SPACE TOKENS
	[Documentation]	Checks if it can get space tokens from the host
	SET CLIENT	srm-reserve-space
	SET PROTOCOL	${PROTOCOL}	${PORT}
	SET HOST	${HOST}
	SET EXTRA ARGUMENTS	-${SRM_VERSION} -retry_num=0
	${SPACE_TOKEN}=		RESERVE SPACE	${SPACE_DESC}	guaranteed_size=2	retention_policy=REPLICA
	COMMAND SHOULD EXECUTE SUCCESSFULLY
	SET CLIENT	srm-get-space-tokens
	GET SPACE TOKENS	space_desc=${SPACE_DESC}
	COMMAND SHOULD EXECUTE SUCCESSFULLY
	SET CLIENT	srm-release-space
	RELEASE SPACE	${SPACE_TOKEN}
	COMMAND SHOULD EXECUTE SUCCESSFULLY


PUT REMOVED
	[Documentation]	(Weird test, ported from G2) Copies a file then removes it and then copies it again.
	SET CLIENT	srmcp
	SET PROTOCOL	${PROTOCOL}	${PORT}
	SET HOST	${HOST}
	SET EXTRA ARGUMENTS	-${SRM_VERSION} -retry_num=0
	${FILE_NAME}=	REPLACE STRING	${TEST NAME}	${SPACE}	${EMPTY}
	CREATE FILE	${LOCAL_FILE}${FILE_NAME}	This is a testfile for ${TEST NAME}
	COPY LOCAL FILE		${LOCAL_FILE}${FILE_NAME}	${REMOTE_FILE}${FILE_NAME}
	COMMAND SHOULD EXECUTE SUCCESSFULLY
	SET CLIENT	srmrm
	REMOVE REMOTE FILE	${REMOTE_FILE}${FILE_NAME}
	COMMAND SHOULD EXECUTE SUCCESSFULLY
	SET CLIENT	srmcp
	COPY LOCAL FILE		${LOCAL_FILE}${FILE_NAME}	${REMOTE_FILE}${FILE_NAME}
	COMMAND SHOULD EXECUTE SUCCESSFULLY
