import sys
from argparse import ArgumentParser
from bader_ofer import get_votes_results
from elections_website import get_election_results_from_website
import plotly.graph_objects as go

VOTES_THRESHOLD_PERCENTAGE = 3.25

remainders_couples_2013 = frozenset(
    [
        frozenset(["מחל", "טב"]),
        frozenset(["שס", "ג"]),
        frozenset(["צפ", "מרץ"]),
        frozenset(["אמת", "פה"]),
        frozenset(["כן", "ץ"]),
        frozenset(["ו", "ד"]),
        frozenset(["זך", "צק"]),
    ]
)

remainders_couples_2015 = frozenset(
    [
        frozenset(["אמת", "מרץ"]),
        frozenset(["כ", "ל"]),
        frozenset(["מחל", "טב"]),
        frozenset(["שס", "ג"]),
    ]
)

remainders_couples_2019a = frozenset(
    [
        frozenset(["אמת", "מרצ"]),
        frozenset(["נ", "ל"]),
        frozenset(["ום", "דעם"]),
        frozenset(["מחל", "טב"]),
        frozenset(["שס", "ג"]),
        frozenset(["ףץ", "ףז"]),
    ]
)

remainders_couples_2019b = frozenset(
    [
        frozenset(["אמת", "מרצ"]),
        frozenset(["פה", "ל"]),
        frozenset(["מחל", "טב"]),
        frozenset(["שס", "ג"]),
        frozenset(["כ", "כף"]),
    ]
)

remainders_couples_2020 = frozenset(
    [
        frozenset(["אמת", "פה"]),
        frozenset(["מחל", "טב"]),
        frozenset(["שס", "ג"]),
    ]
)

def retrieve_elections_result(elections_website, remainders_couples, threshold_percent=VOTES_THRESHOLD_PERCENTAGE):
    votes = get_election_results_from_website(elections_website)
    if not votes:
        return {}
    return get_votes_results(votes, remainders_couples, threshold_percent)


def main():
    parser = ArgumentParser(description='Calculate elections results')
    parser.add_argument("elections_year", nargs=1)
    parser.add_argument("--city", type=int, default=0)
    args = parser.parse_args()
    elections_year = args.elections_year[0]
    city = args.city

    city_get_param = ""
    if (city != 0):
        city_get_param = f"cityresults?cityID={city}"
    
    if elections_year == "2013":
        results = retrieve_elections_result(f"https://www.votes-19.gov.il/{city_get_param}", remainders_couples_2013, threshold_percent=2)
    elif elections_year == "2015":
        results = retrieve_elections_result(f"https://votes20.gov.il/{city_get_param}", remainders_couples_2015)
    elif elections_year == "2019a":
        results = retrieve_elections_result(f"https://votes21.bechirot.gov.il/{city_get_param}", remainders_couples_2019a)
    elif elections_year == "2019b":
        results = retrieve_elections_result(f"https://votes22.bechirot.gov.il/{city_get_param}", remainders_couples_2019b)
    elif elections_year == "2020":
        results = retrieve_elections_result(f"https://votes23.bechirot.gov.il/{city_get_param}", remainders_couples_2020)
    else:
        print("Unknown elections")
        return

    results_parties = list(results.keys())
    results_seats = list(results.values())
    fig = go.Figure(data=[go.Bar(
        x=results_parties,
        y=results_seats,
        text=results_seats,
        textposition='auto',
        marker=go.bar.Marker(color=list(range(len(results_seats))), colorscale="Viridis")
        )])
    fig.update_layout(title=f"Election {elections_year}")
    fig.show()
    print(results)


if __name__ == "__main__":
    main()
