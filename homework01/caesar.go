package main

import (
	"bytes"
)

func main() {
}

func encrypt_caesar(plaintext string) string {
	word := bytes.Runes([]byte(plaintext))
	ciphertext := ""
	for i := 0; i < len(word); i++ {
		if word[i] >= 65 && word[i] <= 87 || word[i] >= 97 && word[i] <= 119 {
			word[i] += 3
		} else if word[i] >= 88 && word[i] <= 90 || word[i] >= 120 && word[i] <= 122 {
			word[i] -= 23
		}
		ciphertext += string(word[i])
	}
	return ciphertext
}

func decrypt_caesar(ciphertext string) string {
	word := bytes.Runes([]byte(ciphertext))
	plaintext := ""
	for i := 0; i < len(word); i++ {
		if word[i] >= 68 && word[i] <= 90 || word[i] >= 100 && word[i] <= 122 {
			word[i] -= 3
		} else if word[i] >= 65 && word[i] <= 67 || word[i] >= 97 && word[i] <= 99 {
			word[i] += 23
		}
		plaintext += string(word[i])
	}
	return plaintext
}
