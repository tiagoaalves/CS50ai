import os
import random
import re
import sys
import random

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    pages = dict()

    baseProb = (1 - damping_factor) / len(corpus)
    linkedProb = damping_factor / len(corpus[page])

    for key in corpus:
        pages[key] = baseProb
        if key in corpus[page]:
            pages[key] += linkedProb

    return pages


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = dict()

    for key in corpus:
        result[key] = 0.0

    page = random.choice(list(corpus.keys()))

    for i in range(n):
        pages = transition_model(corpus, page, damping_factor)
        page = random.choices(list(pages.keys()),
                              weights=list(pages.values()))[0]
        result[page] += 1 / n

    return result


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = dict()
    compare = dict()
    threshold = 0.0005

    baseProb = (1 - damping_factor) / len(corpus)

    for page in corpus:
        compare[page] = 1 / len(corpus)
        result[page] = 0

    repeat = True

    while repeat:

        for page in corpus:

            total = baseProb

            # for every page find every page that has its link
            for key in corpus:

                # A page that has no links at all should be interpreted as having one link for every page in the corpus
                if len(corpus[key]) == 0:
                    total += compare[key] / len(corpus) * damping_factor

                if page in corpus[key]:
                    total += compare[key] / len(corpus[key]) * damping_factor

            # difference = result[page] - total
            # result[page] = total
            compare[page] = total

        repeat = False

        for page in compare:

            difference = compare[page] - result[page]
            result[page] = compare[page]

            # when the new value added is less than the threshold the loop is ended
            if not abs(difference) < threshold:
                repeat = True

    return result


if __name__ == "__main__":
    main()
