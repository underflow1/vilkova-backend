# backend for vilkova.ru
#####Prerequisites
> sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools  python3-venv

#####Add user for backend service:
> adduser vilkova

#####Install
> su vilkova
git clone https://github.com/underflow1/vilkova-backend
cd ~/vilkova-backend
python3 -m venv vilkova-backend-venv
source vilkova-backend-venv/bin/activate
pip install wheel gunicorn flask sendgrid
deactivate

#####Create systemd service file
>[Unit]
Description=Gunicorn instance to serve vilkova-backend
After=network.target

>[Service]
Environment="SENDGRID_API_KEY=YOUR_API_KEY"
Environment="SHOP_EMAIL=email@email.ru"

>[Service]
User=vilkova
Group=www-data
WorkingDirectory=/home/vilkova/vilkova-backend
Environment="PATH=/home/vilkova/vilkova-backend/vilkova-backend-venv/bin"
ExecStart=/home/vilkova/vilkova-backend/vilkova-backend-venv/bin/gunicorn --workers 1 --bind unix:/tmp/vilkova-backend.sock -m 007 wsgi:app

>[Install]
WantedBy=multi-user.target

#####Enable service
> systemctl daemon-reload
systemctl enable vilkova-backend
systemctl restart vilkova-backend
systemctl status vilkova-backend

#####Add nginx entry for api endpoint:
> location /api {
    include proxy_params;
    proxy_pass http://unix:/tmp/vilkova-backend.sock;
}

#####restart nginx
>systemctl restart nginx.service
