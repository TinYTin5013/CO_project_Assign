def DecToBin(n,m=16):
    L = []
    while(n!=0):
        L.append(str(n%2))
        n =n//2
    L.reverse()
    return (("0"*(m-len(L))+"".join(L))[-m:])

s = "abcd"
print(min(3,4))