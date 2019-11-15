Explicitly, these things need to get done in order for the service to begin. Will make a nice lil script for it

`sudo cp services/container_scheduler.service /lib/systemd/system/`
`sudo cp services/motor_controller.service /lib/systemd/system/`

`sudo chmod 644 /lib/systemd/system/container_scheduler.service`
`sudo chmod 644 /lib/systemd/system/motor_controller.service`

`sudo systemctl daemon-reload`
`sudo systemctl enable container_scheduler.service`
`sudo systemctl enable motor_controller.service`

`sudo systemctl start container_scheduler.service`
`sudo systemctl start container_scheduler.service`