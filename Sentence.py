from Scores import Scores


class Sentence():
    def __init__(self, sent=None, sent_id=0):
        self.id = str(sent_id)
        self.tokenized = sent
        self.scores = Scores()

    def toJson(self):
        data = self.__dict__
        data['scores'] = self.scores.toJson()
        return data

    def from_dict(self, loadedDict):
        # self.set_sentence(loadedDict['tokenized'], loadedDict['id'])
        for key in loadedDict:
            if key in self.__dict__ and key != 'scores':
                self.__dict__[key] = loadedDict[key]
        self.scores.from_dict(loadedDict['scores'])

    def set_sentence(self, list_of_tokens, _id='0'):
        if not isinstance(list_of_tokens, list):
            print('A list of token must be given in order to crete a Sentence')
            return
        else:
            self.tokenized = list_of_tokens
            self.id = _id

    def print_Sentence(self):  # Only for debug -> too much verbose
        print([self.tokenized])

    def compute_Scores(self, attributes, score_list=[], loc_th=5,
                       loc=[0, 0, 0, 1, 0], reset=True):
        if reset:
            self.scores.zero()  # Reset to avoid update of loaded values

        attributes['sent_id'] = self.id
        attributes['tokenized'] = self.tokenized
        attributes['location_score_filter'] = loc
        attributes['location_threshold'] = loc_th

        functions = {'TF_score': self.scores.set_TF,
                     'Sentence_location': self.scores.set_sent_location,
                     'Proper_noun': self.scores.set_proper_noun,
                     'Co_occurrence': self.scores.set_co_occour,
                     'Similarity': self.scores.set_similarity_score,
                     'Numerical': self.scores.set_numScore,
                     'TF_IDF': self.scores.set_TF_ISF_IDF,
                     'Sentence_rank': self.scores.set_sentRank,
                     'Sentence_length': self.scores.set_sentLength,
                     'Positive_Negative': self.scores.set_posnegScore,
                     'Thematic_words': self.scores.set_thematicWordsScore,
                     'Named_entities': self.scores.set_namedEntitiesScore}

        if len(score_list) > 0:
            for key in score_list:
                functions.get(key)(attributes)
        else:
            for key in functions:  # If none in input, all scorings will run
                functions.get(key)(attributes)

    def get_total_score(self):
        return self.scores.get_total()

    def get_weighted_total_score(self, weights):
        return self.scores.get_weighted_total(weights)

    def info(self, verbose=True):
        if verbose:
            print('Tokens in sentence: {}'.format(len(self.tokenized)))
        return len(self.tokenized)

    def text(self):
        reconstructed_sentence = ''
        for token in self.tokenized:
            reconstructed_sentence += '{} '.format(token)
        return reconstructed_sentence

    def print_scores(self, text=False, onlyTotal=True):
        print('\nSentence id {}'.format(self.id))
        if text:
            reconstructed_sent = ''
            for token in self.tokenized:
                reconstructed_sent += '{} '.format(token)
            print(reconstructed_sent)
        if onlyTotal:
            self.scores.print_total_scores(detail=False, total=True)
        else:
            self.scores.print_total_scores(detail=True, total=True)
