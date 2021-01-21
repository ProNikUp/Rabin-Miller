from math import gcd
import random  
import hashlib
 
#Рабин Миллер
def power(x, y, p):
  
    res = 1; 
    
    x = x % p; 
    while (y > 0):
       
        if (y & 1):
            res = (res * x) % p
        
        y = y>>1
        x = (x * x) % p
    return res

def miillerTest(d, n):
    
    a = 2 + random.randint(1, n)
    
    x = power(a, d, n)
    if (x == 1 or x == n - 1):
        return True
 
    while (d != n - 1):
        x = (x * x) % n
        d *= 2;
        if (x == 1):
            return False
        if (x == n - 1):
            return True

    return False



def isPrime( n, k):
    
    if (n <= 1 or n == 4):
        return False
    if (n <= 3):
        return True

    d = n - 1
    while (d % 2 == 0):
        d //= 2
    for i in range(k):
        if (miillerTest(d, n) == False):
            return False
    return True
k = 4 
print("All primes smaller than 100: ")
for n in range(1,100):
    if (isPrime(n, k)):
        print(n, end=" ")

print(" ")


def Prime(fr, to, k=4):
    p=random.randint(fr, to)

    while not isPrime(p,k):
        p = random.randint(fr, to)
        
    return p

 
#Диффи-Хеллман
def DiffieHellman (PKeyA, PkeyB):

    prKeyA = Prime(1,1000,2)
    prKeyB = Prime(1,1000,2)
    
    KeyA = (PKeyA ** prKeyA) % PkeyB
    KeyB = (PKeyA ** prKeyB) % PkeyB

    KeyAA = (KeyB ** prKeyA) % PkeyB
    KeyBB = (KeyA ** prKeyB) % PkeyB
       
    return KeyAA, KeyBB  
      
print(DiffieHellman(83, 61))


def xgcd(a, b):

    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0

def modinv(a, m):

    g, x, y = xgcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


#RSA
def RSA(ms):

    p, q = Prime(1,1000,2), Prime(1,1000,2)
    n = p*q
    ph = (p-1)*(q-1)
    e = 3

    while gcd(e, ph)>1:
        e = e+1

    d = modinv(e, ph)
    x = (ms**e) % n
    ms = (x**d) % n

    return ms

print(RSA(999))

def Pow(base, exp, mod):
    if exp == 0: return 1
    if exp & 1 == 0:
        r = Pow(base, exp // 2, mod)
        return (r * r) % mod
    else: return (base % mod * Pow(base, exp - 1, mod)) % mod

def root(modulo):
    required_set = set(num for num in range (1, modulo) if gcd(num, modulo) == 1)
    for g in range(1, modulo):
        actual_set = set(pow(g, powers) % modulo for powers in range (1, modulo))
        if required_set == actual_set:
            return g

#SRP
def SRP(pas):
    N = 1
    q = 1
    g = 1
    while not isPrime(N, 1):
        q = Prime(50, 300, 1)
        N = 2*q + 1
        g = root(N)
    salt = random.getrandbits(3)
    x = int(hashlib.sha256((str(salt)+pas).encode('utf-8')).hexdigest(), 16)
    v = Pow(g,x,N)
    a = random.randint(2,100)
    A = Pow(g,a,N)
    if A!=0:
        b = random.randint(2,100)
        k = 3
        B = (k*v + Pow(g,b,N) )%N
        if B!=0:
            u = int(hashlib.sha256(hex(A+B).encode('utf-8')).hexdigest(), 16)
            if u!=0:
                S1 = Pow((B - k * Pow(g,x,N) ) , (a + u * x), N)
                K1 = int(hashlib.sha256(hex(S1).encode('utf-8')).hexdigest(), 16)
                S2 = Pow((A * (Pow(v,u,N))), b, N)
                K2 = int(hashlib.sha256(hex(S2).encode('utf-8')).hexdigest(), 16)
                if K1==K2:
                    return "success", K1

print(SRP('12355312'))