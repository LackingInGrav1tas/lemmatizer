import nltk
import re
import sys

def is_vowel(character):
    return character.lower() in ["a", "e", "i", "o", "u"]

def voweled(word):
    for character in word:
        if is_vowel(character):
            return True
    return False

def get_m(word):
    """Returns the m value of the word"""
    vowel = is_vowel(word[0])
    changes = .5
    for c in word:
        if is_vowel(c) != vowel:
            changes += .5
            vowel = not vowel
    if changes % 1 == .5: changes -= .5
    return changes
    

def get_o(word):
    """Returns whether the word matches cvc"""
    if (len(word) >= 3):
        return (not is_vowel(word[-3])) and (is_vowel(word[-2])) and (not is_vowel(word[-1]))
    return False

def get_d(word):
    if len(word) > 2:
        return word[-1] == word[-2] and not is_vowel(word[-1])
    return False

step1a = [
    ("sses\\b", "ss"),
    ("ies\\b", "i"),
    ("ss\\b", "ss"),
    ("s\\b", "")
]

step1b = [
    ("eed\\b", "ee", "m", 0, False),
    ("ed\\b", "", "v", True),
    ("ing\\b", "", "v", True)
]

step1b2 = [
    ("at\\b", "ate"),
    ("bl\\b", "ble"),
    ("iz\\b", "ize")
]

step2 = [
    ("ational\\b", "ate"),
    ("tional\\b", "tion"),
    ("enci\\b", "ence"),
    ("anci\\b", "ance"),
    ("izer\\b", "ize"),
    ("abli\\b", "able"),
    ("alli\\b", "al"),
    ("entli\\b", "ent"),
    ("eli\\b", "e"),
    ("ousli\\b", "ous"),
    ("ization\\b", "ize"),
    ("ation\\b", "ate"),
    ("ator\\b", "ate"),
    ("alism\\b", "al"),
    ("iveness\\b", "ive"),
    ("fulness\\b", "ful"),
    ("ousness\\b", "ous"),
    ("aliti\\b", "al"),
    ("iviti\\b", "ive"),
    ("biliti\\b", "ble"),
]

step3 = [
    ("icate\\b", "ic"),
    ("ative\\b", ""),
    ("alize\\b", "al"),
    ("iciti\\b", "ic"),
    ("ical\\b", "ic"),
    ("ful\\b", ""),
    ("ness\\b", ""),
]

step4 = [
    "al", "ance","ence", "er", "ic", "able", "ible", "ant", "ement",
    "ment", "ent", "ou", "ism", "ate", "iti", "ous", "ive", "ize"
]

def lemmize(word):
    """Takes a single word, removes it's suffixes, and returns it"""
    step1a_word = word
    for key in step1a:
        step1a_word = re.sub(key[0], key[1], word)
        if word != step1a_word: break

    proceed = False
    step1b_word = step1a_word
    for key in step1b:
        if key[2] == "v":
            if voweled(re.sub(key[0], key[1], step1a_word)):
                step1b_word = re.sub(key[0], key[1], step1a_word)
        elif key[2] == "m":
            if get_m(re.sub(key[0], key[1], step1a_word)) > key[3]:
                step1b_word = re.sub(key[0], key[1], step1a_word)
        else:
            step1b_word = re.sub(key[0], key[1], step1a_word)
        if step1b_word != step1a_word:
            proceed = key[-1]
            break

    stem = step1b_word

    m = get_m(stem)
    o = get_o(stem)
    d = get_d(stem)

    w = step1b_word
    if proceed:
        for key in step1b2:
            w = re.sub(key[0], key[1], step1b_word)
            if w != step1b_word: break

        if d and not stem[-1] in ["s", "l", "z"]:
            w = w[:-1]

        if m == 1 and o:
            w += "e"
        
    if voweled(stem):
        w = re.sub("y\\b", "i", w)

    step2_word = w
    for key in step2:
        if m > 0:
            step2_word = re.sub(key[0], key[1], w)
        if step2_word != w: break
    
    step3_word = step2_word
    if m > 0:
        for key in step3:
            step3_word = re.sub(key[0], key[1], step2_word)
            if step3_word != step2_word: break

    step4_word = step3_word
    if m > 1:
        if stem[-1] in ["s", "t"] and re.search("ion\\b", step3_word):
            step4_word = re.sub("ion\\b", "", step3_word)
        else:
            for key in step4:
                step4_word = re.sub(key + "\\b", "", step3_word)
                if step4_word != step3_word: break
    
    step5_word = step4_word
    if m > 1 or (m == 1 and not o):
        step5_word = re.sub("e\\b", "", step4_word)

    if m > 1 and d and stem[-1] == "l":
        step5_word = step5_word[:-1]

    return step5_word

def main():
    argv = sys.argv
    if len(argv) >= 2:
        text = argv[1]
    else:
        text = input("Enter some text to lemmize: ")

    tokens = nltk.word_tokenize(text.lower())
    lemmized = []
    for word in tokens:
        lemmized.append(lemmize(word))
    print(lemmized)

if __name__ == "__main__": main()