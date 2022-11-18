import requests
from bs4 import BeautifulSoup

def get_election_results_from_website(website_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }
    req = requests.get(website_url, headers=headers)
    if (req.status_code != 200):
        raise ValueError("Could not fetch website")
    website_content = req.text

    website_parser = BeautifulSoup(website_content, "html.parser")
    results_tables = website_parser.find_all(True, {"class": "TableData"})
    if (len(results_tables) != 1):
        raise ValueError("Too many 'TableData' tables")
    results_table = results_tables[0]
    results_table_rows = results_table.find_all("tr")
    
    results = {}
    for row in results_table_rows:
        cells = row.find_all("td")
        if not cells:
            continue
        party_code = str(cells[0].contents[0]).strip()
        party_votes = int(cells[-1].find("div", {"class": "FloatDir"}).contents[0].strip().replace(",", ""))
        if party_code:
            results[party_code] = party_votes
    return results
