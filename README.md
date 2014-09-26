# wikipedia article visual mapping

ever done that thing where you click on all the links in a wikipedia article and soon your browser is super full and you don't remember which ones came from where, and you're not even sure which ones are really relevent to what you're trying to read about?
this tool allows you to see the hyperlinked articles in an article mapped to that article in a visual map, and you can control which links are represented with a search word/phrase.

for example, if I only wanna spend time reading articles linked in an article I'm reading AND only having to do with opossums, I could filter all the links for the word opossum, or something related to opossums like "opossum mating rituals".

the end result of running the program is a png showing the visual map, and a firefox window containing the hyperlinks so you can actually go to the filtered links. to change this functionality to use your preferred browser, replace the `call(['firefox','links.html'])` input found in wikinet's `network` method with the appropriate terminal command for your browser.

## ways to use it:
### terminal interface:

 - make wikinet.py executable (or not)

 - look at your options with --help!

```sh
$ ./wikinet.py --help
usage: wikinet.py [-h] [-c CAP] search_title search_word

create a node map between a wikipedia article and linked articles in that
article, but only if the linked article contains the positional argument
'search_word'

positional arguments:
  search_title       The article title or keywords in article title you're
                     looking for. No, it's not case sensitive
  search_word        word/s to search for in linked articles

optional arguments:
  -h, --help         show this help message and exit
  -c CAP, --cap CAP  caps the number of links processed
$ ./wikinet.py "olin college" "franklin w. olin" -c 15
```

### python command line:

after adding the wikinet dir to your python path, or running interactive mode from inside the dir:

```sh
>>> from wikinet import wikinet
>>> olinNet = wikinet("olin college", "franklin w. olin")
>>> olinNet.network(15)
```
