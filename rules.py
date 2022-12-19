def change_letter(s1, s2, len_s1, len_s2):
    if len_s1 != len_s2:
        return None
    index = None
    for i in range(len_s1):
        if s1[i] != s2[i]:
            if index != None:
                return None
            index = i
    return index

def change_first_letter(s1, s2, len_s1, len_s2):
    if len_s1 != len_s2:
        return None
    if s1[0] == s2[0]:
        return None
    for i in range(1, len_s1):
        if s1[i] != s2[i]:
            return None
    return True

def change_last_letter(s1, s2, len_s1, len_s2):
    if len_s1 != len_s2:
        return None
    last = len_s1 - 1
    if s1[last] == s2[last]:
        return None
    for i in range(last):
        if s1[i] != s2[i]:
            return None
    return True

def add_first_letter(s1, s2, len_s1, len_s2):
    if len_s1 + 1 != len_s2:
        return None
    for i in range(len_s1):
        if s1[i] != s2[i + 1]:
            return None
    return True

def add_last_letter(s1, s2, len_s1, len_s2):
    if len_s1 + 1 != len_s2:
        return None
    for i in range(len_s1):
        if s1[i] != s2[i]:
            return None
    return True

def add_letter(s1, s2, len_s1, len_s2):
    if len_s1 + 1 != len_s2:
        return None
    index = None
    for i in range(len_s1):
        if index == None:
            if s1[i] != s2[i]:
                index = i
        if index != None:
            if s1[i] != s2[i + 1]:
                return None
    return index

def remove_first_letter(s1, s2, len_s1, len_s2):
    if len_s1 != len_s2 + 1:
        return None
    for i in range(len_s2):
        if s1[i + 1] != s2[i]:
            return None
    return True

def remove_last_letter(s1, s2, len_s1, len_s2):
    if len_s1 != len_s2 + 1:
        return None
    for i in range(len_s2):
        if s1[i] != s2[i]:
            return None
    return True

def remove_letter(s1, s2, len_s1, len_s2):
    if len_s1 != len_s2 + 1:
        return None
    index = None
    for i in range(len_s2):
        if index == None:
            if s1[i] != s2[i]:
                index = i
        if index != None:
            if s1[i + 1] != s2[i]:
                return None
    return index

def anagram(s1, s2, len_s1, len_s2):
    if len_s1 != len_s2:
        return None

    # huge optimization
    sum = 0
    for i in range(len_s1):
        sum += ord(s1[i])
        sum -= ord(s2[i])
    if sum != 0:
        return None

    chars = {}
    for i in range(len_s1):
        c1 = s1[i]
        c2 = s2[i]
        if c1 in chars:
            chars[c1] += 1
        else:
            chars[c1] = 1
        if c2 in chars:
            chars[c2] -= 1
        else:
            chars[c2] = -1
    if any(chars.values()):
        return None
    return [i for i in range(len_s1) if s1[i] != s2[i]]

def swap_two_letters(s1, s2, len_s1, len_s2):
    if len_s1 != len_s2:
        return None
    swapped_index1 = None
    swapped_index2 = None
    for i in range(len_s1):
        if s1[i] != s2[i]:
            if swapped_index1 == None:
                swapped_index1 = i
            else:
                if swapped_index2 != None or s1[swapped_index1] != s2[i] or s1[i] != s2[swapped_index1]:
                    return None
                swapped_index2 = i
    if swapped_index2 == None:
        return None
    return (swapped_index1, swapped_index2)

rules = {
    change_first_letter: None,
    change_last_letter: None,
    change_letter: int,
    add_first_letter: None,
    add_last_letter: None,
    add_letter: int,
    remove_first_letter: None,
    remove_last_letter: None,
    remove_letter: int,
    swap_two_letters: (int, int),
    anagram: [int]
}

def subrules(rule):
    return {
        change_first_letter: [],
        change_last_letter: [],
        change_letter: [change_first_letter, change_last_letter],
        add_first_letter: [],
        add_last_letter: [],
        add_letter: [add_first_letter, add_last_letter],
        remove_first_letter: [],
        remove_last_letter: [],
        remove_letter: [remove_first_letter, remove_last_letter],
        swap_two_letters: [],
        anagram: [swap_two_letters]
    }[rule]

def superrules(rule):
    return {
        change_first_letter: [change_letter],
        change_last_letter: [change_letter],
        change_letter: [],
        add_first_letter: [add_letter],
        add_last_letter: [add_letter],
        add_letter: [],
        remove_first_letter: [remove_letter],
        remove_last_letter: [remove_letter],
        remove_letter: [],
        swap_two_letters: [anagram],
        anagram: []
    }[rule]