def encrypt_caesar(plaintext):
    """
    Encrypt the message with Caesar cipher
    
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    word = [i for i in plaintext]
    ciphertext = ''
    for i in range(len(word)):
        code_of_simbol = ord(word[i])
        if 65 <= code_of_simbol <= 87 or 97 <= code_of_simbol <= 119:
            word[i] = chr(code_of_simbol + 3)
        elif 88 <= code_of_simbol <= 90 or 120 <= code_of_simbol <= 122:
            word[i] = chr(code_of_simbol - 23)
        ciphertext += word[i]
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypt the message with Caesar cipher
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    word = [i for i in ciphertext]
    plaintext = ''
    for i in range(len(word)):
        code_of_simbol = ord(word[i])
        if 68 <= code_of_simbol <= 90 or 100 <= code_of_simbol <= 122:
            word[i] = chr(code_of_simbol - 3)
        elif 65 <= code_of_simbol <= 67 or 97 <= code_of_simbol <= 99:
            word[i] = chr(code_of_simbol + 23)
        plaintext += word[i]
    return plaintext
