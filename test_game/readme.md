## Notes:

Refer to these other projects.

* https://github.com/danielricks/textplayer
* https://github.com/DavidGriffith/frotz.git



setup the directory structure:
```
$ ./do_make_dir.sh

```
This is the url for wiki material. put resulting file in `data` dir. Try this url with the `wget` command or your favorite web browser. Should take approx 2 hrs.
````
$ wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
````

## General:
* Download this project.  Run the `do_make_dir.sh` script.
* Run the `do_make_nltk_data.sh` script. This will install all the nltk resources in a central location on your computer. You need this for the training stage. This script will ask for your administrator password.
* Download the wikipedia file and put it in the `data` directory. This should take 2 or more hours.
* Search the internet for zork1 transcripts and walkthroughs. There are many of these online. You want at least one complete transcript of a complete game. Some walkthrouugh files contain general instruction and some have literal transcripts. For the sake of this project you want at least one literal transcript. 
* Run the `trim_words_list.sh` script on the file to create a `list.txt` file.
You also want to use the transcript you find with the `trim_words.sh` script. This is important for training your models. The output from that script should be called `zork1-output.txt` and should go in the `data` folder.
* Run the script `do_w2v_corpus_wiki.py` after that. This will separate out an approximately 185M text file. Keep this file in the `data` folder.
* Run the script `do_w2v_train.py` first. This should take an hour and a half. After that your models should be trained. Files for the two models should be in the `trained` folder. 
* Launch the game using the `launch_game.sh` script. 

## Names:
Files in the `data` directory need to be named in a certain way. The files all need to end with the `.txt` extension. The file from the `do_w2v_corpus_wiki.py` program must start with a 'w'. The file for the zork walkthrough must be named `zork1-output.txt`. 

Other files containing text on zork1, like the unprocessed walkthrough or other instructive text, can be included and must begin with the letter `z` as well as ending with the suffix `.txt`. 

You should find a transcript of gameplay on line and convert it into a text file and run it through the script, in the script directory, called `trim_words_list.sh`. The output of this script should be saved to a file called `list.txt` and put in the `data` folder. This helps the python code to determine the vocabulary for the actual game.

## Example Setup:
A code sample is below.
````bash
$ git clone https://github.com/radiodee1/awesome-node.git
$ cd awesome-node/test_game/
$ ./do_make_dir.sh
$ cd data
$ **download or copy txt files here as zork1-transcript.txt**
$ ../scripts/trim_words.sh zork1-transcript.txt > zork1-output.txt
$ ../scripts/trim_words_list.sh zork1-transcript.txt > list.txt
$ **download more zork files here saved as zork1-something.txt **
$ cd ..
$ ./do_make_nltk_data.sh
<admin password here>
$ cd data
$ wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
$ cd ..
$ ./do_w2v_corpus_wiki.py data/enwiki.xxx.xml.bz2 data/wiki.en.10000.txt
$ ./do_w2v_train.py
$ ./launch_game.sh

````