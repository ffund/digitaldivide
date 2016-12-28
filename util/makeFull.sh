wget  -O /dat/ "http://data.fcc.gov/download/measuring-broadband-america/2015/data-validated-2014-sept.tar.gz"
# must unpack?!
wget -O /dat/unitprofile.xls "http://data.fcc.gov/download/measuring-broadband-america/2015/FCC_UnitProfile_Sept14.xls"
wget -O /dat/newURS.csv "https://apps.fcc.gov/edocs_public/attachmatch/DOC-333059A1.xlsx"
# convert to csv first for unit profile and URS

#some cleaning is in BasicCleaning.py
python src/stateSpeedsAndBasicCleaning.py
python src/makeFull.csv
