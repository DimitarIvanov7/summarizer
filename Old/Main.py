from Summary import summarize
from Evaluation import calculate_success
from ArticleExtraction import extract_articles

if __name__ == '__main__':

    entry_file = "C:/Users/Stefan Ivanov/PycharmProjects/pythonProject1/btvnovinite.bg/btvnovinite.bg - 2021-01-01.xml"

    articles = extract_articles(entry_file)

    filename = summarize(articles)


    print(calculate_success(filename, "expected_02.txt"))
