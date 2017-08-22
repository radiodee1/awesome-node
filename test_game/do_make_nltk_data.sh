#!/bin/bash

echo "This will download all of the nltk_data to the directory '/usr/local/share/nltk_data'"
echo "You may want to run this when you suspect updates have been made to the nltk_data."
echo "note: administrator password is required."
echo ""

sudo python -m nltk.downloader -d /usr/local/share/nltk_data all
