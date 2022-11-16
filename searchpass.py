#! python3
import yaml   # pip install pyyaml
import hashlib
from getpass import getpass

def indexfile_dict(indexfilename):
    with open(indexfilename,'rt') as indexfilehandle:
        dict = yaml.safe_load(indexfilehandle.read())
    digits = 0
    for item in dict:
        if item[:8].lower() == 'indexes_':
            dict = dict[item][0]
            digits = int(item[8])
    return dict, digits

def ask_password():
    return getpass('Password? (Just press Enter to quit) ')

def sha1sum_password(password):
    hash = hashlib.sha1(password.encode('utf-8'))
    return hash.hexdigest().upper()

def segment(dict, sha, digits):
    fewdigits = sha[:digits]
    begin = dict[fewdigits]["begin_byte"]
    length = dict[fewdigits]["byte_count"]

    return begin, length

def read_segment(hashfilehandle, sha, begin, length, digits):
    hashfilehandle.seek(begin, 0)
    end = begin + length
    pos = hashfilehandle.tell()
    match = False
    while pos < end and not match:
        line = hashfilehandle.readline()
        pos = hashfilehandle.tell()
        if sha[:digits].upper() != line[:digits].upper():
            print(
                f"Error: Need to run index_hashfile.py or there is a bug. Searching for {sha[:digits].upper()} on line: "
            )

            print(line)
            break
        if sha.upper() == line[:40].upper():
            match = True
            print("Match found:")
            print(line)
            break
    if not match:
        print("Match not found.\n")

def main():
    indexfilename = 'pwned-passwords-hash-index_v8.yaml'
    hashlistfilename = 'pwned-passwords-sha1-ordered-by-hash-v8.txt'
    with open(hashlistfilename,'rt') as hashfilehandle:
        print(f"Reading {indexfilename}")
        dict = indexfile_dict(indexfilename)
        digits = dict[1]
        dict = dict[0]
        # print(dict)
        print("")

        password = " "
        while password != "":
            password = ask_password()
            if len(password) < 1:
                break
            sha = sha1sum_password(password)
                    # password = ""
            print(f"Looking for SHA1SUM: {sha}")
            begin = segment(dict, sha, digits)[0]
            length = segment(dict, sha, digits)[1]
            read_segment(hashfilehandle, sha, begin, length, digits)

if __name__ == "__main__":
    main()
