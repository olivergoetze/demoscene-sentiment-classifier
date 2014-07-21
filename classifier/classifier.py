from sentiwordnet import SentiWordNetCorpusReader, SentiSynset
import pickle
import nltk
import csv, os, codecs, io, re
swn_filename = 'SentiWordNet_3.0.0_20130122.txt'
swn = SentiWordNetCorpusReader(swn_filename)

#  Lexikon-Import:
path_to_pos_lexicon = '/Users/oliver/PycharmProjects/build_classifier_data/sentiment_lexicon/lexicon_pos_final_cleaned_w_lengthening.csv'
path_to_neg_lexicon = '/Users/oliver/PycharmProjects/build_classifier_data/sentiment_lexicon/lexicon_neg_final_cleaned_w_lengthening.csv'

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
#print(lexicon_store_neg)

#  Definition Aspekt-Woerter:
lookup_table_graphics_aspects = ['effects', 'gfx', 'visuals', 'visual', 'graphics', '3d', 'animation', 'interface', 'rendering', '2d', 'graphic', 'models', 'particles', 'sprites', 'design', 'effect', 'colors', 'colours', 'color', 'scenes', 'fonts', 'fx', 'objects', 'camera', 'menu', 'raytracing', 'pictures', 'transitions', 'presentation', 'vector']
lookup_table_music_aspects = ['music', 'sound', 'audio', 'soundtrack', 'song', 'synth', 'musics', 'tune', 'tunes', 'sounds', 'mod', 'bass']
lookup_table_tool_aspects = []
lookup_table_texture_aspects = ['textures', 'texture']
lookup_table_engine_aspects = ['engine', 'speed']
lookup_table_code_aspects = ['code', 'filesize', 'coding', 'size', 'coded']
lookup_table_general_aspects = ['production', 'demo', 'prod', 'result', 'execution', 'general', 'executed', 'intro', 'intros', 'concept', 'piece', 'direction', 'theme', 'this', 'it', 'one']

all_lookup_tables = []
all_lookup_tables.append(lookup_table_graphics_aspects)
all_lookup_tables.append(lookup_table_music_aspects)
#all_lookup_tables.append(lookup_table_tool_aspects)
all_lookup_tables.append(lookup_table_texture_aspects)
all_lookup_tables.append(lookup_table_engine_aspects)
all_lookup_tables.append(lookup_table_code_aspects)
all_lookup_tables.append(lookup_table_general_aspects)


#  SentiWordNet-Integration:
"""sent_word = 'wow'
sent_object = swn.senti_synsets(sent_word, 'v')[0]
print(sent_object.pos_score)
print(sent_object.neg_score)
print(sent_object.obj_score)"""

demo_count = 61930
demo_i = 21
comment_i = 1
all_demo_quintuples = []
while demo_i <= demo_count:
    comment_import = []
    try:
        comment_filename = '/Users/oliver/PycharmProjects/build_classifier_data/document_output/%s_%s.p' % (demo_i, comment_i)
        meta_filename = '/Users/oliver/PycharmProjects/build_classifier_data/document_output/%s_%s_meta.p' % (demo_i, comment_i)
        comment_import = pickle.load(open(comment_filename, 'rb'))
        #comment_import = pickle.load(open('/Users/oliver/PycharmProjects/build_classifier_data/document_output/demo_1_doc_1_content.p', 'rb'))
        meta_import = pickle.load(open(meta_filename, 'rb'))
        #print(comment_import)
        #print 'IMPORT-TRY 1, demo_i=', demo_i
        print comment_import
    except:  # wenn alle Kommentare einer Demo bearbeitet, zur naechsten Demo wechseln
        try:
            demo_i += 1
            comment_i = 1
            comment_filename = '/Users/oliver/PycharmProjects/build_classifier_data/document_output/%s_%s.p' % (demo_i, comment_i)
            meta_filename = '/Users/oliver/PycharmProjects/build_classifier_data/document_output/%s_%s_meta.p' % (demo_i, comment_i)
            comment_import = pickle.load(open(comment_filename, 'rb'))
            meta_import = pickle.load(open(meta_filename, 'rb'))
            #print('moving on to next demo...', comment_import)
            #print 'IMPORT-TRY 2, demo_i=', demo_i
            print comment_import
        except:
            pass

    #  hier Abfrage Expertenstatus (Ontologie)
    expert_status_file = '%s_expert.csv' % (demo_i)
    os.chdir('/Users/oliver/PycharmProjects/fetch_expert_status/expert_single')
    #  csv reader
    expert_status_store = []
    expert_status_array = []
    try:
        csvinput = codecs.open(expert_status_file, 'r', 'latin1')
        csv_reader = csv.reader(csvinput, delimiter=';')
        print 'demo_i:', demo_i
        print 'comment_i:', comment_i
        for row in csv_reader:
            expert_status_store.append(row)
    except:
        pass

    boost_graphics = 0
    boost_music = 0
    boost_texture = 0
    boost_engine = 0
    boost_code = 0
    boost_general = 0

    #print demo_i #DEBUG
    #print expert_status_store[1][0]  #DEBUG
    try:
        expert_status_array = expert_status_store[comment_i][3]
        expert_status_array = expert_status_array.split(',')
    except:
        pass
    for expert_status in expert_status_array:
        if expert_status == 'graphics':
            boost_graphics = 1
        if expert_status == 'music':
            boost_music = 1
        if expert_status == 'texture':
            boost_texture = 1
        if expert_status == 'engine':
            boost_engine = 1
        if expert_status == 'code':
            boost_code = 1
        if expert_status == 'general':
            boost_general = 1  # when boost, multiply sentiment * 2

    polarity_pairs = []
    all_comment_quintuples = []  #  entity name, aspect, sentiment on the aspect, opinion holder, time, (Thumbs-Rating) -- fehlende Daten mitliefern ueber build_classifier_data.py (entity name, opinion holder, time)
    sentiment_shifters = ['not', 'never', 'none', 'no', 'neither', 'nor', 'isn']
    sentiment_shifters_exceptions = ['only']  # wenn diese Woerter auf die Sentiment-Shifters folgen, duerfen sie nicht angewandt werden
    for sent in comment_import:
        index_i = 0
        for word in sent:
            """#print(word[0]) #todo: mit RegEx (+ WordBoundaries) ueberpruefen ob Lexikon-Woerter enthalten
            for pos_sent_word in lexicon_store_pos:
                regex_string = '^%s$' % str(pos_sent_word[0])
                #print(regex_string)
                word_match = re.search(regex_string, word[0])
                if word_match:
                    print('MATCH', word_match, word[0])"""
            prior_positive_match = 0
            for aspect_string in lookup_table_graphics_aspects:
                aspect_name = 'graphics'
                regex_string = '^%s$' % aspect_string
                matches_aspect = re.search(regex_string, word[0])
                if matches_aspect:
                    #print('graphics match: ', aspect_string)
                     #  5 Woerter vorher und nachher pruefen auf sentiment words, dann Pairs generieren (f, o) ; durch Iterator feststellen, an welcher Position im Satz Aspekt-Wort auftritt -- Zugriff ueber sent[i];
                    #  Definition der Sentiment-Region:
                    sentiment_region = [1, 2, 3, 4, 5]
                    for region in sentiment_region:
                        # Region nach Aspekt-Wort:
                        try:
                            #print(sent[index_i])
                            sentiment_candidate = sent[index_i+region]
                            candidate_index = index_i+region
                            #print(sentiment_candidate)
                            #  Positives Lexikon:
                            for pos_sent_word in lexicon_store_pos:
                                regex_string = '^%s$' % str(pos_sent_word[0])  # todo: evtl. Begrenzung fuer Wortende entfernen fuer besseren Recall (z.B. flektierte Verbformen)
                                word_match = re.search(regex_string, sentiment_candidate[0])
                                if word_match:
                                    prior_positive_match = 1
                                    #print('graphics-MATCH-after:', aspect_string, pos_sent_word[0], sentiment_candidate[0])
                                    polarity_shift = 0
                                    #  Vorherige zwei Woerter mit sentiment_shifters-List abgleichen. Wenn sentiment shifter auftaucht, dann Polaritaet umkehren:
                                    for shifter in sentiment_shifters:
                                        regex_string_shifter = '^%s$' % shifter
                                        shifter_candidate1 = sent[candidate_index-1]
                                        shifter_candidate2 = sent[candidate_index-2]
                                        shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                        shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])
                                        if shifter_match1:
                                            shifter_candidate1_index = candidate_index-1
                                            for shifter_exception_word in sentiment_shifters_exceptions:
                                                regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                if not shifter_exception_match:
                                                    if boost_graphics == 1:
                                                        polarity_pairs.append([aspect_name, -2])
                                                    else:
                                                        polarity_pairs.append([aspect_name, -1])
                                                    polarity_shift += 1
                                        elif shifter_match2:
                                            shifter_candidate2_index = candidate_index-2
                                            for shifter_exception_word in sentiment_shifters_exceptions:
                                                regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                if not shifter_exception_match:

                                                    if boost_graphics == 1:
                                                        polarity_pairs.append([aspect_name, -2])
                                                    else:
                                                        polarity_pairs.append([aspect_name, -1])
                                                    polarity_shift += 1
                                        else:
                                            polarity_shift += 0

                                    if polarity_shift <= 0:

                                        if boost_graphics == 1:
                                            polarity_pairs.append([aspect_name, 2])
                                        else:
                                            polarity_pairs.append([aspect_name, 1])
                            #  Negatives Lexikon:
                            if prior_positive_match == 0:
                                for neg_sent_word in lexicon_store_neg:
                                    regex_string = '^%s$' % str(neg_sent_word[0])
                                    word_match = re.search(regex_string, sentiment_candidate[0])
                                    if word_match:
                                        #print('graphics-MATCH-after:', aspect_string, neg_sent_word[0], sentiment_candidate[0])
                                        polarity_shift = 0
                                        for shifter in sentiment_shifters:
                                            regex_string_shifter = '^%s$' % shifter
                                            shifter_candidate1 = sent[candidate_index-1]
                                            shifter_candidate2 = sent[candidate_index-2]
                                            shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                            shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])
                                            if shifter_match1:
                                                shifter_candidate1_index = candidate_index-1
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_graphics == 1:
                                                            polarity_pairs.append([aspect_name, 2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, 1])
                                                        polarity_shift += 1
                                            elif shifter_match2:
                                                shifter_candidate2_index = candidate_index-2
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_graphics == 1:
                                                            polarity_pairs.append([aspect_name, 2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, 1])
                                                        polarity_shift += 1
                                            else: polarity_shift += 0

                                        if polarity_shift <= 0:
                                            if boost_graphics == 1:
                                                polarity_pairs.append([aspect_name, -2])
                                            else:
                                                polarity_pairs.append([aspect_name, -1])
                        except:
                            #print('index out of range')
                            pass
                        # Region vor Aspekt-Wort:
                        try:
                            if (index_i-region) >= 0:
                                sentiment_candidate = sent[index_i-region]
                                candidate_index = index_i-region
                                #  Positives Lexikon:
                                for pos_sent_word in lexicon_store_pos:
                                    regex_string = '^%s$' % str(pos_sent_word[0])
                                    word_match = re.search(regex_string, sentiment_candidate[0])
                                    if word_match:
                                        #print('graphics-MATCH-before:', aspect_string, pos_sent_word[0], sentiment_candidate[0])
                                        polarity_shift = 0
                                        for shifter in sentiment_shifters:
                                            regex_string_shifter = '^%s$' % shifter
                                            shifter_candidate1 = sent[candidate_index-1]
                                            shifter_candidate2 = sent[candidate_index-2]
                                            shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                            shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])

                                            if shifter_match1:
                                                shifter_candidate1_index = candidate_index-1
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_graphics == 1:
                                                            polarity_pairs.append([aspect_name, -2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, -1])
                                                        polarity_shift += 1
                                            elif shifter_match2:
                                                shifter_candidate2_index = candidate_index-2
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_graphics == 1:
                                                            polarity_pairs.append([aspect_name, -2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, -1])
                                                        polarity_shift += 1
                                            else:
                                                polarity_shift += 0

                                        if polarity_shift <= 0:
                                            if boost_graphics == 1:
                                                polarity_pairs.append([aspect_name, 2])
                                            else:
                                                polarity_pairs.append([aspect_name, 1])

                                #  Negatives Lexikon:
                                if prior_positive_match == 0:
                                    for neg_sent_word in lexicon_store_neg:
                                        regex_string = '^%s$' % str(neg_sent_word[0])
                                        word_match = re.search(regex_string, sentiment_candidate[0])
                                        if word_match:
                                            #print('graphics-MATCH-before:', aspect_string, neg_sent_word[0], sentiment_candidate[0])
                                            polarity_shift = 0
                                            for shifter in sentiment_shifters:
                                                regex_string_shifter = '^%s$' % shifter
                                                shifter_candidate1 = sent[candidate_index-1]
                                                shifter_candidate2 = sent[candidate_index-2]
                                                shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                                shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])

                                                if shifter_match1:
                                                    shifter_candidate1_index = candidate_index-1
                                                    for shifter_exception_word in sentiment_shifters_exceptions:
                                                        regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                        shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                        shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                        if not shifter_exception_match:
                                                            if boost_graphics == 1:
                                                                polarity_pairs.append([aspect_name, 2])
                                                            else:
                                                                polarity_pairs.append([aspect_name, 1])
                                                            polarity_shift += 1
                                                elif shifter_match2:
                                                    shifter_candidate2_index = candidate_index-2
                                                    for shifter_exception_word in sentiment_shifters_exceptions:
                                                        regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                        shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                        shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                        if not shifter_exception_match:
                                                            if boost_graphics == 1:
                                                                polarity_pairs.append([aspect_name, 2])
                                                            else:
                                                                polarity_pairs.append([aspect_name, 1])
                                                            polarity_shift += 1
                                                else:
                                                    polarity_shift += 0

                                            if polarity_shift <= 0:
                                                if boost_graphics == 1:
                                                    polarity_pairs.append([aspect_name, -2])
                                                else:
                                                    polarity_pairs.append([aspect_name, -1])
                        except:
                            #print('index out of range')
                            pass
            #  **** LOOKUP-TABLE MUSIC ****
            for aspect_string in lookup_table_music_aspects:
                aspect_name = 'music'
                regex_string = '^%s$' % aspect_string
                matches_aspect = re.search(regex_string, word[0])
                if matches_aspect:
                    #print('graphics match: ', aspect_string)
                     #  5 Woerter vorher und nachher pruefen auf sentiment words, dann Pairs generieren (f, o) ; durch Iterator feststellen, an welcher Position im Satz Aspekt-Wort auftritt -- Zugriff ueber sent[i];
                    #  Definition der Sentiment-Region:
                    sentiment_region = [1, 2, 3, 4, 5]
                    for region in sentiment_region:
                        # Region nach Aspekt-Wort:
                        try:
                            #print(sent[index_i])
                            sentiment_candidate = sent[index_i+region]
                            candidate_index = index_i+region
                            #print(sentiment_candidate)
                            #  Positives Lexikon:
                            for pos_sent_word in lexicon_store_pos:
                                regex_string = '^%s$' % str(pos_sent_word[0])
                                word_match = re.search(regex_string, sentiment_candidate[0])
                                if word_match:
                                    prior_positive_match = 1
                                    #print('music-MATCH-after:', aspect_string, pos_sent_word[0], sentiment_candidate[0])
                                    polarity_shift = 0
                                    #  Vorherige zwei Woerter mit sentiment_shifters-List abgleichen. Wenn sentiment shifter auftaucht, dann Polaritaet umkehren:
                                    for shifter in sentiment_shifters:
                                        regex_string_shifter = '^%s$' % shifter
                                        shifter_candidate1 = sent[candidate_index-1]
                                        shifter_candidate2 = sent[candidate_index-2]
                                        shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                        shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])
                                        if shifter_match1:
                                            shifter_candidate1_index = candidate_index-1
                                            for shifter_exception_word in sentiment_shifters_exceptions:
                                                regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                if not shifter_exception_match:
                                                    if boost_music == 1:
                                                        polarity_pairs.append([aspect_name, -2])
                                                    else:
                                                        polarity_pairs.append([aspect_name, -1])
                                                    polarity_shift += 1
                                        elif shifter_match2:
                                            shifter_candidate2_index = candidate_index-2
                                            for shifter_exception_word in sentiment_shifters_exceptions:
                                                regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                if not shifter_exception_match:
                                                    if boost_music == 1:
                                                        polarity_pairs.append([aspect_name, -2])
                                                    else:
                                                        polarity_pairs.append([aspect_name, -1])
                                                    polarity_shift += 1
                                        else:
                                            polarity_shift += 0

                                    if polarity_shift <= 0:
                                        if boost_music == 1:
                                            polarity_pairs.append([aspect_name, 2])
                                        else:
                                            polarity_pairs.append([aspect_name, 1])
                            #  Negatives Lexikon:
                            if prior_positive_match == 0:
                                for neg_sent_word in lexicon_store_neg:
                                    regex_string = '^%s$' % str(neg_sent_word[0])
                                    word_match = re.search(regex_string, sentiment_candidate[0])
                                    if word_match:
                                        #print('music-MATCH-after:', aspect_string, neg_sent_word[0], sentiment_candidate[0])
                                        polarity_shift = 0
                                        for shifter in sentiment_shifters:
                                            regex_string_shifter = '^%s$' % shifter
                                            shifter_candidate1 = sent[candidate_index-1]
                                            shifter_candidate2 = sent[candidate_index-2]
                                            shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                            shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])
                                            if shifter_match1:
                                                shifter_candidate1_index = candidate_index-1
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_music == 1:
                                                            polarity_pairs.append([aspect_name, 2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, 1])
                                                        polarity_shift += 1
                                            elif shifter_match2:
                                                shifter_candidate2_index = candidate_index-2
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_music == 1:
                                                            polarity_pairs.append([aspect_name, 2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, 1])
                                                        polarity_shift += 1
                                            else: polarity_shift += 0

                                        if polarity_shift <= 0:
                                            if boost_music == 1:
                                                polarity_pairs.append([aspect_name, -2])
                                            else:
                                                polarity_pairs.append([aspect_name, -1])
                        except:
                            #print('index out of range')
                            pass
                        # Region vor Aspekt-Wort:
                        try:
                            if (index_i-region) >= 0:
                                sentiment_candidate = sent[index_i-region]
                                candidate_index = index_i-region
                                #  Positives Lexikon:
                                for pos_sent_word in lexicon_store_pos:
                                    regex_string = '^%s$' % str(pos_sent_word[0])
                                    word_match = re.search(regex_string, sentiment_candidate[0])
                                    if word_match:
                                        #print('music-MATCH-before:', aspect_string, pos_sent_word[0], sentiment_candidate[0])
                                        polarity_shift = 0
                                        for shifter in sentiment_shifters:
                                            regex_string_shifter = '^%s$' % shifter
                                            shifter_candidate1 = sent[candidate_index-1]
                                            shifter_candidate2 = sent[candidate_index-2]
                                            shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                            shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])

                                            if shifter_match1:
                                                shifter_candidate1_index = candidate_index-1
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_music == 1:
                                                            polarity_pairs.append([aspect_name, -2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, -1])
                                                        polarity_shift += 1
                                            elif shifter_match2:
                                                shifter_candidate2_index = candidate_index-2
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_music == 1:
                                                            polarity_pairs.append([aspect_name, -2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, -1])
                                                        polarity_shift += 1
                                            else:
                                                polarity_shift += 0

                                        if polarity_shift <= 0:
                                            if boost_music == 1:
                                                polarity_pairs.append([aspect_name, 2])
                                            else:
                                                polarity_pairs.append([aspect_name, 1])

                                #  Negatives Lexikon:
                                if prior_positive_match == 0:
                                    for neg_sent_word in lexicon_store_neg:
                                        regex_string = '^%s$' % str(neg_sent_word[0])
                                        word_match = re.search(regex_string, sentiment_candidate[0])
                                        if word_match:
                                            #print('music-MATCH-before:', aspect_string, neg_sent_word[0], sentiment_candidate[0])
                                            polarity_shift = 0
                                            for shifter in sentiment_shifters:
                                                regex_string_shifter = '^%s$' % shifter
                                                shifter_candidate1 = sent[candidate_index-1]
                                                shifter_candidate2 = sent[candidate_index-2]
                                                shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                                shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])

                                                if shifter_match1:
                                                    shifter_candidate1_index = candidate_index-1
                                                    for shifter_exception_word in sentiment_shifters_exceptions:
                                                        regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                        shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                        shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                        if not shifter_exception_match:
                                                            if boost_music == 1:
                                                                polarity_pairs.append([aspect_name, 2])
                                                            else:
                                                                polarity_pairs.append([aspect_name, 1])
                                                            polarity_shift += 1
                                                elif shifter_match2:
                                                    shifter_candidate2_index = candidate_index-2
                                                    for shifter_exception_word in sentiment_shifters_exceptions:
                                                        regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                        shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                        shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                        if not shifter_exception_match:
                                                            if boost_music == 1:
                                                                polarity_pairs.append([aspect_name, 2])
                                                            else:
                                                                polarity_pairs.append([aspect_name, 1])
                                                            polarity_shift += 1
                                                else:
                                                    polarity_shift += 0

                                            if polarity_shift <= 0:
                                                if boost_music == 1:
                                                    polarity_pairs.append([aspect_name, -2])
                                                else:
                                                    polarity_pairs.append([aspect_name, -1])
                        except:
                            #print('index out of range')
                            pass

            # **** LOOKUP-TABLE TEXTURE ****
            for aspect_string in lookup_table_texture_aspects:
                aspect_name = 'textures'
                regex_string = '^%s$' % aspect_string
                matches_aspect = re.search(regex_string, word[0])
                if matches_aspect:
                    #print('graphics match: ', aspect_string)
                     #  5 Woerter vorher und nachher pruefen auf sentiment words, dann Pairs generieren (f, o) ; durch Iterator feststellen, an welcher Position im Satz Aspekt-Wort auftritt -- Zugriff ueber sent[i];
                    #  Definition der Sentiment-Region:
                    sentiment_region = [1, 2, 3, 4, 5]
                    for region in sentiment_region:
                        # Region nach Aspekt-Wort:
                        try:
                            #print(sent[index_i])
                            sentiment_candidate = sent[index_i+region]
                            candidate_index = index_i+region
                            #print(sentiment_candidate)
                            #  Positives Lexikon:
                            for pos_sent_word in lexicon_store_pos:
                                regex_string = '^%s$' % str(pos_sent_word[0])
                                word_match = re.search(regex_string, sentiment_candidate[0])
                                if word_match:
                                    prior_positive_match = 1
                                    #print('texture-MATCH-after:', aspect_string, pos_sent_word[0], sentiment_candidate[0])
                                    polarity_shift = 0
                                    #  Vorherige zwei Woerter mit sentiment_shifters-List abgleichen. Wenn sentiment shifter auftaucht, dann Polaritaet umkehren:
                                    for shifter in sentiment_shifters:
                                        regex_string_shifter = '^%s$' % shifter
                                        shifter_candidate1 = sent[candidate_index-1]
                                        shifter_candidate2 = sent[candidate_index-2]
                                        shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                        shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])
                                        if shifter_match1:
                                            shifter_candidate1_index = candidate_index-1
                                            for shifter_exception_word in sentiment_shifters_exceptions:
                                                regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                if not shifter_exception_match:
                                                    if boost_texture == 1:
                                                        polarity_pairs.append([aspect_name, -2])
                                                    else:
                                                        polarity_pairs.append([aspect_name, -1])
                                                    polarity_shift += 1
                                        elif shifter_match2:
                                            shifter_candidate2_index = candidate_index-2
                                            for shifter_exception_word in sentiment_shifters_exceptions:
                                                regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                if not shifter_exception_match:
                                                    if boost_texture == 1:
                                                        polarity_pairs.append([aspect_name, -2])
                                                    else:
                                                        polarity_pairs.append([aspect_name, -1])
                                                    polarity_shift += 1
                                        else:
                                            polarity_shift += 0

                                    if polarity_shift <= 0:
                                        if boost_texture == 1:
                                            polarity_pairs.append([aspect_name, 2])
                                        else:
                                            polarity_pairs.append([aspect_name, 1])
                            #  Negatives Lexikon:
                            if prior_positive_match == 0:
                                for neg_sent_word in lexicon_store_neg:
                                    regex_string = '^%s$' % str(neg_sent_word[0])
                                    word_match = re.search(regex_string, sentiment_candidate[0])
                                    if word_match:
                                        #print('texture-MATCH-after:', aspect_string, neg_sent_word[0], sentiment_candidate[0])
                                        polarity_shift = 0
                                        for shifter in sentiment_shifters:
                                            regex_string_shifter = '^%s$' % shifter
                                            shifter_candidate1 = sent[candidate_index-1]
                                            shifter_candidate2 = sent[candidate_index-2]
                                            shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                            shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])
                                            if shifter_match1:
                                                shifter_candidate1_index = candidate_index-1
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_texture == 1:
                                                            polarity_pairs.append([aspect_name, 2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, 1])
                                                        polarity_shift += 1
                                            elif shifter_match2:
                                                shifter_candidate2_index = candidate_index-2
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_texture == 1:
                                                            polarity_pairs.append([aspect_name, 2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, 1])
                                                        polarity_shift += 1
                                            else: polarity_shift += 0

                                        if polarity_shift <= 0:
                                            if boost_texture == 1:
                                                polarity_pairs.append([aspect_name, -2])
                                            else:
                                                polarity_pairs.append([aspect_name, -1])
                        except:
                            #print('index out of range')
                            pass
                        # Region vor Aspekt-Wort:
                        try:
                            if (index_i-region) >= 0:
                                sentiment_candidate = sent[index_i-region]
                                candidate_index = index_i-region
                                #  Positives Lexikon:
                                for pos_sent_word in lexicon_store_pos:
                                    regex_string = '^%s$' % str(pos_sent_word[0])
                                    word_match = re.search(regex_string, sentiment_candidate[0])
                                    if word_match:
                                        #print('texture-MATCH-before:', aspect_string, pos_sent_word[0], sentiment_candidate[0])
                                        polarity_shift = 0
                                        for shifter in sentiment_shifters:
                                            regex_string_shifter = '^%s$' % shifter
                                            shifter_candidate1 = sent[candidate_index-1]
                                            shifter_candidate2 = sent[candidate_index-2]
                                            shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                            shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])

                                            if shifter_match1:
                                                shifter_candidate1_index = candidate_index-1
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_texture == 1:
                                                            polarity_pairs.append([aspect_name, -2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, -1])
                                                        polarity_shift += 1
                                            elif shifter_match2:
                                                shifter_candidate2_index = candidate_index-2
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_texture == 1:
                                                            polarity_pairs.append([aspect_name, -2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, -1])
                                                        polarity_shift += 1
                                            else:
                                                polarity_shift += 0

                                        if polarity_shift <= 0:
                                            if boost_texture == 1:
                                                polarity_pairs.append([aspect_name, 2])
                                            else:
                                                polarity_pairs.append([aspect_name, 1])

                                #  Negatives Lexikon:
                                if prior_positive_match == 0:
                                    for neg_sent_word in lexicon_store_neg:
                                        regex_string = '^%s$' % str(neg_sent_word[0])
                                        word_match = re.search(regex_string, sentiment_candidate[0])
                                        if word_match:
                                            #print('texture-MATCH-before:', aspect_string, neg_sent_word[0], sentiment_candidate[0])
                                            polarity_shift = 0
                                            for shifter in sentiment_shifters:
                                                regex_string_shifter = '^%s$' % shifter
                                                shifter_candidate1 = sent[candidate_index-1]
                                                shifter_candidate2 = sent[candidate_index-2]
                                                shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                                shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])

                                                if shifter_match1:
                                                    shifter_candidate1_index = candidate_index-1
                                                    for shifter_exception_word in sentiment_shifters_exceptions:
                                                        regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                        shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                        shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                        if not shifter_exception_match:
                                                            if boost_texture == 1:
                                                                polarity_pairs.append([aspect_name, 2])
                                                            else:
                                                                polarity_pairs.append([aspect_name, 1])
                                                            polarity_shift += 1
                                                elif shifter_match2:
                                                    shifter_candidate2_index = candidate_index-2
                                                    for shifter_exception_word in sentiment_shifters_exceptions:
                                                        regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                        shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                        shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                        if not shifter_exception_match:
                                                            if boost_texture == 1:
                                                                polarity_pairs.append([aspect_name, 2])
                                                            else:
                                                                polarity_pairs.append([aspect_name, 1])
                                                            polarity_shift += 1
                                                else:
                                                    polarity_shift += 0

                                            if polarity_shift <= 0:
                                                if boost_texture == 1:
                                                    polarity_pairs.append([aspect_name, -2])
                                                else:
                                                    polarity_pairs.append([aspect_name, -1])
                        except:
                            #print('index out of range')
                            pass
            #  **** LOOKUP-TABLE ENGINE ****
            for aspect_string in lookup_table_engine_aspects:
                aspect_name = 'engine'
                regex_string = '^%s$' % aspect_string
                matches_aspect = re.search(regex_string, word[0])
                if matches_aspect:
                    #print('graphics match: ', aspect_string)
                     #  5 Woerter vorher und nachher pruefen auf sentiment words, dann Pairs generieren (f, o) ; durch Iterator feststellen, an welcher Position im Satz Aspekt-Wort auftritt -- Zugriff ueber sent[i];
                    #  Definition der Sentiment-Region:
                    sentiment_region = [1, 2, 3, 4, 5]
                    for region in sentiment_region:
                        # Region nach Aspekt-Wort:
                        try:
                            #print(sent[index_i])
                            sentiment_candidate = sent[index_i+region]
                            candidate_index = index_i+region
                            #print(sentiment_candidate)
                            #  Positives Lexikon:
                            for pos_sent_word in lexicon_store_pos:
                                regex_string = '^%s$' % str(pos_sent_word[0])
                                word_match = re.search(regex_string, sentiment_candidate[0])
                                if word_match:
                                    prior_positive_match = 1
                                    #print('engine-MATCH-after:', aspect_string, pos_sent_word[0], sentiment_candidate[0])
                                    polarity_shift = 0
                                    #  Vorherige zwei Woerter mit sentiment_shifters-List abgleichen. Wenn sentiment shifter auftaucht, dann Polaritaet umkehren:
                                    for shifter in sentiment_shifters:
                                        regex_string_shifter = '^%s$' % shifter
                                        shifter_candidate1 = sent[candidate_index-1]
                                        shifter_candidate2 = sent[candidate_index-2]
                                        shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                        shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])
                                        if shifter_match1:
                                            shifter_candidate1_index = candidate_index-1
                                            for shifter_exception_word in sentiment_shifters_exceptions:
                                                regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                if not shifter_exception_match:
                                                    if boost_engine == 1:
                                                        polarity_pairs.append([aspect_name, -2])
                                                    else:
                                                        polarity_pairs.append([aspect_name, -1])
                                                    polarity_shift += 1
                                        elif shifter_match2:
                                            shifter_candidate2_index = candidate_index-2
                                            for shifter_exception_word in sentiment_shifters_exceptions:
                                                regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                if not shifter_exception_match:
                                                    if boost_engine == 1:
                                                        polarity_pairs.append([aspect_name, -2])
                                                    else:
                                                        polarity_pairs.append([aspect_name, -1])
                                                    polarity_shift += 1
                                        else:
                                            polarity_shift += 0

                                    if polarity_shift <= 0:
                                        if boost_engine == 1:
                                            polarity_pairs.append([aspect_name, 2])
                                        else:
                                            polarity_pairs.append([aspect_name, 1])
                            #  Negatives Lexikon:
                            if prior_positive_match == 0:
                                for neg_sent_word in lexicon_store_neg:
                                    regex_string = '^%s$' % str(neg_sent_word[0])
                                    word_match = re.search(regex_string, sentiment_candidate[0])
                                    if word_match:
                                        #print('engine-MATCH-after:', aspect_string, neg_sent_word[0], sentiment_candidate[0])
                                        polarity_shift = 0
                                        for shifter in sentiment_shifters:
                                            regex_string_shifter = '^%s$' % shifter
                                            shifter_candidate1 = sent[candidate_index-1]
                                            shifter_candidate2 = sent[candidate_index-2]
                                            shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                            shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])
                                            if shifter_match1:
                                                shifter_candidate1_index = candidate_index-1
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_engine == 1:
                                                            polarity_pairs.append([aspect_name, 2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, 1])
                                                        polarity_shift += 1
                                            elif shifter_match2:
                                                shifter_candidate2_index = candidate_index-2
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_engine == 1:
                                                            polarity_pairs.append([aspect_name, 2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, 1])
                                                        polarity_shift += 1
                                            else: polarity_shift += 0

                                        if polarity_shift <= 0:
                                            if boost_engine == 1:
                                                polarity_pairs.append([aspect_name, -2])
                                            else:
                                                polarity_pairs.append([aspect_name, -1])
                        except:
                            #print('index out of range')
                            pass
                        # Region vor Aspekt-Wort:
                        try:
                            if (index_i-region) >= 0:
                                sentiment_candidate = sent[index_i-region]
                                candidate_index = index_i-region
                                #  Positives Lexikon:
                                for pos_sent_word in lexicon_store_pos:
                                    regex_string = '^%s$' % str(pos_sent_word[0])
                                    word_match = re.search(regex_string, sentiment_candidate[0])
                                    if word_match:
                                        #print('engine-MATCH-before:', aspect_string, pos_sent_word[0], sentiment_candidate[0])
                                        polarity_shift = 0
                                        for shifter in sentiment_shifters:
                                            regex_string_shifter = '^%s$' % shifter
                                            shifter_candidate1 = sent[candidate_index-1]
                                            shifter_candidate2 = sent[candidate_index-2]
                                            shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                            shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])

                                            if shifter_match1:
                                                shifter_candidate1_index = candidate_index-1
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_engine == 1:
                                                            polarity_pairs.append([aspect_name, -2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, -1])
                                                        polarity_shift += 1
                                            elif shifter_match2:
                                                shifter_candidate2_index = candidate_index-2
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_engine == 1:
                                                            polarity_pairs.append([aspect_name, -2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, -1])
                                                        polarity_shift += 1
                                            else:
                                                polarity_shift += 0

                                        if polarity_shift <= 0:
                                            if boost_engine == 1:
                                                polarity_pairs.append([aspect_name, 2])
                                            else:
                                                polarity_pairs.append([aspect_name, 1])

                                #  Negatives Lexikon:
                                if prior_positive_match == 0:
                                    for neg_sent_word in lexicon_store_neg:
                                        regex_string = '^%s$' % str(neg_sent_word[0])
                                        word_match = re.search(regex_string, sentiment_candidate[0])
                                        if word_match:
                                            #print('engine-MATCH-before:', aspect_string, neg_sent_word[0], sentiment_candidate[0])
                                            polarity_shift = 0
                                            for shifter in sentiment_shifters:
                                                regex_string_shifter = '^%s$' % shifter
                                                shifter_candidate1 = sent[candidate_index-1]
                                                shifter_candidate2 = sent[candidate_index-2]
                                                shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                                shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])

                                                if shifter_match1:
                                                    shifter_candidate1_index = candidate_index-1
                                                    for shifter_exception_word in sentiment_shifters_exceptions:
                                                        regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                        shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                        shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                        if not shifter_exception_match:
                                                            if boost_engine == 1:
                                                                polarity_pairs.append([aspect_name, 2])
                                                            else:
                                                                polarity_pairs.append([aspect_name, 1])
                                                            polarity_shift += 1
                                                elif shifter_match2:
                                                    shifter_candidate2_index = candidate_index-2
                                                    for shifter_exception_word in sentiment_shifters_exceptions:
                                                        regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                        shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                        shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                        if not shifter_exception_match:
                                                            if boost_engine == 1:
                                                                polarity_pairs.append([aspect_name, 2])
                                                            else:
                                                                polarity_pairs.append([aspect_name, 1])
                                                            polarity_shift += 1
                                                else:
                                                    polarity_shift += 0

                                            if polarity_shift <= 0:
                                                if boost_engine == 1:
                                                    polarity_pairs.append([aspect_name, -2])
                                                else:
                                                    polarity_pairs.append([aspect_name, -1])
                        except:
                            #print('index out of range')
                            pass
            #  **** LOOKUP-TABLE CODE ****
            for aspect_string in lookup_table_code_aspects:
                aspect_name = 'code'
                regex_string = '^%s$' % aspect_string
                matches_aspect = re.search(regex_string, word[0])
                if matches_aspect:
                    #print('graphics match: ', aspect_string)
                     #  5 Woerter vorher und nachher pruefen auf sentiment words, dann Pairs generieren (f, o) ; durch Iterator feststellen, an welcher Position im Satz Aspekt-Wort auftritt -- Zugriff ueber sent[i];
                    #  Definition der Sentiment-Region:
                    sentiment_region = [1, 2, 3, 4, 5]
                    for region in sentiment_region:
                        # Region nach Aspekt-Wort:
                        try:
                            #print(sent[index_i])
                            sentiment_candidate = sent[index_i+region]
                            candidate_index = index_i+region
                            #print(sentiment_candidate)
                            #  Positives Lexikon:
                            for pos_sent_word in lexicon_store_pos:
                                regex_string = '^%s$' % str(pos_sent_word[0])
                                word_match = re.search(regex_string, sentiment_candidate[0])
                                if word_match:
                                    prior_positive_match = 1
                                    #print('code-MATCH-after:', aspect_string, pos_sent_word[0], sentiment_candidate[0])
                                    polarity_shift = 0
                                    #  Vorherige zwei Woerter mit sentiment_shifters-List abgleichen. Wenn sentiment shifter auftaucht, dann Polaritaet umkehren:
                                    for shifter in sentiment_shifters:
                                        regex_string_shifter = '^%s$' % shifter
                                        shifter_candidate1 = sent[candidate_index-1]
                                        shifter_candidate2 = sent[candidate_index-2]
                                        shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                        shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])
                                        if shifter_match1:
                                            shifter_candidate1_index = candidate_index-1
                                            for shifter_exception_word in sentiment_shifters_exceptions:
                                                regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                if not shifter_exception_match:
                                                    if boost_code == 1:
                                                        polarity_pairs.append([aspect_name, -2])
                                                    else:
                                                        polarity_pairs.append([aspect_name, -1])
                                                    polarity_shift += 1
                                        elif shifter_match2:
                                            shifter_candidate2_index = candidate_index-2
                                            for shifter_exception_word in sentiment_shifters_exceptions:
                                                regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                if not shifter_exception_match:
                                                    if boost_code == 1:
                                                        polarity_pairs.append([aspect_name, -2])
                                                    else:
                                                        polarity_pairs.append([aspect_name, -1])
                                                    polarity_shift += 1
                                        else:
                                            polarity_shift += 0

                                    if polarity_shift <= 0:
                                        if boost_code == 1:
                                            polarity_pairs.append([aspect_name, 2])
                                        else:
                                            polarity_pairs.append([aspect_name, 1])
                            #  Negatives Lexikon:
                            if prior_positive_match == 0:
                                for neg_sent_word in lexicon_store_neg:
                                    regex_string = '^%s$' % str(neg_sent_word[0])
                                    word_match = re.search(regex_string, sentiment_candidate[0])
                                    if word_match:
                                        #print('code-MATCH-after:', aspect_string, neg_sent_word[0], sentiment_candidate[0])
                                        polarity_shift = 0
                                        for shifter in sentiment_shifters:
                                            regex_string_shifter = '^%s$' % shifter
                                            shifter_candidate1 = sent[candidate_index-1]
                                            shifter_candidate2 = sent[candidate_index-2]
                                            shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                            shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])
                                            if shifter_match1:
                                                shifter_candidate1_index = candidate_index-1
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_code == 1:
                                                            polarity_pairs.append([aspect_name, 2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, 1])
                                                        polarity_shift += 1
                                            elif shifter_match2:
                                                shifter_candidate2_index = candidate_index-2
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_code == 1:
                                                            polarity_pairs.append([aspect_name, 2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, 1])
                                                        polarity_shift += 1
                                            else: polarity_shift += 0

                                        if polarity_shift <= 0:
                                            if boost_code == 1:
                                                polarity_pairs.append([aspect_name, -2])
                                            else:
                                                polarity_pairs.append([aspect_name, -1])
                        except:
                            #print('index out of range')
                            pass
                        # Region vor Aspekt-Wort:
                        try:
                            if (index_i-region) >= 0:
                                sentiment_candidate = sent[index_i-region]
                                candidate_index = index_i-region
                                #  Positives Lexikon:
                                for pos_sent_word in lexicon_store_pos:
                                    regex_string = '^%s$' % str(pos_sent_word[0])
                                    word_match = re.search(regex_string, sentiment_candidate[0])
                                    if word_match:
                                        #print('code-MATCH-before:', aspect_string, pos_sent_word[0], sentiment_candidate[0])
                                        polarity_shift = 0
                                        for shifter in sentiment_shifters:
                                            regex_string_shifter = '^%s$' % shifter
                                            shifter_candidate1 = sent[candidate_index-1]
                                            shifter_candidate2 = sent[candidate_index-2]
                                            shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                            shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])

                                            if shifter_match1:
                                                shifter_candidate1_index = candidate_index-1
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_code == 1:
                                                            polarity_pairs.append([aspect_name, -2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, -1])
                                                        polarity_shift += 1
                                            elif shifter_match2:
                                                shifter_candidate2_index = candidate_index-2
                                                for shifter_exception_word in sentiment_shifters_exceptions:
                                                    regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                    shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                    shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                    if not shifter_exception_match:
                                                        if boost_code == 1:
                                                            polarity_pairs.append([aspect_name, -2])
                                                        else:
                                                            polarity_pairs.append([aspect_name, -1])
                                                        polarity_shift += 1
                                            else:
                                                polarity_shift += 0

                                        if polarity_shift <= 0:
                                            if boost_code == 1:
                                                polarity_pairs.append([aspect_name, 2])
                                            else:
                                                polarity_pairs.append([aspect_name, 1])

                                #  Negatives Lexikon:
                                if prior_positive_match == 0:
                                    for neg_sent_word in lexicon_store_neg:
                                        regex_string = '^%s$' % str(neg_sent_word[0])
                                        word_match = re.search(regex_string, sentiment_candidate[0])
                                        if word_match:
                                            #print('code-MATCH-before:', aspect_string, neg_sent_word[0], sentiment_candidate[0])
                                            polarity_shift = 0
                                            for shifter in sentiment_shifters:
                                                regex_string_shifter = '^%s$' % shifter
                                                shifter_candidate1 = sent[candidate_index-1]
                                                shifter_candidate2 = sent[candidate_index-2]
                                                shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                                shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])

                                                if shifter_match1:
                                                    shifter_candidate1_index = candidate_index-1
                                                    for shifter_exception_word in sentiment_shifters_exceptions:
                                                        regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                        shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                        shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                        if not shifter_exception_match:
                                                            if boost_code == 1:
                                                                polarity_pairs.append([aspect_name, 2])
                                                            else:
                                                                polarity_pairs.append([aspect_name, 1])
                                                            polarity_shift += 1
                                                elif shifter_match2:
                                                    shifter_candidate2_index = candidate_index-2
                                                    for shifter_exception_word in sentiment_shifters_exceptions:
                                                        regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                        shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                        shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                        if not shifter_exception_match:
                                                            if boost_code == 1:
                                                                polarity_pairs.append([aspect_name, 2])
                                                            else:
                                                                polarity_pairs.append([aspect_name, 1])
                                                            polarity_shift += 1
                                                else:
                                                    polarity_shift += 0

                                            if polarity_shift <= 0:
                                                if boost_code == 1:
                                                    polarity_pairs.append([aspect_name, -2])
                                                else:
                                                    polarity_pairs.append([aspect_name, -1])
                        except:
                            #print('index out of range')
                            pass
            #  **** LOOKUP TABLE GENERAL ASPECTS ****
            matching_aspect_found = 0
            for aspect_string in lookup_table_general_aspects:
                if matching_aspect_found == 0:
                    aspect_name = 'general'
                    regex_string = '^%s$' % aspect_string
                    matches_aspect = re.search(regex_string, word[0])
                    if matches_aspect:
                        #print('graphics match: ', aspect_string)
                         #  5 Woerter vorher und nachher pruefen auf sentiment words, dann Pairs generieren (f, o) ; durch Iterator feststellen, an welcher Position im Satz Aspekt-Wort auftritt -- Zugriff ueber sent[i];
                        #  Definition der Sentiment-Region:
                        matching_aspect_found = 1
                        sentiment_region_found = 0
                        sentiment_region = [1, 2, 3, 4, 5]
                        for region in sentiment_region:
                            if sentiment_region_found == 0:
                                # Region nach Aspekt-Wort:
                                try:
                                    #print(sent[index_i])
                                    sentiment_candidate = sent[index_i+region]
                                    candidate_index = index_i+region
                                    #print(sentiment_candidate)
                                    #  Positives Lexikon:
                                    for pos_sent_word in lexicon_store_pos:
                                        regex_string = '^%s$' % str(pos_sent_word[0])
                                        word_match = re.search(regex_string, sentiment_candidate[0])
                                        if word_match:
                                            sentiment_region_found = 1
                                            prior_positive_match = 1
                                            #print('general-MATCH-after:', aspect_string, pos_sent_word[0], sentiment_candidate[0])
                                            polarity_shift = 0
                                            #  Vorherige zwei Woerter mit sentiment_shifters-List abgleichen. Wenn sentiment shifter auftaucht, dann Polaritaet umkehren:
                                            for shifter in sentiment_shifters:
                                                regex_string_shifter = '^%s$' % shifter
                                                shifter_candidate1 = sent[candidate_index-1]
                                                shifter_candidate2 = sent[candidate_index-2]
                                                shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                                shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])
                                                if shifter_match1:
                                                    shifter_candidate1_index = candidate_index-1
                                                    for shifter_exception_word in sentiment_shifters_exceptions:
                                                        regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                        shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                        shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                        if not shifter_exception_match:
                                                            if boost_general == 1:
                                                                polarity_pairs.append([aspect_name, -2])
                                                            else:
                                                                polarity_pairs.append([aspect_name, -1])
                                                            polarity_shift += 1
                                                elif shifter_match2:
                                                    shifter_candidate2_index = candidate_index-2
                                                    for shifter_exception_word in sentiment_shifters_exceptions:
                                                        regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                        shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                        shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                        if not shifter_exception_match:
                                                            if boost_general == 1:
                                                                polarity_pairs.append([aspect_name, -2])
                                                            else:
                                                                polarity_pairs.append([aspect_name, -1])
                                                            polarity_shift += 1
                                                else:
                                                    polarity_shift += 0

                                            if polarity_shift <= 0:
                                                if boost_general == 1:
                                                    polarity_pairs.append([aspect_name, 2])
                                                else:
                                                    polarity_pairs.append([aspect_name, 1])
                                    #  Negatives Lexikon:
                                    if prior_positive_match == 0:
                                        for neg_sent_word in lexicon_store_neg:
                                            regex_string = '^%s$' % str(neg_sent_word[0])
                                            word_match = re.search(regex_string, sentiment_candidate[0])
                                            if word_match:
                                                sentiment_region_found = 1
                                                #print('general-MATCH-after:', aspect_string, neg_sent_word[0], sentiment_candidate[0])
                                                polarity_shift = 0
                                                for shifter in sentiment_shifters:
                                                    regex_string_shifter = '^%s$' % shifter
                                                    shifter_candidate1 = sent[candidate_index-1]
                                                    shifter_candidate2 = sent[candidate_index-2]
                                                    shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                                    shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])
                                                    if shifter_match1:
                                                        shifter_candidate1_index = candidate_index-1
                                                        for shifter_exception_word in sentiment_shifters_exceptions:
                                                            regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                            shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                            shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                            if not shifter_exception_match:
                                                                if boost_general == 1:
                                                                    polarity_pairs.append([aspect_name, 2])
                                                                else:
                                                                    polarity_pairs.append([aspect_name, 1])
                                                                polarity_shift += 1
                                                    elif shifter_match2:
                                                        shifter_candidate2_index = candidate_index-2
                                                        for shifter_exception_word in sentiment_shifters_exceptions:
                                                            regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                            shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                            shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                            if not shifter_exception_match:
                                                                if boost_general == 1:
                                                                    polarity_pairs.append([aspect_name, 2])
                                                                else:
                                                                    polarity_pairs.append([aspect_name, 1])
                                                                polarity_shift += 1
                                                    else:
                                                        polarity_shift += 0

                                                if polarity_shift <= 0:
                                                    if boost_general == 1:
                                                        polarity_pairs.append([aspect_name, -2])
                                                    else:
                                                        polarity_pairs.append([aspect_name, -1])
                                except:
                                    #print('index out of range')
                                    pass
                                # Region vor Aspekt-Wort:
                                try:
                                    if (index_i-region) >= 0:
                                        sentiment_candidate = sent[index_i-region]
                                        candidate_index = index_i-region
                                        #  Positives Lexikon:
                                        for pos_sent_word in lexicon_store_pos:
                                            regex_string = '^%s$' % str(pos_sent_word[0])
                                            word_match = re.search(regex_string, sentiment_candidate[0])
                                            if word_match:
                                                sentiment_region_found = 1
                                                #print('general-MATCH-before_pos:', aspect_string, pos_sent_word[0], sentiment_candidate[0])
                                                polarity_shift = 0
                                                for shifter in sentiment_shifters:
                                                    regex_string_shifter = '^%s$' % shifter
                                                    shifter_candidate1 = sent[candidate_index-1]
                                                    shifter_candidate2 = sent[candidate_index-2]
                                                    shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                                    shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])

                                                    if shifter_match1:
                                                        shifter_candidate1_index = candidate_index-1
                                                        for shifter_exception_word in sentiment_shifters_exceptions:
                                                            regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                            shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                            shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                            if not shifter_exception_match:
                                                                if boost_general == 1:
                                                                    polarity_pairs.append([aspect_name, -2])
                                                                else:
                                                                    polarity_pairs.append([aspect_name, -1])
                                                                polarity_shift += 1
                                                    elif shifter_match2:
                                                        shifter_candidate2_index = candidate_index-2
                                                        for shifter_exception_word in sentiment_shifters_exceptions:
                                                            regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                            shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                            shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                            if not shifter_exception_match:
                                                                if boost_general == 1:
                                                                    polarity_pairs.append([aspect_name, -2])
                                                                else:
                                                                    polarity_pairs.append([aspect_name, -1])
                                                                polarity_shift += 1
                                                    else:
                                                        polarity_shift += 0

                                                if polarity_shift <= 0:
                                                    if boost_general == 1:
                                                        polarity_pairs.append([aspect_name, 2])
                                                    else:
                                                        polarity_pairs.append([aspect_name, 1])

                                        #  Negatives Lexikon:
                                        if prior_positive_match == 0:
                                            polarity_shift = -1
                                            for neg_sent_word in lexicon_store_neg:
                                                regex_string = '^%s$' % str(neg_sent_word[0])
                                                word_match = re.search(regex_string, sentiment_candidate[0])
                                                if word_match:
                                                    sentiment_region_found = 1
                                                    #print('general-MATCH-before_neg:', aspect_string, neg_sent_word[0], sentiment_candidate[0])
                                                    polarity_shift = 0
                                                    for shifter in sentiment_shifters:
                                                        regex_string_shifter = '^%s$' % shifter
                                                        shifter_candidate1 = sent[candidate_index-1]
                                                        shifter_candidate2 = sent[candidate_index-2]
                                                        shifter_match1 = re.search(regex_string_shifter, shifter_candidate1[0])
                                                        shifter_match2 = re.search(regex_string_shifter, shifter_candidate2[0])

                                                        if shifter_match1:
                                                            #print 'DEBUG: shifter_match1'
                                                            shifter_candidate1_index = candidate_index-1
                                                            for shifter_exception_word in sentiment_shifters_exceptions:
                                                                regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                                shifter_exception_candidate = sent[shifter_candidate1_index+1]
                                                                shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                                if not shifter_exception_match:
                                                                    #print 'DEBUGDEBUG'
                                                                    #polarity_pairs.append([aspect_name, 1])
                                                                    polarity_shift += 1
                                                        elif shifter_match2:
                                                           # print 'DEBUG: shifter_match2'
                                                            shifter_candidate2_index = candidate_index-2
                                                            for shifter_exception_word in sentiment_shifters_exceptions:
                                                                regex_string_shifter_exception = '^%s$' % shifter_exception_word
                                                                shifter_exception_candidate = sent[shifter_candidate2_index+1]
                                                                shifter_exception_match = re.search(regex_string_shifter_exception, shifter_exception_candidate[0])
                                                                if not shifter_exception_match:
                                                                    #polarity_pairs.append([aspect_name, 1])
                                                                    polarity_shift += 1
                                                        else:
                                                            polarity_shift += 0

                                            if polarity_shift == 0:
                                                if boost_general == 1:
                                                    polarity_pairs.append([aspect_name, -2])
                                                else:
                                                    polarity_pairs.append([aspect_name, -1])
                                            elif polarity_shift >= 1:
                                                if boost_general == 1:
                                                    polarity_pairs.append([aspect_name, 2])
                                                else:
                                                    polarity_pairs.append([aspect_name, 1])
                                except:
                                    #print('index out of range')
                                    pass

            index_i += 1
            #print('INDEX_DEBUG:', index_i)
    print(polarity_pairs)
    for pair in polarity_pairs:
        quintuple = [meta_import[0], pair[0], pair[1], meta_import[1], meta_import[2]]
        #print(quintuple)
        if quintuple:
            all_comment_quintuples.append(quintuple)

    comment_i += 1
    print(all_comment_quintuples)
    if all_comment_quintuples:
        all_demo_quintuples.append(all_comment_quintuples)

for single_quintuple in all_demo_quintuples:
    print(single_quintuple)
