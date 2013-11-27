"""
    Given a list of name tokens perform fuzzy matching
    on the names and find movies for actors that are identified.
    returns a movie title if found.
"""

from librarian.constants import TMDB_API_KEY
from utils import ActorDB

from fuzzywuzzy import process
from tmdb import tmdb

MIN_INTERSECTION = 2
MIN_FUZZ_SCORE = 85

tmdb.configure(TMDB_API_KEY)
db = ActorDB()


def find_films(tokens):
    direct_match = get_film_intersection(tokens, _direct_query_match)
    if len(direct_match) != 0 and len(direct_match) <= MIN_INTERSECTION:
        return direct_match

    normalized_match = get_film_intersection(tokens, _normalize_text_match)
    return direct_match.intersection(normalized_match)


def get_film_intersection(tokens, match_func):
    films = set([])
    for name_token in tokens:
        print 'name:', name_token
        matches = match_func(name_token)  # [(actor names, score)]
        print 'matches:', matches
        #[[film_set1, filmset_2, ...], [...]]
        potential_actors = map(get_films, matches)
        print 'potential_actors:', potential_actors
        if not len(potential_actors):
            continue
        print 'films:', films

        #[film_interset1, film_interset2...]
        films = reduce(merge_sets, potential_actors)
        if len(min(films)) <= MIN_INTERSECTION:
            break

    return min(films)


def _direct_query_match(name_token):
    return db.query_name(name_token)


def _normalize_text_match(name_token):
    """
        Perform fuzzing matching to try and match name tokens
    """
    print "normalize_text: name_token:", name_token
    choices = db.query_close_name(name_token)
    print 'normalize_text: choices:', len(choices)
    matches = process.extractOne(name_token, choices)
    print 'normalize_text: matches', matches
    if not isinstance(matches, list):
        matches = [matches]

    filtered_matches = filter(
        lambda x: x is not None and x[1] > MIN_FUZZ_SCORE, matches)
    print "normalize_text:filtered_matches:", filtered_matches
    return map(lambda x: x[0], filtered_matches)


def get_films(actor_name):
    print actor_name
    people = tmdb.People(actor_name)
    return [set([movie.get_original_title() for movie in person.cast()])
            for person in people]


def merge_sets(sets1, sets2):
    """
        merge sets of sets by computing the intersection of each pair
    """
    return filter(lambda x: len(x), [
        s1.intersection(s2) for s2 in sets2
        for s1 in sets1
    ])

if __name__ == "__main__":
    clean_text = [
        'the place mindihe pines', 'the place mendihe pines', 'in order of anpsannca', 'baby jason', 'robins dons', 'anthony angelo pizza jr', 'crvst al powell', 'katie mnnell', 'craig van hook', 'olga merediz', 'eva mendes', 'rev john facci', 'ryan gosling', 'mahershala ali', 'assoclam pmducars', 'ben mendelsohn', 'travis jackson campbell', 'gail maryino', 'teller i  bank', 'bob dieterich', 'rohins dogs', 'rev john facci', 'mather at homa', 'tracev agustin', 'tellar i  bank', 'g douglas griset', 'banker outside bank', 'court lawyer', 'brian smvj', 'ben mendelsohn', 'teller  bank', 'adam nowichi', 'tells i  bank', 'nicole califano', 'baby m', 'arresting oiflcer', 'rose bvrne', 'judas i', 'cvnthia pellefiersullivan', 'cuurl omar', 'mackenzie trainor', 'mahenspirla ali', 'gabe fazio', 'paul steele', 'ean egas', 'tellur i  bank i', 'vanessa thorpe', 'mark j carusd', 'omar jemmn', 'dorothy rutherford', 'shannon plume', 'bradley cooper', 'james j gleason', 'barry aj', 'lynette howell', 'sarah curcio', 'jsnnlfars momur', 'funeral dlroctor', 'dane dehaaii', 'emorv cohen', 'bruce greenwood', 'jan libertucci', 'mm a  cm', 'joe mccarthv', 'biii klllcullan', 'travis jackson campbell', 'dnc cmwlsy', 'annlll nuvnm', 'ephraim benton', 'political modll mvlwr', 'patrick husted', 'ai cross', 'jessica layton', 'harris vulin', 'rose bvrne', 'cum wolvzbvwski', 'trevor jackson campbell', 'gampalun advlsm', 'robert glohessv', 'luca pierucci', 'guidance cnunsalor', 'gabe fazio', 'subrina dhammi', 'n nu n', 'cary gllbuu', 'grfta seacat', 'mark mccracken', 'campaign managar', 'jefrev pollock', 'heather chestnut', 'ray liotta', 'leah bliven', 'matt mortier', 'lawrence c michaelis', 'jennifer sober', 'sum senator', 'melissa mills', 'kayia smalls', 'drug bustlng can', 'kevin craig west', 'imerrouatinu gap', 'dr david ford', 'cwstum coominamr', 'extra special thanks', 'pllzvmacy clark', 'kevin green', 'stunt coordlnaxor', 'george forrester', 'hugh t farley', 'ephraim benton', 'brian smvj', 'adriel linyear', 'mark mdcracken', 'dean denisid', 'michael cullen', 'jeremiah bagley', 'frank j falvo', 'dane dehaan', 'rickv miller', 'breanna dolen', 'ursula c pasduerella', 'alex pulliiig', 'erig revell', 'karen gazda', 'whitney hudson', 'public defends', 'dante shafer', 'mr antmmy', 'lori prince', 'stephanie stokes', 'frank ferrara', 'ryan gosling', 'damn fink', 'erwin urias', 'david crommeit', 'john favre', 'nzvm imam wnl', 'rickv miller', 'luka stunt double', 'billv anagn', 'rich sturtevant', 'globe rldar ll', 'brian smvj', 'david ott', 'globe rlnar i', 'monte rex perlin', 'louie franco', 'freddv esposito', 'selenis leyva', 'fiickv miller', 'blanca camacho', 'peewee piemonte', 'stunt camera driver', 'chris cenatiempo', 'stunt camera work', 'jeffrey gibson', 'bradlev cooper', 'charles a burks', 'stunt coomlnazor', 'craig hunter', 'tim smith', 'mic orourk', 'bob beckles', 'samuel jack wagner', 'luke globe stunt double', 'slum drivers', 'loon group', 'eugene harrison', 'costunt coordinatnl', 'lori prince', 'selenis lewa', 'morgan newell', 'michael woodv', 'post prnmmlon sunarvisnr', 'ethan weinstock', 'shihlev rumierk', 'nd asslslam accauntam', 'jared uhrich', 'locaxlon manager', 'payroll aooounum', 'scum sunarvlsnr', 'jean pesce', 'amanda hiesco', 'st asslsvam accnunum', 'charles a eurks', 'production aocountam', 'ami assistant awoumam', 'bruce nielson winant', 'jennifer sunnenfeld', 'prudunlon supervlsor', 'dvlan tarason', 'marshall johnson', 'dustin bricker', 'assistant location managers', 'derek vip', 'production sammy', 'asslsum edllur', 'holly pilch', 'june frances coleman', 'louise runge', 'carissa hara', 'production coordlnmr', 'dann fink', 'paul bischot', 'loop group', 'sam jaffe', 'blanca camachd', 'david crommfit', 'nicdla westermann', 'bridget rafferty', 'pronorly master', 'isl nssrsram awounuii', 'joseph deluca', 'david eranum', 'mmu ngnnr um', 'an producllon asslsvams', 'frank foster', 'carissa hara', 'on set dresser', 'raul mwnuu', 'jasmine ballou', 'dvlan peitengill', 'kevin chang', 'lean mall', 'mike ahern', 'addhlonal props', 'payroll aooountam', 'matthew amenta', 'richard peee', 'derek kirkaldv', 'liza donatelli', 'mat kowalski', 'ancoumlnu clerk', 'third props', 'james anziand', 'max sherwood', 'henrv bernack', 'john ashton', 'michael woddv', 'an dlmnnr', 'zmi assistant aooountam', 'june frances coleman', 'an dapartmam coordinator', 'robert igoe', 'michael powsner', 'arthur jongewaard', 'assistant properly master', 'set dressers', 'set decorator', 'add asslsmm aoooumam', 'david fischer', 'cooper wright', 'linda slater', 'extras casting provided hy', 'man nluminr', 'rita powers', 'spencer gillis', 'michelle clementine garcia', 'extras castlno', 'sean powers', 'richard peete', 'rita powers casting group', 'adam caldwell', 'derek peterson', 'nd nd asslsmnl dlromor', 'jerry derugatis', 'alex finch', 'addltlonal props', 'christopher ravmcnd', 'cynthia degrus', 'casting assoclate', 'gary sless', 'liza donatelli', 'casting assistant', 'wendv obrien', 'assistant propany masicr', 'inmrunu arm', 'motorcycle mochanic', 'extras casting imam', 'michael powsner', 'isaac gabaeff', 'thlrd flops', 'john sember', 'linda slater', 'cai hall', 'samantha silver', 'frank larson', 'sound ullllty', 'jp dolan', 'vincent camuto', 'bast bov electric', 'michael p frisco jr', 'george tur', 'still photography by', 'sound mlxer', 'reed morano', 'shane duckworth', 'jon delgado', 'michelle clemeniine garcia', 'atsushi nishijima', 'boom operator', 'seth tallman', 'jonathan beck', 'christopher ravmond', 'nathan mcgarigal', 'jason clearv', 'julien zeitouni', 'b samar operator', 'damian elias canelos', 'adrlim asslsmm camera', 'mike arisohn', 'addi electricians', 'john sember', 'bes boy grlo', 'company grips', 'michael j sarluco', 'richard koenig', 'rob harlow', 'james frver', 'lamp operators', 'bast bay eloclric', 'jamie merritt', 'michael p frisco jr', 'abraham altbuch', 'michael cooney', 'jp ddlan', 'nate scaglione', 'elomrlcl lamp opmrms', 'dave ganczewski', 'rluglno electrician', 'dally grip', 'james petersen', 'glvnis burke', 'joe valle sr', 'tom pohl', 'russell boughelle', 'eric williams', 'eddie jones jr', 'john nasta', 'dave kissinger', 'michael represa', 'mati farrell', 'lance goodell', 'kay grlp', 'thomas hearn', 'chris condver', 'brent poleski', 'david kalahiki', 'key makeup', 'greg purcell', 'prnsmetlc makeup grew', 'stephani lewis', 'key helr siyis', 'kazu tsuji', 'patricia grande', 'lori mccdvbell', 'mike fdntaine', 'jamie merriti', 'chris kellv', 'leo won', 'janeen schrever', 'ben shields', 'makeup department head', 'prosthetic makeup deslgner', 'company grips', 'matt farrell', 'mike marino', 'halr dapanment head', 'add giid', 'pmsmetic makeup anis', 'eric williams', 'eddie jones jr', 'andrea grande capone', 'assimm costume desluner', 'talloa deslnn', 'dave prestd', 'drew jiritano', 'costume coordinators', 'brian carmichael', 'frame video pinyhack', 'ben woodward', 'picture car coordimxor', 'egor panchecko', 'stephani lewis', 'picture car pmdumiun ksistam', 'rachel dainerbesi', 'neil bleifeld', 'video assis opcramrs', 'costume production awistams', 'special fx cooniinatui', 'drew jiritano jr', 'wardrobe suparvisnr', 'special fx', 'richard moran', 'meghaii corea', 'james m anziano', 'chrissv kuhn', 'mike mvers', 'olivia janczvk', 'emma strachman', 'james domorski', 'grav madder', 'sol comma', 'dave presto', 'ewa noskowicz', 'assistant costume designer', 'robin pcintbriaiid', 'chris conover', 'key carvemer', 'laura lerner', 'ymnsponatlon cocamaln', 'mario mercaoo', 'david palumbo', 'andrew kanuck', 'julve p calderspinelli', 'bob broder', 'akim hovanecz', 'charge soenlc', 'tonv imgrassellino', 'carpenter foreman', 'ben ross', 'lee sheveit',
        'drew jiritanojr', 'robin monaehan', 'steven gibbs', 'special fx', 'john shimrock', 'shun electric', 'thomas jones', 'sat medics', 'richard moran', 'richard hebrank', 'oonslructlon coordlnaxor', 'drew jihiianu', 'mary lovendusky', 'transportation camalns', 'mike mvers', 'kurt kroll', 'special rx uoomlnaur', 'dlalm coach', 'timothv paustian', 'peter bundrick', 'craig apolito', 'omit servlaa claire wiegand', 'james wrisut paul vevoli', 'ulruzl  iuzcvc', 'add chi sean carroll', 'james degeorgia', 'cmis andrew gilbert', 'luie morales', 'tonv ingrassellino', 'mnspumuuu uapwun', 'alberto peter villafane', 'imlvlni ruuunm', 'aulnnrrvln m hnuurll', 'dan majkut', 'jim powers', 'billv zavac', 'elair howlev', 'st taam production assistant', 'brian ketchum', 'steven lafferty', 'sean carroll', 'claire wiegand', 'woikie production asslsmnt', 'eliav mnz', 'unit production assistant', 'location assistant', 'jack hart', 'kay production assistant', 'michele weeks', 'chelsev cary', 'george lookshire', 'oitioe production assistants', 'location scouts', 'scott cernv', 'mike camion', 'tavlor kim', 'luie morales', 'eliav mlnz', 'craft service', 'wing veong', 'robert wilhelm jr', 'assistant to mr clantnnoe', 'assistant to mr patrinot', 'zacharv mandell', 'assistant to mr gosling', 'christina aoevedo', 'assistant tn mr patriwf', 'assistant to mr clanhanon', 'jessica enoel', 'asslslam to m coupe', 'lauren lebeouf', 'weston middleton', 'jack hart', 'assistant to ms mendes', 'scott cernv', 'asslstavn to ms howell', 'siobhan gorski', 'daniel lachman', 'richard lewis', 'sgciti swar', 'sidney kimmni emertainmcrrt', 'john stegemann', 'earkin smith llp', 'brian detrani', 'nicole vhallo', 'mark mikutowicz', 'david weaver', 'llilllv ouru', 'chief financial oifirer', 'nrwnr ercnu cnnrrn rm', 'lakota polacsek', 'jill l smith', 'tabatha maletich', 'nick batson', 'anita casamassima', 'sari greenberg', 'amanda messenger', 'max newmanplotinick', 'vicki higgins', 'nick hank', 'kelsev thomas', 'asslsurvt controller', 'lauren wells', 'gaev allen', 'april taskin', 'stephen gemmito', 'uuazrn anu zrra', 'christina carmodv', 'elizaiieih whelan', 'chris murphy', 'jonathan herr', 'monioue jones', 'vp production', 'jon campano', 'assistant in mr bcransan', 'vp firrancol cnntroliar', 'uurrru an zurzrvmnru', 'keisva rito', 'roxv campos', 'hanna lindner', 'karl sturk', 'payroll company', 'enterprise rentacar', 'cpmk lighting llc', 'dani weinstein', 'entertainment clearances inc', 'cassandra barbour', 'dewiti stern group inc', 'teiecine pmvided by', 'film finances inc', 'susan muir', 'electric equipment pmvided by', 'medical services pmvided by', 'production lab', 'entertainment partners', 'christina born', 'richard eisenberg', 'thunderwolf grip services inc', 'topo customs', 'picture vehicles pmvided by', 'grip equipment pmvided by', 'jennifer bond', 'unit publicist', 'barkin smith llp', 'camera equipment pmvided by', 'arri csc', 'jill l smith', 'louis a kat md', 'production counsel pmvided by', 'completion guarantor', 'john diesso', 'enterprise rentacar', 'onazam past coordinator', 'i win man', 'jav tilin', 'post production accaumani', 'nwui n nii', 'walkia talkies provided by', 'trace henderson', 'marv prendergast', 'kelsev schuvler', 'vana collins lehman', 'onanm supervisor', 'vtr provided by', 'post production', 'marie de leon', 'topo customs', 'rockbottom rentals', 'dneero films', 'tom poole', 'assistant in derek ciarnranoe', 'trevanna post', 'christa halev', 'frame playback pruvided ivy', 'samantha housman', 'past productiun mslsiam', 'digital intennedlato editors', 'adh recordlst', 'john diesso', 'charles christopher rubino', 'dlalogue edltor', 'dan timmons', 'cd exncutivs producer', 'nrmn ru', 'dallles coiorist', 'liam ford', 'tonv volante', 'foley mist', 'account execrrllve', 'foley recordlst', 'marcelo gandola', 'leslie bloome', 'stefan sonnenfeld', 'adr edltor', 'dloital intarmedlato edltors', 'tltte daslun', 'alchemv post', 'sean dunokley', 'carl shilito', 'evan benjamin', 'dan flusdorf', 'sound lounge', 'patrick christensen', 'droglulntarrnudlato producer', 'andrew gearv', 'mm nnnwunu', 'jay tilin', 'marie de leon', 'david feldman', 'jaime obradovich', 'head of production', 'foley recorded at', 'dan timmons', 'asslsram herecordno mixer', 'raven sia', 'rob browning', 'ryan leonard', 'david toepfer', 'aleksandar djordjevio', 'vendome uhl', 'vlsual elfects coordinator', 'tonv volante', 'alghemv post', 'diohal anlsts', 'producerstudio coordinator', 'herecording mixer', 'alexander koehl', 'david marte', 'igor boshoer', 'visual effects provided dy', 'systems engineers', 'david plombino', 'de lane lea', 'vlsual eflects producer', 'jim rider', 'cara bucklev', 'plpallne td', 'head of production', 'um um', 'dennis huvnh', 'uuw umw', 'alice kahn', 'method studios', 'adr ennlneer', 'adam gamdola', 'foley recorded at', 'adr enninoer vendome uhl', 'adr rocomisl james hyde', 'blk dnm carharti converse', 'kangdl keds lagoste', 'of a find vintage', 'trfiorn vena cava wdlverine', 'artwork pmvided ivy', 'jdvce dannbale gail kessler', 'adr mlxer nick krav', 'robert collin steve honicki', 'wardrobe provided kw', 'carolvn taylor stephen ritzko', 'vailay eniaminmsnt inc', 'gary chester', 'music coordinator', 'suburban riot', 'courtesy of wwwrryinsnamssrom', 'john jennings bovd', 'marv kuuvoumdjian', 'of a find vintage', 'additional music ovchastratur', 'additional music by', 'johannes rana diroctnr', 'arranged vy vladmlv lvanoil', 'vena cava', 'seize sur vingt', 'wwwrcncoom cuiturawm', 'mhsicimiiiuii mv', 'music engineer', 'eric holland', 'wnmn by gregorio aiiegn', 'eric v habhikian', 'jacob nathan', 'punormod by messy marv', 'wmmn by am pm', 'performed by sulcim', 'performed by mlka pmnrl', 'cnunssy of irma rscnmings', 'purlorrnnd by i flamnllnanl', 'wrlllan by am van', 'purrunm try i flammlnalll', 'wrlmn by marvin watson', 'goumsy  columbla reooms', 'written by mike mun', 'm  um', 'written dy ann part', 'wmxan by milru pam', 'condnma by rudoll wanllerl', 'wrmau by am pan', 'permrmed by salem', 'courtesy ol iamsound records', 'wmmn hy alva pm', 'pmnmm hu rem um', 'perionneo by mlke mm', 'wmm by juslln vernon', 'wmm by amon tohln', 'insdous alf', 'written by mlke fmon', 'caunesy of vona', 'courusy of rum rocordlnus', 'wrmen by mllw pinon', 'courtesy of loose recordlnns', 'w  iywvuv', 'pervonnsd by ryan gnsllna', 'green pghiiultural departibit', 'duanes tdvland', 'hes nanal baikg wm', 'alenw x hsforical sgiiew', 'avumi sakamoto', 'niskavwa hie dpartibit', 'min bifeiaiiieit', 'e pamer cm', 'special thanks', 'keith zimmerman', 'alan and susan patfiicof', 'gee w hsforical sxhew', 'knjdav in iv', 'pre wopper', 'svdnev wiseman', 'jamie wiseman', 'gleiscn meal fdjb', 'miit bum forth aiekia', 'm pliie magic', 'diane and tommv pustolka', 'mhawk amkmmx', 'rachel mikolvski', 'musmo bmk', 'david erent heltdn', 'ed wiseman', 'graham taylor', 'eilhit lmano ldznk grip', 'allie and hav legere', 'mike seber', 'oakley mo', 'john buhrmaster', 'chahlotta heltun', 'mnwian mnnwj  dates', 'tiealtanuit fair', 'kellv sawveh patricof', 'neiean redr iywtdvi', 'paul f mayersohn', 'rilev and sawver patricdf', 'hilvvvqjd bhaniej', 'don rittner', 'charlotte wiseman', 'hunter ghav', 'jimmv helton sr', 'migumellj farms', 'justin wilkes', 'glenje pole imeparitent', 'imth emt hlm parties', 'chizuko niikawaheltdn', 'prujtdrs theatre', 'em umn', 'iwtheawhlm partlh', 'wee brand', 'grrcliie nardman', 'brbdan rilev', 'miig uvam', 'in memoryoi', 'im xinimham', 'gus instein', 'wjard hlz', 'brwi kldtilen', 'kate fmev', 'dn eriwlir', 'liinieamjkhn vohgin', 'tdnia hkmel', 'njrwie vrkeht', 'tom pustdlka', 'grav madder', 'in memory', 'samuel wagner', 'ma max sm', 'all rights reserved', 'kimmel distribution llc']
    print find_films(clean_text)
