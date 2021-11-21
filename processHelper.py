#Import libraries 
import re

def processFile(file, name):
    file = updateChars(file)
    words, lineCounts, maxWordsSentence, minWordsSentence, file = removeSplit(file)

    #Write the name to the output file
    output_name = 'processed-text-' + name 
    output_file = open('preprocessed/' + output_name, 'w')
    output_file.write(file)

    countSyllables(file, words, lineCounts, maxWordsSentence, minWordsSentence, name)


def updateChars(f):
    #Replace all punctuation markers with newline characters and convert all characters to lowercase 
    f = f.replace("?", "\n").replace(".", "\n").replace("!", "\n").replace(":", "\n")
    f= f.lower()

    #Resurface the vowels
    f = f.replace("'s", " is").replace("'t", " not").replace("'m", " am").replace("'ve", " have").replace("'re", " are").replace("'ll'", " will")

    #Remove all non-alphabet characters
    f = re.sub(r'[^a-z\n ]', '', f)

    return f


def removeSplit(file):
    #Remove empty lines
    file2 = ''
    lineCounts = 0
    maxWordsSentence = 0
    minWordsSentence = 10000
    sumWords = 0

    #Split the file into a list of words and remove any empty lines 
    lines = file.split("\n")

    non_empty_lines = [
                        line for line in lines 
                        if line.strip() != ''
                        ]

    for line in non_empty_lines:
        file2 += line + "\n"
        lineCounts += 1
        
        #Calculate sentence and word metrics
        temp = line.split(" ")
        maxWordsSentence = max(maxWordsSentence, len(temp))
        minWordsSentence = min(minWordsSentence, len(temp))
        sumWords += len(temp)

    words = file2.split()
    return words, lineCounts, maxWordsSentence, minWordsSentence, file2


def countSyllables(f, words, lineCounts, maxWordsSentence, minWordsSentence, name):
    temp = []
    maxS = 0
    minS = 100
    sumS = 0


    for i in words:  
        #This code segment prepares the word of syllable counting 
        #Exception to following line if 'yer' or 'yers'
        #When y appears together with a vowel, ignore y (e.g., "ya" and "oy")
        if(i.endswith('yer') or i.endswith('yers') or re.search('[aeiou]y', str(i))):
            temp.append(i)
            #print('1' + i)
        
        #y appears in a sequence of a vowel followed by y and e, remove the last e
        elif(re.search('[aeiou]ye', str(i))):
            i.replace('[aeiou]ye', 'y')
            temp.append(i)

        #This section of the code actually counts the syllables in each word after processing
        numSyl = len(re.findall('[aeiou]', i))
        
        #When two vowels appear together, treat them as one vowel (e.g., "ea" -> "e")
        if(re.search('[aeiou][aeiou]', str(i))):
            i = re.sub('[aeiou][aeiou]', 'a', str(i))
            numSyl -= 1

        #When y appears after a consonant, treat y as a vowel
        if(re.search('[b-df-hj-np-tv-xz]y', str(i))):
            numSyl += 1
            temp.append(i)
     
        suffixList = ['ce', 'de', 'fe', 'ge', 'he', 'ke', 'me', 'ne', 'pe', 'qe', 're', 'se', 'te', 've', 'we', 'xe', 'ze']     #Syllables counting phase 
        if(i.endswith('e')):
            if(len(i) == 2 or len(i) == 3):
                numSyl -= 1
            elif(i[-2:] in suffixList):
                numSyl -= 1
        
        if(numSyl < 1 and len(i)):
            numSyl = 1
        
        #print('The number of syllables in {z} is {l}'.format(z=i, l=numSyl))
        maxS = max(maxS, numSyl)
        minS = min(minS, numSyl)
        sumS += numSyl
        
    avgS = sumS / len(words)
    total_num_words = len(words)
    
    # output_name = 'output-' + name 
    # output_file = open('output/' + output_name, 'w')

    # output_file.write('File: {output_name}\n'.format(output_name=name))
    # output_file.write('Total number of words: {totalWords}\n'.format(totalWords=len(words)))
    # output_file.write('Max number of syllables: {maxS}\n'.format(maxS=maxS))
    # output_file.write('Min number of syllables: {minS}\n'.format(minS=minS))
    # output_file.write('Avg number of syllables: '+ str(round(avgS,2)) + '\n')

    # output_file.close()

    # print('Total number of words: {totalWords}'.format(totalWords=len(words)))
    # print('Max number of syllables: {maxS}'.format(maxS=maxS))
    # print('Min number of syllables: {minS}'.format(minS=minS))
    # print('Avg number of syllables: '+ str(round(avgS,2)))
    
    countSen(sumS, lineCounts, maxWordsSentence, minWordsSentence, words, name)
    scoreFlesch(total_num_words, sumS, lineCounts, words, name)
    

def countSen(sumS, lineCounts, maxWordsSentence, minWordsSentence, words, name):
    avgSentence = len(words) / lineCounts

    output_name = 'output-' + name 
    output_file = open('output/' + output_name, 'a')

    output_file.write('Total number of sentences: {lineCounts}\n'.format(lineCounts=lineCounts))
    output_file.write('Max number of words in a sentence: {maxWordsSentence}\n'.format(maxWordsSentence=maxWordsSentence))
    output_file.write('Min number of words in a sentence: {minWordsSentence}\n'.format(minWordsSentence=minWordsSentence))
    output_file.write('Avg number of words across all sentences: ' + str(round(avgSentence, 2)) + '\n')

    output_file.close()

    # print('Total number of sentences: {lineCounts}'.format(lineCounts=lineCounts))
    # print('Max number of words in a sentence: {maxWordsSentence}'.format(maxWordsSentence=maxWordsSentence))
    # print('Min number of words in a sentence: {minWordsSentence}'.format(minWordsSentence=minWordsSentence))
    # print('Avg number of words across all sentences: ' + str(round(avgSentence, 2)))


def scoreFlesch(total_num_words, sumS, lineCounts, words, name):
    word_difficulty = (sumS / total_num_words)
    sentence_difficulty = total_num_words / lineCounts

    FRES = 206.835 - 1.015 * sentence_difficulty - 84.6 * word_difficulty
    
    output_name = 'output-' + name 
    output_file = open('output/' + output_name, 'a')
    output_file.write('FRES score: ' + str(round(FRES,2)))
    output_file.close()

    # print('Word difficulty score: {word_difficulty}'.format(word_difficulty=word_difficulty))
    # print('Sentence difficulty score: {sentence_difficulty}'.format(sentence_difficulty=sentence_difficulty))
    # print('FRES score: ' + str(round(FRES,2))) 
    # print('\n')

