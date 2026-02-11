def find_char (word,mask,c):
    mask = list(mask)
    for index in range(len(word)):
        if word[index].lower() == c.lower():
            mask[index] = word[index]
    mask = ''.join(mask)
    return mask
