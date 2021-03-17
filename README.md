# Form4_Scraper

This code scrapes through SEC's EDGAR for Form4 (Insider Trade) data. Then automatically saves that information to a SQL database and continues to process each individual company's employees trades. 

This also calculates the amount of shares they've exchanged as well as the percent difference.

Once done, a report is made to save to the Desktop.


INSTRUCTIONS:
Run the '.sql' command to initialize the database correctly. 

A sample '.env' file looks as follows:
DB_USER="USERNAME"
DB_PASSWORD="PASSWORD"
DB_HOST="HOSTNAME"
DB_PORT="PORT (Usually 3306)"
DB_DB=form4db
