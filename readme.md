# Commands for updating the service

```commandline
# Logs
cat /var/log/my-python-script.log

# service logs
journalctl -u my-python-script.service -b
```

2. Updating and Restarting the Service

After modifying the service file, reload systemd and restart the service:
```commandline
# stop the service
sudo systemctl stop my-python-script.service

# rename the file in the service config
# Find a line that looks like:
# ExecStart=/home/pi/PycharmProjects/first_one/.venv/bin/python /home/pi/PycharmProjects/first_one/server_and_windowsDec2.py

sudo nano /etc/systemd/system/my-python-script.service

sudo systemctl daemon-reload
sudo systemctl start my-python-script.service
```
 
