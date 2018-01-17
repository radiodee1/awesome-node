git clone https://github.com/tensorflow/nmt/

mkdir data/ model/ raw/
touch nmt/__init__.py

if [ -d raw/sequences  ] ; then
    echo "sequences file exists"
else
    cd raw/
    wget https://github.com/edwin-de-jong/mnist-digits-stroke-sequence-data/raw/master/sequences.tar.gz
    
    tar vxzf sequences.tar.gz
    echo "sequences file created"
    cd ..
fi
