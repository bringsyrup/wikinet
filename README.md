# wikipedia article visual mapping

ever done that thing where you click on all the links in a wikipedia article and soon your browser is super full and you don't remember which ones came from where, and you're not even sure which ones are really relevent to what you're trying to read about?
this tool allows you to see the hyperlinked articles in an article mapped to that article in a visual map, and you can control which links are represented with search words/phrases.

for example, if I only wanna spend time reading articles linked in an article I'm reading AND only having to do with opossums, I could filter all the links for the word opossum, or something related to opossums like "opossum mating rituals" or even "'oppossum mating rituals' 'beautiful trees'".

the end result of running the command line interface is a png showing the visual map, and a firefox window containing the hyperlinks so you can actually go to the filtered links. to change this functionality to use your preferred browser, replace the `call(['firefox','links.html'])` input found in wikinet's `network` method with the appropriate terminal command for your browser.
## dependencies:

 - pattern (github [here](https://github.com/clips/pattern))
	- pip install pattern
 - beautiful soup (home page [here](http://www.crummy.com/software/BeautifulSoup/))
	- pip install beautifulsoup4
 - matplotlib (tar file [here](http://matplotlib.org/downloads.html)) 
	- pip install matplotlib
 - subprocess32 (tar file [here](https://pypi.python.org/pypi/subprocess32/))
 - re and random (installed with python by default)

here's the difficult one:

 - networkx (tar file [here](https://pypi.python.org/pypi/networkx/))
	- requires pygraphviz (tar file [here](https://pypi.python.org/pypi/pygraphviz)) which in turn requires Graphviz (tar file [here](http://graphviz.org/Download_source.php))
	- in ubuntu, you should install Graphviz with `sudo apt-get install graphviz` unless you REALLY like fixing dependency issues
	- other linux/osx may need to install from source, which is tricky with Graphviz. for my installation, I had to edit pygraphviz source code to pass an exception. google is your friend


## ways to use it:
### terminal interface:

 - check/modify/remove the shebang  

 - make wikinet.py executable (or not)

 - look at your options with --help!

```sh
$ ./wikinet.py --help
usage: wikinet.py [-h] [-c CAP] search_title filters

create a node map between a wikipedia article and linked articles in that
article, but only if the linked article contains the positional argument
'filters'. also launches browser page (default firefox) containing
hyperlinked articles

positional arguments:
  search_title       The article title or keywords in article title you're
                     looking for. No, it's not case sensitive
  filters            word/s to search for in linked articles

optional arguments:
  -h, --help         show this help message and exit
  -c CAP, --cap CAP  caps the number of links processed
  -s, --split        splits filters into substrings and filters hyperlinks for
                     substrings. for example: "'franklin w. olin' 'babson
                     college'" will search for each substring and return a
                     hyperlink only if both substrings are found

$ ./wikinet.py "olin college" "franklin w. olin" -c 15
```

### python command line:

wikinet.py contains the wikinet class, which can be easily used from the python command prompt.
after adding the wikinet dir to your python path, or running python from inside the your cloned wikinet repository:

```sh
>>> from wikinet import wikinet
>>> olinNet = wikinet("olin college", "franklin w. olin")
>>> olinNet.network(15)
`
