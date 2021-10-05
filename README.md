# adicht-analysis
Scripts used for the analysis of .adicht files.

## reader.py
This python script extracts peak_tension, time_to_peak_tension, and time_to_half_response from a folder of raw adicht files, where each new trace is a new record ID.
This script requires the adinstruments SDK driver available here: https://github.com/JimHokanson/adinstruments_sdk_python. Windows only.

**Usage:**
 - Store your adicht files in a subdirectory e.g. "./myfiles"
 - Run the command `py reader.py -i "./myfiles" -o "results.csv"`

For the assignment I just used the commands
`py reader.py -i "./drugs" -o "drug_results.csv"`
`py reader.py -i "./calcium" -o "calcium_results.csv"`

## analysis.Rmd
R markdown file containing statistical analysis of the data.
