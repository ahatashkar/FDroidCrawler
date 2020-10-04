#!/bin/bash
source venv/bin/activate
#scrapy runspider fdroid.py -o test.json
#unzip 'Projects/*' -d Projects/Unzip
echo Analysing starts at `date +%T`
python TestFinder.py > Projects/result.csv
mv test.json Projects/
echo Done at `date +%T`
