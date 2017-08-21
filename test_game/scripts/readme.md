# Notes

There are two versions of the trim script. They take text from a walkthrough and remove all the sentences that already have a period. This ends up being all the descriptive lines. What's left is lines that were entered on the ">" prompt. This is all the vocabulary from the game as it is to be used by a player. Then, for the parser, the script puts a period after the sentences.

If you start out with an accurate transcription of the walkthrough, you will have possibly three types of text. You will have (1) headings (2) descriptive passages ending with periods, and (3) the actual text from the commands that are to be entered by the player. The descriptive passages, noted as -2- are removed by the scripts. The headings and the text commands are useful and should be kept. 

It is important to find an actual transcript of game play for the training of the word2vec program. There are many types of walkthrough out there. Try to get a real transcription of game play.

The second version of the shell script in this folder also adds a keyword to the end of the sentences. This is so that they are labled somehow for the w2v program. This second version of the script is probably not needed for most people.
