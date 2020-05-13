item = {}
item['name'] = ['abc', 'bcd', 'cde']
item['player'] = ['123', '456', '789']
item['lyric'] = ['aaa', 'bbb', 'ccc']
item['number'] = [3, 5, 6]
for i in range(3):
    for it in item:
        print(str(item[it][i]) + " ", end="")
    print()