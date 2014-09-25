#! /bin/env python

import matplotlib.pyplot as mplot
import pattern.web as pweb
import networkx as nwx
import argparse as ap
import random as rand

"""
create visual map of wikipedia article connected to linked articles as nodes. 
a link is only shown if the linked article contains the given searchword
"""

def get_title(search_title):
    '''
    return the actual title from wikipedia from search
    '''
    try:
        wiki_title = pweb.Wikipedia().search(search_title)
    except TypeError:
        print "error: search must be string"
        return
    wiki_title = str(wiki_title)
    for n in range(len(wiki_title)):
        if wiki_title[n] == "=":
            wiki_title = wiki_title[n+3:-2]
            break
    return wiki_title
 
def search_links(href, search_word):
    link = href[len('href="'):-1]
    article = pweb.plaintext(pweb.URL('https://en.wikipedia.org' + link).download())
    if search_word.lower() in article.lower():
        return True
    else:
        return False

def create_nodes(search_title, search_word, cap=None):
    wiki_title = get_title(search_title)
    title_url = [' ']*len(wiki_title)
    for i in range(len(wiki_title)):
        if wiki_title[i] == ' ':
            title_url[i] = '_'
        else:
            title_url[i] = wiki_title[i]
    title_url = ''.join(title_url)
    wiki_url = 'https://en.wikipedia.org/wiki/Special:WhatLinksHere/' + title_url
    hrefs = []
    html = pweb.URL(wiki_url).download().split()
    for item in html:
        if 'href="/wiki/' in item and ':' not in item and title_url not in item and 'Main_Page' not in item:
            hrefs.append(item)
    rand.shuffle(hrefs)
    nodes = []
    for href in hrefs:
        include = search_links(href, search_word)
        if include == True:
            node = [' ']*len(href)
            for i in range(len(href)):
                if href[i] == '/':
                    start = i+1
                elif href[i] == '"':
                    stop = i
                if href[i] == '_':
                    node[i] = ' '
                else:
                    node[i] = href[i]
            nodes.append(''.join(node)[start:stop])
        if  len(nodes) == cap:
            break
    nodes.insert(0, wiki_title)
    return nodes

def network(search_title, search_word, cap=None):
    nodes = create_nodes(search_title, search_word, cap)
    G=nwx.balanced_tree(len(nodes)-1,1)
    pos=nwx.graphviz_layout(G,prog='twopi',args='')
    labels = {}
    for i in range(len(nodes)):
        labels[i] = nodes[i]
    nwx.draw(G,
        pos,
        node_size=[800] + [300]*(len(nodes)),
        alpha=0.3,
        node_color = "blue",
        edge_color = "black",
        linewidths = 0,
        labels=False
        )
    nwx.draw_networkx_labels(G,
            pos,
            font_size = 10,
            labels = labels
            )

    mplot.axis('off')
    mplot.show()
        

if __name__=="__main__":
    
    parser = ap.ArgumentParser(
            description = "create a node map between a wikipedia article and linked articles in that article, but only if the linked article contains the positional argument 'search_word'"
            )
    parser.add_argument("search_title",
            type = str,
            help = "The article title or keywords in article title you're looking for. No, it's not case sensitive"
            )
    parser.add_argument("search_word",
            type = str,
            help = "word/s to search for in linked articles"
            )
    parser.add_argument("-c", "--cap",
            type = int,
            action = "store",
            help = "caps the number of links processed"
            )
    args = parser.parse_args()

    if args.cap:
        network(args.search_title, args.search_word, args.cap)
    else:
        network(args.search_title, args.search_word)
