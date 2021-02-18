def datum(t):
    return t[0]

def children(t):
    return t[1:]

def is_leaf(t):
    return len(children(t)) == 0

def is_empty(t):
    return t == []


#root_bul a giren paarmetreyi bastırıyor
#part_list'in aşağıdaki how_many_list ve price_list'ten arındırılmış hali
#tree yapımda sadece parça isimlerine yer verdiğim için böyle bir fonksiyon oluşturdum
def do_pre_tree(untree):
    pre_tree = []
    for a in range(len(untree)):
        if type(untree[a][1]) != float:
            pre_tree.append(little_tree(untree[a]))
    return pre_tree


#parça fiyatlarını part_list'ten çekerek ayrı bir listeye alıyor
def do_price_list(untree):
    price_list = []
    for a in range(len(untree)):
        if type(untree[a][1]) == float:
            price_list.append(untree[a])
    return price_list

#hangi parçadan kaç adet olduğunu ve isimlerini part_list'ten çekerek ayrı bir listeye alıyor
def do_how_many_list(untree):
    how_many_list = []
    for a in range(len(untree)):
        if type(untree[a][1]) != float:
            for m in range(len(untree[a])):
                if type(untree[a][m]) == tuple:
                    how_many_list.append(untree[a][m])

    return how_many_list

#tree'ye eklenecek elemanların hangi sırada ekleneceklerine karar veriyor
liste444 = []
def root_bul(part_list):
    if part_list == []:
        return liste444
    for i in part_list:
        x = 0
        for j in part_list:
            a = j.count(i[0])
            b = j.count([i[0]])
            x += a+b
        if x == 1:
            part_list.remove(i)
            tree = i
            liste444.append(tree)
            return root_bul(part_list)

#tree oluşturma
def tree_main(liste):
    tree = []
    def tree_yap(ordered):
        nonlocal tree
        lenght = len(ordered)
        def turn_into_tree(lst, x):
            return turn_into_tree_helper(lst, x, 0)
        def turn_into_tree_helper(lst, x, depth):
            nonlocal tree
            newlist = []
            for item in lst:
                if type(item) == list:
                    a = turn_into_tree_helper(item, x, depth=x[1:][0])
                    newlist.append(a)
                else:
                    if item == x[0]:
                        newlist.append(item)
                        for i in x[1:]:
                            newlist.append(i)
                    else:
                        newlist.append(item)
            if newlist == []:
                newlist.extend(x)
            tree = newlist
            return newlist
        for i in range(lenght):
            x = ordered.pop(0)
            if x == []:
                return tree
            turn_into_tree(tree, x)
        return tree
    result = tree_yap(liste)
    return result

#do_pre_tree de kullandığım ufak bir fonksiyon
def little_tree(liste):#["bike", (2, "wheel"), (1, "frame")]
    tree = []
    for i in liste:
        if type(i) == str:
            tree.append(i)
        else:
            if len(i) >1:
                tree.append([i[1]])
            else:
                tree.append([i[0]])
    return tree


#aranan elemandan kaç tane olduğunu veriyor (part_list'te verilen sayılar)
def how_many(aranan,liste):
    for j in liste:
        if j[1] == aranan:
            return j[0]
    return 1


def calculate_price(part_list):

    pre_tree = do_pre_tree(part_list)
    root = root_bul(pre_tree)
    tree = tree_main(root)

    how_many_list = do_how_many_list(part_list)
    price_list = do_price_list(part_list)
    if len(part_list) == 1: #eğer [[bike,500.0]] gibi bir fonksiyon verilirse oluşturduğum case
        tree = [part_list[0][0]]
        price_list = [part_list[0][1]]
        how_many_list = [(1,part_list[0][0])]
    return calculate_price_helper(tree,price_list,how_many_list)
def calculate_price_helper(tree, price_list,how_many_list,price_pre ="1"):
    if len(price_list) ==1 and len(tree) == 1 and len(how_many_list) ==1:
        return price_list[0]
    if len(tree) == 0:
        return eval(price_pre)
    if type(datum(tree)) == list:
        if len(tree) == 1:
            return calculate_price_helper(datum(tree),price_list,how_many_list, price_pre)
        m = calculate_price_helper(datum(tree),price_list,how_many_list,price_pre)
        n = calculate_price_helper(children(tree),price_list, how_many_list,price_pre)
        return m+n
    else:
        if how_many(datum(tree), how_many_list) == 0:
            return calculate_price_helper(children(tree),price_list,how_many_list)
        else:
            for i in price_list:
                if i[0] == datum(tree):
                    piece_price = i[1]
                    break
                else:
                    piece_price = 1
            price_pre += f"*{how_many(datum(tree), how_many_list)}*{piece_price}"
            return calculate_price_helper(children(tree),price_list,how_many_list, price_pre)


#tree'nin children'larını tek tek fonksiyona gönderiyoruz
def parcalayici(child,how_many_list,nihai_liste,total_quantity):
    for ch in child:
        required_parts_helperr(ch,how_many_list,nihai_liste,total_quantity)
    return nihai_liste
def required_parts(part_list):

    pre_tree = do_pre_tree(part_list)
    root = root_bul(pre_tree)
    tree = tree_main(root)
    how_many_list = do_how_many_list(part_list)
    if len(part_list) == 1:
        tree = [part_list[0][0]]
        how_many_list = [(1,part_list[0][0])]
    return required_parts_helperr(tree,how_many_list,nihai_liste=[])
def required_parts_helperr(tree,how_many_list,nihai_liste, total_quantity ="1"):
    if is_leaf(tree) and type(tree[0]) == str:
        total_quantity += f"*{how_many(tree[0], how_many_list)}"
        x = eval(total_quantity)
        sss = (x,tree[0])
        nihai_liste.append(sss)

    else:
        if type(datum(tree)) == str: #eğer bir tree ise
            k = how_many(datum(tree), how_many_list)
            total_quantity += f"*{k}"
            return parcalayici(children(tree),how_many_list,nihai_liste,total_quantity)
        else:
            k = how_many(datum(tree), how_many_list)
            total_quantity += f"*{k}"


def stock_check(part_list,stock_list):

    pre_tree = do_pre_tree(part_list)
    root = root_bul(pre_tree)
    tree = tree_main(root)
    how_many_list = do_how_many_list(part_list)
    if len(part_list) == 1:
        tree = [part_list[0][0]]
        how_many_list = [(1,part_list[0][0])]
    return stock_check_helper(tree,stock_list,how_many_list,shortage_list=[])
def stock_check_helper(tree, stock_list,how_many_list,shortage_list):
    requ_p = required_parts_helperr(tree,how_many_list,[])
    copy_requ_p = requ_p[:]
    for i in range(len(requ_p)):
        for j in range(len(stock_list)):
            if requ_p[i][1] == stock_list[j][1]:
                N,M = requ_p[i][0],stock_list[j][0]
                if N-M > 0:
                    xx = (requ_p[i][1],N-M)
                    shortage_list.append(xx)
                copy_requ_p.remove(requ_p[i])
    if copy_requ_p != []:
        for m in copy_requ_p:
            a,b = m[1],m[0]
            shortage_list.append((a,b))
    return shortage_list