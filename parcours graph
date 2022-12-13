# Créé par vanierdesaintau, le 13/12/2022 en Python 3.7
dico = {1:[2], 2:[3,6], 3:[4], 4:[3], 5:[1,4], 6:[1,4,5]}


def chemin(graph,deb,fin):
    chem = []
    file = [(deb,[])]
    while file != []:
        sommet,deja_vu = file.pop(0)
        file = file + parcours_voisins(graph,sommet,deja_vu,fin,chem)
    return chem

def parcours_voisins(graph,sommet,deja_vu,fin,chem):
    if sommet == fin:
        temp = deja_vu.append(fin)
        chem.append(deja_vu)
        return []
    elif graph[sommet] == []:
        return []
    elif sommet in deja_vu:
        return []
    else:
        liste = []
        temp = deja_vu
        temp.append(sommet)
        for elm in graph[sommet]:
            liste.append((elm,temp))
        return liste
