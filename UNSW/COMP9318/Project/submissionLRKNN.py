## Using LR on Vowel2, Using KNN on Vowel3, Vowel4
## Based on P400 KNN

## Import some modules
import numpy as np
import pandas as pd
import helper
import submission
import re
import pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression

## Helper functions
def split_to_list(curr_row):
    word = curr_row[:curr_row.index(':')]
    splitted_list = curr_row[curr_row.index(':') + 1 : ].split(' ')
    return word, splitted_list

def check(splitted_list):
    count = 0
    target = 0
    removed_stress = []
    for item in splitted_list[:]:
        try: # vowel
            curr = int(item[-1]) 
            removed_stress.append(item[:-1])
            count += 1
            if curr == 1:
                target = count
        except: # consonant
            removed_stress.append(item)
    return removed_stress, target

def count_vowel(removed_stress, vowel):
    count = 0
    for item in removed_stress[:]:
        if item in vowel:
            count += 1
    return count

## Filters
def singular_filter(word, removed_stress):
    
    ## If the word has no more than 3 letters we do not refine it(to avoid abbrevation)
    if len(word) <= 3:
        return word, removed_stress
    
    sub_string1 = word[-2: ]
    sub_string2 = word[-3: ]
    sub_string3 = word[-6: ]    
    sub_string4 = word[-4: ]
    
    pattern1 = re.compile('[BCDFGHJKLMNOPQRTVWYZ]{1}S$')
    pattern2 = re.compile('XS$')
    # For CDFGHKLPWRTWYZ --> remove 'S' from word, remove 'S/Z' from removed_stress
    if re.match(pattern1, sub_string1):
        return word[:-1], removed_stress[:-1]
    # For X --> remove 'S' from word, remove 'IH Z' from removed_stress
    if re.match(pattern2, sub_string1):
        return word[:-1], removed_stress[:-2]
    
    # -ES
    pattern3 = re.compile('[ABDEFJKLMNOPQRTUWY]{1}ES$')
    pattern4 = re.compile('IES$')
    pattern5 = re.compile('HES$')
    pattern55 = re.compile('ZZES$|SSES$')
    pattern6 = re.compile('[CGSXZ]{1}ES$')
    pattern7 = re.compile('SELVES$')
    pattern8 = re.compile('IVES$')
    pattern9 = re.compile('VES$')
    
    if re.match(pattern3, sub_string2): # ES --> E
        return word[:-1], removed_stress[:-1]
    if re.match(pattern4, sub_string2): # IES --> Y
        word = word[:-3] + 'Y'
        return word, removed_stress[:-1]
    if re.match(pattern5, sub_string2):
        return word[:-2], removed_stress[:-2]
    if re.match(pattern55, sub_string4):
        return word[:-2], removed_stress[:-2]
    if re.match(pattern6, sub_string2):
        return word[:-1], removed_stress[:-2]
    if re.match(pattern7, sub_string3):
        word = word[:-6] + 'SELF'
        removed_stress.pop()
        removed_stress.pop()
        removed_stress.append('F')
        return word, removed_stress
    if re.match(pattern8, sub_string4) and (removed_stress[-3:] == ['AY', 'V', 'Z']):
        word = word[:-3] + 'FE'
        removed_stress.pop()
        removed_stress.pop()
        removed_stress.append('F')
        return word, removed_stress
    if re.match(pattern9, sub_string2):
        return word[:-1], removed_stress[:-1]
    
    return word, removed_stress

def neutral_filter1(word, removed_stress):
    pattern1 = re.compile('ABLY$')
    if re.search(pattern1, word):
        word = word[:-1] + 'E'
        return word, removed_stress[:-1]
    
    pattern2 = re.compile('LL[YI]{1}$|LLED$|SSED$|FFED$')
    if re.search(pattern2, word):
        return word[:-2], removed_stress[:-1]
    
    pattern3 = re.compile('L[YI]{1}$')
    if re.search(pattern3, word) and removed_stress[-2:] == ['L', 'IY']:
        return word[:-2], removed_stress[:-2]
    
    pattern4 = re.compile('DDED$|TTED$')
    if re.search(pattern4, word):
        return word[:-3], removed_stress[:-2]
    
    pattern5 = re.compile('[AEIOU]{1}[DFT]{1}ED$')
    if re.search(pattern5, word):
        return word[:-1], removed_stress[:-2]
    
    pattern6 = re.compile('[AEIOU]{1}[KMNSR]{1}ED$|IBED$')
    if re.search(pattern6, word):
        return word[:-1], removed_stress[:-1]
    
    pattern7 = re.compile('BBED$|GGED$|MMED$|NNED$|PPED$|RRED$')
    if re.search(pattern7, word):
        return word[:-3], removed_stress[:-1]
    
    pattern10 = re.compile('[BHKMNOPSWXY]{1}ED$')
    if re.search(pattern10, word):
        return word[:-2], removed_stress[:-1]
    
    pattern11 = re.compile('IED$')
    if re.search(pattern11, word):
        word = word[:-3] + 'Y'
        return word, removed_stress[:-1]
    
    pattern12 = re.compile('[CGLUVZ]{1}ED$')
    if re.search(pattern12, word):
        return word[:-1], removed_stress[:-1]
    
    pattern13 = re.compile('[DFTR]{1}ED$')
    if re.search(pattern13, word):
        return word[:-2], removed_stress[:-2]
    
    pattern14 = re.compile('ISM$')
    if re.search(pattern14, word):
        return word[:-3], removed_stress[:-4]    
    
    pattern15 = re.compile('FUL$')
    if re.search(pattern15, word):
        return word[:-3], removed_stress[:-3]  
    
    pattern16 = re.compile('NESS$') # remove 'NESS', remove 'N AH0 S'
    if re.search(pattern16, word):
        return word[:-4], removed_stress[:-3]
    
    pattern17 = re.compile('[A-HK-Z]ING$') # JING is omitted ("BEIJING")
    if re.search(pattern17, word):
        return word[:-3], removed_stress[:-2]
    
    return word, removed_stress

def compound_filter(word, removed_stress):
    l74 = re.compile('SHOOTER$|FIGHTER$')
    if re.search(l74, word):
        return word[:-7], removed_stress[:-4]
    l75 = re.compile('BREAKER$|CRACKER$')
    if re.search(l75, word):
        return  word[:-7], removed_stress[:-5]
    l76 = re.compile('QUARTER$|SCRAPER$')
    if re.search(l76, word):
        return  word[:-7], removed_stress[:-6]
    
    l64 = re.compile('LENGTH$|COOLER$|DEALER$|SELLER$|LETTER$|HAMMER$|WRITER$|FLOWER$|FATHER$|MOTHER$|TELLER$|BEARER$|TANKER$|KEEPER$|BUTTER$|FISHER$|BURGER$|WASHER$|WEALTH$|LOCKER$|SITTER$|RUBBER$|BAGGER$')
    l65 = re.compile('MONGER$|CASTER$|DRIVER$|GROUND$|PERSON$|COMING$|NEPHEW$|STRIKE$|STROKE$|STRIPE$|STREAM$|AROUND$|MOBILE$|STRUCK$|RADISH$|MASTER$|SPREAD$|FINGER$|SISTER$|CENTER$|CASTLE$')
    l66 = re.compile('PARENT$|MARKET$|CARPET$')
    if re.search(l64, word):
        return word[:-6], removed_stress[:-4]
    if re.search(l65, word):
        return word[:-6], removed_stress[:-5]
    if re.search(l66, word):
        return word[:-6], removed_stress[:-6]
    
    l53 = re.compile('BEACH$|THING$|SHARE$|THROW$|TOOTH$|GUARD$|CHECK$|SHINE$|CHAIR$|WATCH$|MATCH$|TOUCH$|PIECE$|STEAM$|HOUSE$|PAYER$|SHEEP$|CAUSE$|WHITE$|OTHER$|SIGHT$|WHERE$|THERE$|SHORE$|SHELL$|NOISE$|VILLE$|WHEEL$|WHILE$')
    l54 = re.compile('[A-OQ-Z]{1}POINT$|FIELD$|BERRY$|DRESS$|TOWER$|UPPER$|SCALE$|SWEET$|GRADE$|GRAVE$|CYCLE$|GLASS$|SMITH$|UNDER$|IMAGE$|CLASS$|CLOTH$|QUAKE$|AFTER$|WATER$|BOARD$|CARRY$|SNAKE$|TABLE$|DAIRY$|UNCLE$|SCAPE$|SPOON$|STICK$|WAIST$|PROOF$|HONEY$|PAPER$|MAKER$|PLANE$|CHILD$|TRACK$|GRASS$|CLOCK$|STONE$|SHADY$|TAKER$|SLIDE$|FRUIT$|BRAIN$|SPICE$|SKATE$|DREAM$|DRIVE$|STORE$|COURT$|BLOOD$|BREAD$|RIVER$|BELLY$|STOCK$|SPOUT$|SHARP$|HORSE$|SPACE$|PASTE$')
    l55 = re.compile('SCOPY$|EVERY$|STORM$|PRINT$|WOMAN$|WOMEN$|SHELF$|CRAFT$|STRAP$|DRIFT$|MELON$|BREAK$')
    if re.search(l53, word):
        return word[:-5], removed_stress[:-3]
    if re.search(l54, word):
        return word[:-5], removed_stress[:-4]
    if re.search(l55, word):
        return word[:-5], removed_stress[:-5]
    
    l42 = re.compile('ATCH$|HIGH$|SHOE$|SHOW$|ACHE$')
    l43 = re.compile('ELSE$|ROLL$|LUKE$|FORE$|MEAT$|HEAD$|WHEN$|JACK$|POLE$|NOTE$|IRON$|EVER$|BOWL$|CREW$|BEAR$|DIAL$|DRAW$|SHOP$|LONG$|SAIL$|SIDE$|BIRD$|TAPE$|LIME$|TAIL$|HOOK$|TEAM$|KEEP$|FOOT$|FARE$|PIPE$|PATH$|TOWN$|PICK$|OVER$|FREE$|ROAD$|GOAT$|AUNT$|SHIP$|HERE$|TYPE$|MOTH$|BAIT$|BEAN$|PACE$|SICK$|MAID$|MEAL$|MATE$|KICK$|WISE$|CARE$|WIPE$|BELL$|BOOK$|MAIL$|COOL$|ROAR$|BLUE$|EART$|BOAT$|ROOT$|BACK$|FACE$|HOME$|GEAR$|JAIL$|BITE$|HAIR$|HOLE$|DEAD$|LIFE$|PACK$|AGER$|WHAT$|BOMB$|RAIL$|WITH$|MADE$|LAID$|DOWN$|BALL$|AWAY$|PLAY$|COME$|SNOW$|DOOM$|COCK$|WEED$|CROW$|RING$|CASE$|BEAT$|NOON$|DOOR$|WORM$|WASH$|WORD$|CAVE$|DUCK$|FIRE$|MEAN$|GOOD$|FORK$|FALL$|RACK$|POOL$|LACE$|SLOW$|WARE$|THEM$|CAME$|PASS$|WORK$|LIKE$|FISH$|DISH$|TIME$|PAWS$|FOWL$|HILL$|WEEK$|WAVE$|BOOT$|BLOW$|CAKE$|WIDE$|SOME$|ROOF$|SHOT$|BEAM$|ROCK$|LOAD$|CUFF$|FLOW$|MORE$|MOON$|TOOL$|BASE$|HOOD$|MAKE$|ROOM$|FEET$|BURN$|BURG$|BERG$')
    l44 = re.compile('COPY$|LINK$|TASK$|STOP$|MILK$|TURN$|STAR$|PONY$|WARN$|SLAP$|LIST$|TRAP$|HAND$|BOLD$|SPIN$|ALSO$|DISK$|DROP$|UPON$|YARD$|JUMP$|WARM$|BODY$|SOFT$|BAND$|BANK$|PARK$|LARK$|FORD$|WORN$|HELD$|TOLD$|BABY$|SLUM$|REST$|MINT$|MOST$|LORD$|BOLT$|CAST$|FOLD$|WIND$|POST$|SAND$|TAGA$|WALK$|FORT$|LIFT$|STEP$')
    l45 = re.compile('TEXT$|TAXI$')
    if re.search(l42, word):
        return word[:-4], removed_stress[:-2]
    if re.search(l43, word):
        return word[:-4], removed_stress[:-3]
    if re.search(l44, word):
        return word[:-4], removed_stress[:-4]
    if re.search(l45, word):
        return word[:-4], removed_stress[:-5]
    
    l31 = 'EYE$'
    l32 = re.compile('EGG$|TIE$|KEY$|HOW$|WAY$|BOY$|PAY$|OFF$|DEW$')
    l33 = re.compile('IST$|FEW$|CUP$|GUN$|CAB$|LEG$|CAR$|BID$|POP$|SIX$|JET$|GUM$|BUS$|CAT$|HOP$|NUT$|SUN$|POT$|LOG$|WAR$|FLY$|PAD$|DOG$|TAX$|ROP$|MAT$|BUG$|CAP$|NOT$|SET$|COM$|ARM$')
    l34 = re.compile('WAX$|BOX$')
    if re.search(l31, word):
        return word[:-3], removed_stress[:-1]
    if re.search(l32, word):
        return word[:-3], removed_stress[:-2]
    if re.search(l33, word):
        return word[:-3], removed_stress[:-3]
    if re.search(l34, word):
        return word[:-3], removed_stress[:-4]
    
    return word, removed_stress

def combined_filter(word, removed_stress, vowel):
    
    word, removed_stress = singular_filter(word, removed_stress)
    if len(word) == 0 or len(removed_stress) == 0: 
        return 1, [1]
    
    #if count_vowel(removed_stress, vowel) <= 2:
     #   return word, removed_stress
    word, removed_stress = neutral_filter1(word, removed_stress)
    if len(word) == 0 or len(removed_stress) == 0: 
        return 1, [1]

    #if count_vowel(removed_stress, vowel) <= 2:
     #   return word, removed_stress
    word, removed_stress = compound_filter(word, removed_stress)
    if len(word) == 0 or len(removed_stress) == 0: 
        return 1, [1]
    
    if count_vowel(removed_stress, vowel) == 0:
        return 1, [1]
    
    return word, removed_stress

## Preprocessing
def get_structure_and_vowels(removed_stress, vowel, consonant):
    structure = ''
    num_vowels = 0
    count = 0
    vowels = []
    vowel_positions = []
    VowelMap = []
    ConsonantMap = []
    VectorMap = [0] * 39
    for item in removed_stress[:]:
        vowel_index = consonant.get(item)
        VectorMap[vowel_index] = 1
        if item in vowel:
            structure += 'V'
            vowels.append(vowel_index)
            VowelMap.append(1)
            ConsonantMap.append(0)
            vowel_positions.append(count)
            num_vowels += 1
            count += 1
        else:
            VowelMap.append(0)
            ConsonantMap.append(1)
            structure += 'C'
            count += 1
            
    if count < 15:
        VowelMap += [0] * (15 - count)
        ConsonantMap += [0] * (15 - count)
    return vowels, vowel_positions, structure, VowelMap, ConsonantMap, VectorMap

################### LR ##########################
def get_structure_and_vowels_LR(removed_stress, vowel):
    structure = ''
    num_vowels = 0
    count = 0
    vowels = []
    vowel_positions = []
    for item in removed_stress[:]:
        if item in vowel:
            structure += 'V'
            vowels.append(vowel.get(item))
            vowel_positions.append(count)
            num_vowels += 1
            count += 1
        else:
            structure += 'C'
            count += 1
        
    return vowels, vowel_positions, num_vowels, structure
#################################################

def get_prefix_and_suffix(vowel_positions, removed_stress, consonant):
    result = []
    for curr_position in vowel_positions[:]:
        if curr_position == 0: # no prefixes
            prefix1 = 39
        else:
            prefix1 = consonant.get(removed_stress[curr_position - 1])
        result.append(prefix1)
        try:
            suffix1 = consonant.get(removed_stress[curr_position + 1])
        except:
            suffix1 = 39
        result.append(suffix1)
    return result

## get syllables
def split_structure_vowel2(vowel_positions, removed_stress):
    split_result = []
    if vowel_positions[1] - vowel_positions[0] > 1: 
        split_result.append(' '.join(removed_stress[:vowel_positions[1] - 1]))
        split_result.append(' '.join(removed_stress[vowel_positions[1] - 1 : ]))
    else:
        split_result.append(' '.join(removed_stress[:vowel_positions[0] + 1]))
        split_result.append(' '.join(removed_stress[vowel_positions[0] + 1 : ]))
    return split_result
def split_structure_vowel3(vowel_positions, removed_stress):
    if vowel_positions[1] - vowel_positions[0] > 1: # CVCCCVXXXX
        part1 = removed_stress[:vowel_positions[1] - 1]
        removed_stress = removed_stress[vowel_positions[1] - 1 : ]
        
    else: # CVVXXXX
        part1 = removed_stress[:vowel_positions[0] + 1]
        removed_stress = removed_stress[vowel_positions[0] + 1 : ]
    
    vowel_positions = [vowel_positions[1] - len(part1), vowel_positions[2] - len(part1)]
    sub_split_result = split_structure_vowel2(vowel_positions, removed_stress)
    split_result = [' '.join(part1)]
    split_result.extend(sub_split_result)
    return split_result
def split_structure_vowel4(vowel_positions, removed_stress):
    if vowel_positions[1] - vowel_positions[0] > 1: # CVCCCVXXXX
        part1 = removed_stress[:vowel_positions[1] - 1]
        removed_stress = removed_stress[vowel_positions[1] - 1 : ]
        
    else: # CVVXXXX
        part1 = removed_stress[:vowel_positions[0] + 1]
        removed_stress = removed_stress[vowel_positions[0] + 1 : ]
    
    vowel_positions = [vowel_positions[1] - len(part1), vowel_positions[2] - len(part1), vowel_positions[3] - len(part1)]
    sub_split_result = split_structure_vowel3(vowel_positions, removed_stress)
    split_result = [' '.join(part1)]
    split_result.extend(sub_split_result)
    return split_result




## Get dataset and dataframe
def get_splitted_data(raw_data, vowel, consonant):
    vowel2 = []
    structure_dict_2 = {}
    vowel3 = []
    vowel4 = []
    
    for curr_row in raw_data[:]:
        word, splitted_list = split_to_list(curr_row)
        removed_stress, target = check(splitted_list)
        word, removed_stress = combined_filter(word, removed_stress, vowel)
        
        if word == 1 or removed_stress == [1]:
            continue
        
        num_vowel = count_vowel(removed_stress, vowel)
        
        if num_vowel <= 1:
            continue

        elif num_vowel == 2: ## Use LR here
            row_data = [target, word, ' '.join(removed_stress)]
            vowels, vowel_positions, num_vowels, structure = get_structure_and_vowels_LR(removed_stress, vowel)

            row_data.extend(vowels)
            row_data.extend(vowel_positions)
        
            prefix_suffix = get_prefix_and_suffix(vowel_positions, removed_stress, consonant)

            row_data.extend(prefix_suffix)
            if structure in structure_dict_2:
                structure_index = structure_dict_2.get(structure)
            else:
                structure_index = len(structure_dict_2)
                structure_dict_2[structure] = structure_index
            row_data.append(structure_index)

            vowel2.append(row_data)


        elif num_vowel == 3:
            vowels, vowel_positions, structure, VowelMap, ConsonantMap, VectorMap = get_structure_and_vowels(removed_stress, vowel, consonant)
            prefix_suffix = get_prefix_and_suffix(vowel_positions, removed_stress, consonant)
            syllables = split_structure_vowel3(vowel_positions, removed_stress)
            row_data = [target, word, vowels, prefix_suffix, VowelMap, ConsonantMap, VectorMap, syllables]
            vowel3.append(row_data)
        else:
            vowels, vowel_positions, structure, VowelMap, ConsonantMap, VectorMap = get_structure_and_vowels(removed_stress, vowel, consonant)
            prefix_suffix = get_prefix_and_suffix(vowel_positions, removed_stress, consonant)
            syllables = split_structure_vowel4(vowel_positions, removed_stress)
            row_data = [target, word, vowels, prefix_suffix, VowelMap, ConsonantMap, VectorMap, syllables]
            vowel4.append(row_data)
    
    return vowel2, vowel3, vowel4, structure_dict_2

def vowels_to_bin(Vowels, vowel):
    result = []
    for item in Vowels[:]:
        curr = [0] * 15
        curr[item] += 1
        result.extend(curr)
    return result
def prefix_suffix_to_bin(PrefixSuffix, consonant):
    result = []
    for item in PrefixSuffix[:]:
        curr = [0] * 40 # note "39" is for boundary
        curr[item] += 1
        result.extend(curr)
    return result
def get_combination(Syllables):
    combination = []
    length = len(Syllables)
    for curr_length in range(1,length + 1):
        for start_position in range(length - curr_length + 1):
            combination.insert(0, ' '.join(Syllables[start_position : start_position + curr_length]))
    return combination

def get_df(data, vowel, consonant):
    df = pd.DataFrame(data, columns=['Target', 'Word', 'Vowels','PrefixSuffix', 'VowelPosition', 'ConsonantPosition', 'Occurrence', 'Syllables'])
    df['VowelsBin'] = df.Vowels.apply(vowels_to_bin, vowel = vowel)
    df['PrefixSuffixBin'] = df.PrefixSuffix.apply(prefix_suffix_to_bin, consonant = consonant)
    df['SyllableCombination'] = df.Syllables.apply(get_combination)
    return df

################## LR ###########################
def get_df_LR(train2):
    numCol = len(train2[0])
    
    c0tar = ['Target']
    c1 = ['Word', 'RemovedStress']
    c2 = ['Vowel1', 'Vowel2']
    c3 = ['V1_in_RS', 'V2_in_RS']
    c4 = ['V1P1','V1S1']
    c5 = ['V2P1','V2S1']
    c8 = ['Structure']
    
    if numCol == 11:
        columns = c1 + c2 + c3 + c4 + c5 + c8
        
    else:
        columns = c0tar + c1 + c2 + c3 + c4 + c5 + c8
        
    df = pd.DataFrame(train2, columns = columns)
    return df

def build_transformed_df(df0, prefixdf, consonant_OHE, position_OHE, structure_OHE_2):
    
    numCol = df0.shape[1]
    
    transform_con = ['Vowel1', 'Vowel2', 'V1P1', 'V1S1', 'V2P1', 'V2S1']
    transform_pos = ['V1_in_RS', 'V2_in_RS']
    structure_OHE = structure_OHE_2
        
    structure_pos = 'Structure'
    
    tdata = np.array(consonant_OHE.transform(df0[[transform_con[0]]]).toarray())
        
    for item in transform_con[1:]:
        np1 = np.array(consonant_OHE.transform(df0[[item]]).toarray())
        tdata = np.concatenate([tdata, np1], axis = 1)
    
    for item in transform_pos[:]:
        np1 = np.array(position_OHE.transform(df0[[item]]).toarray())
        tdata = np.concatenate([tdata, np1], axis = 1)
    
    np1 = np.array(structure_OHE.transform(df0[[structure_pos]]).toarray())
    tdata = np.concatenate([tdata, np1], axis = 1)

    # build transformed dataframe
    subdf = pd.DataFrame(tdata)
    return prefixdf.join(subdf)

# Function add rules
def add_rules(df):

    numCol = df.shape[1]
    # Position -1
    suffix1 = 'MAIN$|[BM]{1}ADE$|[NPYR]{1}EE$|[BDKM]{1}ESE$|EER$|ETTE$|[AW]{1}INE$|OON$|JOUS$|QUE$|[EJ]{1}ICE$|SCE$|[AH]{1}RAL$'
    # Position -2
    suffix2 = 'HI$|JI$|TSU|[MW]{1}A$|SKI$|KIN$|SONIC$|[GHJ]{1}EE$|HESE$|ION$|[BCEPY]{1}OUS$|[CGTX]{1}IOUS$|[DGKLMOSVYZ]{1}AL$|[CLT]{1}IAL$|[AGMRU]{1}NAL$|[DIU]{1}RAL$|[ACFST]{1}IAN$|[A-HJ-XZ]{1}GIAN$|[A-UW-Z]{1}IC$|[LMR]{1}ICE$|[ABCI]{1}CH$|[AOT]{1}IA$|AIBLE$|CIENT$|[ABKLNPRTUVW]{1}ISH$|[BCDFGHKLNPRSVWXZ]{1}IT$|LIAR$|OSIS$|SIVE$|[BCDFGHJKLMNPRSTVXYZ]{1}O$|[DEK]{1}Y$|[CSU]{1}HY$|[CDTWZ]{1}NY$|EN$'
    # Position -3
    suffix3 = 'VICH$|ULAR$|SHADE$|[BDLNPRV]{1}IOUS$|[LMNT]{1}OUS$|[CFJU]AL$|HAL$|[BGHRVX]{1}IAL$|[IEO]{1}NAL$|[EG]{1}RAL$|[BDHLMPRUVZ]{1}IAN$|[IJKNY]{1}GIAN$|[BDFHVXZ]{1}IA$|[CDGLST]{1}IBLE$|[BDNPRTV]{1}IENT$|[EI]{1}O$|[TFP]{1}Y$|[AEGPT]{1}HY$|[ER]{1}NY$'
    # Position -4(1)
    suffix4 = 'RAIN$|TEEN$|[AEO]{1}V$|APPOINT$|NEW$|RAY$|BYE|SUPPLY$|EUR$|GRADE$|OO$|[HP]{1}AL$|[RN]{1}IAL$|[DEFHLMNPRSTW]{1}ICH$|[JKLMNR]{1}IA$|[DFGMY]{1}ISH$|UIT$|IZE$'
    
    df['Suffix1'] = pd.Series(df.Word.str.contains(suffix1), index=df.index)
    
    pattern2 = suffix2 + '|' + suffix3 + '|' + suffix4
    df['Suffix2'] = pd.Series(df.Word.str.contains(pattern2), index=df.index)
    return df
##################################################

## Get final train data
def get_final_trainset(df, num_vowels):
    unpacked_dataset1 = pd.DataFrame.from_records(df.VowelPosition.tolist(),columns = range(1,16))
    unpacked_dataset2 = pd.DataFrame.from_records(df.ConsonantPosition.tolist(),columns = range(16,31))
    unpacked_dataset3 = pd.DataFrame.from_records(df.Occurrence.tolist(),columns = range(31, 70))
    
    if num_vowels == 2:
        unpacked_dataset0 = pd.DataFrame.from_records(df.SyllableCombination.tolist(),columns = ['C12','C2','C1'])
        unpacked_dataset4 = pd.DataFrame.from_records(df.VowelsBin.tolist(),columns = range(100,130))
        unpacked_dataset5 = pd.DataFrame.from_records(df.PrefixSuffixBin.tolist(),columns = range(1000,1160))
    elif num_vowels == 3:
        unpacked_dataset0 = pd.DataFrame.from_records(df.SyllableCombination.tolist(),columns = ['C123','C23','C12', 'C3','C2','C1'])
        unpacked_dataset4 = pd.DataFrame.from_records(df.VowelsBin.tolist(),columns = range(100,145))
        unpacked_dataset5 = pd.DataFrame.from_records(df.PrefixSuffixBin.tolist(),columns = range(1000,1240))
    else:
        unpacked_dataset0 = pd.DataFrame.from_records(df.SyllableCombination.tolist(),columns = ['C1234','C234','C123','C34','C23','C12','C4','C3','C2','C1'])
        unpacked_dataset4 = pd.DataFrame.from_records(df.VowelsBin.tolist(),columns = range(100,160))
        unpacked_dataset5 = pd.DataFrame.from_records(df.PrefixSuffixBin.tolist(),columns = range(1000,1320))
    final_dataset = pd.concat([df.Target, unpacked_dataset0], axis=1) # Syllable Combinations
    final_dataset = pd.concat([final_dataset, unpacked_dataset1], axis=1) # VowelPositionMap
    final_dataset = pd.concat([final_dataset, unpacked_dataset2], axis=1) # ConsonantPositionMap
    final_dataset = pd.concat([final_dataset, unpacked_dataset3], axis=1) # VectorMap
    final_dataset = pd.concat([final_dataset, unpacked_dataset4], axis=1) # VowelMap
    final_dataset = pd.concat([final_dataset, unpacked_dataset5], axis=1) # PrefixSuffixMap
    
    return final_dataset

    ## Get refined dataframe for testing
def get_refined_df(test_combination, df, num_vowels):
    if num_vowels == 2:
        df_features = ['C12','C2','C1']
    elif num_vowels == 3:
        df_features = ['C123','C23','C12', 'C3','C2','C1']
    else:
        df_features = ['C1234','C234','C123','C34','C23','C12','C4','C3','C2','C1']
    for i in range(len(df_features)):
        sub_df = df[df[df_features[i]].str.contains('^' + test_combination[i] + '$')]
        if sub_df.shape[0] > 0:
            return sub_df
    return df


################# Check suffix and prefix ########################
def check_suffix_4(word):
    pattern4 = 'ETTE$|ETE$|EUR$|DAD$|STEVAN$|OPPOTUNE$|S[OA]{1}MINE$|REPRESENT$|[ID]{1}JAN$|NEER$|UNDERSTAND$|SUPPLY$|FINANCE$|EXPOSE$|PERU$|MODULATE$|CRIBE$|DIAGNOSE$|INTERVIEWEE$|KUMAR$|PROTECT$|MAIN$|EXTEND$|CONNECT$|REPORT$|ERSE$|TIK$|IANE$'
    pattern3 ='[^AU]IN|YN$|IAH$|ONE$|NAN$|[DG]{1}URE$|[SM]{1}ARE$|ORE$|NAM$|[AEOU]K$|[CNOP]TIVE$|[^CEI]{1}A$|I$|[^EIOU]{1}U$|[BCDFGJKLMNPRSTVXYZ]{1}O$|SONIC$|HESE$|ION$|[BCEPY]{1}OUS$|[DGKLMOSVYZ]{1}AL$|[CLT]{1}IAL$|[AGMRU]{1}NAL$|[DIU]{1}RAL$|[ACFST]{1}IAN$|[A-HJ-XZ]{1}GIAN$|[A-UW-Z]{1}IC$|[LMR]{1}ICE$|CIENT$|[ABKLNPRTUVW]{1}ISH$|LIAR$|OSIS$|SIVE$|KY$'

    if re.search(pattern4, word):
        return 4
    if re.search(pattern3, word):
        return 3
    return -1

def check_suffix_3(word):
    pattern2 = 'KY$|OSIS$|LIAR$|[ABKLNPTUVW]{1}ISH$|[AGMRU]{1}NAL$|[ACFST]{1}IAN$|[A-HJ-XZ]{1}GIAN$|[CLT]{1}IAL$|[DGKLMOSVYZ]{1}AL$|CIENT$|CEOUS$|ION$|[CNOP]TIVE$|SIVE$|[DG]{1}URE$|[ABDFGHJKLMNOPQRSTVYZ]{1}A$|[^AEGIOU]{1}U$|[^AEO]{1}I$|[^EGHIMOU]{1}O$|[A-UW-Z]{1}IC$'
    if re.search(pattern2, word):
        return 2
    return -1







################### Main Function #####################
def train(data, classifier_file):
    # put code here #
    vowel = {'AA': 0, 'AW': 1, 'AY': 2, 'ER': 3, 'EY': 4, 'IY': 5, 'OW': 6, 'OY': 7, 'UW': 8, 'AE': 9, 'AH': 10, 'AO': 11, 'EH': 12, 'IH': 13, 'UH': 14}
    consonant = {'AA': 0, 'AW': 1, 'AY': 2, 'ER': 3, 'EY': 4, 'IY': 5, 'OW': 6, 'OY': 7, 'UW': 8, 'AE': 9, 'AH': 10, 'AO': 11, 'EH': 12, 'IH': 13, 'UH': 14, 'P': 15, 'B': 16, 'CH': 17, 'D': 18, 'DH': 19, 'F': 20, 'G': 21, 'HH': 22, 'JH': 23, 'K': 24, 'L': 25, 'M': 26, 'N': 27, 'NG': 28, 'R': 29, 'S': 30, 'SH': 31, 'T': 32, 'TH': 33, 'V': 34, 'W': 35, 'Y': 36, 'Z': 37, 'ZH': 38}
    
    vowel2, vowel3, vowel4, structure_dict_2 = get_splitted_data(data, vowel, consonant)
    

    ################ df2 LR #################
    df2 = get_df_LR(vowel2)
    df2 = add_rules(df2)
    # One-Hot encoders
    # consonant_OHE
    consonant_index = []
    for x in range(39):
        consonant_index.append([x])
    consonant_index.append([100])
    consonant_OHE = OneHotEncoder()
    consonant_OHE.fit(consonant_index)
    # position_OHE
    position_index = []
    for x in range(14):
        position_index.append([x])
    position_index.append([100])
    position_OHE = OneHotEncoder()
    position_OHE.fit(position_index)
    # Structure_OHE
    structure_2_index = []
    for x in range(len(structure_dict_2)):
            structure_2_index.append([x])
    structure_2_index.append([1000])
    structure_OHE_2 = OneHotEncoder()
    structure_OHE_2.fit(structure_2_index)

    prefix_train = df2[['Target','Suffix1', 'Suffix2']]
    df2_train = build_transformed_df(df2, prefix_train, consonant_OHE, position_OHE, structure_OHE_2)
    features = list(df2_train.columns)[1:]
    X2 = df2_train[features]
    y2 = df2_train[['Target']]
    lr2 = LogisticRegression(solver = 'newton-cg', multi_class='multinomial')
    lr2.fit(X2, np.ravel(y2))
    #############################################

    df3 = get_df(vowel3, vowel, consonant)
    df4 = get_df(vowel4, vowel, consonant)
    final3 = get_final_trainset(df3, 3)
    final4 = get_final_trainset(df4, 4)
    
    file = open(classifier_file, 'wb')
    pickle.dump(vowel, file)
    pickle.dump(consonant, file)
    pickle.dump(structure_dict_2, file)
    pickle.dump(consonant_OHE, file)
    pickle.dump(position_OHE, file)
    pickle.dump(structure_OHE_2, file)
    pickle.dump(lr2, file)
    pickle.dump(final3, file)
    pickle.dump(final4, file)
    file.close()

def test(data, classifier_file):

    # load the model
    file = open(classifier_file, 'rb')
    vowel = pickle.load(file)
    consonant = pickle.load(file)
    structure_dict_2 = pickle.load(file)
    consonant_OHE = pickle.load(file)
    position_OHE = pickle.load(file)
    structure_OHE_2 = pickle.load(file)
    lr2 = pickle.load(file)
    train3 = pickle.load(file)
    train4 = pickle.load(file)
    file.close()
    
    prediction = []
    for curr_row in data[:]:
        word, removed_stress = split_to_list(curr_row)
        word, removed_stress = combined_filter(word, removed_stress, vowel)
        
        if word == 1 or removed_stress == [1]:
            prediction.append(1)
            continue
        
        num_vowel = count_vowel(removed_stress, vowel)
        
        if num_vowel <= 1: 
            ppp1 = re.compile('^NON|^MC[B-DFGHK-NP-TV-Z]{1}|^SUB|^RE|^TRAN|^PRE|^FORE|^WITH|^[AEIOU][A-Z]{1}|^DIS|^MIS[^S]|^CON|^CUR|^SUR')
            if re.search(ppp1, word):
                prediction.append(2)
            else:
                prediction.append(1)
            continue
        
        elif num_vowel == 2: ## LR

            row_data = [word, ' '.join(removed_stress)]

            vowels, vowel_positions, num_vowels, structure = get_structure_and_vowels_LR(removed_stress, vowel)
            row_data.extend(vowels)
            row_data.extend(vowel_positions)
        
            prefix_suffix = get_prefix_and_suffix(vowel_positions, removed_stress, consonant)
            row_data.extend(prefix_suffix)
            if structure in structure_dict_2:
                structure_index = structure_dict_2.get(structure)
            else:
                structure_index = 1000
            row_data.append(structure_index)
            df2 = get_df_LR([row_data])
            df2 = add_rules(df2)            
            prefix_test = df2[['Suffix1', 'Suffix2']]
            df2_test = build_transformed_df(df2, prefix_test, consonant_OHE, position_OHE, structure_OHE_2)
            curr_pred = lr2.predict(df2_test)[0]
            prediction.append(curr_pred)

        elif num_vowel == 3:
            if check_suffix_3(word) == 2:
                prediction.append(2)
                continue

            vowels, vowel_positions, structure, VowelMap, ConsonantMap, VectorMap = get_structure_and_vowels(removed_stress, vowel, consonant)
            prefix_suffix = get_prefix_and_suffix(vowel_positions, removed_stress, consonant)
            syllables = split_structure_vowel3(vowel_positions, removed_stress)
            VowelsBin = vowels_to_bin(vowels, vowel)
            PrefixSuffixBin = prefix_suffix_to_bin(prefix_suffix, consonant)
            SyllableCombination = get_combination(syllables)
            
            refined_df = get_refined_df(SyllableCombination, train3, 3)
            features = list(refined_df.columns)[7:]
            train_X = refined_df[features]
            train_y = refined_df['Target']
            test_X = VowelMap + ConsonantMap + VectorMap + VowelsBin + PrefixSuffixBin
            test_X = np.array(test_X).reshape((1,-1))

            if refined_df.shape[0] < 13:
                neigh = KNeighborsClassifier(n_neighbors = train_X.shape[0], weights = 'distance')
            else:
                neigh = KNeighborsClassifier(n_neighbors = 13, weights = 'distance')
            neigh.fit(train_X, train_y)
            curr_pred = neigh.predict(test_X)[0]
            prediction.append(curr_pred)
            
        else:
            if check_suffix_4(word) == 4:
                prediction.append(4)
                continue
            if check_suffix_4(word) == 3:
                prediction.append(3)
                continue

            vowels, vowel_positions, structure, VowelMap, ConsonantMap, VectorMap = get_structure_and_vowels(removed_stress, vowel, consonant)
            prefix_suffix = get_prefix_and_suffix(vowel_positions, removed_stress, consonant)
            syllables = split_structure_vowel4(vowel_positions, removed_stress)
            VowelsBin = vowels_to_bin(vowels, vowel)
            PrefixSuffixBin = prefix_suffix_to_bin(prefix_suffix, consonant)
            SyllableCombination = get_combination(syllables)
            
            refined_df = get_refined_df(SyllableCombination, train4, 4)
            features = list(refined_df.columns)[11:]
            train_X = refined_df[features]
            train_y = refined_df['Target']
            test_X = VowelMap + ConsonantMap + VectorMap + VowelsBin + PrefixSuffixBin
            test_X = np.array(test_X).reshape((1,-1))
            
            if refined_df.shape[0] < 15:
                # neigh = KNeighborsClassifier(n_neighbors = train_X.shape[0], weights = 'distance')
                neigh = KNeighborsClassifier(n_neighbors = 1, weights = 'distance')
            else:
                neigh = KNeighborsClassifier(n_neighbors = 15, weights = 'distance')
            neigh.fit(train_X, train_y)
            curr_pred = neigh.predict(test_X)[0]
            prediction.append(curr_pred)
    
    return prediction
        
