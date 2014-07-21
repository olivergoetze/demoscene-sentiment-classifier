import httplib2, os

home = "/Users/oliver/PycharmProjects/parse_comments"
i= 1

while i <= 61930:
    try:
        downloadurl = 'http://www.pouet.net/prod.php?which=%s' % (i)
        (response, content) = httplib2.Http().request(downloadurl, 'GET')
        print(response.status)

        filename = '%s.html' % (i)
        directory = '%s' % (i)
        os.chdir('demo')
        os.mkdir(directory)
        os.chdir(directory)
        print('Demo-ID', i, 'was successfully extracted from remote.')
        with open(filename, 'wb') as outputfile:
            outputfile.write(content)
    except:
        print('Demo-ID is not existing.')
        pass
    os.chdir(home)
    print(i)
    i += 1
