#!/bin/bash

SERVICE_NAME="startup_dashboard"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
SCRIPT_DIR="$HOME/go2_dashboard"
SERVER_SCRIPT="${SCRIPT_DIR}/startup_dashbord.sh"
REQUIREMENTS_FILE="${SCRIPT_DIR}/requirements.txt"

sudo apt update
sudo apt install -y python3 python3-venv python3-pip systemd

if ! command -v cmake &> /dev/null; then
    echo "CMake not found. Installing..."
    sudo apt install -y cmake
else
    echo "CMake is already installed. Skipping installation."
fi

if [ ! -d "$HOME/cyclonedds/install" ]; then
    echo "CycloneDDS not found. Installing..."
    cd ~ || exit
    git clone https://github.com/eclipse-cyclonedds/cyclonedds -b releases/0.10.x 
    cd cyclonedds || exit
    mkdir build install && cd build || exit
    cmake .. -DCMAKE_INSTALL_PREFIX="$HOME/cyclonedds/install"
    cmake --build . --target install

    # Export and persist environment variable
    export CYCLONEDDS_HOME="$HOME/cyclonedds/install"
    echo "export CYCLONEDDS_HOME=\"$HOME/cyclonedds/install\"" >> "$HOME/.bashrc"
    echo "CycloneDDS installed and environment variable set."
else
    echo "CycloneDDS is already installed. Skipping installation."
fi

# Load environment variables immediately
source "$HOME/.bashrc"

cd "$SCRIPT_DIR" || exit

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

if [ -f "$REQUIREMENTS_FILE" ]; then
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "requirements.txt not found. Please add your packages there."
fi

cat << EOF > "$SERVER_SCRIPT"
#!/bin/bash

cd $SCRIPT_DIR

source venv/bin/activate

python3 app.py
EOF

chmod +x "$SERVER_SCRIPT"

sudo bash -c "cat << EOF > $SERVICE_FILE
[Unit]
Description=Automatically start the Go2 dashboard
After=network.target

[Service]
Type=simple
ExecStart=$SERVER_SCRIPT
Restart=always
User=$(whoami)
WorkingDirectory=$SCRIPT_DIR
Environment=CYCLONEDDS_HOME=$HOME/cyclonedds/install

[Install]
WantedBy=multi-user.target
EOF"

sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

echo "Go2 dashboard setup complete."
echo "Use 'sudo systemctl status $SERVICE_NAME' to check its status."
