# wikipedia article visual mapping

ever done that thing where you click on all the links in a wikipedia article and soon your browser is super full and you don't remember which ones cam from where, and you're not even sure which ones are really relevent to what you're trying to read about?
this tool allows you to see the hyperlinks in an article mapped to that article in a visual map, but you can control which links are represented with a searchphrase.

for example, if I wanna only spend time reading articles related to an article I'm reading about AND only having to do with apossums, I could filter all the links for the word apossum, or something related to apossums.

## ways to use it:
### terminal interface:

 - make wikinet.py executable (or not)

 - look at your options with --help!


```sh
$ ./wikinet.py --help
```

### python command line:

after adding the wikinet dir to your python path, or running interactive mode from inside the dir:

```sh
>>> from wikinet import wikinet
>>> olinNet = wikinet("olin college", "franklin w. olin")
>>> olinNet.network(15)
```
