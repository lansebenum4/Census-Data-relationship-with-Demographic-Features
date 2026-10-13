#!/usr/bin/env python3

'''
average_hourly_wage.py
  Author(s): Jamie Boseley (1368525), Mercy Awosoga (1392553), Zafina Ahmed (1300606), Similoluwa Lansebe (1371681)
  Earlier contributors(s): None. 

  Project:  Comparing Average Hourly Wage and Voter Turnout Project Script (Iteration 1)
  Date of Last Update: Mar 8, 2026.

  Functional Summary
      average_hourly_wage.py searches the voter turnout file for the voter turnout percentage across 2021, 2019 & 2015.
      It then opens each file for the average hourly wage across the years for the province and stores that data. The
      program then outputs a table showcasing the data side by side.

     Commandline Parameters: 1
        argv[1] = name of the province

     References
        Voter turnout file from https://open.canada.ca/data/en/dataset/065439a9-c194-4259-9c95-245a852be4a1
        Average hourly wage files from https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410044201
'''

import csv
import sys

def main(argv):
    # Check the amount of arguments presented.
    if len(argv) != 2:
        print("Usage: average_hourly_wage.py <province>")
        sys.exit(1)

    # Take province name from command line.
    province = argv[1]

    # To DO: Add error handling for the province name.

    # Initialize variables.
    voter_turnout = {
        2021: None,
        2019: None,
        2015: None
    }
    province_wages = {
        2021: None,
        2019: None,
        2015: None
    }
    years = [2015, 2019, 2021]

    # Open the voter data file.
    try:
        voter_turnout_fh = open("data/voter_turnout_2021_2019_2015.csv", "r", encoding = "utf-8-sig")
    except IOError as err:
        # TO DO: Add error handling message.
        sys.exit(1)

    # Create a csv reader for the voter turnout file.
    voter_turnout_reader = csv.reader(voter_turnout_fh)
    
    # Increment through each row in the csv.
    for row_data_fields_vote in voter_turnout_reader:
        # Searches for the row belonging to the province parameter.
        if row_data_fields_vote[0] == province:
            # Store the voter turnout percent for the province for 2021, 2019, 2015.
            # TO DO: Add error handling for float conversion.
            voter_turnout[2021] = float(row_data_fields_vote[9])
            voter_turnout[2019] = float(row_data_fields_vote[10])
            voter_turnout[2015] = float(row_data_fields_vote[11])
    
    # Close the voter turnout file.
    voter_turnout_fh.close()

    # TO DO: Add all provinces.
    if province.lower() == "newfoundland and labrador":
        province = "newfoundland"
    if province.lower() == "ontario":
        province = "ontario"

    # Open file for each year for the province.
    for year in years:
        filename = f"data/wages/{province}_wages_{year}.csv"
        try:
            province_wages_fh = open(filename, "r", encoding = "utf-8-sig")
        except IOError as err:
            # TO DO: Add error handling message.
            sys.exit(1)

        
        # Create a csv reader for the wages file.
        province_wages_reader = csv.reader(province_wages_fh)
        
        # Increment through each row in the csv.
        for row_data_fields_wage in province_wages_reader:
            if row_data_fields_wage[0] == "Average offered hourly wage":
                # Take the average wage for each quarter of the year.
                # TO DO: Add error handling for float conversion.
                q1 = float(row_data_fields_wage[2])
                q2 = float(row_data_fields_wage[3])
                q3 = float(row_data_fields_wage[4])
                q4 = float(row_data_fields_wage[5])
                province_wages[year] = (q1 + q2 + q3 + q4) / 4
        # Close each file.
        province_wages_fh.close()

    # After all data is collected. Output results.
    # TO DO: Implement output as a graph.
    print("Year | Voter Turnout (%) | Avg Hourly Wage ($)")
    print("-----------------------------------------------")
    for year in years:
        print(f"{year} | {voter_turnout[year]:.2f} | {province_wages[year]:.2f}")

if __name__ == "__main__":
    main(sys.argv)
        




    
    



    