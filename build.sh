#!/bin/bash
declare -a folders=("csharp" "java" "python" "golang" "nodejs")

for i in `seq 1 10`;
do
  for folder in "${folders[@]}"
  do
    cd $folder
    pwd
    
    serverless deploy -v

    cd ..
  done

  node invoke-functions.js
done
