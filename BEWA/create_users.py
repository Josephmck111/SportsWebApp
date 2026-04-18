from pymongo import MongoClient
import bcrypt

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.WebApp
users = db.users        

user_list = [
          { 
            "name" : "Joe McKenna",
            "username" : "Joem",  
            "password" : b"joe_m",
            "email" : "joem@glen.net",
            "admin" : True
          },
          { 
            "name" : "Rory Kavanagh",
            "username" : "roryk",  
            "password" : b"rory_k",
            "email" : "roryk@glen.net",
            "admin" : True
          },
          { 
            "name" : "Adam Speers",
            "username" : "adams",  
            "password" : b"adam_s",
            "email" : "adams@glen.net",
            "admin" : True
          },        
          { 
            "name" : "David",
            "username" : "davidd",  
            "password" : "david_d",
            "email" : "davidd@glen.net",
            "admin" : True
          },
          { 
            "name" : "John McCamley",
            "username" : "johnm",  
            "password" : b"john_m",
            "email" : "johnm@glen.net",
            "admin" : True
          }, 
          { 
            "name" : "Stephen Convery",
            "username" : "stephenc",  
            "password" : b"stephen_c",
            "email" : "stephenc@glen.net",
            "admin" : True
          }, 
          { 
            "name" : "Ciaran McFaul",
            "username" : "ciaranm",  
            "password" : b"ciaran_m",
            "email" : "ciaranm@glen.net",
            "admin" : False
          }, 
          { 
            "name" : "Connor Carville",
            "username" : "connorc",  
            "password" : b"connor_c",
            "email" : "connorc@glen.net",
            "admin" : False
          }, 
          { 
            "name" : "Spike",
            "username" : "spikew",  
            "password" : b"spike_w",
            "email" : "spikew@glen.net",
            "admin" : False
          }, 
                              { 
            "name" : "Dougie",
            "username" : "dougie",  
            "password" : b"dougie_r",
            "email" : "dougie@glen.net",
            "admin" : False
          }, 
                              { 
            "name" : "Cathal Mulholland",
            "username" : "cathalm",  
            "password" : b"cathal_m",
            "email" : "cathalm@glen.net",
            "admin" : False
          }, 
                              { 
            "name" : "Dom Carville",
            "username" : "domc",  
            "password" : b"dom_c",
            "email" : "domc@glen.net",
            "admin" : False
          }, 
                              { 
            "name" : "Ethan Doherty",
            "username" : "ethand",  
            "password" : b"ethan_d",
            "email" : "ethand@glen.net",
            "admin" : False
          }, 
                              { 
            "name" : "Conor Glass",
            "username" : "conorg",  
            "password" : b"conor_g",
            "email" : "conorg@glen.net",
            "admin" : False
          }, 
                              { 
            "name" : "Connlan Bradley",
            "username" : "connlanb",  
            "password" : b"connlan_b",
            "email" : "connlanb@glen.net",
            "admin" : False
          }, 
                                        { 
            "name" : "Emmett Bradley",
            "username" : "emmettb",  
            "password" : b"emmett_b",
            "email" : "emmettb@glen.net",
            "admin" : False
          }, 
          
                                        { 
            "name" : "Stevie Ohara",
            "username" : "stevieo",  
            "password" : b"stevie_o",
            "email" : "stevieo@glen.net",
            "admin" : False
          }, 
          
                                        { 
            "name" : "Eunan Mulholland",
            "username" : "eunanm",  
            "password" : b"eunan_m",
            "email" : "eunanm@glen.net",
            "admin" : False
          }, 
          
                                        { 
            "name" : "Jack Doherty",
            "username" : "jackd",  
            "password" : b"jack_d",
            "email" : "jackd@glen.net",
            "admin" : False
          }, 
          
                                        { 
            "name" : "Tiarnan Flanagan",
            "username" : "tiarnanf",  
            "password" : b"tiarnan_f",
            "email" : "tiarnanf@glen.net",
            "admin" : False
          }, 
          
                                        { 
            "name" : "Conleth McGuckian",
            "username" : "conlethm",  
            "password" : b"conleth_m",
            "email" : "conlethm@glen.net",
            "admin" : False
          }, 
          
                                        { 
            "name" : "Alex Doherty",
            "username" : "alexd",  
            "password" : b"alex_d",
            "email" : "alexd@glen.net",
            "admin" : False
          }, 
          
                                        { 
            "name" : "Danny Tallon",
            "username" : "dannyt",  
            "password" : b"danny_t",
            "email" : "dannyt@glen.net",
            "admin" : False
          }, 
                                        { 
            "name" : "Andy Warnock",
            "username" : "andyw",  
            "password" : b"andy_w",
            "email" : "andyw@glen.net",
            "admin" : False
          }, 
                                        { 
            "name" : "Conor Convery",
            "username" : "conorc",  
            "password" : b"conor_c",
            "email" : "conorc@glen.net",
            "admin" : False
          }, 
                                        { 
            "name" : "Paul Gunning",
            "username" : "paulg",  
            "password" : b"paul_g",
            "email" : "paulg@glen.net",
            "admin" : False
          }, 
                                        { 
            "name" : "Odhran Molloy",
            "username" : "odhranm",  
            "password" : b"odhran_m",
            "email" : "odhranm@glen.net",
            "admin" : False
          }, 
                                        { 
            "name" : "Conleth Lagan",
            "username" : "conlethl",  
            "password" : b"conleth_l",
            "email" : "conlethl@glen.net",
            "admin" : False
          }, 
                                        { 
            "name" : "Johnny McGuckian",
            "username" : "johnnym",  
            "password" : b"johnny_m",
            "email" : "johnnym@glen.net",
            "admin" : False
          }, 
                                        { 
            "name" : "Ryan Gallagher",
            "username" : "ryang",  
            "password" : b"ryan_g",
            "email" : "ryang@glen.net",
            "admin" : False
          }, 
                                        { 
            "name" : "Conor Gallagher",
            "username" : "conorg",  
            "password" : b"conor_g",
            "email" : "conorg@glen.net",
            "admin" : False
          }, 
                                        { 
            "name" : "Cathal Gallagher",
            "username" : "cathalg",  
            "password" : b"cathal_g",
            "email" : "cathalg@glen.net",
            "admin" : False
          }, 
                                        { 
            "name" : "Lorcan McCauley",
            "username" : "lorcanm",  
            "password" : b"lorcan_m",
            "email" : "lorcanm@glen.net",
            "admin" : False
          }, 
                                        { 
            "name" : "Andy Ferg",
            "username" : "andyf",  
            "password" : b"andy_f",
            "email" : "andyf@glen.net",
            "admin" : False
          }, 
                                        { 
            "name" : "Caca Glass",
            "username" : "cacag",  
            "password" : b"caca_g",
            "email" : "cacag@glen.net",
            "admin" : False
          }, 
                                        { 
            "name" : "Marc Dixon",
            "username" : "marcd",  
            "password" : b"marc_d",
            "email" : "marcd@glen.net",
            "admin" : False
          }, 
                                        { 
            "name" : "Conor Bryson",
            "username" : "conorb",  
            "password" : b"conor_b",
            "email" : "conorb@glen.net",
            "admin" : False
          }, 
                                        { 
            "name" : "James Bryson",
            "username" : "jamesb",  
            "password" : b"james_b",
            "email" : "jamesb@glen.net",
            "admin" : False
          }, 
        
       ]

for new_user in user_list:
      if isinstance(new_user["password"], str):
        new_user["password"] = new_user["password"].encode('utf-8')
      new_user["password"] = bcrypt.hashpw(new_user["password"], bcrypt.gensalt())
      users.insert_one(new_user)
