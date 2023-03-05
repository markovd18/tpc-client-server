# TCP server and client
This repo contans a very simple implementation of multithreaded TCP server and client in Python 3.

## Usage
To start the server, run `python3 server.py [port] [thread count]`.

Arguments:
- `port (optional)` - port on which the server should listen
  - may be arbitraty unsigned integer, but may not work depending on port accessibility on your device
  - defaults to `8080`
- `thread count (optional)` - maximum number of thread workers to run
  - has to be an unsigned integer
  - maximum allowed number of threads is capped to `6`
  - defaults to `3`


To start the client, run the server first, then run `python3 client.py <server port> <message>`.

Arguments:
- `server port (required)` - port on which the server is listening
  - same constraints as with server
  - no default value
- `message (required)` - message to send to server
  - messages longer than 255B will be trimmed
  
### Example
*server*
```bash
> python3 server.py 8080
Parsing parameters: ['server.py', '8080']
Listening on port '8080'.
Maximum number of threads is set to 3.
```
*client*
```bash
> python3 client.py 8080 'Hello, world'
Parsing parameters: ['client.py', '8080', 'Hello, world']
sending message: b'\x0cHello, world'
Response: b'\x0cdlrow ,olleH'
```
*server*
```
// ...
Received connection from ('127.0.0.1', 34394)
received message: b'Hello, world'
sending back message: b'dlrow ,olleH'
```

## Protocol
Server expects incoming data of maximum length of 256B. The first byte is reserved for the length of the message, therefore the maximum length of message may be 255.

Returned message is always of the same length.
- first byte is, again, the length of the message
- rest of the payload is the reversed message which was received

## Implementation caveats
Server implementation is located in the `server.py` file. Client implementation in `client.py`. `shared.py` module contains some of the shared functionality and constants.

### Server
Server multithreading is implementing via Python 3's `concurrent.futures.ThreadPoolExecutor`. Upon starting, server initiates thread pool with configured number of threads. When receiving a connection, main thread submits message handler to be executed by available worker from thread pool.

Connection timeout is set to `60 seconds`.
