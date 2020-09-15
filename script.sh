#!/bin/bash
source venv/bin/activate
scrapy runspider fdroid.py -o test.json
cd Project
unzip '*' -d Unzip
