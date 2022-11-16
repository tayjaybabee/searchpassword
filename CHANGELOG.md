

## 11/15/22 5:51 AM

- File change history added by Taylor-Jayde Blackstone <t.blackstone@inspyre.tech>
- General readability refactorings;
  - Added constant objects to the module level:
    - INDEX_FILENAME:
        The name of the index file. No path, just name and  extension. String.
    - INDEX_FILEPATH:
        The path of the index file. Includes the file name  and path to parent directory. pathlib.Path object.
        >Note: <br>Also serves as the default index filepath provided  for the **new** :param:`index_file` parameter for the:func:`index_file`.
        
        - HASH_LIST_FILENAME:
            The name of the hash-list file. No path, just name  and extension. String.
        
        - HASH_LIST_FILEPATH:
            The path of the hash-list file. pathlib.Path object.
            
            Also serves as the default hash-list filepath  provided for the **new** :param:``hash_list_file`` 
            parameter.
            
    - Changed names in order to better fit [PEP 8](https://peps.python.org/pep-0008/) conventions:
        |  Old Name   | New Name     |
        |-------------|:-------------|
        |  beginpos   | begin_pos    |
        |  bytecount  | byte_count   |
        | currentdict | current_dict |
        |  hashindex  | hash_index   |
        |   prevpos   | prev_pos     |
        |  searchfor  | query        |
        
        > Note:
            <br>The object previously named `searchfor` wasn't renamed to `search_for`, why for?
        
    - Changed names due to the shadowing of builtin keywords:
        - dict -> _dict
    - Removed names:
        - hashfilehandle
        - indexfilehandle
- Removed file handler references, instead opting for the more  secure, more pythonic 'context manager' pattern.
