
def beautifulQuadruples(a, b, c, d):
    #
    # Write your code here.
    #
    dict1 = {}
    list1 = []
    for i1 in range(1, a+1):
        for i2 in range(1, b+1):
            for i3 in range(1, c+1):
                for i4 in range(1, d+1):
                    if i1^i2^i3^i4 != 0:
                        tmp_l = [i1, i2, i3, i4]
                        tmp_l.sort()
                        dict1[str(tmp_l)] = 1
                        list1.append(str(tmp_l))
                        print(str(tmp_l))
    print('\n\n')
    print('\n'.join(list1))
    return len(dict1.keys())

beautifulQuadruples(1, 2, 3, 4)