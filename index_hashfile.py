#! python3
import yaml  # pip install pyyaml

def buildstring(digits):
    return '%0' + str(digits) + 'X'

def index_file(digits):
    indexfilename = 'pwned-passwords-hash-index_v8.yaml'
    hashlistfilename = 'pwned-passwords-sha1-ordered-by-hash-v8.txt'

    hashfilehandle = open(hashlistfilename,'rt')
    indexfilehandle = open(indexfilename, 'wt')
    begin = []
    bytecount = []

    for hashindex in range(16**digits):
        
        searchfor = buildstring(digits) % hashindex
        print(searchfor)
        beginpos = hashfilehandle.tell()
        prevpos = beginpos
        current = hashfilehandle.readline()[0:digits]
        while searchfor == current:
            #print(searchfor + " " + current)
            #print("  " + str(hashfilehandle.tell()))
            prevpos = hashfilehandle.tell()
            current = hashfilehandle.readline()[0:digits]

        begin.append(beginpos)
        bytecount.append(prevpos - beginpos)

    print("\n\n")
    dict = {}
    dict['indexes_' + str(digits) + '_digit_hex'] = []
    currentdict = {}
    for index_num in range(len(begin)):
        currentdict[buildstring(digits) % index_num] = {
            "begin_byte": begin[index_num],
            "byte_count": bytecount[index_num]
            }
        # indexfilehandle.write(str(begin[index_num])+", "+str(bytecount[index_num])+"\n")
    dict['indexes_' + str(digits) + '_digit_hex'].append(currentdict)
    # indexfilehandle.write(yaml.dump(dict,sort_keys=False))
    indexfilehandle.write(yaml.dump(dict))

    hashfilehandle.close()
    indexfilehandle.close()
    print(dict)

def main():
    digits = 3
    print("File will be split " + str(16**digits) + " ways.")
    index_file(digits)

if __name__ == "__main__":
    main()
