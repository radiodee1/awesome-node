git clone https://github.com/tensorflow/nmt/

mkdir tmp
## nmt/nmt/scripts/download_iwslt15.sh ./tmp/nmt_data
mkdir ./tmp/nmt_model

git clone --recursive https://github.com/daniel-kukiela/nmt-chatbot
## cd nmt-chatbot/

pip3 install tqdm colorama regex


mkdir tmp/chat_model tmp/chat_data tmp/chat_new

if [ -f data/RC_2015-01.bz2 ] ; then
    echo "found RC"
    cd data/
    
    if [ -f RC_2015-01 ] ; then
    
        echo "already unzipped"
        mv RC_2015-01 ../tmp/chat_new/.
        
    else
        if [ -f ../tmp/chat_new/RC_2015-01 ] ; then
            echo "already moved"
            
        else
            bunzip2 -k RC_2015-01.bz2
            mv RC_2015-01 ../tmp/chat_new/.    
        fi
  
    
    fi
    cd ../
else
    
    echo "nothing for RC_2015-01"
fi
