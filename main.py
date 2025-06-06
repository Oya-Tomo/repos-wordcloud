import os
import re
import json

import matplotlib.pyplot as plt

from gensim.corpora import Dictionary
from gensim.models import TfidfModel

from wordcloud import WordCloud

from scraper import (
    remove_directory,
    clone_repo,
    get_files_in_directory,
    get_file_content,
)


def split_identifier(name: str) -> list[str]:
    parts = name.split("_")
    split_parts = []
    for part in parts:
        split_parts += re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])", part)
    return [p.lower() for p in split_parts if p]


def extract_words_of_repo(url: str) -> list[str]:
    clone_path = "repo"
    remove_directory(clone_path)
    clone_repo(url, clone_path)
    files = get_files_in_directory(clone_path)
    corpus = []
    for file in files:
        if file.find(".git") != -1:
            continue
        content = get_file_content(file)
        if content:
            parts = split_identifier(content)
            corpus.extend(parts)
    remove_directory(clone_path)
    return corpus


def main():
    with open("config.json", "r") as f:
        config = json.loads(f.read())

    font = config["font"]
    urls = config["repos"]

    width = config["size"]["width"]
    height = config["size"]["height"]

    max_words = config["max_words"]

    documents = []
    for url in urls:
        words = extract_words_of_repo(url)
        print(f"Extracted {len(words)} words from {url}")
        documents.append(words)

    dictionary = Dictionary(documents)
    print("docs num:", dictionary.num_docs)
    print("dfs", len(dictionary.dfs))

    corpus = [*map(lambda x: dictionary.doc2bow(x), documents)]
    tfidf_model = TfidfModel(corpus)
    corpus_tfidf = tfidf_model[corpus]

    tfidf_max = {}
    for tfidf in corpus_tfidf:
        for word_id, score in tfidf:
            word = dictionary[word_id]
            if word not in tfidf_max or score > tfidf_max[word]:
                tfidf_max[word] = score
    print(tfidf_max)

    x = dict(tfidf_max.items())
    im = WordCloud(
        font_path=font,
        width=width,
        height=height,
        prefer_horizontal=1,
        background_color="white",
        colormap="viridis",
        max_words=max_words,
        random_state=0,
    ).generate_from_frequencies(x)
    plt.axis("off")
    plt.imshow(im, interpolation="bilinear")

    if not os.path.exists("export"):
        os.makedirs("export")
    plt.savefig("export/wordcloud.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
