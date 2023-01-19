chmod +x main.py
source venv/bin/activate
echo "Launching barbara in new screen... Run screen -r barbara"
screen -dmS bounty python3 main.py