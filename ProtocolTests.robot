*** Settings ***
Library  ProtocolTesterLib.py




*** Variables ***
${PROTOCOL}     srm
${HOST}         prometheus.desy.de

${LOCAL_FILE}   /scratch/jenkins/jenkins/workspace/robot-g2-tests/testfile777
${REMOTE_FILE}  /Users/kermit/testo
${REMOTE_DIRECTORY}  /Users/kermit/test_directory/


*** Test Cases ***
COPY FILE
    SET CLIENT          srmcp
    SET PROTOCOL        ${PROTOCOL}
    SET HOST            ${HOST}
    COPY LOCAL FILE     ${LOCAL_FILE}   ${REMOTE_FILE}      add_timestamp=${TRUE}
    ERROR SHOULD BE     ${EMPTY}

REMOVE FILE
    SET CLIENT          srmrm
    SET PROTOCOL        ${PROTOCOL}
    SET HOST            ${HOST}
    REMOVE REMOTE FILE  ${REMOTE_FILE}
    ERROR SHOULD BE     ${EMPTY}


CREATE DIR
    SET CLIENT          srmmkdir
    SET PROTOCOL        ${PROTOCOL}
    SET HOST            ${HOST}
    CREATE REMOTE DIRECTORY  ${REMOTE_DIRECTORY}
    ERROR SHOULD BE     ${EMPTY}


REMOVE DIR
    SET CLIENT          srmrmdir
    SET PROTOCOL        ${PROTOCOL}
    SET HOST            ${HOST}
    REMOVE REMOTE DIRECTORY  ${REMOTE_DIRECTORY}
    ERROR SHOULD BE  ${EMPTY}