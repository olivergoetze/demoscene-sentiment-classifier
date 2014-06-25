import os, codecs, re, csv

home = "/Users/oliver/PycharmProjects/parse_comments/output_rev1_sub_windows"
i= 1
os.chdir(home)
sum_num_lines = 0

while i <= 61930:
    try:
        inputfile = '%s.csv' % (i)
        csvinput = codecs.open(inputfile, 'r', 'latin1')
        num_lines = sum(1 for line in csvinput)
        print(i, ':', num_lines)
        sum_num_lines += num_lines
    except:
        pass
    i += 1

print('Gesamtzahl der Kommentare:', sum_num_lines)

