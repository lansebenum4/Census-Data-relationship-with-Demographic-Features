# Census-Data-relationship-with-Demographic-Features
Purpose: The project uses public data from Statistics Canada and Elections Canada to look at how demographics and the economy relate to results in the 2015, 2019 and 2021 federal elections. It asks three questions:

Do provinces with older populations vote differently?
Does average hourly wage relate to voter turnout?
How evenly are seats split between men and women in each party?

How it runs: Each question has its own Python script, run from the command line. The scripts read CSV data files and check their inputs for errors.

age_grouping.py <year> <party> works out each province’s share of people aged 65 and older and pairs it with the party’s vote share. It saves a scatter plot with a line of best fit.
average_hourly_wage.py <province> prints a table of voter turnout next to average hourly wage for each election year.
question2.py <party> adds up the party’s male and female seats from 2021 and says which is higher.
