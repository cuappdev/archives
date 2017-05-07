import gensim
from stop_words import get_stop_words

class TopicModel:
    """
    Topic model for episodes. Uses latent dirichlet allocation.
    """
    lda_model = None
    dictionary = None
    
    def _episode_corpus(self, episodes):
        """
        Preprocesses episodes and creates a gensim corpus.
        """
        stop_words = get_stop_words("en")
        texts = []
        documents = [e.summary for e in episodes]
        for doc in documents:
            texts.append([word for word in document.lower().split() if word not in stop_words])
        dictionary = gensim.corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        return corpus
    
    def __init__(self, episodes, n_tags):
        """
        Creates a topic model for a collection of episodes.
        Can be accessed using bracket notation.
        """
        corpus = self._episode_corpus(episodes)
        self.lda_model = gensim.models.LdaModel(corpus, num_topics=n_tags)
        
    def top_tag_for_episode(self, episode):
        """
        Uses the topic model to grab the top tag for an episode.
        """
        bow = self.dictionary.doc2bow(episode.summary)
        if self.lda_model is not None:
            topic_dist = self.lda_model[bow]
            sorted_topic_dist = sorted(topic_dist, key=lambda t:t[1], reverse=True)
            return sorted_topic_dist[0][0]