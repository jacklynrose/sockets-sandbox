# Socket Sandbox

### What does it do

- `pico.py` is the server
  - It will accept commands
  - Commands are the first 24 bits
  - Commands must start with 1
  - First 4 bits are the command header
  - Next 20 bits are the command data
- `quicksend.py` allows sending a command to the server
  - `python3 quicksend.py <binary>`
- `pi.py` is an example echo client
  - it will connect and send an initial command
  - it will then wait to receive a response
  - it will do this every 2 seconds

### Usage

#### Start the server

```bash
python3 pico.py
```

Control-C will exit gracefully

The server will handle clients disconnecting and wait for a new connection.

#### Send a quick command

None of these actually do anything except print to the console from the server

```bash
# Invalid command
python3 quicksend.py 101

# Emit command
python3 quicksend.py 111110101010101010101010

# Return status  command
python3 quicksend.py 101010101010101010101010

# Power saving mode command
python3 quicksend.py 100110101010101010101010
```
