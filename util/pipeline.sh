
# Requirements
# sudo apt-get install gnumeric 


cd dat

# Get Urban Rate Survey for 2015
wget https://apps.fcc.gov/edocs_public/attachmatch/DOC-333059A1.xlsx
ssconvert -S DOC-333059A1.xlsx DOC-333059A1.csv
rm DOC-333059A1.csv.0
mv DOC-333059A1.csv.1 DOC-333059A1.csv

# Keep only large ISPs, and normalize names
cat "DOC-333059A1.csv" | \
    grep "Provider\|DSL\|Cable\|FTTH" | \
    grep "Provider\|CenturyLink, Inc.\|AT\&T Services, Inc.\|Charter Communications, Inc.\|Charter Communications\|COMCAST CABLE COMMUNICATIONS, INC.\|Cox Communications, Inc\|Frontier Communications\|Frontier Communications Corporation\|Mediacom Illinois LLC\|Mediacom Iowa LLC\|Mediacom Minnesota LLC\|Time Warner Cable Enterprises LLC\|Time Warner Cable Inc.\|Verizon California Inc.\|Verizon Florida LLC\|Verizon New England Inc.\|Verizon New Jersey Inc.\|Verizon New York Inc.\|Verizon Pennsylvania Inc.\|Verizon Virginia Inc.\|Windstream Corporation" | \
    sed -e 's/Provider/isp/g' -e 's/CABLE/CABLE/g' -e 's/FTTH/FIBER/g' -e 's/CenturyLink, Inc./CenturyLink/g' -e 's/AT\&T Services, Inc./AT\&T/g' -e 's/BENTON CABLEVISION, INC./Cablevision/g' -e 's/Charter Communications, Inc./Charter/g' -e 's/Charter Communications/Charter/g' -e 's/COMCAST CABLE COMMUNICATIONS, INC./Comcast/g' -e 's/Cox Communications, Inc/Cox/g' -e 's/Frontier Communications Corporation/Frontier/g' -e 's/Frontier Communications/Frontier/g'  -e 's/Mediacom Illinois LLC/Mediacom/g' -e 's/Mediacom Iowa LLC/Mediacom/g' -e 's/Mediacom Minnesota LLC/Mediacom/g' -e 's/Time Warner Cable Enterprises LLC/Time Warner Cable/g' -e 's/Time Warner Cable Inc./Time Warner Cable/g' -e 's/Verizon California Inc./Verizon/g' -e 's/Verizon Florida LLC/Verizon/g' -e 's/Verizon New England Inc./Verizon/g' -e 's/Verizon New Jersey Inc./Verizon/g' -e 's/Verizon New York Inc./Verizon/g' -e 's/Verizon Pennsylvania Inc./Verizon/g' -e 's/Verizon Virginia Inc./Verizon/g' -e 's/Windstream Corporation/Windstream/g'  > urs.csv

# Remove files that are no longer needed
rm DOC-333059A1.xlsx DOC-333059A1.csv

# Download validated data
if [ ! -f "data-validated-2014-sept.tar.gz" ]
then
	wget http://data.fcc.gov/download/measuring-broadband-america/bytes_sec2015/data-validated-2014-sept.tar.gz
    tar -xzvf data-validated-2014-sept.tar.gz
fi

# Download profile info, which includes advertised rates
wget http://data.fcc.gov/download/measuring-broadband-america/2015/FCC_UnitProfile_Sept14.xls
ssconvert FCC_UnitProfile_Sept14.xls FCC_UnitProfile_Sept14.csv
rm FCC_UnitProfile_Sept14.xls

# Remove the lines where "Technology" is "REMOVE"
# Remove the lines where "State" is "UNKNOWN"
# Remove the lines where "SK UP" is not numeric
# Rename some ISPs to their parent companies
head --lines=1 FCC_UnitProfile_Sept14.csv > fixedunitprofile.csv
cat FCC_UnitProfile_Sept14.csv | \
	awk -F  "," '{ if ( $3 != "REMOVE" ) { print $0; } }'  | \
	awk -F  "," '{ if ( $8 != "UNKNOWN" ) { print $0; } }'  | \
	awk -F ',' '$5~/^[0-9.]+$/ { print $0; }'  | \
    sed -e 's/Verizon DSL/Verizon/g' -e 's/Insight/Time Warner Cable/g' -e 's/Qwest/CenturyLink/g'  >> fixedunitprofile.csv

# Note: we don't have satellite rates

