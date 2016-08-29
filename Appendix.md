All the PNG, PDF, and SVG files were used in a presentation I delivered about what you are about to do.

README.md : read it and follow the directions to run the experiment :)

TalkingPoints.md : Main points of my talk with all the important ideas

linkQuality.csv : a compact csv made by combining information so that each household number has one number
        associated to every link characteristic

newURS.csv : fixed Urban Rate Survey so it only includes rows with all necessary information, and converted to csv

fixedunitprofile.csv : fixed unit profile excel file to sort out bad rows, and put it into a csv

household.csv : combines linkQuality.csv and fixedunitprofile.csv by matching household ID

full.csv : the final csv. Added a price variable to household.csv by matching each of its households ISP, state,
        and speed with a similar household from newURS.csv, and using that similar household's price

In the src subdirectory:


makeHouseholdcsv.py, linkQuality.py, writeCompleteCsv.py, stateSpeedsAndBasicCleaning.py : to create all of the previously states csv files

speedgraphs.py : generated a frequency histogram graph of the average download and upload speeds of households in the Measuring Broadband America dataset

stateParticipants.py : Found number of participants in eery region and added the state and the number to a csv

priceForEachHouse.py : Looked for a price that most closely matched each house in household.csv . Then gave each house a price (then added to full.csv).

finalexperiment.py : Can take an input of a house ID, state, or price range, and returns a json file which can be usedin the ATC eperiment,
        and writes a file to miniexperiment.xml , which is used to generate a network on GENI. Also returns netem commands to use on GENI

