from mw.lib.title import normalize


def split_page_name(ns, page_name):
    if ns == 0:
        return "", normalize(page_name)
    else:
        nsname, title = page_name.split(":", 1)
        
        return normalize(nsname), normalize(title)
