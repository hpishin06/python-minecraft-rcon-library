# python-minecraft-rcon-library
2024 working python library to send rcon commands to minecraft server ( with output )

<h2>example</h2>
```python
import Rcon
host = '127.0.0.2'  # Server host name or IP
port = 25575            # Port rcon is listening on
password = 'xxx'      # rcon.password setting set in server.properties
timeout = 3             # How long to timeout.

Rcon = Rcon.Rcon(host, port, password, timeout)

if Rcon.connect():
    mame = Rcon.send_command("kill @a")
    print(mame)
```

special thanks to [this repo](https://github.com/thedudeguy/PHP-Minecraft-Rcon) for logics!
