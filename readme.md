# Commands for updating the service

# Procedure for updating
Push changes to master from Master computer and pull using the operational computer


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
sudo systemctl daemon-reload
sudo systemctl start my-python-script.service
```
 

3. If you want to see the service file:
```commandline

# The current file used for the service is the one without a date
# ExecStart=/home/pi/PycharmProjects/first_one/.venv/bin/python /home/pi/PycharmProjects/first_one/server_and_windows.py

sudo nano /etc/systemd/system/my-python-script.service
```