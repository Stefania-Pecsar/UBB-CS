def gnome_sort(the_list, key=lambda x: x, cmp=lambda x, y: x > y, reverse=False):
    # Sortare de complexitate O(n^2)
    # Un algoritm simplu și intuitiv, dar mai puțin eficient pentru seturi mari de date.
    n = len(the_list)
    index = 0

    while index < n:
        if index == 0 or not cmp(key(the_list[index]), key(the_list[index - 1])):
            index += 1
        else:
            the_list[index], the_list[index - 1] = the_list[index - 1], the_list[index]
            index -= 1

    if reverse:
        the_list.reverse()

def quick_sort(the_list, key=lambda x: x, cmp=lambda x, y: x > y, reverse=False):
    # Sortare de complexitate O(n log n) în caz mediu
    # Algoritm rapid și eficient pentru majoritatea dataset-urilor.

    if len(the_list) <= 1:
        return the_list

    pivot = key(the_list[len(the_list) // 2])
    left = [x for x in the_list if cmp(pivot, key(x))]
    middle = [x for x in the_list if not cmp(key(x), pivot) and not cmp(pivot, key(x))]
    right = [x for x in the_list if cmp(key(x), pivot)]

    sorted_list = quick_sort(left, key, cmp, reverse) + middle + quick_sort(right, key, cmp, reverse)

    if reverse:
        sorted_list.reverse()

    return sorted_list