import random, json

def generate_dummy_data():
    teams = ['Glen', 'Ballinderry', 'Bellaghy', 'Lavey', 'Newbridge', 
             'Dungiven', 'Steelstown', 'Kilrea', 'Slaughtneil', 'Ballinascreen', 
             'Magherafelt', 'Glenullin', 'Drumsurn', 'Faughanvale', 'Banagher', 'Claudy',
              'Ballerin', 'Coleraine', 'Castledawson', 'DoireTrasna']
    teams_list =  []

    for i in range(100):
        num = str(i)
        team = teams[random.randint(0, len(teams)-1)]
        division = random.randint(1, 2)
        teams_list.append( { "No." : num, 
                             "Team" : team, 
                             "Division" : division, 
                             "Comments" : [] }  )

    return teams_list

teams = generate_dummy_data()

fout = open("data10.json", "w")
fout.write(json.dumps(teams))
fout.close()