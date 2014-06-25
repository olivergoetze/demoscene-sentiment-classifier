# Um vocabulary_select zu generieren, extract_aspects.py verwenden
import httplib2, json, codecs, re, csv
from wordnik import *

vocabulary_select = ['.', ',', ':', "'", ')', '"', 'nice', '...', 's', 'music', '?', '(', 'demo', 't', 'good', 'like', 'one', 'great', 'it', 'really', 'cool', '=', 'i', 'thumb', 'http', 'well', 'd', 'time', 'prod', 'still', 'effects', 'stuff', 'intro', 'work', 'bit', 'ok', 'don', 'much', 'see', 'better', 'love', '>', 'first', 'www', 'bad', 'demos', 'even', 'would', 'best', 'scene', 'quite', 'awesome', 'though', 'design', 'also', 'watch', 'think', '1', 'could', 'm', 'said', 'get', 'looks', '3', 'pretty', 'boring', 'style', 'tune', 'something', 've', 'way', 'effect', 'liked', 'yes', 'code', 'made', 'make', 'part', 'lt', 'didn', 'know', 'yeah', 'done', 'gfx', 'version', '3d', 'video', 'com', 'that', 'youtube', 'soundtrack', 'visuals', 'amp', 'little', 'net', 'p', 'pouet', 'ever', 'please', 'seen', 'oh', 'thing', 'lot', 'rulez', 'graphics', 'nothing', 'new', 'old', 'back', 'screen', 'amiga', 'idea', 'doesn', 'maybe', 'party', 'anyway', 'sound', 'wow', '4k', 'can', '2', 'look', 'people', 'got', 'o', 'actually', 'php', 'say', 'ugly', 'guys', 'long', 'excellent', 'funny', 'big', 'colors', 'gt', 'production', 'sorry', 'thumbs', 'use', 'scenes', 'next', 'interesting', 'you', 'compo', 'thanks', 'sucks', 'run', 'rocks', 'real', 'never', ']', 'oi', 'slow', 'impressive', 'fun', 'sure', 'end', 'always', 'amazing', 'shit', 'go', 'll', 'want', 'sux', 'remember', 'many', 'v', 'usa', 'another', 'rules', 'short', 'release', '0', 'which', 'especially', 'game', 'simple', 'original', 'here', 'org', 'right', 'link', 'works', 'lol', 'seems', 'parts', 'years', 'and', 'try', 'last', 'indeed', 'enough', 'mirrorman', 'quality', 'used', 'beautiful', 'logo', 'there', 'classic', 'need', 'pc', 'guess', 'btw', 'art', 'damn', 'fucking', 'cute', 'least', 'keep', 'kind', 'font', 'makes', 'since', '@', 'without', 'die', 'saw', 'different', 'file', 're', 'rest', 'must', 'looking', 'tunes', '^', 'text', 'totally', 'screenshot', 'overall', 'yet', 'download', '[', 'final', 'probably', 'give', 'things', 'second', 'prods', 'crap', 'already', 'zip', 'rather', 'show', 'far', 'hard', 'fast', 'c64', 'times', 'everything', 'loved', 'fine', 'dont', 'this', 'lovely', 'sweet', 'fuck', 'place', 'thought', 'watching', 'year', 'released', 'find', '64k', 'the', 'special', 'whole', 'feel', 'read', 'hell', 'job', 'kinda', 'isn', 'ass', 'neat', 'concept', 'won', '4', 'using', 'runs', 'around', 'put', 'anything', 'scroll', 'every', 'smooth', 'scroller', 'found', 'piggy', 'hope', 'but', 'alles', 'uber', 'perfect', 'course', 'come', 'ftp', 'somehow', 'although', 'okay', 'simply', 'going', 'wasn', 'almost', 'niederland', 'point', 'sounds', 'atmosphere', 'wrong', 'name', 'track', 'start', 'watched', 'intros', 'two', 'strange', 'demoscene', 'worth', 'sync', 'ideas', 'windows', 'me', 'either', 'machine', 'fantastic', 'looked', 'enjoyed', 'hey', 'group', 'content', 'comment', 'else', 'might', 'hmm', 'feeling', 'however', 'stylish', 'someone', 'top', 'let', 'de', 'making', 'agree', 'less', 'wtf', 'days', 'atari', 'weird', 'respect', 'decent', 'us', 'enjoyable', 'small', 'forgot', 'finally', 'favourite', 'absolutely', 'man', 'yep', 'c', 'textures', 'working', 'instead', 'definitely', 'tho', 'happy', 'brilliant', '5', 'disk', 'taste', 'understand', 'together', 'take', 'black', 'no', 'fx', 'background', 'needs', 'day', 'running', 'coding', 'usual', 'all', 'mean', 'hardware', 'fit', 'platform', 'true', 'beginning', 'hehe', '8', 'u', 'comments', 'animation', 'size', 'coder', 'lame', 'oldschool', 'colours', 'haha', 'except', 'what', 'interface', 'reason', 'cracktro', 'fact', 'so', 'cubes', 'picture', 'perhaps', 'a', '10', 'pure', 'add', 'color', 'very', 'fresh', 'effort', 'img', 'rendering', 'anyone', 'objects', 'port', 'ripped', 'stop', 'haven', 'vote', 'lots', 'problem', 'full', 'imho', 'gets', 'piece', 'reminds', 'mood', 'thank', 'wait', 'tunnel', 'b', 'too', 'logotype', 'superb', 'greetings', 'we', 'otherwise', 'e', 'world', 'computer', 'horrible', 'enjoy', 'engine', 'productions', 'ago', 'again', 'didnt', 'story', 'solid', 'st', 'getting', 'etc', 'direction', 'up', 'visual', 'piggie', 'missing', 'mode', 'n', 'noise', 'camera', 'not', 'others', 'play', 'mind', 'hate', 'check', 'exactly', 'win', 'issue', 'bytes', 'cube', 'rule', 'later', 'fixed', 'average', 'seem', 'nicely', 'fix', 'cup', 'ati', 'goes', 'clean', 'wish', 'high', 'or', 'everyone', 'may', 'possible', 'wonder', 'favorite', 'song', 'technically', 'change', 'oldskool', 'crashes', 'exe', 'massive', 'left', 'believe', 'invitation', 'is', 'software', 'worked', 'ones', 'tried', 'free', 'rotating', 'feels', 'suck', 'seriously', 'deserves', 'system', 'yay', 'thats', 'title', 'called', 'xp', 'fr', 'synth', 'tea', 'fits', 'now', 'added', 'error', 'god', 'heard', 'files', 'wonderful', 'k', 'sometimes', 'asd', 'today', '2d', 'started', 'plasma', '256b', 'blue', 'groups', 'help', 'annoying', 'soon', 'waiting', 'life', 'space', 'couldn', 'forward', 'white', '1k', 'flow', 'words', 'linux', 'wild', 'eyes', '`', 'future', 'plus', 'able', 'wanted', 'stupid', 'menu', 'card', 'source', 'ah', 'credits', 'releases', 'away', 'lack', 'opinion', 'moving', 'gif', '0b11111111', 'doesnt', 'seeing', 'texture', 'dead', 'expected', 'whatever', 'x', 'super', 'call', 'balls', 'coded', 'live', 'ps', 'message', 'minutes', 'support', 'completely', 'winner', 'felt', 'perfectly', 'crazy', 'graphic', 'random', 'realtime', 'imo', 'red', 'pub', 'rock', 'omg', 'came', 'entertaining', 'available', 'low', 'somewhat', 'bits', '2nd', 'half', 'kicks', 'meh', '1st', 'says', 'joke', 'shame', 'trying', 'poor', 'side', 'they', 'guy', '100', 'pictures', 'ran', '_', 'tell', 'broken', 'mod', 'hm', 'articles', 'cant', 'main', 'prefer', 'missed', 'transitions', 'incredible', 'hear', 'kick', 'mostly', 'im', 'care', 'crappy', 'scheisse', '20', 'emulator', 'word', 'home', 'serious', 'theme', 'presentation', 'o_o', 'speed', 'proper', 'object', 'mag', 'gargaj', 'sense', 'shown', 'bug', 'loading', 'flash', 'url', 'behind', 'feature', 'shows', 'tv', 'expect', 'ace', 'seconds', 'wouldn', 'crash', 'in', 'previous', 'coming', 'f', 'inside', 'dark', 'comes', 'due', 'forget', 'pig', 'audio', 'radeon', 'sort', 'line', 'lacks', 'huge', 'example', 'player', 'resolution', 'lines', 'teh', 'cpc', 'mp3', 'alone', 'deserved', 'anyways', 'blur', 'couple', 'parties', 'thx', '6', 'light', 'taat', 'case', 'easy', 'r', 'thumbed', 'post', 'technical', 'basic', 'problems', 'impressed', 'dos', 'several', '7', 'models', 'kewl', 'mfx', 'playing', 'nfo', 'supposed', 'congrats', 'bigscreen', 'experience', 'memories', 'unfortunately', 'more', 'miss', 'stunning', 'face', 'fan', 'higher', 'tool', 'matter', 'killer', 'on', 'extremely', 'image', 'anymore', 'ram', 'hand', 'standard', 'fullscreen', 'took', 'lost', 'somewhere', 'screens', 'write', 'bass', 'went', 'single', 'set', 'masterpiece', 'optimus', 'crashed', 'heh', 'avi', 'level', 'la', 'water', 'sine', 'listen', 'sceners', 'similar', 'l', 'pack', 'dull', 'particles', 'designed', 'memory', 'awful', 'dosbox', 'english', 'id', 'sprites', 'bugs', 'repetitive', 'holy', 'rocked', 'trip', 'usually', 'unfinished', 'needed', 'early', 'amount', 'head', 'fonts', 'product', 'late', 'cpu', 'sad', 'move', 'w', 'magic', 'worse', 'da', 'dll', 'green', 'info', 'en', 'dunno', 'obviously', 'rip', 'gives', 'g', 'games', 'polished', 'aswell', 'hours', 'be', 'beat', 'gotta', 'cause', 'remix', 'asm', 'entry', 'apart', 'musicdisk', 'hd', 'weak', 'result', 'outstanding', 'kb', 'assembly', 'gave', 'unique', 'for', 'releasing', 'keops', 'seemed', 'kickass', 'managed', 'drivers', 'plain', 'slideshow', 'reading', 'bp', 'longer', 'dots', 'faster', 'spirit', 'create', 'nvidia', 'chiptune', 'hmmm', 'coders', 'laugh', 'meant', 'as', 'fake', 'falcon', 'hidden', 'plz', 'tracks', 'execution', 'extra', 'fire', 'static', 'compared', 'certainly', 'ending', 'nah', 'cannot', 'dig', 'em', 'latest', 'preacher', 'forever', 'gonna', 'musics', 'breakpoint', 'features', 'personal', 'close', 'aren', 'view', 'competition', 'means', 'vector', 'stingray', 'stars', 'diskmag', 'likes', 'ask', 'contains', 'mac', 'press', 'chip', 'typical', 'type', 'thumbing', 'win32', 'farbrausch', 'funky', 'scrolling', 'touch', 'okish', 'stream', 'html', 'correct', 'often', 'haujobb', 'ste', 'general', 'esc', 'pixel', 'sick', 'mad', 'french', 'samples', 'surely', 'played', 'evil', 'learn', 'note', 'power', 'finished', 'songs', 'girl', 'at', 'thanx', 'techno', 'past', '16', 'fuckings', 'considering', 'empty', 'alot', 'bouncing', 'movement', 'beauty', 'cheesy', 'starts', 'fps', 'points', '9', 'details', 'three', 'motion', 'nowadays', 'capture', 'action', 'rox', 'saying', 'thinking', 'nevertheless', 'takes', 'then', 'actual', 'data', 'epic', 'megademo', 'executed', 'pic', 'raster', 'wanna', 'smash', 'tbl', 'sample', 'surprise', 'talking', 'spectrum', 'potential', 'fucked', 'modern', 'gba', 'terrible', 'copy', 'load', 'cheap', 'hugi', 'moment', 'page', 'everybody', 'worst', 'buggy', 'cd', 'down', 'total', 'choice', 'welcome', 'if', 'invitro', 'bored', 'middle', 'box']

vocab_test = ['lying']

results = []
# vocabulary_select-array iterativ verarbeiten, dabei POS-Tags per API beziehen
apiUrl = 'http://api.wordnik.com/v4'  # Wordnik
apiKey = 'b7d8663cecaa07babf3010338ab0a1fb84c7995785537c213'
client = swagger.ApiClient(apiKey, apiUrl)
i = 1
for vocab in vocabulary_select:
    try:
        wordApi = WordApi.WordApi(client)
        example = wordApi.getDefinitions(vocab, sourceDictionaries='ahd-legacy', limit=200)
        #correctionstring_wordnik = example.partOfSpeech
        word_result = [i, vocab, example[0].partOfSpeech, example[0].text]
        print word_result
        results.append(word_result)
    except:
        print 'manuell bestimmen:', i,  vocab
        results.append(['manuell bestimmen:', i, vocab])
    #print(i)
    i += 1

"""outputfile_pos_tags = 'pos_tags.csv'
with codecs.open(outputfile_pos_tags, 'w', encoding='latin1') as output_pos:
    writer = csv.writer(output_pos, delimiter=';')
    writer.writerows(results)"""