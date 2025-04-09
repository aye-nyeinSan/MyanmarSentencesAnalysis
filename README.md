###  Burmease language Sentiment Analysis Project 


## Required Packages

- selenium
- pandas

### How to install libraries
pip install -r requirements.txt

### Comment Scrapping script 
run `python Comment_Scrapper.py`

### SetUp
first , generate the bigram dictionary with  `cd external/myWord/dict_ver1`
there will be 
 then run `./combine-all-splitted-files.sh ` 

You will get the combined ngram dictionaries:
```
$ ls
bigram-phrase.bin  bigram-phrase.txt  bigram-word.bin  bigram-word.txt
```


## Tokenizing Tools

Tokenizing tool is exported as submodule in external/myWord.
 ```
myWord: Syllable, Word and Phrase Segmenter for Burmese, Ye Kyaw Thu, Sept 2021, 
GitHub Link: https://github.com/ye-kyaw-thu/myWord
 ``` 
