#!/bin/bash 

excludedFile='.excludedFiles'

localSharedFolder=`python3 -c 'import jsonReader; reader = jsonReader.JSONReader(); print(reader.getLocalSharedFolder())'`
globalSharedFolder=`python3 -c 'import jsonReader; reader = jsonReader.JSONReader(); print(reader.getGlobalSharedFolder())'`

excludedFilesString=`python3 -c 'import jsonReader; reader = jsonReader.JSONReader(); print(reader.getExcludeFilesAsString())'`
excludedFilesArray=(`echo ${excludedFilesString}`);

: '

'
onFind() {
	venvPath=$1
	echo $venvPath
	source $venvPath/bin/activate
	pip freeze > $venvPath/../requirements.txt
	deactivate
}
export -f onFind

# Create excludedFilesfind . -type d -name "venv" -exec echo '{}' +

touch $excludedFile
echo $excludedFile > $excludedFile
for entry in "${excludedFilesArray[@]}"
do
   echo $entry >> $excludedFile
done

find $localSharedFolder -type d -name "venv" -exec bash -c 'onFind "$@"' bash '{}' \;

rsync -av --exclude-from $excludedFile $localSharedFolder'/' $globalSharedFolder --delete
