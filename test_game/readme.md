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
Here is a list of python modules that need to be installed.
```
gensim
numpy
gTTS
pocketsphynx
google-api-python-client
SpeechRecognition
PyAudio
google-cloud-speech
```
Here is a list of common ubuntu/linux packages that must be installed:
```
mpg321
build-essential
portaudio
rhythmbox
libreoffice
vlc
thunderbird
google-chrome
```
## General:
* This project is a 'Work-In-Progress'.
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

## Using `do_w2v_test.py` after training your model:

* `do_w2v_test.py` is a work in progress. You may have to edit the code yourself to get it to run to your specifications.
* Optionally get the text file from the following address:  
http://download.tensorflow.org/data/questions-words.txt    
Put the downloaded file in the `data/` directory.
* basic usage: `./do_w2v_test.py` This will run basic tests that show if you have trained your model sufficiently. It will only test the models that you have trained yourself. The model tested is the one you creaate and save in the `trained/` folder.  
For example, several lines with analogies will print on the screen. They will show if the basic relationship between the cardinal directions have formed.
* making an 'odd_vec': `./do_w2v_test.py 20` This will run the part of the script which tries to save the 'odd_vec' npy file. This vector is used by the test program and the game class to suggest game words when non game words are used by the player.  
The command above devides the vector into patches that are 20 features wide. Good results can be achieved with values of 10, 20, up to 50. This is the reason that a well trained network is desired, so that this function will suggest words better.  
The patch size number must be the first argument on the command line after the script-name.
* results from 'odd_vec': `./do_w2v_test.py -no-find` This prints lists to the terminal showing exactly which non game words are translated to which game words.
* You can also use the `-load-special` flag. This must be used in combination with a downloaded pre-trained model saved in binary form. The one used in the script is from google. A download link on google drive is:    
https://code.google.com/archive/p/word2vec/    
or     
https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing  
This is a 3+ gig download. After downloading the model, run `mkdir -p trained/saved_google/` and put the `bin` file there. Then you should be able to use the `-load-special` flag when creating your 'odd_vec' and when running `-no-find` on your 'odd_vec'.  
The `-load-special` flag must be after all other flags on the terminal command line.

## Training:

* There are two basic methods for training. One uses the `do_w2v_train.py` script and any text you might have. The other method uses the wikipedia articles downloaded above. This second method is more complex and time consuming. It uses three scripts, the `do_w2v_corpus_wiki.py` script, the `do_w2v_corpus_wiki_mod.py` script, and the `do_w2v_train_wiki.py` script.    

## Notes on using Google Speech Recognition
* Install all the recommended python packages and make sure they work.
* Test google speech recognition with the `do_test_google_sr.py` script. The script may be helpful at different times to tell if your setup attempt is working.
* https://cloud.google.com/sdk/docs/quickstart-linux See this url for details.
* https://cloud.google.com/speech/docs/quickstart  See this location for more google setup info.
* https://console.cloud.google.com/apis/ Try this url and see if it works for you.
* You may need to set up a billing account with Google for yourself.

1. Download and install the Google-Cloud-Sdk. This package has the `gcloud` command.
  * This includes downloading the google-cloud-sdk file, unpacking it, and executing the command `./google-cloud-sdk/install.sh`
  * You must also restart your terminal.
2. Use Google Cloud Platform Console to create a project and download a project json file.
  * Setup a google cloud platform account and project. For a project name I used `awesome-sr`
  * I put my project json file in a directory called `/home/<myname>/bin` .
  * Use the `gcloud` command to set up your authentication. I used the following: `gcloud auth activate-service-account --key-file=bin/awesome-sr-*.json`
3. (OPTIONAL) Go to the Google Cloud Platform's API's and Services Page. Generate an API key.
  * Copy the contents to a file called `api_key.txt` . Save this file in the `test_game` directory of this project. (NOTE: I couldn't get the api_key to work and instead tried to use the `gcloud` command.)
  * Execute the script `do_move_api_key_file.sh` after you have placed your key in the `api_key.txt` file.
