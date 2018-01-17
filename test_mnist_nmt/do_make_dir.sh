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

exit

## do_make_train_test.py does this!!

if [ -f raw/train-labels-idx1-ubyte.gz ] ; then
    echo ""
else
    cd raw/
    wget http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz
    gunzip train-labels-idx1-ubyte.gz
    cd ..
fi

if [ -f raw/t10k-labels-idx1-ubyte.gz ] ; then
    echo ""
else
    cd raw/
    wget http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz
    gunzip t10k-labels-idx1-ubyte.gz
    cd ..
fi
