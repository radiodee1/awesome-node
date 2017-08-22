mkdir -p data trained
echo "the data directory is for sample text"
echo "the trained directory is for saving the trained neural net"
echo "both are essential."
cd textplayer
git submodule init
git submodule update
cd ..
cd frotz
git submodule init
git submodule update
make dumb
cd ..
cp -r frotz/ textplayer/frotz
touch ./textplayer/.gitignore
echo "frotz" >> ./textplayer/.gitignore
echo "" >> ./textplayer/.gitignore
echo "textplayer" >> .gitignore
echo "" >> .gitignore
echo "frotz" >> .gitignore
echo "" >> .gitignore
git rm -r --cached textplayer/
