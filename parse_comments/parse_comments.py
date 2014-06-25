from bs4 import BeautifulSoup

import os, codecs, re, csv, httplib2, urllib, json

home = "/Users/oliver/PycharmProjects/parse_comments"
outputdir = "/Users/oliver/PycharmProjects/parse_comments/output_rev1_sub_windows"
outputfile_experts = 'experts.csv'
i = 1
piggiecount = 0
commentcount = 0
limit_platform = 1
limit_platform_regex = 'platform os_windows'

while i <= 61930:
    #try:
    inputfile = '%s.html' % (i)
    outputfile = '%s.csv' % (i)
    directory = '%s' % (i)
    os.chdir(directory)

    inputcontent = codecs.open(inputfile, 'r', 'latin1')
    all_comments = []
    expert_comments = []
    # here goes the parser
    soup = BeautifulSoup(inputcontent)
    #print(soup.original_encoding)
    titlesoup = soup.find("span", {"id": "title"})
    stattablesoup = soup.find("table", {"id": "stattable"})
    try:
        platformsoup = stattablesoup.find("span", {"class": limit_platform_regex})
    except:
        platformsoup = None
    try:
        titlestr = titlesoup.big.string
    except:
        print('Demo-ID nicht vorhanden')
        pass
    for tag in soup.find_all(id=re.compile("^c\d"), class_=re.compile("cite-")):
        tagstring = str(tag)
        tagstring = tagstring.replace('\n', ' ').replace('\r', '').replace('<br/>', '')
        #print(tagstring)
        tagsoup = BeautifulSoup(tagstring)
        #for child in tagsoup.descendants:
         #   print(child)
        contentsoup = tagsoup.find("div", {"class": "content"})
        contentsoup = str(contentsoup)
        contentsoup = contentsoup.replace('<a href=', '').replace('</a>', '').replace(';', '.')
        contentsoup_notags = BeautifulSoup(contentsoup)
        footsoup = tagsoup.find("div", {"class": "foot"})
        usersoup = footsoup.find("a", {"class": "user"})
        datesoup = footsoup.find("a", {"href": re.compile("prod.php\?post")})
        ratingsoup = footsoup.find("span", {"class": re.compile("vote")})
        heartsoup = footsoup.find("span", {"class": re.compile("cdc")})
        authorsoup = tagsoup.find("div", {"class": re.compile("author")})

        # RULEZ noch parsen

        contentstr = contentsoup_notags.string
        userstr = usersoup.string
        datestr = datesoup.string
        if ratingsoup is not None:
            ratingstr = ratingsoup.string
        else:
            ratingstr = ''
        if heartsoup is not None:
            heartstr = heartsoup.string
        else:
            heartstr = ''
        if authorsoup is not None:
            authorstr = 1
            piggiecount += 1
        else:
            authorstr = ''
        print(contentstr)
        print(userstr, ', ')
        print(datestr, ', ')
        print(ratingstr)
        print(heartstr)
        print(authorstr)
        if titlesoup is not None:
            print(titlestr, '\n')
        else:
            titlestr = ''
        expert_value = ''
        """if authorstr != 1:
            try:
                expert_candidate = userstr.lower()
                query = 'PREFIX :<http://www.w3.org/2002/07/owl#> PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> PREFIX ns:<http://purl.org/marl/ns#> PREFIX psys:<http://proton.semanticweb.org/protonsys#> PREFIX erlangen-crm:<http://erlangen-crm.org/120111/> PREFIX owl:<http://www.w3.org/2002/07/owl#> PREFIX xsd:<http://www.w3.org/2001/XMLSchema#> PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX pext:<http://proton.semanticweb.org/protonext#> PREFIX demoage:<http://www.m-e-g-a.org/ontologies/demoage#> SELECT DISTINCT ?expert_evidence WHERE {demoage:%s rdf:type erlangen-crm:E21_Person . demoage:%s erlangen-crm:P11i_participated_in ?expert_evidence }' % (expert_candidate, expert_candidate)
                repository = 'demoage'
                endpoint = 'http://localhost:8080/openrdf-sesame/repositories/%s' % (repository)

                print("POSTing SPARQL query")
                params = { 'query': query}
                headers = {
                    'content-type': 'application/x-www-form-urlencoded',
                    'accept': 'application/sparql-results+json'
                }
                (response, content) = httplib2.Http().request(endpoint, 'POST', urllib.parse.urlencode(params), headers=headers)
                print("Sesame Response", response.status)
                content = content.decode('utf-8')
                results = json.loads(content)

                expertstring = results['results']['bindings'][0]['expert_evidence']['value']
                #print(expertstring)
                expert_match = re.search(r'_creation', expertstring)
                if expert_match:
                    expert_value = 'expert'
                else:
                    expert_value = ''
                print(expert_value)
            except:
                expert_value = ''
                pass"""


        single_comment = [str(i), titlestr, contentstr, userstr, datestr, ratingstr, heartstr, authorstr, expert_value]
        if titlesoup is not None and authorstr != 1:
            all_comments.append(single_comment)
            commentcount += 1
            if expert_value == 'expert':
                expert_comments.append(single_comment)


        #for tag in tagsoup.find_all(class_=re.compile("content")):
         #   print(tag.string)




    # output: extracted comment including metadata; als CSV, sep=';'
    os.chdir(outputdir)
    if titlesoup is not None and platformsoup is not None:
        with open(outputfile, 'w', newline='', encoding='latin1') as output:
            writer = csv.writer(output, delimiter=';')
            writer.writerows(all_comments)

    os.chdir(home)
    #print('***', i, 'Demos verarbeitet')
    #print('***', commentcount, 'Comments extrahiert')
    #print('***', 'Entfernte Piggies:', piggiecount)
    i += 1

with open(outputfile_experts, 'w', newline='', encoding='latin1') as output_experts:
    writer_experts = csv.writer(output_experts, delimiter=';')
    writer_experts.writerows(expert_comments)

print('***', i, 'Demos verarbeitet')
print('***', commentcount, 'Comments extrahiert')
print('***', 'Entfernte Piggies:', piggiecount)


