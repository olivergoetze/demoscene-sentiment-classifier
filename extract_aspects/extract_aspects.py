# must be run using Python 2!
from __future__ import division
import nltk, re, pprint
import csv, os, codecs, io
import pickle
from nltk import *
from nltk.corpus import stopwords

tokenize_again = 0

home = "/Users/oliver/PycharmProjects/extract_aspects"
output_dir = "/Users/oliver/PycharmProjects/extract_aspects"
outputfile_aspects = "extracted_aspects.csv"

stopwords_en = nltk.corpus.stopwords.words('english')
stopwords_de = nltk.corpus.stopwords.words('german')

if tokenize_again != 0:
    dump_open = open('merged_dump_all_python2.txt', 'r')
    full_comment_dump = dump_open.read()
    full_comment_dump_with_stopwords = full_comment_dump
    print('urspruengliche Laenge:', len(full_comment_dump))
    for stopword_item in stopwords_en:
        replace1 = ' ' + stopword_item + ' '
        full_comment_dump = full_comment_dump.replace(replace1, ' ')
        replace2 = ' ' + stopword_item + '.'
        full_comment_dump = full_comment_dump.replace(replace2, ' ')
        replace3 = ' ' + stopword_item + '!'
        full_comment_dump = full_comment_dump.replace(replace3, ' ')
        replace4 = ' ' + stopword_item + '?'
        full_comment_dump = full_comment_dump.replace(replace4, ' ')
        replace5 = ' ' + stopword_item + '...'
        full_comment_dump = full_comment_dump.replace(replace5, ' ')
    print('Laenge ohne Stoppwoerter:', len(full_comment_dump))
    #print(type(full_comment_dump))
    #print(len(full_comment_dump))
    #full_comment_dump = [w for w in full_comment_dump if w not in stopwords_de]
    pattern = r'''(?x)
                ([A-Z]\.)+
                | \w+(-\w+)*
                | \$?\d+(\.\d+)?%?
                | \.\.\.
                | [][.,;"'?():-_`]
                '''
    #test_sent = 'This is a test. U.S.A. test sentence, this is.'
    tokenized_dump = nltk.regexp_tokenize(full_comment_dump, pattern)
    tokenized_dump_with_stopwords = nltk.regexp_tokenize(full_comment_dump_with_stopwords, pattern)
    pickle.dump(tokenized_dump, open('tokenized_dump_all_python2.p', 'wb'))
    pickle.dump(tokenized_dump_with_stopwords, open('tokenized_dump_all_with_stopwords_python2.p', 'wb'))

tokenized_dump = pickle.load(open('tokenized_dump_all_python2.p', 'rb'))
tokenized_dump_with_stopwords = pickle.load(open('tokenized_dump_all_with_stopwords_python2.p', 'rb'))
#words = full_comment_dump.words
#print(tokenized_dump[:200])

# Umwandlung Token-List in NLTK-Text
tokenized_dump_nltk_text = nltk.Text(tokenized_dump)
tokenized_dump_with_stopwords_nltk_text = nltk.Text(tokenized_dump_with_stopwords)
#print(type(tokenized_dump_nltk_text))
#print(tokenized_dump_nltk_text[:20])

# Frequency Distribution
fdist1 = FreqDist(tokenized_dump_nltk_text)
vocabulary1 = fdist1.keys()
print(len(vocabulary1))
vocabulary_select = vocabulary1[:1000]
#print(fdist1['music'])
#print('radeon: ', fdist1['radeon'])
#print('resolution: ', fdist1['resolution'])
#print('soundtrack: ', fdist1['soundtrack'])
#print('textures: ', fdist1['textures'])
#print('engine: ', fdist1['engine'])
#print('filesize: ', fdist1['filesize'])
#fdist1.plot(50, cumulative=True)
#print(fdist1.hapaxes())
#print(vocabulary_select)
"""
print('\n****** Konkordanzen der Grafik-Aspekte ******')
asp_graphics = ['effects', 'gfx', 'visuals', 'visual', 'graphics', 'radeon', 'resolution', '3d', 'animation', 'interface', 'rendering', '2d', 'graphic', 'models', 'particles', 'sprites']
for aspect in asp_graphics:
    print('Konkordanzen fuer:', aspect)
    concordance_1 = tokenized_dump_with_stopwords_nltk_text.concordance(aspect)
    print(concordance_1)
    print(fdist1[aspect])
    print('-------')

print('\n****** Konkordanzen der Music-Aspekte ******')
asp_music = ['music', 'sound', 'audio', 'soundtrack', 'song', 'synth', 'musics']
for aspect in asp_music:
    print('Konkordanzen fuer:', aspect)
    concordance_1 = tokenized_dump_with_stopwords_nltk_text.concordance(aspect)
    print(concordance_1)
    print(fdist1[aspect])
    print('-------')

print('\n****** Konkordanzen der Tool-Aspekte ******')
asp_tool = ['tool']
for aspect in asp_tool:
    print('Konkordanzen fuer:', aspect)
    concordance_1 = tokenized_dump_with_stopwords_nltk_text.concordance(aspect)
    print(concordance_1)
    print(fdist1[aspect])
    print('-------')

print('\n****** Konkordanzen der Texture-Aspekte ******')
asp_texture = ['textures', 'texture']
for aspect in asp_texture:
    print('Konkordanzen fuer:', aspect)
    concordance_1 = tokenized_dump_with_stopwords_nltk_text.concordance(aspect)
    print(concordance_1)
    print(fdist1[aspect])
    print('-------')

print('\n****** Konkordanzen der Engine-Aspekte ******')
asp_engine = ['engine']
for aspect in asp_engine:
    print('Konkordanzen fuer:', aspect)
    concordance_1 = tokenized_dump_with_stopwords_nltk_text.concordance(aspect)
    print(concordance_1)
    print(fdist1[aspect])
    print('-------')

print('\n****** Konkordanzen der Code-Aspekte ******')
asp_code = ['code', 'filesize', '4k', '64k', 'coding', 'size', 'coder', '256b', '1k', 'coded']
for aspect in asp_code:
    print('Konkordanzen fuer:', aspect)
    concordance_1 = tokenized_dump_with_stopwords_nltk_text.concordance(aspect)
    print(concordance_1)
    print(fdist1[aspect])
    print('-------')

print('\n****** Konkordanzen der General-Aspekte ******')
asp_general = ['production', 'demo', 'prod', 'compo', 'release', 'game', 'product', 'result', 'execution', 'general', 'executed']
for aspect in asp_general:
    print('Konkordanzen fuer:', aspect)
    concordance_1 = tokenized_dump_with_stopwords_nltk_text.concordance(aspect)
    print(concordance_1)
    print(fdist1[aspect])
    print('-------')
"""
"""
print('\n****** Konkordanzen der noch nicht zugeordneten Aspekte ******')

asp_unknown = ['intro', 'intros', 'scene', 'design', 'style', 'tune', 'tunes', 'effect', 'video', 'youtube', 'screen', 'colors', 'colours', 'scenes', 'parts', 'quality', 'logo', 'art', 'font', 'fonts', 'text', 'screenshot', 'prods', 'concept', 'sounds', 'atmosphere', 'track', 'tracks', 'content', 'fx', 'background', 'hardware', 'cubes', 'picture', 'color', 'img', 'objects', 'port', 'problem', 'piece', 'mood', 'logotype', 'story', 'world', 'direction', 'mode', 'noise', 'camera', 'bytes', 'cube', 'ati', 'crashes', 'exe', 'software', 'system', 'title', 'xp', 'error', 'files', 'plasma', 'life', 'space', 'linux', 'menu', 'source', 'credits', 'opinion', 'moving', 'gif', 'random', 'realtime', 'bits', 'pictures', 'mod', 'transitions', 'emulator', 'home', 'theme', 'presentation', 'speed', 'bug', 'bugs', 'buggy', 'loading', 'flash', 'feature', 'features', 'crash', 'crashed', 'seconds', 'player', 'lines', 'mp3', 'blur', 'light', 'technical', 'mfx', 'playing', 'nfo', 'bigscreen', 'fan', 'image', 'ram', 'fullscreen', 'screens', 'bass', 'optimus', 'level', 'water', 'listen', 'memory', 'dosbox', 'cpu', 'dll', 'asm', 'hd', 'drivers', 'slideshow', 'dots', 'nvidia', 'fake',  'static', 'vector', 'stars', 'stingray', 'mac', 'win32', 'esc', 'pixel', 'songs', 'techno', '16', 'bouncing', 'movement', 'beauty', 'fps', 'details', 'motion', 'pic', 'raster', 'sample']
for aspect in asp_unknown:
    print('Konkordanzen fuer:', aspect)
    concordance_1 = tokenized_dump_with_stopwords_nltk_text.concordance(aspect)
    print(concordance_1)
    print(fdist1[aspect])
    print('-------')"""
"""
print('\n****** Konkordanzen der Sentiment Lexicon Kandidaten ******')

sent_cand = ['like', 'well', 'ok', 'better', 'cool', 'love', 'best', 'pretty', 'liked', 'party', 'funny', 'big', 'interesting', 'fun', 'simple', 'original', 'quality', 'art', 'damn', 'fucking', 'fuck', 'special', 'hell', 'alles', 'uber', 'perfect', 'worth', 'content', 'top', 'respect', 'favourite', 'working', 'pure', 'fresh', 'win', 'wonder', 'favorite', 'yay', 'winner', 'omg', 'kicks', 'mfx', 'congrats', 'killer', 'standard', 'high standard', 'low standard', 'polished', 'dig', 'forever', 'funky', 'thanx', 'fuckings', 'beauty', 'old', 'slow', 'shit', 'lol', 'die', 'hell', 'ass', 'wrong', 'strange', 'wtf', 'weird', 'small', 'lame', 'ripped', 'problem', 'missing', 'hate', 'average', 'crashes', 'error', 'stupid', 'lack', 'random', 'meh', 'joke', 'broken', 'missed', 'scheisse', 'lacks', 'miss', 'unfinished', 'sad', 'worse', 'rip', 'fake', 'nah', 'okish', 'fucked', 'copy', 'worst', 'buggy', 'down', 'bored']
for sent_word in sent_cand:
    print('Konkordanzen fuer:', sent_word)
    concordance_1 = tokenized_dump_with_stopwords_nltk_text.concordance(sent_word)
    print(concordance_1)
    print(fdist1[sent_word])
    print('-------')"""
"""
print('\n****** Konkordanzen der Smilie-Kandidaten ******')  # vgl ~/PycharmProjects/build_classifier_data/sentiment_lexicon/smilies.txt

sent_cand = [':)', ':))', ':)))', ':-)', ':-))', ':-)))', '=)', '=))', '=)))', ';)', ';))', ';)))', ';-)', ';-))', ';-)))', ':d', ':DD', ':DDD', ':-D', ':-DD', ':-DDD', '=D', '=DD', '=DDD', ':(', ':((', ':(((', ':-(', ':-((', ':-(((', '=(', '=((', '=(((', '-.-', ':P', ':PP', ':PPP', ':-P', ':-PP', ':-PPP', '=P', 'lol']
for sent_word in sent_cand:
    print('Konkordanzen fuer:', sent_word)
    concordance_1 = tokenized_dump_with_stopwords_nltk_text.concordance(sent_word)
    print(concordance_1)
    print(fdist1[sent_word])
    print('-------')"""
"""
print('\n****** Extraktion der Lengthening-Kandidaten ******')  # Quelle: tokenized_dump
#print(tokenized_dump[:10])
lengthening_candidates = []
tokenized_dump_test = ['greeat', 'greeeeeeat', 'niiice']
lengthening_pattern = re.compile(r"[a]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[e]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[o]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[u]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[i]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)"""
"""
lengthening_candidates = []
non_vocals = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']

lengthening_pattern = re.compile(r"[b]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[c]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[d]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[f]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[g]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[h]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[j]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[k]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[l]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[m]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[n]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[p]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[q]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[r]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[s]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[t]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[v]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[w]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[x]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[y]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)

lengthening_pattern = re.compile(r"[z]{3,}")
for token in tokenized_dump:
    lengthening_match = re.search(lengthening_pattern, token)
    #lengthening_match = re.search('eee', token)
    if lengthening_match:
        print token, ';', fdist1[token]
        lengthening_candidates.append(token)"""

"""
path_to_pos_lexicon = '/Users/oliver/PycharmProjects/build_classifier_data/sentiment_lexicon/lexicon_pos_final_cleaned.csv'
path_to_neg_lexicon = '/Users/oliver/PycharmProjects/build_classifier_data/sentiment_lexicon/lexicon_neg_final_cleaned.csv'

lexicon_store_pos = []
csvinput = codecs.open(path_to_pos_lexicon, 'r', 'latin1')
reader = csv.reader(csvinput, delimiter=';')
for row in reader:
    lexicon_store_pos.append(row)
#print(lexicon_store_pos)

lexicon_store_neg = []
csvinput = codecs.open(path_to_neg_lexicon, 'r', 'latin1')
reader = csv.reader(csvinput, delimiter=';')
for row in reader:
    lexicon_store_neg.append(row)

print('\nPositive Candidates for .similar:')
for pos_word in lexicon_store_pos:
    print '[POS] Similar Contexts: ', pos_word[0]
    print tokenized_dump_nltk_text.similar(pos_word[0])

print('\nNegative Candidates for .similar:')
for neg_word in lexicon_store_neg:
    print '[NEG] Similar Contexts: ', neg_word[0]
    print tokenized_dump_nltk_text.similar(neg_word[0])"""

#tokenized_dump_nltk_text.collocations()
tokenized_dump_nltk_text.concordance('but')



"""
#Collocations
collocations_tokenized_dump_nltk_text = tokenized_dump_nltk_text.collocations()
print(collocations_tokenized_dump_nltk_text)"""