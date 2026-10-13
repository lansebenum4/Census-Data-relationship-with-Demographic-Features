#!/usr/bin/env python3

'''
older_pop_party_preprocess_script.py
  Author(s): Jamie Boseley (1368525), Mercy Awosoga (1392553), Zafina Ahmed (1300606), Similoluwa Lansebe (1371681)
  Earlier contributors(s): None. 

  Project:  Comparing Older Populations & Vote Share Preprocessing Data Script (Iteration 1)
  Date of Last Update: Mar 15, 2026.

  Functional Summary
      older_pop_party_preprocess_script.py computes the percentage aged 65+ for each province in a given year and
      gathers the corresponding vote share for a given party and outputs this data to an organized CSV file.

     Commandline Parameters: 1
        argv[1] = year (int)
        argv[2] = party (string)

     References
        Population estimates from https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000501
        Percentage of valid votes by politcal affiliation from https://open.canada.ca/data/en/dataset/065439a9-c194-4259-9c95-245a852be4a1/resource/1dbb335b-8e54-44fa-bf41-493d65125edd
'''

import csv
import sys

def main(argv):

    # Check the program has the correct number of parameters to function.
    if len(argv) != 3:
        print("Usage: older_pop_party_preprocess_script.py <year> <party>")
        sys.exit(1)

    # Take year and party from command line.
    try:
        year = int(argv[1])
    except ValueError as err:
        print(f"Error: <year> is not a valid integer: {err}")
        sys.exit(1)
    
    party = argv[2].lower()

    # Check party parameter is allowed.
    if party != "liberal" and party != "conservative" and party != "new democratic party" and party != "green" and party != "people" and party != "bloc":
        print(f"Error: {party} is invalid. Expected one of: Liberal, Conservative, New Democratic Party, Green, People, or Bloc.")
        sys.exit(1)

    # Initialize variables.
    provinces_list = {
        "ontario": "Ontario",
        "alberta": "Alberta",
        "british_columbia": "British Columbia",
        "manitoba": "Manitoba",
        "saskatchewan": "Saskatchewan",
        "quebec": "Quebec",
        "new_brunswick": "New Brunswick",
        "nova_scotia": "Nova Scotia",
        "pei": "Prince Edward Island",
        "newfoundland": "Newfoundland and Labrador",
        "nunavut" : "Nunavut",
        "yukon" : "Yukon",
        "northwest_territories" : "Northwest Territories"
    }
    province_elder_pop = {}
    province_party_vote = {}
    ages_65_plus = {
        "65 to 69 years",
        "70 to 74 years",
        "75 to 79 years",
        "80 to 84 years",
        "85 to 89 years",
        "90 to 94 years",
        "95 to 99 years",
        "100 years and older"
    }
    province_vote_map = {
        "Ont.": "Ontario",
        "Alta.": "Alberta",
        "B.C.": "British Columbia",
        "Man.": "Manitoba",
        "Sask.": "Saskatchewan",
        "Que.": "Quebec",
        "N.B.": "New Brunswick",
        "N.S.": "Nova Scotia",
        "P.E.I.": "Prince Edward Island",
        "N.L.": "Newfoundland and Labrador",
        "Y.T." : "Yukon",
        "N.W.T." : "Northwest Territories",
        "Nun." : "Nunavut"
    }
    vote_columns = {}

    # Open population age data for each province.
    for province in provinces_list:

        elder_total = 0
        total_age = 0
        year_column_index = -1

        # Attempt to open file.
        try:
            province_ages_fh = open(f"data/{province}_ages.csv", "r", encoding = "utf-8-sig")
        except IOError as err:
            print(f"Error: Unable to open data/{province}_ages.csv: {err}.")
            sys.exit(1)
        
        # Create CSV reader.
        province_ages_reader = csv.reader(province_ages_fh)

        # Find the header row.
        for row in province_ages_reader:
            if row and "Age group" in row[0]:
                # Set header row.
                header_province_ages = row
                break

        # Find the column index in the file for the corresponding year.
        for i, column_data_fields_age in enumerate(header_province_ages):
            if str(year) in column_data_fields_age:
                year_column_index = i
        
        # Check to see if the year was found in the file.
        if year_column_index == -1:
            print(f"Error: {year} was not found in the file data/{province}_ages.csv.")
            province_ages_fh.close()
            sys.exit(1)

        # Increment through the rows of the CSV file.
        for row_data_fields_age in province_ages_reader:

            if not row_data_fields_age:
                continue

            # Get the total count of each province to calculate percentages.
            if "All ages" in row_data_fields_age[0]:
                try:
                    total_age = int(row_data_fields_age[year_column_index].replace(",", "")) # TO DO: Add error handling.
                except ValueError as err:
                    print(f"Error: Could not convert {row_data_fields_age[year_column_index]} to an integer: {err}.")
                    province_ages_fh.close()
                    sys.exit(1)
            
            # Get the population for each age range.
            if row_data_fields_age[0] in ages_65_plus:
                try:
                    elder_total += int(row_data_fields_age[year_column_index].replace(",", "")) # TO DO: Add error handling.
                except ValueError as err:
                    print(f"Error: Could not convert {row_data_fields_age[year_column_index]} to an integer: {err}.")
                    province_ages_fh.close()
                    sys.exit(1)
        
        # Calculate percentages.
        province_elder_pop[provinces_list[province]] = elder_total / total_age * 100

        # Close file.
        province_ages_fh.close()
    
    # Open valid vote data.
    try:
        valid_vote_fh = open(f"data/valid_votes_political_affiliation_{year}.csv", "r", encoding = "utf-8-sig")
    except IOError as err:
        print(f"Error: Unable to open data/valid_votes_political_affiliation_{year}.csv: {err}.")
        sys.exit(1)
    
    # Create CSV reader.
    valid_vote_reader = csv.reader(valid_vote_fh)

    # Set the header row.
    header_votes = next(valid_vote_reader)

    # Find the provinces indexes.
    for i, column_data_fields_votes in enumerate(header_votes):
        for province_short_form in province_vote_map:
            if province_short_form in column_data_fields_votes:
                vote_columns[province_vote_map[province_short_form]] = i

    # Increment through the rows of the vote distribution file.
    for row_data_fields_votes in valid_vote_reader:
        if party in row_data_fields_votes[0].lower():
               for province in vote_columns:
                    try:
                        province_party_vote[province] = float(row_data_fields_votes[vote_columns[province]])
                    except ValueError as err:
                        print(f"Error: Could not convert to a float: {err}.")
                        valid_vote_fh.close()
                        sys.exit(1)

    
    # Close file.
    valid_vote_fh.close()
    
    if party == "new democratic party":
        party = "ndp"

    # Print to output CSV file.
    # Try to open a CSV to output data to.
    try:
        data_output_fh = open(f"{party}_vote_age_distribution_{year}.csv", "w", encoding = "utf-8-sig")
    except IOError as err:
        print(f"Error: Unable to open {party}_vote_age_distribution_{year}.csv: {err}.")
        sys.exit(1)
    
    # Print header.
    data_output_fh.write("Province,Percentage 65+,Party Vote Share\n")

    # Print the data for each row.
    for province in provinces_list:
        data_output_fh.write(f"{provinces_list[province]},{province_elder_pop[provinces_list[province]]:.2f},{province_party_vote[provinces_list[province]]:.2f}\n")

    # Close the output file.
    data_output_fh.close()

    print(f"Success: The preprocessed data for the percentage of populations aged 65+ and the party vote share for {party} in {year} have been outputted.")
            
        
main(sys.argv)
            

        
        
