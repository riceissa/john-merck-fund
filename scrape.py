#!/usr/bin/env python3

import requests
import sys
import csv
from bs4 import BeautifulSoup

import pdb

def main():
    fieldnames = ["date", "donee", "donee_url", "description", "program_area", "focus", "amount"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()

    url_pattern = "https://www.jmfund.org/program-grants/?fwp_paged={}"

    # sys.argv[1] should be the last page (inclusive), e.g. if it says "Page
    # 447 of 447" then it should be "447".
    for i in range(1, int(sys.argv[1]) + 1):
        url = url_pattern.format(i)
        print("Downloading " + url, file=sys.stderr)
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 '
                                              '(X11; Linux x86_64) AppleWebKit/537.36 '
                                              '(KHTML, like Gecko) '
                                              'Chrome/63.0.3239.132 Safari/537.36'})
        soup = BeautifulSoup(response.content, "lxml")
        table = soup.find("table")
        # The [1:] skips the header row
        for row in table.find_all("tr")[1:]:
            cells = row.find_all("td")

            lst = cells[1].find_all("p")
            # Our life is much easier if we don't have to deal with
            # multiple-paragraph descriptions; it looks like none of the
            # descriptions have multiple paragraphs, but make this assertion to
            # be sure
            assert len(lst) == 0 or len(lst) == 1 or (len(lst) == 2 and lst[1].text.strip() == "")
            if len(lst) == 0:
                description = ""
            else:
                description = lst[0].text

            try:
                donee_url = cells[1].h3.a.get("href")
            except AttributeError:
                donee_url = ""

            writer.writerow({
                "date": cells[0].text,
                "donee": cells[1].h3.text,
                "donee_url": donee_url,
                "description": description,
                "program_area": cells[2].text.strip(),
                "focus": cells[3].text.strip(),
                "amount": cells[4].text,
            })


if __name__ == "__main__":
    main()
