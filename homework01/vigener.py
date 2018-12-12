def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    word = [i for i in plaintext]
    keys = [i for i in keyword*(len(plaintext)//len(keyword)+1)]
    ciphertext = ''
    for i in range(len(word)):
        code_of_simbol = ord(word[i])
        code_of_key = ord(keys[i])
        if 65 <= code_of_key <= 90:
            code_of_key -= 65
        elif 97 <= code_of_key <= 122:
            code_of_key -= 97
        if 65 <= code_of_simbol <= 90 - code_of_key or 97 <= code_of_simbol <= 122 - code_of_key:
            word[i] = chr(code_of_simbol + code_of_key)
        elif 90 - code_of_key < code_of_simbol <= 90 or 122 - code_of_key < code_of_simbol <= 122:
            word[i] = chr(code_of_simbol + code_of_key - 26)
        ciphertext += word[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    word = [i for i in ciphertext]
    keys = [i for i in keyword * (len(ciphertext) // len(keyword) + 1)]
    ciphertext = ''
    for i in range(len(word)):
        code_of_simbol = ord(word[i])
        code_of_key = ord(keys[i])
        if 65 <= code_of_key <= 90:
            code_of_key -= 65
        elif 97 <= code_of_key <= 122:
            code_of_key -= 97
        if 65 + code_of_key <= code_of_simbol <= 90 or 97 + code_of_key <= code_of_simbol <= 122:
            word[i] = chr(code_of_simbol - code_of_key)
        elif 65 <= code_of_simbol < 65 + code_of_key or 97 <= code_of_simbol < 97 + code_of_key:
            word[i] = chr(code_of_simbol - code_of_key + 26)
        ciphertext += word[i]
    return ciphertext


