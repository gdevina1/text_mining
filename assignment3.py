import urllib.request
import string
import os
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import math

url = 'http://www.gutenberg.org/cache/epub/28/pg28.txt'
response = urllib.request.urlopen(url)
data = response.read()  # a `bytes` object
text = data.decode('utf-8')
# os.chdir(r"c:\Users\gdevina1\Documents\GitHub\text_mining")
# cwd = os.getcwd()
# print(cwd)
#print(text) # for testing

def process_online_text(text, skip_header):
    """
    Makes a histogram that contains the words from a gutenberg online source file.

    filename: string
    skip_header: boolean, whether to skip the Gutenberg header
    
    returns: map from each word to the number of times it appears.
    """
    hist = {}

    if skip_header:
        text = skip_gutenberg_start_end(text)

    text = text.split()
    # text = map(toLowerCase,text)

    for i in text:
        i = i.replace('-', ' ')
        strippables = string.punctuation + string.whitespace

        for word in i.split():
            # remove punctuation and convert to lowercase
            word = word.strip(strippables)
            word = word.lower()

            # update the histogram
            hist[word] = hist.get(word, 0) + 1

    return hist

def process_file(filename, skip_header):
    """Makes a histogram that contains the words from a local file.

    filename: string
    skip_header: boolean, whether to skip the Gutenberg header

    returns: map from each word to the number of times it appears.
    """
    hist = {}
    fp = open(filename, encoding='utf8')

    if skip_header:
        skip_gutenberg_header(fp)

    for line in fp:
        strippables = string.punctuation + string.whitespace

        for word in line.split():
            # remove punctuation and convert to lowercase
            word = word.strip(strippables)
            word = word.lower()

            # update the histogram
            hist[word] = hist.get(word, 0) + 1

    return hist

def skip_gutenberg_start_end(text):
    """
    Reads from text until it finds the line that ends the header.

    text: open file object

    returns: remaining text starting from 'start' and ends with 'end'
    """
    start = "The Man, the Boy, and the Donkey        The Fox and the Goat"
    i = text.find(start)
    end = "End of the Project Gutenberg EBook of Aesop's Fables, by Aesop"
    x = text.find(end)

    return text[i+(len(start)):x]

def extract_fable(text,start,end):
    """
    Reads from text until it finds the line that ends the header.

    text: open file object
    start: string in text
    end: string in text

    returns: remaining text starting from 'start' and ends with 'end'
    """
    i = text.find(start)
    x = text.find(end)

    return text[i+(len(start)):x+(len(end))]

def compare(hist,animals):
    """
    Finds matches of keys in hist and keys in animals, iterates while counting frequency of word appearance.

    hist = map from word to frequency
    animals = text file of list of animals

    returns = list of frequency,word pairs
    """
    match = {}
    for key in animals:
        if key in hist:
            match[key] = hist.get(key, 0)
    return match

def no_stop_words(hist, key):
    """
    Deletes stop words from dictionary

    hist = map from word to frequency
    key = elements to delete

    returns = list of frequency,word pairs
    """
    hist2 = hist.copy()
    for i in key:
        if i in hist2:
            del hist2[i]
    return hist2

def sentiment_analysis(text):
    score = SentimentIntensityAnalyzer().polarity_scores(text)
    #return the polarity score of the text
    return score

def most_common(hist):
    """Makes a list of word-freq pairs in descending order of frequency.

    hist: map from word to frequency

    returns: list of (frequency, word) pairs
    """
    t = []
    # remove word from filtered_word_list if it is a stop word
    for key, value in hist.items():
        t.append((value, key))
    t.sort()
    t.reverse()
    return t

def most_common_all(hist):
    """
    Prints a list of word-freq pairs in descending order of frequency.

    hist: map from word to frequency

    prints: list of (frequency, word) pairs
    """
    t = []
    for key, value in hist.items():
        t.append((value, key))
    t.sort()
    t.reverse()

    for value, key in t:
        print("{:14}{}".format(key, value))


def most_common_limited(hist, num=10):
    """
    Prints the most commons words in a histogram and their frequencies.

    hist: histogram (map from word to frequency)
    num: number of words to print
    """
    t = most_common(hist)
    for freq, word in t[:num]:
        print("{:14}{}".format(word, freq))

def total_words(hist):
    """
    Returns the total of the frequencies in a histogram.
    """
    return sum(hist.values())

def numerator(fable_one, fable_two):
    """
    Calculates the numerator of cosine similarity function using 

    fable_one: histogram
    fable_two: histogram
    
    returns = number
    """
    num = 0
    for word in fable_one:
        if word in fable_two:
             num += fable_one[word]*fable_two[word]
    return num

def cosine_similarity(fable_one, fable_two):
    """
    Calculates cosine similarity of two texts (histograms)

    fable_one: histogram
    fable_two: histogram

    returns = number 
    """
    num = numerator(fable_one, fable_two)
    denom = math.sqrt(numerator(fable_one,fable_two)*numerator(fable_two,fable_two))
    return math.acos(num/denom)

def main():
    hist = process_online_text(text,True)
    animals = list(process_file('animals.txt', False).keys())
    animals.remove(animals[0])
    # print(animals)
    # print(compare(hist, animals))
    hist2 = hist.copy()
    # print(hist2)
    # print(no_stop_words(hist2))
    # most_common(hist)
    # print(no_stop_words(hist2,stop_words))
    stop_words = stopwords.words('english')
    print("")
    print("The most common words in the text (without stop words) are:")
    most_common_limited(no_stop_words(hist2,stop_words))
    print("")
    print("------------------------------------------------------------")
    print("")
    print("List of all the animals appearing in Aesop's Fables")
    most_common_all(compare(hist,animals))
    print("")
    print("Total number of animals appearing in text: ", total_words(compare(hist,animals)))
    print("------------------------------------------------------------")
    print("")
    print("Total number of words in Aesop's Fables collection: ", total_words(hist))
    print("Percentage of total words in text that are animals: {0:.2f}%" .format(total_words(compare(hist,animals))/total_words(hist) *100))
    print("")
    print("------------------------------------------------------------")
    tabcon= extract_fable(text,start="1-21                                    22-42",end="The Fox and the Goat")
    tableofcontents = process_online_text(tabcon,False)
    # print(tableofcontents)
    print("")
    print("The 5 most common animals in the Aesop's Fables' titles:")
    most_common_limited(compare(tableofcontents,animals),num=5)
    print("")
    print("------------------------------------------------------------")
    print("")
    print("The 5 most common animals in the entire text:")
    most_common_limited(compare(hist,animals),num=5)
    print("")
    print("------------------------------------------------------------")
    hare_and_tortoise = extract_fable(text, start="It is easy to propose impossible remedies.", end="Plodding wins the race.")
    hist_hare_and_tortoise = process_online_text(hare_and_tortoise,False)
    wolf_sheep_clothing = extract_fable(text, start="you cannot reckon.", end="Appearances are deceptive.")
    hist_wolf_sheep_clothing = process_online_text(wolf_sheep_clothing,False)
    fox_and_grapes = extract_fable(text,start="Nothing escapes the master's eye.", end="It is easy to despise what you cannot get.")
    hist_fox_and_grapes = process_online_text(fox_and_grapes,False)
    print("")
    print("Sentiment analysis results of The Hare and The Tortoise:")
    print(sentiment_analysis(hare_and_tortoise))
    print("")
    print("Sentiment analysis results of The Wolf in Sheep's Clothing")
    print(sentiment_analysis(wolf_sheep_clothing))
    print("")
    print("Setiment analysis of The Fox and the Grapes")
    print(sentiment_analysis(fox_and_grapes))
    print("")
    print("------------------------------------------------------------")
    print("")
    print ("The Hare and The Tortoise and The Wolf in Sheep's Clothing is {:.2f}% similar.".format(cosine_similarity(hist_hare_and_tortoise,hist_wolf_sheep_clothing)/(math.pi/2)))
    print("")
    print("The Hare and The Tortoise and The Fox and the Grapes is {:.2f}% similar.".format(cosine_similarity(hist_hare_and_tortoise,hist_fox_and_grapes)/(math.pi/2)))
    print("")
    print("The Fox and the Grapes and The Wolf in Sheep's Clothing is {:.2f}% similar.".format(cosine_similarity(hist_wolf_sheep_clothing,hist_fox_and_grapes)/(math.pi/2)))
    print("")
    print("------------------------------------------------------------")
    print("END OF ANALYSIS")
    print("------------------------------------------------------------")
    

if __name__ == '__main__':
    main()