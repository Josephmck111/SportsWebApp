import random, json

def generate_dummy_data():
    users = ['Bean', 'Joe', 'Rory', 'Conleth', 'Adam', 'Stevie', 'Spike', 'McFaul', 'Emmett', 'ConorG', 'Gallagher',
             'Cathal', 'Jody', 'Danny', 'Johnny', 'Jude', 'Dara', 'Oran', 'Odhran', 'Ethan', 'Dicko', 'JD', 'Alex', 
             'DannyT', 'Gagsy', 'Dom', 'Carville', 'Dougie', 'Gouj', 'Euny']
    user_list =  []

    for i in range(300):
        num = str(i)
        user = users[random.randint(0, len(users)-1)]
        user_list.append( { "User" : num, 
                            "Name" : user,
                            "Role" : "Standard",
                            "Comments" : [] }  )

    return user_list

users = generate_dummy_data()

fout = open("data12.json", "w")
fout.write(json.dumps(users))
fout.close()