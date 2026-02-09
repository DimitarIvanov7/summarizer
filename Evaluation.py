#from Summary import nlp


def generate_comparison_lists(result_filename, expected_filename):

    with open(result_filename, encoding='utf-8', mode="r") as f_res:
        results = [nlp(line.strip('\n')) for line in f_res if line != '\n']

    with open(expected_filename, encoding='utf-8', mode="r") as f_exp:
        expected = [nlp(line.strip('\n')) for line in f_exp if line != '\n']

    quotes = '„“"'
    result_sentences = [r.sentences for r in results]

    expected_sentences = [r.sentences for r in expected]

    result_text = []
    expected_text = []
    ress = []

    for r in result_sentences:
        for l in r:
            ress.append(l.text.translate(str.maketrans('', '', quotes)))
        result_text.append(ress)
        ress = []

    for e in expected_sentences:
        for l in e:
            ress.append(l.text.translate(str.maketrans('', '', quotes)))
        expected_text.append(ress)
        ress = []

    return result_text, expected_text


def calculate_success(result_filename, expected_filename):
    result_list, expected_list = generate_comparison_lists(result_filename, expected_filename)

    success_perc = []

    for i in range(len(result_list)):
        a = result_list[i]
        b = expected_list[i]
        success = 0
        for k in a:
            for s in b:
                if k == s:
                    success += 1
        success_perc.append(success / (len(result_list[0])))

    return sum(success_perc) / len(success_perc)


from rouge_score import rouge_scorer

def evaluate_summary(reference, generated):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, generated)
    return scores