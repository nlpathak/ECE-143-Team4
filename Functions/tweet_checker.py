import pickle
import model_functions as MF
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

#Load trained models
'''
TfIdf_Model = pickle.load(open('tfidf_model.pickle', 'rb'))
TfIdf_Vectorizer = pickle.load(open('tfidf_vect.pickle', 'rb'))
'''
#w2v = gensim.models.Word2Vec.load('word2vec.model')
CountVect_Model = pickle.load(open('count_vect_model.pickle', 'rb'))
CountVect_Vect = pickle.load(open('count_vectorizer.pickle', 'rb'))


print('Tweet checker. Test the positivity of your tweet (before sending it!)')

userText = input('Type your tweet (up to 280 characters) to check positivity or \'end\' if you\'re done: ')
while userText != 'end':
    assert len(userText)<280
    if input('Select the model to use: Tf-Idf (1) or Count Vectorizer (2): ') == '1':
        '''
        model = TfIdf_Model
        vectorizer = TfIdf_Vectorizer
        modelLabel = 'Tf-Idf'
        '''
    else:
        model = CountVect_Model
        vectorizer = CountVect_Vect
        modelLabel = 'Count Vectorizer'
    tweetObj = MF.predict([userText], vectorizer, model, silence=True)

    tweetColor = np.ones((3,3))*tweetObj[0][2]
    tweetColor = tweetColor if tweetObj[0][1] == 'Positive' else -1*tweetColor
    tweetColor = (tweetColor+1)/2

    fig, ax = plt.subplots()
    im = ax.imshow(tweetColor, cmap=cm.get_cmap('RdYlGn'), vmax=1.0, vmin=0.0)
    ax.axis('off')
    if len(userText)>20:
        fontSize=15
    else:
        fontSize=-3/(2*len(userText)) + 30
    plt.text(1, 1, userText,
              bbox={'facecolor': 'beige', 'alpha': 1, 'edgecolor': 'none', 'pad': 1},
              ha='center', va='center', fontsize=int(fontSize))
    plt.text(1,2, 'Your tweet classifies as: ' + tweetObj[0][1], ha='center',va='center', fontsize=15)
    plt.show()
    userText = input('Type your tweet (up to 280 characters) to check positivity or \'end\' if you\'re done: ')

print('Thank you for using Tweet Checker!')