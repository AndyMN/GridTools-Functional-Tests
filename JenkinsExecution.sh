#!/bin/bash

CUTOFF_V1="2.16"

TESTS="./*Tests.robot"

OUTPUTS=""

for test in $TESTS; do
	name=$(basename $test .robot)
	if [[$test != "Srm*Tests.robot"]]
	then
		robot -o ${name}_output $test && OUTPUTS="$OUTPUTS ${name}_output.xml" || :
	else
		robot -o ${name}_outputSRMV2 --variable SRM_VERSION:2 $test && OUTPUTS="$OUTPUTS ${name}_outputSRMV2.xml" || :
		IsOlderThanCutoff=$(python IsdCacheVersionOlderThan.py $CUTOFF_V1)
		if [[$IsOlderThanCutOff == "true"]]
		then
			robot -o ${name}_outputSRMV1 --variable SRM_VERSION:1 $test && OUTPUTS="$OUTPUTS ${name}_outputSRMV1.xml" || :		
		fi
	fi
done

if [ "$OUTPUTS" != ""]; then
	rebot --output output_xml $OUTPUTS
else
	touch output.xml
fi

	
