# TUS - Time User Signature

TUS is a client-server communication protocol that aims to
verify the validity of a call by signing the transmitted data.

This implementation (javascript / python flask) makes it very easy
to manage client-server communication through the use of: 

* javascript method
* python decorator
  
This implementation also allows you to restrict access
to certain endpoints by using roles.

Some implementation logics are intentionally abstract as they depend 
on the underlying architecture which cannot and should not be binding.

The scope of use is very broad, however it is particularly useful in handling
calls to the methods of an API.

![Schema](https://raw.githubusercontent.com/Amecom/TUS/master/schema.png)

## CLIENT - JAVASCRIPT

The file "tuslib.js" defines two objects "tuslib" and "fun".

* "fun" contains helper functions which should not be called directly.
* "tuslib" contains the three main methods: login, logout and request.

The "request" method allows you to delegate the logics of signing
requests once you have logged in.

This interface allows you to make calls to the server in a very simple way
by passing as parameters:

- the path of the uri
- a dictionary of {properties: value} (data to be sent to the server)
- onSuccess Callback executed on success upon receiving an object with
  data returned from the server
- onError Callback executed in the event of an error that receives a
  string with the error description
  
## SERVER - PYTHON / FLASK

On the server side, the routes using this protocol must simply be decorated 
with the "tus" function of the "tus.py" file

More information can be found in the files.