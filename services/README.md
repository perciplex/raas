Explicitly, these things need to get done in order for the service to begin. Will make a nice lil script for it

`sudo cp services/raas_cs.service /lib/systemd/system/`
`sudo cp services/raas_mc.service /lib/systemd/system/`

`sudo chmod 644 /lib/systemd/system/raas_cs.service`
`sudo chmod 644 /lib/systemd/system/raas_mc.service`

`sudo systemctl daemon-reload`
`sudo systemctl enable raas_cs.service`
`sudo systemctl enable raas_mc.service`

`sudo systemctl start raas_mc.service`
`sudo systemctl start raas_cs.service`