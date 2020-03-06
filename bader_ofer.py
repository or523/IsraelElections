from collections import defaultdict

NUMBER_OF_SEATS = 120

def get_votes_results(votes, remainders_couples, threshold_percent):
    """
    Gets the results of the elections.
    votes - dict of the votes results
    """

    results = defaultdict(int)
    total_votes = sum(votes.values())

    # Remove parties who did not pass threshold
    votes_to_threshold = int((total_votes * threshold_percent) // 100)
    for party_name in list(votes.keys()):
        if votes[party_name] < votes_to_threshold:
            del votes[party_name]
    total_votes = sum(votes.values())

    # First step - calculate plain results
    votes_to_seat = total_votes / NUMBER_OF_SEATS
    for party_name, party_votes in votes.items():
        results[party_name] = int(party_votes / votes_to_seat)

    # Second step - do Bader-Ofer 
    # Decide which party (couples?) should get additional seats
    seats_left = NUMBER_OF_SEATS - sum(results.values())
    parties_for_bader_ofer = set()
    for party_couple in remainders_couples:
        if all(party_name in results.keys() for party_name in party_couple):
            parties_for_bader_ofer.add(party_couple)

    for party_name in results.keys():
        if any(party_name in party_couple for party_couple in parties_for_bader_ofer):
            continue
        parties_for_bader_ofer.add(frozenset([party_name]))

    party_sets_votes = {}
    party_sets_bader_ofer_seats = {}
    for party_set in parties_for_bader_ofer:
        party_sets_votes[party_set] = sum(votes[party_name] for party_name in party_set)
        party_sets_bader_ofer_seats[party_set] = sum(results[party_name] for party_name in party_set) + 1

    seats_to_add = defaultdict(int)
    for _ in range(seats_left):
        party_sets_votes_to_pay = {}
        for party_set in parties_for_bader_ofer:
            party_sets_votes_to_pay[party_set] = party_sets_votes[party_set] / party_sets_bader_ofer_seats[party_set]
        
        winning_party_set = max(party_sets_votes_to_pay, key=party_sets_votes_to_pay.get)
        party_sets_bader_ofer_seats[winning_party_set] += 1
        seats_to_add[winning_party_set] += 1
    
    # Step 3 - decide to which of the parties set we actually
    # give the additional seats
    for party_set, seats_to_add_to_parties in seats_to_add.items():
        if len(party_set) == 1:
            results[list(party_set)[0]] += seats_to_add_to_parties
            continue
        
        joined_votes_per_seat = party_sets_votes[party_set] / (sum(results[party_name] for party_name in party_set) + seats_to_add_to_parties)
        seats_per_party = {
            party_name: int(votes[party_name] / joined_votes_per_seat) for party_name in party_set
        }

        # Edge case - there is still a seat left that we need to give one of the parties.
        seats_remaining = party_sets_bader_ofer_seats[party_set] - 1 - sum(seats_per_party.values())
        if seats_remaining > 0:
            for _ in range(seats_remaining):
                parties_votes_to_pay = {}
                for party_name in party_set:
                    parties_votes_to_pay[party_name] = votes[party_name] / (seats_per_party[party_name] + 1)
            
                winning_party = max(parties_votes_to_pay, key=parties_votes_to_pay.get)
                seats_per_party[winning_party] += 1

        # Actually give parties the seats
        for party_name, party_seats in seats_per_party.items():
            results[party_name] = party_seats

    assert sum(results.values()) == NUMBER_OF_SEATS
    return results
