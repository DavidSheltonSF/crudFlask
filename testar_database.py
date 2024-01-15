import pickle

with open("database.pickle", "rb") as db:
    data_base = pickle.load(db)

print(data_base)


