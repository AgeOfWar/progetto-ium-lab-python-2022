def anagram(s1, s2, len_s1, len_s2):
    if len_s1 != len_s2:
        return None
    chars = dict.fromkeys(s1 + s2, 0)
    for c in s1:
        chars[c] += 1
    for c in s2:
        chars[c] -= 1
    return None if any(chars.values()) else True

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

rules = {
    anagram: None,
    change_first_letter: None,
    change_last_letter: None,
    change_letter: int,
    add_first_letter: None,
    add_last_letter: None,
    add_letter: int,
    remove_letter: int
}