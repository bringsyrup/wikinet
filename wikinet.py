#! /bin/env python

import re
import matplotlib.pyplot as mplot
import pattern.web as pweb
import networkx as nx
import argparse as ap
import random as rand
from bs4 import BeautifulSoup as bs
from subprocess32 import call

"""
create visual map of a wikipedia article connected to hyperlinked articles as nodes.
a linked article is only represented if that article contains the given searchword/s/phrase.
additionally, a web browser page (default firefox) is launched containing the hyperlinks.
"""

class wikinet(object):
    '''
    class for creating visual map and browser page conataining hyperlinks 
    '''
    def __init__(self, search_title, filters):
        try:
            search_title = str(search_title)
            filters = str(filters)
        except ValueError:
            print "ValueError: arguments must be strings or callable by str()"
            return
        self.search_title = search_title.lower()
        self.filters = filters.lower()

    def get_title(self):
        '''
        return best match wikipedia article title from search_title
        '''
        wiki_title = str(pweb.Wikipedia().search(self.search_title))[25:-2]
        return wiki_title
     
    def search_links(self, href, split=False):
        '''
        called by create_nodes to filter out articles not containing filters.
        returns a boolean for every hyperlink in main article
        '''
        link = href[len('href="'):-1]
        raw = bs(pweb.plaintext(pweb.URL('https://en.wikipedia.org' + link).download()))
        article = str(raw.get_text).lower()
        if split == True:
            filters = filter(lambda word: word.strip(), re.split('[\'\"]', self.filters))
            if all(word in article.lower() for word in filters):  
                return True
            else:
                return False
        else:
            if self.filters.lower() in article:
                return True
            else:
                return False

    def create_nodes(self, cap=None, split=False):
        '''
        returns list of node labels
        '''
        wiki_title = self.get_title()
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
            if 'href="/wiki/' in item and ':' not in item and title_url not in item and 'Main_Page' not in item and item not in hrefs:
                hrefs.append(item)
        rand.shuffle(hrefs)
        link_file = open('links.html', 'w')
        nodes = []
        for href in hrefs:
            if self.search_links(href, split):
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
                node = ''.join(node)[start:stop]
                nodes.append(node)
                link_file.write('<a '+href[:len('href="')]+'http://en.wikipedia.org'+href[len('href="'):]+'>'+node+'</a><br>\n')
            if  len(nodes) == cap:
                break
        link_file.close()
        nodes.insert(0, wiki_title)
        return nodes

    def network(self, cap=None, split=False):
        '''
        creates visual map from nodes and launches browser page with hyperlinks
        '''
        nodes = self.create_nodes(cap, split)
        G = nx.balanced_tree(len(nodes)-1,1)
        pos = nx.graphviz_layout(G)
        labels = {}
        for i in range(len(nodes)):
            labels[i] = nodes[i]
        nx.draw(G,
            pos,
            node_size=[900] + [200]*(len(nodes)),
            alpha=0.2,
            node_color = "blue",
            edge_color = "black",
            linewidths = 0,
            labels=False
            )
        nx.draw_networkx_labels(G,
                pos,
                font_size = 12,
                labels = labels
                )
        '''to change default web browser change line below'''
        call(["firefox", "links.html"])       
        mplot.axis('off')
        mplot.show()

if __name__=="__main__":
    
    parser = ap.ArgumentParser(
            description = "create a node map between a wikipedia article and linked articles in that article, but only if the linked article contains the positional argument 'filters'. also launches browser page (default firefox) containing hyperlinked articles"
            )
    parser.add_argument("search_title",
            type = str,
            help = "The article title or keywords in article title you're looking for. No, it's not case sensitive"
            )
    parser.add_argument("filters",
            type = str,
            help = "word/s to search for in linked articles"
            )
    parser.add_argument("-c", "--cap",
            type = int,
            action = "store",
            help = "caps the number of links processed"
            )
    parser.add_argument("-s", "--split",
            action = "store_true",
            help = "splits filters into substrings and filters hyperlinks for substrings. for example: \"'franklin w. olin' 'babson college'\" will search for each substring and return a hyperlink only if both substrings are found"
            )
    args = parser.parse_args()

    wikigraph = wikinet(args.search_title, args.filters)

    if args.cap or args.split:
        if args.cap and not args.split:
            wikigraph.network(cap=args.cap)
        elif args.split and not args.cap:
            wikigraph.network(split=args.split)
        else:
            wikigraph.network(args.cap, args.split)
    else:
        wikigraph.network()
