

## Import some modules
import numpy as np
import pandas as pd
import helper
import submission
import re
import pickle
from sklearn.neighbors import KNeighborsClassifier

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

def combined_filter(word, removed_stress, vowel):
    
    word, removed_stress = singular_filter(word, removed_stress)
    if len(word) == 0 or len(removed_stress) == 0: 
        return 1, [1]
    
    word, removed_stress = neutral_filter1(word, removed_stress)
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
        elif num_vowel == 2:
            vowels, vowel_positions, structure, VowelMap, ConsonantMap, VectorMap = get_structure_and_vowels(removed_stress, vowel, consonant)
            prefix_suffix = get_prefix_and_suffix(vowel_positions, removed_stress, consonant)
            syllables = split_structure_vowel2(vowel_positions, removed_stress)
            row_data = [target, word, vowels, prefix_suffix, VowelMap, ConsonantMap, VectorMap, syllables]
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
    
    return vowel2, vowel3, vowel4

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

################### Main Function #####################
def train(data, classifier_file):
    # put code here #
    vowel = {'AA': 0, 'AW': 1, 'AY': 2, 'ER': 3, 'EY': 4, 'IY': 5, 'OW': 6, 'OY': 7, 'UW': 8, 'AE': 9, 'AH': 10, 'AO': 11, 'EH': 12, 'IH': 13, 'UH': 14}
    consonant = {'AA': 0, 'AW': 1, 'AY': 2, 'ER': 3, 'EY': 4, 'IY': 5, 'OW': 6, 'OY': 7, 'UW': 8, 'AE': 9, 'AH': 10, 'AO': 11, 'EH': 12, 'IH': 13, 'UH': 14, 'P': 15, 'B': 16, 'CH': 17, 'D': 18, 'DH': 19, 'F': 20, 'G': 21, 'HH': 22, 'JH': 23, 'K': 24, 'L': 25, 'M': 26, 'N': 27, 'NG': 28, 'R': 29, 'S': 30, 'SH': 31, 'T': 32, 'TH': 33, 'V': 34, 'W': 35, 'Y': 36, 'Z': 37, 'ZH': 38}
    
    vowel2, vowel3, vowel4 = get_splitted_data(data, vowel, consonant)
    df2 = get_df(vowel2, vowel, consonant)
    df3 = get_df(vowel3, vowel, consonant)
    df4 = get_df(vowel4, vowel, consonant)
    final2 = get_final_trainset(df2, 2)
    final3 = get_final_trainset(df3, 3)
    final4 = get_final_trainset(df4, 4)
    
    return final2, final3, final4

def test(data, classifier_file):

    # load the model
    file = open(classifier_file, 'rb')
    vowel = pickle.load(file)
    consonant = pickle.load(file)
    train2 = pickle.load(file)
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
            prediction.append(1)
            continue
        
        elif num_vowel == 2:
            vowels, vowel_positions, structure, VowelMap, ConsonantMap, VectorMap = get_structure_and_vowels(removed_stress, vowel, consonant)
            prefix_suffix = get_prefix_and_suffix(vowel_positions, removed_stress, consonant)
            syllables = split_structure_vowel2(vowel_positions, removed_stress)
            VowelsBin = vowels_to_bin(vowels, vowel)
            PrefixSuffixBin = prefix_suffix_to_bin(prefix_suffix, consonant)
            SyllableCombination = get_combination(syllables)
            
            refined_df = get_refined_df(SyllableCombination, train2, 2)
            features = list(refined_df.columns)[4:]
            train_X = refined_df[features]
            train_y = refined_df['Target']
            test_X = VowelMap + ConsonantMap + VectorMap + VowelsBin + PrefixSuffixBin
            test_X = np.array(test_X).reshape((1,-1))
            
            if refined_df.shape[0] < 5:
                neigh = KNeighborsClassifier(n_neighbors = train_X.shape[0], weights = 'distance')
            else:
                neigh = KNeighborsClassifier(n_neighbors = 5, weights = 'distance')
            neigh.fit(train_X, train_y)
            curr_pred = neigh.predict(test_X)[0]
            prediction.append(curr_pred) 
            
        elif num_vowel == 3:
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

            if refined_df.shape[0] < 6:
                neigh = KNeighborsClassifier(n_neighbors = train_X.shape[0], weights = 'distance')
            else:
                neigh = KNeighborsClassifier(n_neighbors = 6, weights = 'distance')
            neigh.fit(train_X, train_y)
            curr_pred = neigh.predict(test_X)[0]
            prediction.append(curr_pred)
            
        else:
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
            
            if refined_df.shape[0] < 13:
                neigh = KNeighborsClassifier(n_neighbors = train_X.shape[0], weights = 'distance')
            else:
                neigh = KNeighborsClassifier(n_neighbors = 13, weights = 'distance')
            neigh.fit(train_X, train_y)
            curr_pred = neigh.predict(test_X)[0]
            prediction.append(curr_pred)
    
    return prediction
        
