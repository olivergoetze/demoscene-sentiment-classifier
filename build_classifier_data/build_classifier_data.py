import nltk, pprint, pickle
import httplib2, json, os, codecs, re, langid, collections, csv
from bs4 import BeautifulSoup
from wordnik import *
import time
from nltk.corpus import brown
timestamp = int(time.time())

# *** must be run in Python 2.7


"""source_doc = "no Clue about the code, but i really think you guys need a designer. i don't know, have the graphician sit next to you while you code the effects, or something. for me, the horribly ugly colours and completely saturated effects (too much happening at the same time to be able to actually see any of it) kind of ruined the demo-experience.. not bad in general though, so piggie. n1ce gfx, u guys r0ck, r34lly nice, best ev0r!"  # 33703.csv ('New World'), user = skrebbel, no thumb rating"""  # old source-doc from testing




# def. spellcheck class
def words(text): return re.findall('[a-z]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('big.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

#  new dynamic file import: (taken from fetch_from_ontology.py)
sourcedir = "/Users/oliver/PycharmProjects/parse_comments/output_rev1_testset"
outputdir = "/Users/oliver/PycharmProjects/build_classifier_data/document_output"

document_i =1
csv_store = []

while document_i <= 61930:
    try:
        inputfile = '%s.csv' % document_i
        os.chdir(sourcedir)
        csvinput = codecs.open(inputfile, 'r', 'latin1')
        reader = csv.reader(csvinput, delimiter=';')
        csv_row_count = 0
        for row in reader:
            csv_store.append(row)
    except:
        pass
    document_i += 1

from cPickle import dump
def pos_features_consec(sentence, i, history):
    features = {"suffix(1)": sentence[i][-1:], "suffix(2)": sentence[i][-2:], "suffix(3)": sentence[i][-3:]}
    if i == 0:
        features["prev-word"] = "<START>"
        features["prev-tag"] = "<START>"
    else:
        features["prev-word"] = sentence[i-1]
        features["prev-tag"] = history[i-1]
    return features

os.chdir('/Users/oliver/PycharmProjects/build_classifier_data/taggers')
cpickle_consec_tagger_outputfile = 'pos_consecutive_tagger_%s.pkl' % (str(timestamp))
cpickle_consec_tagger_output = open(cpickle_consec_tagger_outputfile, 'wb')
class ConsecutivePosTagger(nltk.TaggerI):
    def __init__(self, train_sents):
        train_set = []
        for tagged_sent in train_sents:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = pos_features_consec(untagged_sent, i, history)
                train_set.append( (featureset, tag) )
                history.append(tag)
        self.classifier = nltk.NaiveBayesClassifier.train(train_set)
        dump(self.classifier, cpickle_consec_tagger_output, -1)
        cpickle_consec_tagger_output.close()

    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = pos_features_consec(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)

print 'Sets erstellen'
tagged_sents = brown.tagged_sents(categories='news')
size = int(len(tagged_sents) * 0.1)
train_sents, test_sents = tagged_sents[size:], tagged_sents[:size]
print 'Training und Classification...'
consec_pos_classifier = ConsecutivePosTagger(train_sents)
print consec_pos_classifier.evaluate(test_sents)


comment_i = 0
first_iteration = 1
comment_i_indicator = 1
while comment_i <= len(csv_store):
    try:
        source_document = csv_store[comment_i][2]
        demo_i = csv_store[comment_i][0]
        demo_name = csv_store[comment_i][1]
        user = csv_store[comment_i][3]
        comment_date = csv_store[comment_i][4]
        thumb_rating = csv_store[comment_i][5]
        doc_meta = [demo_name, user, comment_date, thumb_rating]

        if first_iteration != 1:
            if demo_i != demo_i_indicator:
                comment_i_indicator = 1
        first_iteration = 0
        demo_i_indicator = demo_i

        # 1. Segmentierung (Satzweise, Punkt Segmenter)
        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle') # todo: nicht optimal, z.b. wird '..' nicht zur Segmentierung verwendet --> evtl. Segmenter mit eigenen Ausdruecken implementieren (--> ch. 6.2)
        sents = sent_tokenizer.tokenize(source_document)
        #pprint.pprint(sents)

        # 2. Tokenisierung
        token_pattern = r'''(?x)
                        ([A-Z]\.)+
                        | \w+(-\w+)*
                        | \$?\d+(\.\d+)?%?
                        | \.\.\.
                        | [][.,;"'?():-_`]
                        '''
        tokenized_sents = []
        for sent in sents:
            tokenized_sent = nltk.regexp_tokenize(sent, token_pattern)
            tokenized_sents.append(tokenized_sent)

        #print(tokenized_sents)

        # 3. Spracherkennung (evtl. sogar satzweise moeglich!)
        print_i= 1
        langid.set_languages(['en', 'de'])
        detected_language = ''
        language_matching = []
        for sent in sents:
            detected_language = langid.classify(sent)
            #print(print_i, sent, detected_language)
            language_matching.append([print_i, sent, detected_language[0]])
            print_i += 1
        print(language_matching)

        # 4. Normalisierung (lowercase, stopwords, spellcheck, thesauri)
        stopwords_en = nltk.corpus.stopwords.words('english')  # Definition der stopword Corpora
        stopwords_de = nltk.corpus.stopwords.words('german')

        for sent in sents:
            #print(type(sent))
            sents_no_stopwords = []
            sent = sent.lower()  # lowercase
            for stopword_item in stopwords_en:  # stopwords entfernen
                replace1 = ' ' + stopword_item + ' '
                sent = sent.replace(replace1, ' ')
                replace2 = ' ' + stopword_item + '.'
                sent = sent.replace(replace2, ' ')
                replace3 = ' ' + stopword_item + '!'
                sent = sent.replace(replace3, ' ')
                replace4 = ' ' + stopword_item + '?'
                sent = sent.replace(replace4, ' ')
                replace5 = ' ' + stopword_item + '...'
                sent = sent.replace(replace5, ' ')
                #replace6 = ' ' + stopword_item + '..'
                #sent = sent.replace(replace6, ' ')

            sents_no_stopwords.append(sent)  # erstmal nicht weiter verwendet, da wichtige informationen wie bei 'not bad' das not entfernt werden
            #print(sents_no_stopwords)

        tokenized_sents_no_stopwords = []
        for sent in sents_no_stopwords:
            tokenized_sent_no_stopwords = nltk.regexp_tokenize(sent, token_pattern)
            tokenized_sents_no_stopwords.append(tokenized_sent_no_stopwords)
        #print(tokenized_sents_no_stopwords)

        spellcheck_matching = []
        for sent in tokenized_sents_no_stopwords:
            for token in sent:
                leetspeak_match = re.search(r'[a-zA-Z]\d', token)  # Leetspeak-Woerter mit Spellcheck bearbeiten
                #if token != '.' and token != ',' and token != ', ' and token != '!' and token != '?':
                if leetspeak_match:
                    spellcheck_cand = correct(token)
                    if spellcheck_cand != '':
                        spellcheck_matching.append([token, spellcheck_cand])
                        #print(token, spellcheck_cand)
        #print(spellcheck_matching)

        # stopword free corpus verwenden, um relevante tokens dem spellcheck und thesauri check zu unterziehen, anschliessend im sents-corpus (mit stopwords) die entsprechenden woerter ersetzen und _dann_ tokenisieren
        spellchecked_sents = []
        for sent in sents:
            sent = sent.lower()
            for match_pair in spellcheck_matching:
                sent = sent.replace(match_pair[0], match_pair[1])
            spellchecked_sents.append(sent)
        #print(spellchecked_sents)

        #tokenisieren..
        tokenized_spellchecked_sents = []
        for sent in spellchecked_sents:
            tokenized_spellchecked_sent = nltk.regexp_tokenize(sent, token_pattern)
            tokenized_spellchecked_sents.append(tokenized_spellchecked_sent)
        print(tokenized_spellchecked_sents)

        # 5. POS Tagging
        # todo: training corpus von getaggten Dok. erstellen und diesen verwenden, um das haeufigste Tag zu finden (vom DefaultTagger benoetigt) --> Ch.5, S. 15
        #tags = [tag for (word, tag) in brown.tagged_words(categories='news')]
        #nltk.FreqDist(tags).max()
        default_tagger = nltk.DefaultTagger('NN')  # default tagger als baseline und fallback
        default_tagger__tokenized_spellchecked_sents = []
        for sent in tokenized_spellchecked_sents:
            default_tagger__tokenized_spellchecked_sent = default_tagger.tag(sent)
            default_tagger__tokenized_spellchecked_sents.append(default_tagger__tokenized_spellchecked_sent)
        #print(default_tagger__tokenized_spellchecked_sents)
        #print(type(default_tagger__tokenized_spellchecked_sents))

        #baseline_tagger = nltk.UnigramTagger(model=likely_tags, backoff=nltk.DefaultTagger('NN'))

        """
        print('Suffixe extrahieren')
        suffix_fdist = nltk.FreqDist()
        for word in brown.words():
            word = word.lower()
            suffix_fdist.inc(word[-1:])
            suffix_fdist.inc(word[-2:])
            suffix_fdist.inc(word[-3:])
        common_suffixes = suffix_fdist.keys()[:100]
        print common_suffixes

        def pos_features(word):
            features = {}
            for suffix in common_suffixes:
                features['endswith(%s)' % suffix] = word.lower().endswith(suffix)
            return features
        print('Sets generieren')
        tagged_words = brown.tagged_words(categories='news')
        featuresets = [(pos_features(n), g) for (n,g) in tagged_words]
        size = int(len(featuresets) * 0.1)
        train_set, test_set = featuresets[size:], featuresets[:size]
        #print(test_set[:100])"""
        """
        print('Training...')
        pos_tree_classifier = nltk.DecisionTreeClassifier.train(train_set)
        print('Tagger sichern')
        os.chdir('taggers')
        cpickle_tagger_output = open('pos_decision_tree_classifier_suffixes_brown_news.pkl', 'wb')
        dump(pos_tree_classifier, cpickle_tagger_output, -1)
        cpickle_tagger_output.close()
        #print nltk.classify.accuracy(pos_tree_classifier, test_set)


        print('Import Tagger...')
        from cPickle import load
        os.chdir('taggers')
        cpickle_tagger_input = open('pos_decision_tree_classifier_suffixes_brown_news.pkl', 'rb')
        pos_tree_classifier = load(cpickle_tagger_input)
        cpickle_tagger_input.close()

        tagged_tokenized_spellchecked_tokens = []
        tagged_tokenized_spellchecked_sents = []
        print('classifying')
        for sent in tokenized_spellchecked_sents:
            tagged_tokenized_spellchecked_tokens = []
            for token in sent:
                token_tag = pos_tree_classifier.classify(pos_features(token))
                tagged_tokenized_spellchecked_tokens.append((token, token_tag))
            tagged_tokenized_spellchecked_sents.append(tagged_tokenized_spellchecked_tokens)
        print(tagged_tokenized_spellchecked_sents)
        """




        consec_sents = []
        print('classifying')
        tagged_tokenized_spellchecked_sents = []
        for sent in tokenized_spellchecked_sents:
            sent_tagged = consec_pos_classifier.tag(sent)
            tagged_tokenized_spellchecked_sents.append(sent_tagged)
        print(tagged_tokenized_spellchecked_sents)
        os.chdir('/Users/oliver/PycharmProjects/build_classifier_data/document_output')
        doc_output = '%s_%s.p' % (str(demo_i), str(comment_i_indicator))
        meta_output = '%s_%s_meta.p' % (str(demo_i), str(comment_i_indicator))
        pickle.dump(tagged_tokenized_spellchecked_sents, open(doc_output, 'wb'))
        pickle.dump(doc_meta, open(meta_output, 'wb'))
        #sent_tag = consec_pos_classifier.classify(token)
         #   consec_sents.append(sent_tag)
        #print(consec_sents)
        # (6. Bau des Vokabulars) -- ggf. ausgliedern

        comment_i_indicator += 1
    except:
        pass

    comment_i +=1
