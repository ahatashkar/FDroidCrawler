#!/bin/bash
source venv/bin/activate
if [ -z "$1" ]
  then
    echo "Please enter F-Droid category link"
    exit 1
fi
scrapy runspider fdroid.py -a url=$1 -o Projects/Output/info.json
unzip 'Projects/*' -d Projects/Unzip
python TestFinder.py $1 > Projects/Output/result.csv
echo Done!
