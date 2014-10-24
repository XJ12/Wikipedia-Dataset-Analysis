import sys

def main():
    infile = open(sys.argv[1])
    label_out = int(sys.argv[2])
    word_num = int(sys.argv[3])
    outfile_base = sys.argv[4]
    
    counts_people = {}
    counts_nonpeople = {}
    
    i = 0
    for line in infile:
        fields = line.strip('\n').split(',')
        label_in = int(fields[1])
        contents = ' '.join(fields[2:])
        words = contents.split(' ')
        
        for word in words:
            if len(word) <= 2:
                continue
            
            if label_in == 0:
                if counts_nonpeople.has_key(word):
                    counts_nonpeople[word] += 1
                else:
                    counts_nonpeople[word] = 1
            elif label_in == 1:
                if counts_people.has_key(word):
                    counts_people[word] += 1
                else:
                    counts_people[word] = 1
        
        i += 1
        
        if i%100000 == 0:
            print '%s lines processed...' % (i)
            
        
    counts_people = sorted(counts_people.items(), key=lambda x: x[1], reverse=True)
    counts_nonpeople = sorted(counts_nonpeople.items(), key=lambda x: x[1], reverse=True)
    
    outpeople = open(outfile_base+'_people.txt', 'w')
    print '#################Top %s words about people#################' % (word_num) 
    for i in range(0, word_num):
        print '%s, %s' % (counts_people[i][0], counts_people[i][1])
        outpeople.write((counts_people[i][0] + ', ')*int(round(1.0*counts_people[i][1]/5000)) + '\n')
            
    
    outnonpeople = open(outfile_base+'_nonpeople.txt', 'w')
    print '#################Top %s words about non-people#################' % (word_num)
    for i in range(0, word_num):
        print '%s, %s' % (counts_nonpeople[i][0], counts_nonpeople[i][1])
        outnonpeople.write((counts_nonpeople[i][0] + ', ')*int(round(1.0*counts_nonpeople[i][1]/5000)) + '\n')


    outpeople.close()
    outnonpeople.close()

if __name__ == '__main__':
    main()
