package main

import (
	"errors"
	"math/rand"
)

type Key struct {
	key int
	n   int
}

type KeyPair struct {
	Private Key
	Public  Key
}

func main() {
}

func is_prime(n int) bool {
	var dividers int
	for i := 1; i < n; i++ {
		if n%i == 0 {
			dividers += 1
		}
	}
	if dividers == 1 {
		return true
	} else {
		return false
	}
}

func gcd(a int, b int) int {
	for a != b {
		if a > b {
			a -= b
		} else {
			b -= a
		}
	}
	return a
}

func multiplicative_inverse(e int, phi int) int {
	var a = []int{phi}
	var b = []int{e}
	var a_mod_b = []int{phi % e}
	var a_div_b = []int{phi / e}
	var x = []int{0}
	var y = []int{1}
	var i = 0
	for a[i]%b[i] != 0 {
		a = append(a, b[i])
		b = append(b, a_mod_b[i])
		a_mod_b = append(a_mod_b, a[i+1]%b[i+1])
		a_div_b = append(a_div_b, a[i+1]/b[i+1])
		i += 1
	}
	for j := 1; j < len(a); j++ {
		x = append(x, y[j-1])
		y = append(y, x[j-1]-y[j-1]*a_div_b[len(a)-j-1])
	}
	var d = y[len(a)-1] % phi
	if d < 0 {
		d += phi
	}
	return d
}

func generate_keypair(p int, q int) (KeyPair, error) {
	if !(is_prime(p) && is_prime(q)) {
		return KeyPair{}, errors.New("Both numbers must be prime.")
	} else if p == q {
		return KeyPair{}, errors.New("p and q cannot be equal")
	}
	// n = pq
	n := p * q
	// phi = (p-1)(q-1)
	phi := (p - 1) * (q - 1)

	// Choose an integer e such that e and phi(n) are coprime
	e := rand.Intn(phi-1) + 1

	// Use Euclid's Algorithm to verify that e and phi(n) are comprime
	g := gcd(e, phi)
	for g != 1 {
		e = rand.Intn(phi-1) + 1
		g = gcd(e, phi)
	}

	// Use Extended Euclid's Algorithm to generate the private key
	d := multiplicative_inverse(e, phi)
	// Return public and private keypair
	// Public key is (e, n) and private key is (d, n)
	return KeyPair{Key{e, n}, Key{d, n}}, nil
}
