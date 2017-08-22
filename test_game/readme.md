## Notes:

Refer to these other projects.
```
see: https://github.com/danielricks/textplayer
also see: $ git clone https://github.com/DavidGriffith/frotz.git
```

building frotz for this project:
```
$ git clone https://github.com/danielricks/textplayer.git
$ cd textplayer
$ git clone https://github.com/DavidGriffith/frotz.git
$ cd frotz
$ make dumb
$ cd ..
```
setup the directory structure:
```
$ ./do_make_dir.sh

```
This is the url for wiki material. put resulting file in 'data/' dir. Try this url with the `wget` command or your favorite web browser. Should take approx 2 hrs.
````
https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
````

* Download this project and follow the instructions above to build `frotz` for use by the python scripts in this project. You will want to build the `textplayer` project also for everything to work. You need a copy of the file `zork1.z5` in the `textplayer/games` folder. That is the file for the actual game.
* Run the `do_make_nltk_data.sh` script. This will install all the nltk resources in a central location on your computer. You need this for the training stage.
* Download the wikipedia file and put it in the `data` directory. This should take 2 or more hours.
* Run the script `do_w2v_corpus_wiki.py` after that. This will separate out an approximately 185M text file. Keep this file in the `data` folder.
* Run the script `do_w2v_train.py` first. This should take an hour and a half. After that your models should be trained. Files for the two models should be in the `trained` folder. 
* Launch the game using the `launch_game.sh` script. 