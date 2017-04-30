import os
import sys
import random
import json
import csv
import pandas as pd
import numpy as np


# Import local libraries
import digitaldivide

# Setting command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--output-dir", help="Specify a directory in which to put output files.")
parser.add_argument("--state", help="Specify a state from which to draw a sample household. (two letter state code)")
parser.add_argument("--houseid", help="Specify a household ID from the Measuring Broadband America data set.")
parser.add_argument("--price-range", help="A number, followed by a '-', followed by a number greater than the first (number is amount in dollars). Only integer values, please.")
parser.add_argument("--technology", help="CABLE, FIBER, SATELLITE, or DSL.")
parser.add_argument("--users", help="(Integer) number of end users to represent (default: 1)")
parser.add_argument('--weights', help="Use weighted sample of households.", dest='useweights', action='store_true')
parser.add_argument('--no-weights', help="Don't use weighted sample of households.", dest='useweights', action='store_false')
parser.set_defaults(useweights=True)
parser.add_argument('--info', help="Print household information.", dest='info', action='store_true')
parser.add_argument('--no-info', help="Don't print household information.", dest='info', action='store_false')
parser.set_defaults(info=True)
parser.add_argument('--rspec', help="Create an Rspec to use with GENI.", dest='rspec', action='store_true')
parser.add_argument('--no-rspec', help="Don't create an Rspec.", dest='rspec', action='store_false')
parser.set_defaults(rspec=False)
parser.add_argument('--json', help="Create a JSON file to use with Augmented Traffic Control.", dest='json', action='store_true')
parser.add_argument('--no-json', help="Don't create a JSON file for Augmented Traffic Control.", dest='json', action='store_false')
parser.set_defaults(json=False)
parser.add_argument('--netem-up', help="Print netem commands to use for uplink (on client).", dest='netemup', action='store_true')
parser.set_defaults(netemup=False)
parser.add_argument('--netem-down', help="Print netem commands to use for downlink (on server/router).", dest='netemdown', action='store_true')
parser.set_defaults(netemdown=False)
parser.add_argument('--validate', help="Prepare to validate link settings.", dest='validate', action='store_true')
parser.add_argument('--no-validate', help="Don't prepare to validate link settings.", dest='validate', action='store_false')
parser.set_defaults(validate=False)


args = parser.parse_args()


# Sample household(s)
allcsv = pd.read_csv('dat/household-internet-data.csv')

if args.output_dir:
    output_dir = args.output_dir
else:
    output_dir = os.getcwd()

if not args.houseid:
    if args.state:
        allcsv = allcsv[allcsv.state == args.state.upper()]
    if args.price_range:
        allcsv = allcsv[allcsv.monthly.charge >= int(args.price_range.split("-")[0])]
        allcsv = allcsv[allcsv.monthly.charge <= int(args.price_range.split("-")[1])]
    if args.technology:
        allcsv = allcsv[allcsv.technology == args.technology.upper()]

    nusers = int(args.users) if args.users else 1

    if not args.useweights:
        housearray = allcsv.sample(n=nusers)
    else:
        housearray = allcsv.sample(n=nusers, weights=allcsv.weight)

if args.houseid:
    house = int(args.houseid)
    housearray = allcsv[allcsv.unit_id == house]
    nusers = 1

if housearray.empty:
    # Get a random sample to suggest house id's to try
    sample_ids = allcsv.sample(n=5)['unit_id'].tolist()
    print "\nThere is no unit with that ID in the data set."
    print "Here are some valid IDs you can try: %s\n" % ", ".join(map(str, sample_ids))
    sys.exit()

if args.rspec:
    star = digitaldivide.Star()
for rowindex, house in housearray.iterrows():

    h = digitaldivide.Household(house)

    if args.info:
        h.print_house_info()

    if args.rspec:
        star.add_household(h)

    if args.netemup:
        print h.netem_template_up("10.0.%d.0" % star.house_count)
    if args.netemdown:
        print h.netem_template_down("10.0.%d.0" % star.house_count)

    if args.json:
        jfile = os.path.join(output_dir, "house-%d.json" % h.unit_id)
        with open(jfile, 'w') as f:
            json.dump(h.json_template(), f)
            print "JSON for Augmented Traffic Control written to %s" % jfile

    if args.validate:
        tfile = os.path.join(output_dir, "truth-%d.csv" % h.unit_id)
        a = h.truth_template()
        with open(tfile, "w") as f:
            writer = csv.writer(f)
            writer.writerows(a)
            print "CSV of household link stats written to %s" % tfile

        star.add_validate_services()

if args.rspec:
    rspec = os.path.join(output_dir, "houses.xml")
    star.rspec_write(rspec)
    print "Rspec written to %s\n" % rspec

