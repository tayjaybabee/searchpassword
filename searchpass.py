#! python3
import yaml   # pip install pyyaml
import hashlib
from getpass import getpass

def indexfile_dict(indexfilename):
    indexfilehandle = open(indexfilename,'rt')
    dict = yaml.safe_load(indexfilehandle.read())
    indexfilehandle.close()
    digits = 0
    for item in dict:
        if item[0:8].lower() == 'indexes_':
            dict = dict[item][0]
            digits = int(item[8])
    return dict, digits

def ask_password():
    password = getpass('Password? (Just press Enter to quit) ')
    return password

def sha1sum_password(password):
    hash = hashlib.sha1(password.encode('utf-8'))
    sha = hash.hexdigest().upper()
    return sha

def segment(dict, sha, digits):
    fewdigits = sha[0:digits]
    begin = dict[fewdigits]["begin_byte"]
    length = dict[fewdigits]["byte_count"]

    return begin, length

def read_segment(hashfilehandle, sha, begin, length, digits):
    hashfilehandle.seek(begin, 0)
    end = begin + length
    pos = hashfilehandle.tell()
    match = False
    while pos < end and match == False:
        line = hashfilehandle.readline()
        pos = hashfilehandle.tell()
        if sha[0:digits].upper() != line[0:digits].upper():
            print("Error: Need to run index_hashfile.py or there is a bug. Searching for " + sha[0:digits].upper() + " on line: ")
            print(line)
            break
        if sha.upper() == line[0:40].upper():
            match = True
            print("Match found:")
            print(line)
            break
    if match == False:
        print("Match not found.\n")

def main():
    indexfilename = 'pwned-passwords-hash-index_v8.yaml'
    hashlistfilename = 'pwned-passwords-sha1-ordered-by-hash-v8.txt'
    hashfilehandle = open(hashlistfilename,'rt')
    print("Reading " + indexfilename)
    dict = indexfile_dict(indexfilename)
    digits = dict[1]
    dict = dict[0]
    # print(dict)
    print("")

    password = " "
    while len(password) > 0:
        password = ask_password()
        if len(password) < 1:
            break
        sha = sha1sum_password(password)
        # password = ""
        print("Looking for SHA1SUM: " + sha)
        begin = segment(dict, sha, digits)[0]
        length = segment(dict, sha, digits)[1]
        read_segment(hashfilehandle, sha, begin, length, digits)
    hashfilehandle.close()

if __name__ == "__main__":
    main()
