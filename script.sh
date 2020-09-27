#!/bin/bash
source venv/bin/activate
#scrapy runspider fdroid.py -o test.json
#unzip 'Projects/*' -d Projects/Unzip
python TestFinder.py > result.csv
echo Done!
