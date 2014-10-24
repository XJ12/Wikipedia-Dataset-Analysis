#usage: python ./getPeopleFromWikiXML.py input.xml title.txt article.txt

import sys
import xml.etree.ElementTree as ET

def main():
    tree = ET.parse(sys.argv[1])
    outlist = open(sys.argv[2], 'w')
    outtext = open(sys.argv[3], 'w')
    
    root = tree.getroot()

    i = 0
    for child in root:
        if child.tag[-4:] != 'page':
            continue
        try:
            title = child[0].text.encode('utf-8')
        except:
            continue
        revision = child[3]
        
        if revision.tag[-8:] != 'revision':
            continue

        for j in range(0, len(revision)):
            if revision[j].tag[-4:] == 'text':
                try:
                    text = revision[j].text.encode('utf-8')
                except:
                    continue
                if '{{Persondata' in text:
                    i += 1
                    if i%1000 == 0:
                        print title
                    outlist.write(title + '\n')
                    outtext.write('<title>\n' + title + '\n</title>\n')
                    outtext.write('<text>\n' + text + '\n</text>\n')
                break

    outlist.close()
    outtext.close()
    
if __name__ == '__main__':
    main()
