import httplib2, urllib, json, re, os, csv, codecs
expert_results = []
sourcedir = "/Users/oliver/PycharmProjects/parse_comments/output_rev1_sub_windows"
outputdir = "/Users/oliver/PycharmProjects/fetch_expert_status"
outputdir_single = "/Users/oliver/PycharmProjects/fetch_expert_status/expert_single"
outputfile_experts = 'expert_results.csv'

document_i = 1 # todo: reset to '1' after debugging

csv_store = []
while document_i <= 61930:  # wieder zurueckaendern auf 60000
    try:
        inputfile = '%s.csv' % (document_i)
        os.chdir(sourcedir)
        csvinput = codecs.open(inputfile, 'r', 'latin1')
        #num_lines = sum(1 for line in csvinput)
        #print(num_lines)
        reader = csv.reader(csvinput, delimiter=';')
        csv_row_count = 0
        for row in reader:
            csv_store.append(row)
    except:
        pass
    document_i += 1

#print(len(csv_store))
comment_i = 0
first_iteration = 1
comment_i_indicator = 1
os.chdir(outputdir_single)
while comment_i <= len(csv_store):  # wieder zurueckaendern auf 60000
    try:
        #comment_i_indicator = comment_i
        expert_candidate = csv_store[comment_i][3]
        source_document = csv_store[comment_i][2]
        demo_i = csv_store[comment_i][0]
        if first_iteration != 1:
            if demo_i != demo_i_indicator:
                outputfile_experts = '%s_expert.csv' % (demo_i_indicator)
                with open(outputfile_experts, 'w', newline='', encoding='latin1') as output_experts:
                    writer = csv.writer(output_experts, delimiter=';')
                    writer.writerows(expert_results)
                comment_i_indicator = 1
                expert_results = []
        first_iteration = 0
        demo_i_indicator = demo_i
        #expert_candidate = 'jb'
        expert_candidate = expert_candidate.replace(' ', '_').replace('\\', '_').replace('|', '_').replace('#', '_').replace('"', '_').replace('^', '_').replace('<', '_').replace('>', '_').replace('{', '_').replace('}', '_').replace('[', '_').replace(']', '_').replace('%', '_').replace('`', '_').replace('�', '_').lower()
        source_document = source_document.lower()


        query = 'PREFIX :<http://www.w3.org/2002/07/owl#> PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> PREFIX ns:<http://purl.org/marl/ns#> PREFIX psys:<http://proton.semanticweb.org/protonsys#> PREFIX erlangen-crm:<http://erlangen-crm.org/120111/> PREFIX owl:<http://www.w3.org/2002/07/owl#> PREFIX xsd:<http://www.w3.org/2001/XMLSchema#> PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX pext:<http://proton.semanticweb.org/protonext#> PREFIX demoage:<http://www.m-e-g-a.org/ontologies/demoage#> SELECT DISTINCT ?expert_evidence WHERE {demoage:%s rdf:type erlangen-crm:E21_Person . demoage:%s erlangen-crm:P11i_participated_in ?x . ?x rdf:type erlangen-crm:E65_Creation . ?x erlangen-crm:P14_carried_out_by demoage:%s . ?x erlangen-crm:P2_has_type ?y. ?y erlangen-crm:P3_has_note ?expert_evidence }' % (expert_candidate, expert_candidate, expert_candidate)
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
        #print(content)
        #print(type(content))
        try:
            results = json.loads(content)
        except:
            pass
        #print(results)

        i = 0
        expert_dict = []
        while i <= 6:
            expertstring = ''
            try:
                expertstring = results['results']['bindings'][i]['expert_evidence']['value']
            except:
                pass
            expert_dict.append(str(expertstring))
            i += 1

        #print(expertstring)
        #expert_match = re.search(r'_creation', expertstring)
        #if expert_match:
         #   expert_value = 'expert'
        #else:
         #   expert_value = ''
        print_i = 0

        while print_i <= i-1:
            #print(expert_dict[print_i])
            print_i += 1

        # extracting the types of participation and setting the lookup tables which are to be used
        use_lookup_table_graphics = 0  # default values
        use_lookup_table_music = 0
        use_lookup_table_tool = 0
        use_lookup_table_texture = 0
        use_lookup_table_engine = 0
        use_lookup_table_code = 0
        use_lookup_table_general = 0

        aspect_select_i = 0
        while aspect_select_i <= print_i-1:
            if expert_dict[aspect_select_i] == 'graphics creation':
                use_lookup_table_graphics = 1
            if expert_dict[aspect_select_i] == 'music creation':
                use_lookup_table_music = 1
            if expert_dict[aspect_select_i] == 'tool creation':
                use_lookup_table_tool = 1
            if expert_dict[aspect_select_i] == 'texturing creation':
                use_lookup_table_texture = 1
            if expert_dict[aspect_select_i] == 'engine creation':
                use_lookup_table_engine = 1
            if expert_dict[aspect_select_i] == 'code creation':
                use_lookup_table_code = 1
            if expert_dict[aspect_select_i] == 'demosceneart production creation':
                use_lookup_table_general = 1

            aspect_select_i += 1


        #*** defining the lookup tables for the aspects
        #lookup table for graphics aspect
        if use_lookup_table_graphics == 1:
            lookup_table_graphics_aspects = ['effects', 'gfx', 'visuals', 'visual', 'graphics', '3d', 'animation', 'interface', 'rendering', '2d', 'graphic', 'models', 'particles', 'sprites', 'design', 'effect', 'colors', 'colours', 'color', 'scenes', 'fonts', 'fx', 'objects', 'camera', 'menu', 'raytracing', 'pictures', 'transitions', 'presentation', 'vector']
        # lookup table for music aspect
        if use_lookup_table_music == 1:
            lookup_table_music_aspects = ['music', 'sound', 'audio', 'soundtrack', 'song', 'synth', 'musics', 'tune', 'tunes', 'sounds', 'mod', 'bass']
        # lookup table for tool aspect
        if use_lookup_table_tool == 1:
            lookup_table_tool_aspects = []
        # lookup table for texture aspect
        if use_lookup_table_texture == 1:
            lookup_table_texture_aspects = ['textures', 'texture']
        # lookup table for engine aspect
        if use_lookup_table_engine == 1:
            lookup_table_engine_aspects = ['engine', 'speed']
        # lookup table for code aspect
        if use_lookup_table_code == 1:
            lookup_table_code_aspects = ['code', 'filesize', 'coding', 'size', 'coded']
        # lookup table for general aspect
        if use_lookup_table_general == 1:
            lookup_table_general_aspects = ['production', 'demo', 'prod', 'result', 'execution', 'in general', 'executed', 'intro', 'intros', 'concept', 'piece', 'direction', 'theme']


        # *** Abgleich Kommentarinhalt und Ontologieinfo mittels Lookup Table
        #source_document = 'The gfx on this prod are rly n1. Also the soundtrack and the filesize are impressive.'
        matching_document_aspects = ''

        if use_lookup_table_graphics == 1:
            for aspect_string in lookup_table_graphics_aspects:
                matches_aspect = re.search(aspect_string, source_document) #% (aspect_string)
                if matches_aspect:
                    #print('graphics match: ', aspect_string)
                    matching_document_aspects += 'graphics,'

        if use_lookup_table_music == 1:
            for aspect_string in lookup_table_music_aspects:
                matches_aspect = re.search(aspect_string, source_document)
                if matches_aspect:
                    #print('music match: ', aspect_string)
                    matching_document_aspects += 'music,'

        if use_lookup_table_tool == 1:
            for aspect_string in lookup_table_tool_aspects:
                matches_aspect = re.search(aspect_string, source_document)
                if matches_aspect:
                    #print('tool match: ', aspect_string)
                    matching_document_aspects += 'tool,'

        if use_lookup_table_texture == 1:
            for aspect_string in lookup_table_texture_aspects:
                matches_aspect = re.search(aspect_string, source_document)
                if matches_aspect:
                    #print('texture match: ', aspect_string)
                    matching_document_aspects += 'texture,'

        if use_lookup_table_engine == 1:
            for aspect_string in lookup_table_engine_aspects:
                matches_aspect = re.search(aspect_string, source_document)
                if matches_aspect:
                    #print('engine match: ', aspect_string)
                    matching_document_aspects += 'engine,'

        if use_lookup_table_code == 1:
            for aspect_string in lookup_table_code_aspects:
                matches_aspect = re.search(aspect_string, source_document)
                if matches_aspect:
                    #print('code match: ', aspect_string)
                    matching_document_aspects += 'code,'

        if use_lookup_table_general == 1:
            for aspect_string in lookup_table_general_aspects:
                matches_aspect = re.search(aspect_string, source_document)
                if matches_aspect:
                    #print('code match: ', aspect_string)
                    matching_document_aspects += 'general,'

        expert_single = [demo_i, comment_i_indicator, expert_candidate, matching_document_aspects]
        #  expert_single als pickle speichern, Dateiname: %s_%s_expert
        #doc_output = '%s_%s_expert.csv' % (str(demo_i), str(comment_i_indicator))
        #with open(doc_output, 'w', newline='', encoding='latin1') as output_single_expert:
        """with open(doc_output, 'w', encoding='latin1') as output_single_expert:
            writer_single = csv.writer(output_single_expert, delimiter=';')
            writer_single.writerows(str(expert_single[3]))"""
        expert_results.append(expert_single)
        #for item in matching_document_aspects:  # Aspekte, in welchen dem Autor ein erhöhtes Gewicht zugewiesen werden sollte
         #   print(item)
        #print(expert_results)
        print(expert_single)
        comment_i_indicator += 1


    except:
        #print('error:', comment_i)
        pass

    comment_i += 1

#os.chdir(outputdir)
#with open(outputfile_experts, 'w', newline='', #encoding='latin1') as output_experts:
  #  writer = csv.writer(output_experts, delimiter=';')
   # writer.writerows(expert_results)
