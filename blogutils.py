def title_to_url(title):
    nonoChars = ['!', ',', '^', '-', '[', ']', '(', ')', '{', '}', '/', '|', '\'', '\"', '@', '#', '&' '$', '%', '*',
                 '~', '+', '=', '?', '<', '>', '.', '`', 'and']

    newTitle = title
    newTitle = newTitle.lstrip().rstrip().lower()
    for ch in nonoChars:
        if ch in newTitle:
            newTitle = newTitle.replace(ch, '')

    newTitle = smart_truncate(newTitle, 60)
    newTitle = newTitle.replace('  ', '-').replace(' ', '-')

    return newTitle

def smart_truncate(content, length=100, suffix=''):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix