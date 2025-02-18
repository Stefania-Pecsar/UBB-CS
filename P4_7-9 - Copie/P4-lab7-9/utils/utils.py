import random
import string

def getYear_from_CNP(CNP):
    """
    Returneaza anul nasterii obtinut din analizarea CNP-ului
    :param CNP: cnp-ul persoanei
    :return: anul nasterii%100
    """
    year = CNP[11] * 10 + CNP[10]
    return year


def getMonth_from_CNP(CNP):
    """
    Returneaza luna nasterii
    :param CNP: cnp-ul persoanei
    :return: luna nasterii
    """
    month = CNP[9] * 10 + CNP[8]
    return month


def getDay_from_CNP(CNP):
    """
    Returneaza ziua nasterii
    :param CNP: cnp-ul persoanei
    :return: ziua nasterii
    """
    day = CNP[7] * 10 + CNP[6]
    return day

def last_digit_control(CNP):
    """
    Aplicarea algoritmului de validare pe baza ultimei cifre a CNP-ului
    :param CNP: cnp-ul de verificat
    :return: True sau False
    """
    validator=[2,7,9,1,4,6,3,5,8,2,7,9]
    sum=0
    for index in range(12):
        sum+=CNP[12-index]*validator[index]
    sum%=11
    if sum>9:
        sum=1
    return sum==CNP[0]

def string_generator(size):
        return ''.join(random.choice(string.ascii_uppercase) for _ in range(size))

def number_string_generator(size):
        return ''.join(random.choice(string.digits) for _ in range(size))

def comb_sort(the_list, key=lambda x: x, cmp=lambda x, y: x > y, reverse=False):
# este o sortare de complexitate O(n^2)
# este un algoritm de sortare îmbunătățit față de bubble sort, dar poate deveni ineficient pentru seturi de date mari.
    n = len(the_list)
    gap = n
    shrink = 1.3
    swapped = True

    while gap > 1 or swapped:
        gap = max(1, int(gap / shrink))
        swapped = False

        for i in range(n - gap):
            if cmp(key(the_list[i]), key(the_list[i + gap])):
                the_list[i], the_list[i + gap] = the_list[i + gap], the_list[i]
                swapped = True

    if reverse:
        the_list.reverse()

def insertion_sort(the_list, key=lambda x: x, cmp=lambda x, y: x > y, reverse=False):
# este o sortare de complexitate O(n^2)
# este un algoritm de sortare stabil, dar este mai puțin eficient pentru seturi de date mari.
    for i in range(1, len(the_list)):
        current_value = the_list[i]
        position = i

        while position > 0 and cmp(key(the_list[position - 1]), key(current_value)):
            the_list[position] = the_list[position - 1]
            position -= 1

        the_list[position] = current_value

    if reverse:
        the_list.reverse()