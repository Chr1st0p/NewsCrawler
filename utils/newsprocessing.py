import lda
import numpy as np

from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

from stop_words import get_stop_words

from gensim import corpora, models
import gensim

if __name__ == '__main__':
    docA = """A Certis Cisco aviation security officer stole from passengers
    whose bags he was supposed to be screening at Changi Airport.Esyaran Mogan,
    now 29, grabbed a gold chain and cash from two women\'s belongings while
    searching through the bags at departure gates at Terminal 1. He was jailed
    for eight months yesterday after pleading guilty to two counts of theft.
    Esyaran, a Malaysian, was deployed as a manual bag searcher on July 24
    last year when he targeted his first victim, Ms Fu Qin, at around 11.30pm.
    Ms Fu, who was travelling to Beijing, had placed her handbag in an X-ray machine
    and it detected a pair of scissors among her belongings.Esyaran searched
    her handbag and spotted a gold chain, estimated to be worth $1,164, inside.
    While carrying the bag to the X-ray machine, he took the chain and slipped it
    into the right pocket of his trousers.When he searched the bag a second time,
    he found $350 in cash.Deputy Public Prosecutor Nicholas Wuan said: "Tempted,
    he stole the $350, again concealing the cash in his glove and placing it
    in his right pants pocket."Ms Fu discovered her losses only when she was
    in a taxi in Beijing.Esyaran struck again a week later.This time,
    he stole $106 in cash from an unidentified woman after she had shown
    him the contents of her pouch. The woman later approached Esyaran and
    asked him if he had found any money.DPP Wuan said: "The accused said
    he had not and pretended to search the area, before informing (her) that
    the cash could not be found. Later, the accused was informed by an airline
    staff member that (the passenger) intended to make a complaint. This
    caused the accused to worry."Esyaran tossed the cash under the X-ray machine
    and told his colleagues that he had "found" the money. His offences came to
    light after Certis Cisco Security reviewed closed-circuit television footage
    of the area.District Judge Low Wee Ping said Esyaran\'s offences could have
    affected the reputation of Changi Airport. He added: "You operated like a
    magician with a sleight of hand. (It was) quite impressive yet appalling.\"For
    each count of theft, Esyaran could have been jailed up to three years and fined."""
    raw = docA.lower()
    tokens = word_tokenize(raw)
    texts = []
    enStop = get_stop_words('en')
    stoppedTokens = [w for w in tokens if not w in enStop]

    pStemmer = PorterStemmer()
    stemmedTokens = [pStemmer.stem(w) for w in stoppedTokens]

    texts.append(stemmedTokens)
    vocab = stemmedTokens
    print len(stemmedTokens)

    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    # ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=4, id2word=dictionary, passes=30)
    # X = np.array(corpus[0])
    # print X
    # print X.shape
    # model = lda.LDA(n_topics=30, n_iter=500, random_state=1)
    # model.fit(X)
    # topic_word = model.topic_word_
    # n = 5
    # for i, topic_dist in enumerate(topic_word):
    #     topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n + 1):-1]
    #     print('*Topic {}\n- {}'.format(i, ' '.join(topic_words)))
