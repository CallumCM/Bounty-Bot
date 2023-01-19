curl -O -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb 
sudo apt update 
sudo apt install -f ./google-chrome-stable_current_amd64.deb 
sudo apt-get install chromium-chromedriver
chmod 777 /usr/local/bin/chromedriver
PATH="$PATH:/usr/lib/chromium-browser/"