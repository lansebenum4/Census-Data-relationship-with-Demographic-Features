#!/usr/bin/env python3

'''
average_hourly_wage.py
  Author(s): Jamie Boseley (1368525), Mercy Awosoga (1392553), Zafina Ahmed (1300606), Similoluwa Lansebe (1371681)
  Earlier contributors(s): None. 

  Project: Looking at a political party's male and female seat count Project Script (Iteration 1)
  Date of Last Update: Mar 9, 2026.

  Functional Summary
    Question2.py searches the 44th general election gender seats file for the number of male and female seats in each political party. 
    The program prints the total number of males and femals per party and shows which count is higher. 
    
    Commandline Parameters: 1
        argv[1] = name of the political party

     References
        44th General Election gender seats file from https://open.canada.ca/data/en/dataset/065439a9-c194-4259-9c95-245a852be4a1/resource/ee21862c-e718-43d2-bb0c-357b58aafed0 
        
'''

import sys
import csv

def main(argv):
    
    #Check the amount of arguments presented.
    if len(argv) != 2:
        print("Usage: question2.py <party_name>")
        sys.exit(1)
        
    # Take party name from command line.
    party_name = argv[1]
    
    # Initialize Valiables
    male_count = 0
    female_count = 0
    
    # Open seats.csv
    try:
        seats_fh = open("seats.csv", "r", encoding = "utf-8-sig")
    except IOError as err:
        print(f"Error opening seats.csv: {err}")
        sys.exit(1)
        
    # CSV reader for file
    seats_reader = csv.reader(seats_fh)
    
    # Loop through the first row to find header columns
    
    for row_data_fields in seats_reader:
        # This is the header row
        header = row_data_fields  
        # Find Male and Female colums using header
        male_index = None
        female_index = None
        
        column_index = 0
        
        for column_name in header:
            if party_name in column_name and "_Male" in column_name:
                male_index = column_index
            if party_name in column_name and "_Female" in column_name:
                female_index = column_index
            column_index += 1
            
        # Only for the header row   
        break
    
    # Error check if column is empty
    if male_index is None or female_index is None:
        print(f"Party '{party_name}' not found.")
        seats_fh.close()
        sys.exit(1)
        
    # Reopen seats.csv to loop through data rows
    seats_fh.close()
    try:
        seats_fh = open("seats.csv", "r", encoding = "utf-8-sig")
        
        # Skip the header row
        seats_reader = csv.reader(seats_fh)
        next(seats_reader)
    except IOError as err:
        print(f"Error re-opening seats.csv: {err}")
        sys.exit(1)
        
    # Increment through each row in the CSV.
    for row_data_fields_seats in seats_reader:
        
        # Find the sum of male and female seats for a specific province. Convert from string to integer.
        male_count += int(row_data_fields_seats[male_index])
        female_count += int(row_data_fields_seats[female_index])
        
    # Close the seats file.
    seats_fh.close()
    
    # Printed Output (Note: Figure out graphing later)
    print(f"{party_name}")
    print(f"Number of Male seats:   {male_count}")
    print(f"Number of Female seats: {female_count}")
    
    if male_count > female_count:
        print("Results: More male seats overal.")
    elif female_count > male_count:
        print("Results: More female seats overal.")
    else:
        print("Results: Equal Male and Female seats.")
        
if __name__ == "__main__":
    main(sys.argv)
        