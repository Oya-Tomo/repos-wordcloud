import re

import pandas as pd
import numpy as np
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
    urls = [
        "https://github.com/Oya-Tomo/alpha-rebrew-py",
        "https://github.com/Oya-Tomo/lunar-lander-ppo-pt",
        # "https://github.com/Oya-Tomo/paper-crawler",
        # "https://github.com/Oya-Tomo/paper-summarizer",
        # "https://github.com/Oya-Tomo/wavier-keys",
        # "https://github.com/Oya-Tomo/keyboard-firmware-l432kc",
        # "https://github.com/Campfire-Social-Impl/disaster_flow",
        # "https://github.com/Oya-Tomo/genesis_tryout_example",
        # "https://github.com/Oya-Tomo/ollama-openwebui-docker",
        # "https://github.com/Oya-Tomo/business-card-typst",
        # "https://github.com/Oya-Tomo/translation-stack",
        # "https://github.com/Oya-Tomo/sudoku-rs",
        # "https://github.com/Oya-Tomo/hairo2024_central_node",
        # "https://github.com/Oya-Tomo/hairo2024_collection_node",
        # "https://github.com/Oya-Tomo/hairo2024_operation_panel",
        # "https://github.com/Oya-Tomo/hairo2024_right_footer_node",
        # "https://github.com/Oya-Tomo/hairo2024_left_footer_node",
        # "https://github.com/Oya-Tomo/wifi_connector",
        # "https://github.com/Oya-Tomo/peach_tree",
        # "https://github.com/Oya-Tomo/lime",
        # "https://github.com/Oya-Tomo/robot-arm-controller",
        # "https://github.com/Oya-Tomo/sclp",
        # "https://github.com/Oya-Tomo/shikanoko",
        # "https://github.com/Oya-Tomo/dotfiles",
        # "https://github.com/Oya-Tomo/easy-2d-renderer",
        # "https://github.com/Oya-Tomo/ress-receiver",
        # "https://github.com/Oya-Tomo/notesketch",
        # "https://github.com/Oya-Tomo/meteorites",
        # "https://github.com/Oya-Tomo/bocchi",
        # "https://github.com/Oya-Tomo/markdown-parser-dart",
        # "https://github.com/Oya-Tomo/determinant-calculation",
        # "https://github.com/Oya-Tomo/happy-new-year",
        # "https://github.com/Oya-Tomo/log-builder",
        # "https://github.com/Oya-Tomo/monaka-editor",
        # "https://github.com/Oya-Tomo/homepage",
        # "https://github.com/Oya-Tomo/react-actixweb-routing-example",
        # "https://github.com/Oya-Tomo/tui-renderer",
        # "https://github.com/Oya-Tomo/devtheme-posh",
        # "https://github.com/Oya-Tomo/text-editor",
        # "https://github.com/Oya-Tomo/PySQLite",
        # "https://github.com/Oya-Tomo/codeLight",
        # "https://github.com/Oya-Tomo/todo-app",
    ]

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

    font_path = "/home/oyatomo/.local/share/fonts/FiraCodeNerdFont-Regular.ttf"
    max_words = 50

    x = dict(tfidf_max.items())  # 文書の{単語:TF-IDF}の辞書
    im = WordCloud(
        font_path=font_path,
        width=600,
        height=400,
        prefer_horizontal=1,
        background_color="white",
        colormap="viridis",
        max_words=max_words,
        random_state=0,
    ).generate_from_frequencies(x)
    plt.axis("off")
    plt.imshow(im, interpolation="bilinear")
    plt.savefig("export/wordclouds.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
