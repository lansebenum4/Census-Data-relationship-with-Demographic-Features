#!/usr/bin/env python3

#
# age_grouping.py
#  Author(s): Simi Lansebe (1371681), Zafina Ahmed (1300606),
#             Mercy Awosoga (1392553), Jamie Boseley (1368525)
#
#  Project: MILESTONE II
#  Date of Last Update: March 20th 2026
#
#  Functional Summary
#      age_grouping.py reads the preprocessed CSV file produced by
#      older_pop_party_preprocess_script.py for a given year and party,
#      then generates a scatter plot of:
#          X-axis : percentage of the province population aged 65+
#                   tick intervals of 10
#          Y-axis : party's provincial vote share (%)
#                   tick intervals of 10
#          Dots   : one dot per province
#          Trend  : line of best fit (OLS)
#
#      If the preprocessed CSV is missing, this script automatically
#      runs older_pop_party_preprocess_script.py to generate it.
#      Both scripts must be in the same directory as the data/ folder.
#
#  Commandline Parameters: 2
#      argv[1] = year   (int:    2015, 2019, or 2021)
#      argv[2] = party  (string: liberal, conservative,
#                                "new democratic party", green, or bloc)
#
#  Usage
#      python3 age_grouping.py 2021 liberal
#      python3 age_grouping.py 2019 conservative
#      python3 age_grouping.py 2021 "new democratic party"
#
#  References
#      Population estimates from
#        https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000501
#      Percentage of valid votes by political affiliation from
#        https://open.canada.ca/data/en/dataset/065439a9-c194-4259-9c95-245a852be4a1
#

import csv
import sys
import os
import subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')           
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Validate command-line arguments
# ------------------------------------------------------------------
if len(sys.argv) != 3:
    print("Usage: python3 age_grouping.py <year> <party>")
    print("       year  : 2015, 2019, or 2021")
    print("       party : liberal | conservative | \"new democratic party\" | green | bloc")
    sys.exit(1)

try:
    year = int(sys.argv[1])
except ValueError:
    print(f"Error: '{sys.argv[1]}' is not a valid integer year.")
    sys.exit(1)

valid_years = {2015, 2019, 2021}
if year not in valid_years:
    print(f"Error: year must be one of {sorted(valid_years)}, got {year}.")
    sys.exit(1)

party_input = sys.argv[2].lower().strip()

# Maps user-entered party name -> (display label, file prefix, colour)
PARTY_CONFIG = {
    "liberal":              ("Liberal",              "liberal",      "#CC0000"),
    "conservative":         ("Conservative",         "conservative", "#1F4E87"),
    "new democratic party": ("NDP",                  "ndp",          "#F07B20"),
    "ndp":                  ("NDP",                  "ndp",          "#F07B20"),
    "green":                ("Green",                "green",        "#2CA02C"),
    "bloc":                 ("Bloc Quebecois",        "bloc",         "#33B2CC"),
}

if party_input not in PARTY_CONFIG:
    print(f"Error: '{party_input}' is not a recognised party.")
    print("       Choose from: liberal, conservative, \"new democratic party\", green, bloc")
    sys.exit(1)

party_label, file_prefix, colour = PARTY_CONFIG[party_input]

# The preprocess script always expects the full name for NDP
PREPROCESS_ARG = {
    "liberal":      "liberal",
    "conservative": "conservative",
    "ndp":          "new democratic party",
    "green":        "green",
    "bloc":         "bloc",
}

PREPROCESS_SCRIPT = "older_pop_party_preprocess_script.py"

# ------------------------------------------------------------------
# Auto-run preprocess script if the CSV is missing
# ------------------------------------------------------------------
filename = f"{file_prefix}_vote_age_distribution_{year}.csv"

if not os.path.isfile(filename):
    print(f"'{filename}' not found — generating it now...")

    if not os.path.isfile(PREPROCESS_SCRIPT):
        print(f"Error: Cannot find '{PREPROCESS_SCRIPT}' in the current directory.")
        print("       Make sure both scripts are in the same folder as data/")
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, PREPROCESS_SCRIPT, str(year), PREPROCESS_ARG[file_prefix]],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error: Preprocess script failed:\n{result.stderr.strip()}")
        sys.exit(1)
    print(result.stdout.strip())

# ------------------------------------------------------------------
# Load preprocessed data
# ------------------------------------------------------------------
xs, ys, provinces = [], [], []

try:
    with open(filename, "r", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            try:
                xs.append(float(row["Percentage 65+"]))
                ys.append(float(row["Party Vote Share"]))
                provinces.append(row["Province"])
            except ValueError as err:
                print(f"Error reading {filename}: {err}")
                sys.exit(1)
except IOError as err:
    print(f"Error: Unable to open {filename}: {err}")
    sys.exit(1)

# ------------------------------------------------------------------
# Build scatter plot
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 7))

# One dot per province
ax.scatter(xs, ys, color=colour, s=120, zorder=5, label=party_label)

# Province name labels above each dot
for x_val, y_val, prov in zip(xs, ys, provinces):
    ax.annotate(
        prov,
        xy=(x_val, y_val),
        xytext=(0, 9),
        textcoords="offset points",
        fontsize=8,
        ha="center",
        color="dimgray",
    )

# Line of best fit (OLS)
coeffs = np.polyfit(xs, ys, 1)
poly   = np.poly1d(coeffs)
x_fit  = np.linspace(0, max(xs) + 2, 300)
ax.plot(
    x_fit, poly(x_fit),
    color="black", linewidth=1.8, linestyle="--", zorder=4,
    label=f"Line of Best Fit  (slope = {coeffs[0]:.2f})",
)

# ------------------------------------------------------------------
# Axis formatting — intervals of 10 on both axes
# ------------------------------------------------------------------
ax.set_xlim(0, 30)
ax.set_ylim(0, 70)
ax.set_xticks(range(0, 31, 10))
ax.set_yticks(range(0, 71, 10))

ax.set_xlabel("Population Aged 65+ per Province (%)", fontsize=12)
ax.set_ylabel(f"{party_label} Vote Share per Province (%)", fontsize=12)
ax.set_title(
    f"{party_label} Vote Share vs. Population Aged 65+ by Province\n"
    f"{year} Canadian Federal Election",
    fontsize=13, fontweight="bold",
)
ax.legend(loc="upper right", fontsize=10)
ax.grid(True, linestyle=":", alpha=0.5)

plt.tight_layout()

# ------------------------------------------------------------------
# Save plot to file
# ------------------------------------------------------------------
output_file = f"{file_prefix}_voting_analysis_{year}.png"
plt.savefig(output_file, dpi=150)
plt.close()
print(f"Success: Plot saved to {output_file}")