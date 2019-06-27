## HonoursListParser
A Python script for parsing the names of UK honours recipients.

The names of individuals in receipt of awards are all listed in a single column, which makes cross-referencing against existing databases tricky. The script aims to separate out the prefixes, first names, middle names, surnames and suffixes into the appropriate fields of a destination csv, for easy matching against, or inport into, existing database systems.

## Getting Started
UK honours lists are available from [gov.uk](https://www.gov.uk/search/all?parent=&keywords=honours+list&level_one_taxon=&manual=&public_timestamp%5Bfrom%5D=&public_timestamp%5Bto%5D=&order=relevance). 

## Running the script
1. Update the value of **source_file_full_path** to point to a csv file obtained from gov.uk containing a list of honours recipients.
2. Define the output file by updating the value of **output_file_full_pat**
3. Run the script

## Known Issues
The script is unlikely to be comprehensive in that it may not correctly identify all possible suffixes and prefixes, and therefore produce invalid data for some individuals, but it will be accurate for the vast number of honours recipients. Additionally, modifications to the values in the suffixes and prefixes lists should resolve any problem records.

## Authors
* **Grant Quick** - *Initial work* - [GrantQuick](https://github.com/GrantQuick)