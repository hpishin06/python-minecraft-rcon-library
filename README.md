# Python Minecraft RCON Library

A working Python library to send RCON commands to a Minecraft server (with output).

## Example

```python
import Rcon

host = '127.0.0.2'  # Server host name or IP
port = 25575         # Port RCON is listening on
password = 'xxx'     # rcon.password setting in server.properties
timeout = 3          # Timeout duration in seconds

rcon = Rcon.Rcon(host, port, password, timeout)

if rcon.connect():
    response = rcon.send_command("kill @a")
    print(response)
else:
    print("Connection failed.")
```

Special thanks to [this repository](https://github.com/thedudeguy/PHP-Minecraft-Rcon) for the logic!
