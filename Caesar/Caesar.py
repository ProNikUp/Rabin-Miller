import os
import re


regex = re.compile('[а-яА-ЯёЁ]')
def isRus(ch): 
    return len(regex.findall(ch))>0

def count_freq(lines, freq): 
    for i in range(len(lines)):
        for let in lines[i].lower():
            if let.isalpha():
                if let in freq:
                    if isRus(let):
                        freq[let] = freq[let]+1
                else:
                    if isRus(let):
                        freq[let] = 1

def Caesar(line, key): 
    small_alphabet = [chr(i) for i in range(ord("а"), ord("я")+1)]
    big_alphabet = [chr(i) for i in range(ord("А"), ord("Я")+1)]
    s = line.strip()
    res = ''
    for c in s:
        if isRus(c):
            alp = small_alphabet if c in small_alphabet else big_alphabet
            res += alp[(alp.index(c) + key) % len(alp)]
        else:
            res += c
    return res

def read_book(dir): #подсчет суммарных частот книг
    books = []
    for file in os.listdir(dir):
        if os.path.isfile(dir + file):
            with open(dir + file, 'r', encoding='utf-8') as f:
                books.append(f.readlines())
    orig_freq = {}

    for i in range(len(books)):
        for j in range(len(books[i])):
            books[i][j] = books[i][j].replace('ё', 'е')
        count_freq(books[i], orig_freq)
        return orig_freq

def frequent_decode(origf, newf): 
    convert = {}
    for i in range(len(newf)):
        #print(origf[i][0], newf[i][0])
        convert[newf[i][0]] = origf[i][0]
    return convert

def deсoder_analys(conv, line): #дешифровать строки по карте конвертации
    nl = []
    for i in line:
        if i.lower() in conv:
            if i.isupper():
                nl.append(conv[i.lower()].upper())
            else:
                nl.append(conv[i])
        else:
            nl.append(i)
    return ''.join(nl)

def crypto_analys(name, cdir, key): #зашифровка строки цезарем
    with open(cdir + name +'.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for j in range(len(lines)):
            lines[j] = lines[j].replace('ё', 'е')

    for i in range(len(lines)):
        lines[i] = Caesar(lines[i], key)

    with open(cdir + name+' шифр.txt', 'w+', encoding='utf-8') as f:
        f.writelines(lines)

def decrypto_analys(name, conv, lines, cdir): #расшифровка строки частотным анализом
    for i in range(len(lines)):
        lines[i] = deсoder_analys(conv, lines[i])
    with open(cdir + name+' анализ.txt', 'w+', encoding='utf-8') as f:
        f.writelines(lines)


dir = r'D:\Users\nikit\Desktop\INF\Rabin\Caesar\\' 
encrypted = r'D:\Users\nikit\Desktop\INF\Rabin\Caesar\\' 
name = '1-2'
key = 5
crypto_analys(name, encrypted, key)
orig_freq = read_book(dir) 
orig_sorted = sorted(orig_freq.items(), key=lambda x: x[1], reverse=True)
lines = [] 
new_freq = {}
with open(encrypted + name+' шифр.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

count_freq(lines, new_freq) 
new_sorted = sorted(new_freq.items(), key=lambda x: x[1], reverse=True)
conv = frequent_decode(orig_sorted, new_sorted) 
decrypto_analys(name, conv, lines, encrypted) 