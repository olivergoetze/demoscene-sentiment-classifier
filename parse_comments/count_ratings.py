import os, codecs, re, csv

home = "/Users/oliver/PycharmProjects/parse_comments/output_rev1_sub_windows"
outputdir = "/Users/oliver/PycharmProjects/parse_comments/output_stats"
outputfile = 'ratings_rev1_sub_windows.csv'
i= 1
os.chdir(home)
sum_num_lines = 0
rating_all = []
while i <= 61930:
    try:
        sum_positives = 0
        sum_negatives = 0
        sum_neutral = 0
        inputfile = '%s.csv' % (i)
        csvinput = codecs.open(inputfile, 'r', 'latin1')
        reader = csv.reader(csvinput, delimiter=';')
        csv_store = []
        ratings_store = []
        count = 0
        for row in reader:
            csv_store.append(row)
            demo_id = csv_store[count][0]
            first_comment_date = csv_store[0][4]
            if csv_store[count][5] == 'rulez':
                sum_positives += 1
            elif csv_store[count][5] == 'sucks':
                sum_negatives += 1
            else:
                sum_neutral += 1
                pass
            count += 1
        print(sum_positives)
        print(sum_negatives)
        print(sum_neutral)
        rating_demo = [demo_id, first_comment_date, sum_positives, sum_negatives, sum_neutral]
        rating_all.append(rating_demo)

    except:
        pass
    i += 1

os.chdir(outputdir)
with open(outputfile, 'w', newline='', encoding='latin1') as output:
    writer = csv.writer(output, delimiter=';')
    writer.writerows(rating_all)