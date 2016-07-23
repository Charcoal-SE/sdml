import cPickle
import os.path
import re

class NaiveBayesClassifier:
    def __init__(self, prior_spam, prior_ham):
        if os.path.isfile('prob.nbcd'):
            with open('prob.nbcd') as f:
                self.data = cPickle.loads(f.read())

            self.pspam = prior_spam
            self.pham = prior_ham
            print("NB Classifier: data loaded. pspam={0}, pham={1}".format(self.pspam, self.pham))
        else:
            raise Exception('The analyze and prepare scripts must be run before instantiating a classifier.')

    def classify(self, post, attribs):
        scores = {}
        nscores = {
            'spam': 0,
            'ham': 0
        }

        for attrib in attribs:
            if attrib not in post or post[attrib] is None:
                print("[classify] Post object does not contain attribute '{0}'. Classification accuracy will be affected.".format(attrib))
                continue

            scores[attrib] = {
                'spam': self.pspam,
                'ham': self.pham
            }

            post_words = re.findall(r"[\w']+", post[attrib])
            for word in post_words:
                word = word.lower()
                for dtype in self.data:
                    if word in self.data[dtype][attrib] and self.data[dtype][attrib][word] is not None:
                        scores[attrib][dtype] *= self.data[dtype][attrib][word]

            nfact = scores[attrib]['spam'] + scores[attrib]['ham']
            if nfact > 0:
                nscores['spam'] += float(scores[attrib]['spam']) / float(nfact)
                nscores['ham'] += float(scores[attrib]['ham']) / float(nfact)
            else:
                print("nfact=0 (sspam={0}, sham={1}, attrib={2}); cannot normalize. Skipping: classification accuracy will be affected."
                      .format(scores[attrib]['spam'], scores[attrib]['ham'], attrib))
                continue

        for name, score in nscores.iteritems():
            nscores[name] /= len(attribs)

        return (nscores['spam'] > nscores['ham']), nscores['spam'], nscores['ham']
