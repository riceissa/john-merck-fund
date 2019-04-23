# John Merck Fund

This repo is for Vipul Naik's Donations List Website: https://github.com/vipulnaik/donations

Relevant issue: https://github.com/vipulnaik/donations/issues/96

## Instructions for running the scripts

Download the data into CSV:

```bash
# The argument given is the final page number. To get this number,
# to go https://www.jmfund.org/program-grants/ and click on the ">>"
# in the pagination menu. The bottom of the page should now say
# something like "Page 447 of 447".
./scrape.py 447 > data.csv
```

Use the CSV to generate the SQL file:

```bash
./proc.py data.csv > out.sql
```

## License

CC0 for scripts and readme.
