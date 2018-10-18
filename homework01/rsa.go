package main

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
