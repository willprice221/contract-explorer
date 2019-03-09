function setup() {
    sudo apt-get update
    sudo apt-get install python-pip -y

    sudo apt-get install virtualenv -y
    sudo apt-get install python3.6-dev -y
}

function install_contract_explorer() {
    git clone https://github.com/willprice221/contract-explorer.git
    cd contract-explorer/web

    virtualenv -p python3 venv
    source venv/bin/activate

    pip install -r requirements.txt
    # getting the model file
    sudo apt-get install unzip -y
    gsutil cp gs://contract-explorer-dataset/models.zip .
    unzip models.zip -d models
}

function setup_webapp() {
cat << EOT > ~/webapp.service
[Unit]
Description=Webapp
[Service]
ExecStart=/home/ankit/contract-explorer/web/venv/bin/python /home/ankit/contract-explorer/web/main.py
User=root
Group=root
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure
RestartPreventExitStatus=255
Type=simple
[Install]
WantedBy=multi-user.target
EOT

sudo mv ~/webapp.service  /etc/systemd/system/webapp.service
}

setup
install_contract_explorer
setup_webapp
sudo systemctl enable webapp
sudo systemctl start webapp