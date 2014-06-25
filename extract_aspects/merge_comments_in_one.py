# must be run in Python 3!

import csv, os, codecs
import pickle

home = "/Users/oliver/PycharmProjects/parse_comments/output_rev1"
output_dir = "/Users/oliver/PycharmProjects/extract_aspects"

# loading stopwords for stripping them from partial strings:
#stopwords_en = pickle.load(open('stopwords_corpus_dump_en.p', 'rb'))
#stopwords_de = pickle.load(open('stopwords_corpus_dump_de.p', 'rb'))

os.chdir(home)
fullstring = ''
i = 1
limit = 61930
while i <= limit:
    try:
        inputfile = '%s.csv' % (i)
        csvinput = codecs.open(inputfile, 'r', 'latin1')
        reader = csv.reader(csvinput, delimiter=';')
        csv_store = []
        count = 0
        for row in reader:
            csv_store.append(row)
            partstring = csv_store[count][2]
            partstring = str(partstring).lower() # lowercase for normalization
            # stripping stopwords:
            #partstring_stripped = [w for w in partstring if w not in stopwords_en]
            #partstring_stripped = [w for w in partstring_stripped if w not in stopwords_de]

            fullstring += str(' ')
            fullstring += str(partstring)
            count +=1
    except:
        print('error')
        pass
    #print(fullstring)
    print(i, ' / ', limit)
    i += 1
#print(fullstring)
os.chdir(output_dir)
#pickle.dump(fullstring, open('merged_dump_all_python2.p', 'wb'))

with open('merged_dump_all_python2.txt', 'wb') as outputfile:
    outputfile.write(fullstring.encode())


