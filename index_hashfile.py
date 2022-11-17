#!/usr/bin/env python3

from __future__ import annotations
import yaml  # pip install pyyaml
from dill import dump
from pathlib import Path
from tqdm import trange


FILE_DIR = Path(__file__).parent

INDEX_FILENAME = 'pwned-passwords-hash-index_v8.yaml'
INDEX_FILEPATH = FILE_DIR.joinpath(INDEX_FILENAME)

HASH_LIST_FILENAME = 'pwned-passwords-sha1-ordered-by-hash-v8.txt'
HASH_LIST_FILEPATH = FILE_DIR.joinpath(HASH_LIST_FILENAME)


def build_string(digits):
    return f'%0{str(digits)}X'


def index_file(
        digits,
        index_fp: (str | Path) = INDEX_FILEPATH,
        hash_list_file: (str | Path) = HASH_LIST_FILEPATH
):
    index_fp = index_fp
    hash_list_fp = hash_list_file

    with open(hash_list_fp, 'rt') as hf:
        begin = []
        byte_count = []

        for hash_index in trange(16 ** digits):

            query = build_string(digits) % hash_index
            # print(query)
            begin_pos = hf.tell()
            prev_pos = begin_pos
            current = hf.readline()[:digits]
            while query == current:
                # print(searchfor + " " + current)
                # print("  " + str(hashfilehandle.tell()))
                prev_pos = hf.tell()
                current = hf.readline()[:digits]

            begin.append(begin_pos)
            byte_count.append(prev_pos - begin_pos)

        # print("\n\n")
        _dict = {
                f'indexes_{str(digits)}_digit_hex': []
        }
        current_dict = {
                build_string(digits) % index_num: {
                        "begin_byte": begin[index_num],
                        "byte_count": byte_count[index_num]
                } for index_num in range(len(begin))
        }

        _dict[f'indexes_{str(digits)}_digit_hex'].append(current_dict)
        # indexfilehandle.write(yaml.dump(dict,sort_keys=False))

    with open(index_fp, 'w') as ifp:
        ifp.write(yaml.dump(_dict))

    with open(Path('./index.pkl').resolve(), 'wb') as file:
        dump(_dict, file)


def main():
    digits = 3
    print(f"File will be split {str(16 ** digits)} ways.")
    index_file(digits)


if __name__ == "__main__":
    main()

"""
File Change History:

    - 11/15/22 5:51 AM:
        - File change history added by Taylor-Jayde Blackstone <t.blackstone@inspyre.tech>
        - General readability refactorings;
            - Added constant objects to the module level:
                - INDEX_FILENAME:
                    The name of the index file. No path, just name and extension. String.

                - INDEX_FILEPATH:
                    The path of the index file. Includes the file name and path to parent directory. pathlib.Path 
                    object.

                    Also serves as the default index filepath provided for the **new** :param:`index_file` parameter.

                - HASH_LIST_FILENAME:
                    The name of the hash-list file. No path, just name and extension. String.

                - HASH_LIST_FILEPATH:
                    The path of the hash-list file. pathlib.Path object.

                    Also serves as the default hash-list filepath provided for the **new** :param:'hash_list_file` 
                    parameter.

            - Changed names in order to better fit (PEP 8)[https://peps.python.org/pep-0008/] conventions:
                - bytecount -> byte_count
                - hashindex -> hash_index
                - searchfor -> query 
                - beginpos -> begin_pos
                - prevpos -> prev_pos
                - currentdict -> current_dict
            - Changed names due to the shadowing of builtin keywords:
                - dict -> _dict
            - Removed names:
                - hashfilehandle -> Replaced with context manager
                - indexfilehandle -> Replaced with context manager
        - Removed file handler references, instead opting for the more secure, more pythonic 'context manager' pattern.

"""
