package main

import (
	"bytes"
	"strings"
)

func main() {
}
func encrypt_vigener(plaintext string, keywords string) string {
	word := bytes.Runes([]byte(plaintext))
	keywords = strings.Repeat(keywords, len(plaintext)/len(keywords)+1)
	keys := bytes.Runes([]byte(keywords))
	ciphertext := ""
	for i := 0; i < len(word); i++ {
		if 65 <= keys[i] && keys[i] <= 90 {
			keys[i] -= 65
		} else if 97 <= keys[i] && keys[i] <= 122 {
			keys[i] -= 97
		}
		if 65 <= word[i] && word[i] <= 90-keys[i] || 97 <= word[i] && word[i] <= 122-keys[i] {
			word[i] += keys[i]
		} else if 90-keys[i] < word[i] && word[i] <= 90 || 122-keys[i] < word[i] && word[i] <= 122 {
			word[i] += keys[i] - 26
		}
		ciphertext += string(word[i])
	}
	return ciphertext
}
