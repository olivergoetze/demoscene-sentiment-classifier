from nltk.corpus import wordnet as wn
import os, codecs, csv
lexicon_dir = "/Users/oliver/PycharmProjects/build_classifier_data/sentiment_lexicon"

"""
print([str(lemma.name) for lemma in wn.synset('beneficial.s.01').lemmas])
print(wn.synset('good.a.01').definition) # todo: ADJ als POS Tag mitgeben
#print(wn.synset('good.a.01').examples[0])
print wn.synsets('good')

good = wn.synset('good.a.01')
good_ant = good.lemmas[0].antonyms()
print(wn.synset('bad.a.01').lemmas[0])

print(wn.synsets('epic', pos=wn.ADJ))
print(wn.synset('epic.a.01').lemmas[0].antonyms())
print(wn.synset('epic.a.01').definition)
print(wn.synset('epic.a.01').examples[0])

print(good.lemmas[0].derivationally_related_forms())
print(good.lemmas[0].pertainyms())
print(wn.synset('wow.v.01').definition)
print(wn.synset('wow.v.01').lemmas[0].antonyms())
print(wn.synsets('quality'))
print(wn.synset('quality.n.01').definition)
print(wn.synset('quality.n.01').examples[0])
print(wn.synset('quality.n.01').lemmas[0].antonyms())
"""

pos_csv = []
pos_result = []
neg_result = []  # Antonyme
os.chdir(lexicon_dir)
inputfile = 'pos_final.csv'
csvinput = codecs.open(inputfile, 'r', 'latin1')
reader = csv.reader(csvinput, delimiter=';')
for row in reader:
    pos_csv.append(row)
#print len(pos_csv)
#print(pos_csv)

pos_csv_i = 0
while pos_csv_i <= (len(pos_csv) - 1):
    try:
        pos_word = pos_csv[pos_csv_i][0]
        pos_tag = pos_csv[pos_csv_i][1]
        string = '%s.%s.01' % (pos_word, pos_tag)
        pos_syns = [str(lemma.name) for lemma in wn.synset(string).lemmas] #% (pos_word, pos_tag) # Lemma-Names
        for syn in pos_syns:
            pos_result.append(syn) # Synonyme hinzufuegen
            print(syn)
        #pos_lemmas = [str(lemma) for lemma in wn.synset('%s.%s.01').lemmas] % (pos_word, pos_tag) # Lemmas
        #for lemma in pos_lemmas:
        syns_i = 0
        while syns_i <= (len(pos_syns) - 1):
            string = '%s.%s.01' % (pos_word, pos_tag)
            pos_ant = wn.synset(string).lemmas[syns_i].antonyms() #% (pos_word, pos_tag)
            for lemma in pos_ant:
                pos_ant_name = str(lemma.name)
                print(lemma)
                neg_result.append(pos_ant_name) # Antonyme hinzufuegen
            pos_deriv = wn.synset(string).lemmas[syns_i].derivationally_related_forms() #% (pos_word, pos_tag)
            for lemma in pos_deriv:
                pos_deriv_name = str(lemma.name)
                pos_result.append(pos_deriv_name) # derivationally related forms hinzufuegen
            syns_i += 1

        pos_csv_i += 1

    except:
        print('error', pos_csv_i)
        pos_csv_i += 1
        pass
print(pos_result)
for item in pos_result:
    print(item)

print(neg_result)
for item in neg_result:
    print(item)

"""outputfile = 'pos_wn.csv'
with open(outputfile, 'wb') as output:
    writer = csv.writer(output, delimiter=';')
    writer.writerows(pos_result)"""