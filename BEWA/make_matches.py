import random, json
from datetime import datetime, timedelta

def generate_dummy_data():
    teams = ['Glen', 'Ballinderry', 'Bellaghy', 'Lavey', 'Newbridge', 
             'Dungiven', 'Steelstown', 'Kilrea', 'Slaughtneil', 'Ballinascreen', 
             'Magherafelt', 'Glenullin', 'Drumsurn', 'Faughanvale', 'Banagher', 'Claudy',
              'Ballerin', 'Coleraine', 'Castledawson']
    matches_list = []

    for team in teams:
        for i in range(15):  # 15 home games
            match_id = f"{team}_home_{i}"
            opponent = random.choice([t for t in teams if t != team])
            match_date = datetime.now() + timedelta(days=random.randint(1, 100))
            match = {
                "MatchID": match_id,
                "HomeTeam": team,
                "AwayTeam": opponent,
                "Date": match_date.strftime("%Y-%m-%d"),
                "VideoURL": f"http://example.com/match_videos/{match_id}.mp4",
                "Comments": []
            }
            matches_list.append(match)

        for i in range(15):  # 15 away games
            match_id = f"{team}_away_{i}"
            opponent = random.choice([t for t in teams if t != team])
            match_date = datetime.now() + timedelta(days=random.randint(1, 100))
            match = {
                "MatchID": match_id,
                "HomeTeam": opponent,
                "AwayTeam": team,
                "Date": match_date.strftime("%Y-%m-%d"),
                "VideoURL": f"http://example.com/match_videos/{match_id}.mp4",
                "Comments": []
            }
            matches_list.append(match)

    return matches_list

matches = generate_dummy_data()

with open("data13.json", "w") as fout:
    fout.write(json.dumps(matches, indent=4))

