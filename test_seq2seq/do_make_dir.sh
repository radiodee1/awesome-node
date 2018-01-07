git clone https://github.com/tensorflow/nmt/

mkdir tmp
## nmt/nmt/scripts/download_iwslt15.sh ./tmp/nmt_data
mkdir ./tmp/nmt_model

git clone --recursive https://github.com/daniel-kukiela/nmt-chatbot
## cd nmt-chatbot/

pip3 install tqdm colorama regex
mkdir data/

mkdir tmp/chat_model tmp/chat_data
