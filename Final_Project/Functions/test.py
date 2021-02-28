import pickle

read_vect = pickle.load(open('count_vectorizer.pickle', 'rb'))
read_model = pickle.load(open('count_vect_model.pickle', 'rb'))
'''
example_vector = read_vect.transform(['I hate you but I love you!'])
print(read_model.predict(example_vector))
'''

# pull tweets like chris
# sum similar words
# word cloud
# color word cloud

