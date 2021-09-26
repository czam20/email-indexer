from pathlib import Path
import os
import re

INDEX = {}
STOP_WORDS = ["able","about","above","abroad","according","accordingly","across","actually","adj","after","afterwards","again","against","ago","ahead","ain't","all","allow","allows","almost","alone","along","alongside","already","also","although","always","am","amid","amidst","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","a's","aside","ask","asking","associated","at","available","away","awfully","back","backward","backwards","be","became","because","become","becomes","becoming","been","before","beforehand","begin","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","came","can","cannot","cant","can't","caption","cause","causes","certain","certainly","changes","clearly","c'mon","co","co.","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't","course","c's","currently","dare","daren't","definitely","described","despite","did","didn't","different","directly","do","does","doesn't","doing","done","don't","down","downwards","during","each","edu","eg","eight","eighty","either","else","elsewhere","end","ending","enough","entirely","especially","et","etc","even","ever","evermore","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","fairly","far","farther","few","fewer","fifth","first","five","followed","following","follows","for","forever","former","formerly","forth","forward","found","four","from","further","furthermore","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","had","hadn't","half","happens","hardly","has","hasn't","have","haven't","having","he","he'd","he'll","hello","help","hence","her","here","hereafter","hereby","herein","here's","hereupon","hers","herself","he's","hi","him","himself","his","hither","hopefully","how","howbeit","however","hundred","i'd","ie","if","ignored","i'll","i'm","immediate","in","inasmuch","inc","inc.","indeed","indicate","indicated","indicates","inner","inside","insofar","instead","into","inward","is","isn't","it","it'd","it'll","its","it's","itself","i've","just","k","keep","keeps","kept","know","known","knows","last","lately","later","latter","latterly","least","less","lest","let","let's","like","liked","likely","likewise","little","look","looking","looks","low","lower","ltd","made","mainly","make","makes","many","may","maybe","mayn't","mac","tgts","me","mean","meantime","meanwhile","merely","might","mightn't","mine","minus","miss","more","moreover","most","mostly","mr","mrs","much","must","mustn't","my","myself","name","namely","nd","near","nearly","necessary","need","needn't","needs","neither","never","neverf","neverless","nevertheless","new","next","nine","ninety","no","nobody","non","none","nonetheless","noone","no-one","nor","normally","not","nothing","notwithstanding","novel","now","nowhere","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","one's","only","onto","opposite","or","other","others","otherwise","ought","oughtn't","our","ours","ourselves","out","os","outside","over","overall","own","particular","particularly","past","per","perhaps","placed","please","plus","possible","presumably","probably","provided","provides","que","quite","qv","rather","rd","re","really","reasonably","recent","recently","regarding","regardless","regards","relatively","respectively","right","round","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","shan't","she","she'd","she'll","she's","should","shouldn't","since","six","so","some","somebody","someday","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","take","taken","taking","tell","tends","th","than","thank","thanks","thanx","that","that'll","thats","that's","that've","the","their","theirs","them","themselves","then","thence","there","thereafter","thereby","there'd","therefore","therein","there'll","there're","theres","there's","thereupon","there've","these","they","they'd","they'll","they're","they've","thing","things","think","third","thirty","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","till","to","together","too","took","toward","towards","tried","tries","truly","try","trying","t's","twice","two","un","under","underneath","undoing","unfortunately","unless","unlike","unlikely","until","unto","up","upon","upwards","us","use","used","useful","uses","using","usually","v","value","various","versus","very","via","viz","vs","want","wants","was","wasn't","way","we","we'd","welcome","well","we'll","went","were","we're","weren't","we've","what","whatever","what'll","what's","what've","when","whence","whenever","where","whereafter","whereas","whereby","wherein","where's","whereupon","wherever","whether","which","whichever","while","whilst","whither","who","who'd","whoever","whole","who'll","whom","whomever","who's","whose","why","will","willing","wish","with","within","without","wonder","won't","would","wouldn't","yes","yet","you","you'd","you'll","your","you're","yours","yourself","yourselves","you've","zero","a","how's","i","when's","why's","b","c","d","e","f","g","h","j","l","m","n","o","p","q","r","s","t","u","uucp","w","x","y","z","I","www","amount","bill","bottom","call","computer","con","couldnt","cry","de","describe","detail","due","eleven","empty","fifteen","fifty","fill","find","fire","forty","front","full","give","hasnt","herse","himse","interest","itse”","mill","move","myse”","part","put","show","side","sincere","sixty","system","ten","thick","thin","top","twelve","twenty","abst","accordance","act","added","adopted","affected","affecting","affects","ah","announce","anymore","apparently","approximately","aren","arent","arise","auth","beginning","beginnings","begins","biol","briefly","ca","date","ed","effect","et-al","ff","fix","gave","giving","heres","hes","hid","home","id","im","immediately","importance","important","index","information","invention","itd","keys","kg","km","largely","lets","line","'ll","means","mg","million","ml","mug","na","nay","necessarily","nos","noted","obtain","obtained","omitted","ord","owing","page","pages","poorly","possibly","potentially","pp","predominantly","present","previously","primarily","promptly","proud","quickly","ran","readily","ref","refs","related","research","resulted","resulting","results","run","sec","section","shed","shes","showed","shown","showns","shows","significant","significantly","similar","similarly","slightly","somethan","specifically","state","states","stop","strongly","substantially","successfully","sufficiently","suggest","thered","thereof","therere","thereto","theyd","theyre","thou","thoughh","thousand","throug","til","tip","ts","ups","usefully","usefulness","'ve","vol","vols","wed","whats","wheres","whim","whod","whos","widely","words","world","youd","youre"]

def is_stopword(word):
    """Check if a word is a stopword"""
    if word in STOP_WORDS:
        return True
    return False


def obtain_emails(line):
    """Get emails in text"""
    email_patron = re.compile('[A-Za-z0-9]{2,}@[a-z]{2,}\.[a-z]{2,}')
    emails = email_patron.findall(line)
    return emails


def obtain_words(line):
    """Get words in text excluding the stop words"""
    words_patron = re.compile('[a-zA-Z]{2,}')
    words = words_patron.findall(line)
    for word in words:
        if word in STOP_WORDS:
            words.remove(word)
    return words


def open_dir(route):
    """Get the files in the path"""
    if os.path.exists(route):
        if route.is_file(): #Checks if it's a file and reads it
            read_words(route)
            return
        else: #If it is a directory, it goes through it and recursively calls the function
            for folder in route.iterdir():
                open_dir(folder)
    else:
        raise Exception("Cannot find the path specified")


def read_words(route):
    """Get the keywords for the indexer"""
    text = []
    try:
        with open(route, 'r') as file:
            #All lines from the file are read and stored in a list
            text = file.readlines()
            file.close()
    except:
        return

    for line in text:
        line = line.lower()

        emails = obtain_emails(line)
        for email in emails:
            if email:
                create_indexes(email, route)

        words = obtain_words(line)
        for word in words:
            if word:
                create_indexes(word, route)


def create_indexes(key, route):
    """Create the indexes dictionary"""
    if not is_stopword(key): #check if not a stopword
        if not key in INDEX:
            INDEX[key] = []
        if not route in INDEX[key]:
            INDEX[key].append(route)


def indexer(route):
    """Generate the indexes"""
    try:
        open_dir(route)
    except Exception as e:
        raise e

    #create the indexer.txt file
    with open('indexer.txt', 'w') as file:
        for key in INDEX.keys():
            file.write(key+'->')
            routes = INDEX[key]
            for route in routes:
                file.write(str(route)+',')
            file.write('\n')
        file.close()
    return


def retriever(search):
    """Retrieve the paths where the search matches"""
    with open('indexer.txt', 'r') as file:
        indexer = file.readlines()
        file.close()

    keys = [index.split('->')[0] for index in indexer] #get the keywords

    words = obtain_words(search)
    emails = obtain_emails(search)

    if emails:
        words = words + emails

    routes_int = []
    i=0
    for word in words:
        if word in keys:
            index = indexer[keys.index(word)]
            routes = index.split('->')[1]
            routes = routes.split(',')
            routes.pop(-1)

            if i == 0:
                routes_int = routes
            set_routes = set(routes_int) & set(routes)
            routes_int = list(set_routes)
        i += 1

    if routes_int:
        return routes_int
    return ['No matches found']

if __name__ == '__main__':

    ban = True

    while ban:
        try:
            path = input('Enter the folder path: ')
            indexer(Path(path))
            ban = False
        except Exception as error:
            print(error)

    ban = True

    while ban:
        print('Write "out" to get out')
        word = input('Search: ')

        if word == 'out':
            ban = False
        else:
            routes = retriever(word.lower())
            for route in routes:
                print(route)