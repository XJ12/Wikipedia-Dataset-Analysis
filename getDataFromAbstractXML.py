#usage: python ./getPeopleFromWikiXML.py input.xml title.txt article.txt

import sys
import re

def main():
    inabstract = open(sys.argv[1])
    inpeople = open(sys.argv[2])
    outdata = open(sys.argv[3], 'w')
    
    people_lst = map(lambda s:s.strip('\n'), inpeople.readlines())
    
    state = 0
    for line in inabstract:
        if line[0:6] == '<feed>' or line[0:7] == '</feed>':
            continue
        
        if line[0:5] == '<url>':
            continue
        
        if line[0:5] == '<doc>':
            state = 1
            title = ''
            abstract = ''
            is_people = 0
            keywords_lst = []
            continue
            
        if line[0:7] == '<title>' and state == 1:
            state = 2
            title = line[18:-9]
            if title in people_lst:
                is_people = 1
                
            continue
        
        if line[0:10] == '<abstract>' and state == 2:
            abstract = re.sub(r'\W', ' ', line[10:-11])
            continue
        
        if line[0:7] == '<links>' and state == 2:
            state = 3
            continue
        
        if line[0:8] == '<sublink' and state == 3:
            start = line.find('<anchor>') + 8
            end = line.find('</anchor>')
            key_word = line[start:end]
            keywords_lst.append(key_word)
            continue
        
        if line[0:8] == '</links>' and state == 3:
            state = 4
            continue
        
        if line[0:6] == '</doc>' and state == 4:
            state = 0
            entry = []
            entry.append(title)
            entry.append(str(is_people))
            entry.extend(keywords_lst)
            entry.append(abstract)
            
            outdata.write(','.join(entry) + '\n')
    
    
    
    
    inabstract.close()
    inpeople.close()
    outdata.close()
    
    
if __name__ == '__main__':
    main()
