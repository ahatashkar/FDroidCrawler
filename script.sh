#!/bin/bash
source venv/bin/activate
scrapy runspider fdroid.py -a url=$1 -o Projects/Output/info.json
unzip 'Projects/*' -d Projects/Unzip
python TestFinder.py > Projects/Output/result.csv
echo Done!
