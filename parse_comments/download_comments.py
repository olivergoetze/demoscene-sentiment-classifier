import httplib2, os

home = "/Users/oliver/PycharmProjects/parse_comments"
i= 10001

while i <= 61930:
    try:
        downloadurl = 'http://www.pouet.net/prod.php?which=%s' % (i)
        (response, content) = httplib2.Http().request(downloadurl, 'GET')
        print(response.status)

        filename = '%s.html' % (i)
        directory = '%s' % (i)
        os.mkdir(directory)
        os.chdir(directory)
        with open(filename, 'wb') as outputfile:
            outputfile.write(content)
    except:
        print('error')
        pass
    os.chdir(home)
    print(i)
    i += 1