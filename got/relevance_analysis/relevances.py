import re

import numpy as np

from east.asts import base


def clear_text(text, lowerize=True):

    pat = re.compile(r'[^A-Za-z0-9 \-\n\r.,;!?А-Яа-я]+')
    cleared_text = re.sub(pat, ' ', text)

    if lowerize:
        cleared_text = cleared_text.lower()

    tokens = cleared_text.split()
    return tokens


def make_substrings(tokens, k=4):

    for i in range(max(len(tokens) - k + 1, 1)):
        yield ' '.join(tokens[i:i + k])


def get_corelevance_matrix(texts):

    matrix = np.empty((0, len(texts)), float)
    prepared_text_tokens = [clear_text(t) for t in texts]
    prepared_texts = [' '.join(t) for t in prepared_text_tokens]

    for text_tokens in prepared_text_tokens:
        ast = base.AST.get_ast(list(make_substrings(text_tokens)))
        row = np.array([ast.score(t) for t in prepared_texts])
        matrix = np.append(matrix, [row], axis=0)

    return matrix


def get_relevance_matrix(texts, strings):

    matrix = np.empty((0, len(strings)), float)
    prepared_text_tokens = [clear_text(t) for t in texts]

    prepared_string_tokens = [clear_text(s) for s in strings]    
    prepared_strings = [' '.join(t) for t in prepared_string_tokens]

    for text_tokens in prepared_text_tokens:
        ast = base.AST.get_ast(list(make_substrings(text_tokens)))
        row = np.array([ast.score(s) for s in prepared_strings])
        matrix = np.append(matrix, [row], axis=0)

    return matrix


def save_matrix(matrix):
    np.savetxt("filename", matrix)


if __name__ == "__main__":

    # Corelevance matrix:
    texts = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit,",
             "qui dolorem ipsum, quia dolor sit, amet!",
             "lorem ipsum"]

    corelevance_matrix = get_corelevance_matrix(texts)
    print("Corelevance mairix:")
    print(corelevance_matrix)

    # Saving
    save_matrix(corelevance_matrix)

    # Relevance between the texts and strings:
    strings = ["Loramet, ipsum",
               "sit dolor amet r 6565?",
               "il lorem",
               "ip sum3"]

    relevance_matrix = get_relevance_matrix(texts, strings)
    print("Relevance mairix:")
    print(relevance_matrix)
