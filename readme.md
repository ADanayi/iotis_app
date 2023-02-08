<!-- In the name of Allah -->

# Iotis

**This library is designed for the application layer of Iotis. For Node layer, please refer to the corresponding repository.**

Iotis is a 2 layer abstract IoT (Internet of Things) platform, designed and implemented in order to make you enjoy the full potential of IoT as easy as drinking a glass of water!

> Let's IoTize our projects and products!

## Python examples
*Note: You should first clone or download `iotis_app` repository on your server or computer. Right now, `iotis_app` can not be installed using `pip`. But we're going to add the `PyPI` support in the future.*

### What kind of applications can I use?
It depends on your product and bought plans. If you have a GPIotis board, you can use all of the functionality of `gpio` module. If you have submitted for an `admin` plan, you can also use `core` module which can let you send and receive any kind of message to your node and vice-versa.

### Starting up! (For admin users)
The first step is to create a `CoreEngine` object.

You'll need the `username` and your public key file which can be downloaded from Iotis panel. Iotis uses it's own authentication protocol which is included in the library and you don't need to implement it. 

Just remember to install `pycryptodome` library using `pip`:
```bash
pip install pycryptodome
```

Once you installed `pycryptodome` and you have your username and key file, you're ready to start everything:

```python
import iotis_app.python as iot

iotis_server_url = "https://my.iotis.ir/v1/core" # This is the address of our test server's core!
username = "abolfazl" # Replace abolfazl with your application-username 
public_key_path = "./pub.key" # Replace "./pub.key" with the address of your security key file's address

req_engine = iot.CoreEngine(username, public_key_path, iotis_server_url)
```

If you are registered for a dedicated server, please change the `iotis_server_url` with your given server's url in your admin panel. (Please check our plans in [iotis's website](https://iotis.ir)). 


### Checking node's connection status
You can check the connectedness of a node every time you need.

```python
node_uid = '2KE3tl6Ra87B'
resp = req_engine.node_is_connected(node_uid)

if resp:
    # Request is succussful
    node_status = resp.result['connected']
    print('Node is ', end='')
    if node_status:
        print('connected.')
    else:
        print('not connected.')
else:
    print('Request error with error code: %d' % resp.error_code)
```

### Sending a message to node
When you want the message to node **right now**, you can `send` it.

The message can be a standard `string`. A `JSON` is also a `string`, but you need to parse or convert it at the node layer.

```python
resp = req_engine.send_message_to_node(node_uid, "This is a test message!")

if resp:
    print('Message is sent to the node.')
else:
    print('Request error with error code: %d' % resp.error_code)
```

**Note: You will get a #21 error if the node is not connected when calling this request.**

### Pushing a message to node
Sometimes, you want the node to get your message as soon as it's connected, but it's not necessary to get it right now. In such scenario, you can use `push` mechanism. 

```python
resp = req_engine.push_message_to_node(node_uid, "This is a test message!")

if resp:
    print('Message is pushed to the node.')
else:
    print('Request error with error code: %d' % resp.error_code)
```
