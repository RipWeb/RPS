a = open('users.txt', 'r')
f = open('users2.txt', 'w')

b = a.readlines()

for i in b:
    if i[0] == '-':
        pass
    else:
        i = int(i)
        f.write(str(i) + '\n')