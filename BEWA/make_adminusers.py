import random, json

def generate_dummy_data():
    admusers = ['Joe', 'John', 'Rory', 'David', 'Adam', 'Stephen']
    admuser_list =  []

    for i in admusers:
        num = str(i)
        admuser_list.append( { "User" : num, 
                               "Role" : "Admin",
                               "Comments" : [] }  )

    return admuser_list

admusers = generate_dummy_data()

fout = open("data11.json", "w")
fout.write(json.dumps(admusers))
fout.close()