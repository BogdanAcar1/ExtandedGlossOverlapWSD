import wikipedia as wp

if __name__ == '__main__':
    target = "soda"
    print(wp.suggest(target))
    page = wp.page(target)
    print(page.lemma)
