import os
import random
import re
import sys

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
    damp = random.random() > damping_factor
    if damp or len(corpus[page])==0:
        page = random.choice(list(corpus.keys()))
    else:
        page = random.choice(corpus[page])
    return page



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # convert corpus values from sets to lists
    corpus = {key:list(value) for key, value in corpus.items()}
    # get all pages
    all_pages = list(corpus.keys())
    count_dict = {key:0.0 for key in corpus.keys()}
    page = random.choice(all_pages)
    for i in range(n):
        page = transition_model(corpus, page, damping_factor)
        count_dict[page]+=1
    count_dict = {key: value/n for key, value in count_dict.items()}


    return count_dict



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus.keys())
    # initial ranking
    pagerank = {key: 1/num_pages for key in corpus.keys()}
    # interpret pages with no links as having one link to each other page
    for page, links in corpus.items():
        if len(links)==0:
            corpus[page] = list(corpus.keys)
            # remove the page itself
            corpus[page].remove(page)
    # get a dictionary of incoming pages
    incoming_page = {}
    for target_page in corpus.keys():
        incoming_page[target_page] = [page for page in corpus.keys() if target_page in corpus[page]]


    threshold = 0.001

    while True:

        new_rank = {}
        deltas = []
        for page, links in corpus.items():
            new_rank[page] = ((1-damping_factor)/num_pages) + damping_factor * sum([pagerank[incoming]/len(corpus[incoming]) for incoming in incoming_page[page]])
            deltas.append(abs(new_rank[page]-pagerank[page]))

        # update ranking
        pagerank=new_rank
        # convergence check
        if max(deltas) < threshold:
            break

    return pagerank



if __name__ == "__main__":
    main()
