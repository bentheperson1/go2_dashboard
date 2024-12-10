#!/bin/bash

SERVICE_NAME="startup_dashboard"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
SCRIPT_DIR="$HOME/go2_dashboard"
SERVER_SCRIPT="${SCRIPT_DIR}/startup_dashbord.sh"
REQUIREMENTS_FILE="${SCRIPT_DIR}/requirements.txt"

sudo apt update
sudo apt install -y python3 python3-venv python3-pip systemd

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

[Install]
WantedBy=multi-user.target
EOF"

sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

echo "Flask service setup complete."
echo "Use 'sudo systemctl status $SERVICE_NAME' to check its status."
