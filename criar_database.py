import pickle

data_base = [{"username": "David", "lastname": "Shelton", "userpassword": "david123", "userbirthday": "26/02/2002", "usergender": "masculino"}]
with open("database.pickle", "wb") as db:
    pickle.dump(data_base, db)
