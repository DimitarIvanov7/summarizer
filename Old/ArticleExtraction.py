def extract_articles(filename):
    with open(filename,
              encoding='utf-8', mode='r') as file:
        whole_text = [line for line in file]

    j = 0
    articles = [[]]

    for i, line in enumerate(whole_text):
        if '<p>' in line:
            if 'Снимка:' not in line:
                # Stripping '<p>' from the beginning and '</p>\n' of every paragraph
                articles[j].append(line[3:-5])
            if '</div>' in whole_text[i+1]:
                j += 1
                articles.append([])

    articles_by_paragraphs = []

    with open("articles.txt", encoding='utf-8', mode="w") as f:
        for article in articles[:-1]:
            text = ' '.join([p if p[-1] == '.' else p + '.' for p in article])
            f.write(text + '\n')
            articles_by_paragraphs.append(text)

    return articles_by_paragraphs
