#  Burmese language Sentiment Analysis Project 


### Required Packages

- selenium
- pandas
- [myWord](https://github.com/ye-kyaw-thu/myWord)

### How to install libraries
```
pip install -r requirements.txt
```

### Comment Scrapping script 
Run the following command to start the comment scrapping script:

 ```
 python Comment_Scrapper.py
```

## SetUp

### Step 1 
First, navigate to the external dictionary folder:

```
cd external/myWord/dict_ver1
```
 
There will be multiple splitted bigram dictionary files.

![image](https://github.com/user-attachments/assets/ae5d8c71-c470-40e4-87dd-4897c5e47816)

Then, run the following command to combine all the splitted files:

```
bash ./combine-all-splitted-files.sh
``` 

You will get the combined ngram dictionaries:
```
$ ls
bigram-phrase.bin  bigram-phrase.txt  bigram-word.bin  bigram-word.txt
```
These combined files are quite large, and GitHub may not be able to accommodate them.

If you're using Git, it's best not to add these files to your git lifecycle or staging area.


### Step 2 
Go to root project folder , there is `testscript.py` for testing purpose.

```
python testscript.py
```

check output using following command :
```
cat output.txt
``` 

# Tokenizing with myWord

You can use the tokenize_text() function  by importing the [myWord](https://github.com/ye-kyaw-thu/myWord) package.
```
from myword import tokenize_text

text = "ကျွန်တော်ကသုတေသနသမားပါ။"

tokens = tokenize_text(text)
print(tokens)

#Output: ကျွန်တော် က သုတေသန သမား ပါ ။ <== word segmented sentence 
```


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
## Repo Explaining Diagram
> Diagram is exported by [gitdiagram](https://gitdiagram.com/)

![diagram](https://github.com/user-attachments/assets/140691da-1bd4-4fa3-a47b-74198a5736f6)


