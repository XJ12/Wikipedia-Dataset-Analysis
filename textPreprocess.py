import sys
import re
import nltk

stopwords = nltk.corpus.stopwords.words('english')
stopwords_wiki = ['see also', 'references', 'further reading', 'external links',
                  'additional references', 'additional references' ]

def HasStopwordsWiki(words):
    label = False
    
    for i in range(0, len(stopwords_wiki)):
        if words.find(stopwords_wiki[i]) >= 0:
            label = True
            break
        
    return label

def ProcessWords(words):
    lmtzr = nltk.stem.wordnet.WordNetLemmatizer()
    words = re.sub(r'\W', ' ', words).replace('_', ' ').lower()
    word_lst = words.split(' ')
    word_lst_new = []
        
    for j in range(0, len(word_lst)):
        word = word_lst[j]
            
        if word in stopwords or word == '':
            continue
            
        word_new = lmtzr.lemmatize(word)
        word_lst_new.append(word_new)
        
    words_new = ' '.join(word_lst_new)
    
    return words_new
    
    

def ProcessContents(contents):
    contents_new = []
    
    for i in range(0, len(contents)):
        words = re.sub(r'\W', ' ', contents[i]).lower()
        
        if HasStopwordsWiki(words):
            continue
        
        words_new = ProcessWords(words)
        
        if len(words_new) == 0:
            continue

        contents_new.append(words_new)
        
    return contents_new

def main():
    infile = open(sys.argv[1])
    outfile = open(sys.argv[2], 'w')
    
    for line in infile:
        fields = line.strip('\n').split(',')
        title = fields[0]
        label = fields[1]
        contents = fields[2:-1]
        abstract = fields[-1]
        
        contents_new = ProcessContents(contents)
        abstract_new = ProcessWords(abstract)
        
        line_new = []
        line_new.append(title)
        line_new.append(label)
        line_new.extend(contents_new)
        line_new.append(abstract_new)
        line_new = ','.join(line_new) + '\n'
        
        outfile.write(line_new)

    
    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
