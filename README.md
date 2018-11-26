# Minimal Zimbra REST API
_Work in progress ahead!_

This is a REST API for Zimbra based on [python zimbra core framework](https://github.com/Zimbra-Community/python-zimbra).

### Available Endpoints
At this time there are only a couple:

* `/users`: TL;DR: returns id and name of user mailbox.
* `/users/quota`: return id, name of user mailbox, used space and limit space.

### Environment Variables
The API can be configured by setting environment variables:

* `ZIMBRA_URL`: This is Zimbra SOAP endpoint, it is a value in the format of `https://zimbra.hostname:7071/service/admin/soap`.
* `ZIMBRA_USER`: This is Zimbra admin user account, it is a value in the format of `username@zimbra-domain`.
* `ZIMBRA_PASSWORD`: This is Zimbra admin user account password.

### Configuration File
This service can be configured by placing a `service.conf` file in the working directory (filename is mandatory at this time). This is a INI configuration file with one section:

* `[zimbra]`: Zimbra URL, user and password settings.

**Example**
A `service.conf` file is included as an example:

```bash
[zimbra]
zimbra_url: https://zimbra.example.com:7071/service/admin/soap
zimbra_user: admin@example.com
zimbra_password: secret
```

### Variables Processing
All environment variables override configuration variables in `services.conf`. Also, configuration variables are checked with every request at this moment, this might not be a good idea but it's handy for development, so it's a fake hot-reload of configuration.

### Examples
If you decide to run this from your command line:

```bash
$ git clone https://github.com/mxdlx/zimbra-rest-api

# pip shouldn't be used with sudo but unless running inside virtualenv it's possible you'll need to install dependencies at a system-wide level
$ sudo pip install -r requirements.txt

$ FLASK_APP=main.py ZIMBRA_URL=https://zimbra.example.com:7071/service/admin/soap \
                    ZIMBRA_USER=admin@example.com \
		    ZIMBRA_PASSWORD=secret flask run
# Try it
$ curl -I http://127.0.0.1:5000/users
```

If you want yo try this with Docker, there's an available automated build:

```bash
$ sudo docker run -d -p 5000:5000 -e ZIMBRA_URL=https://zimbra.example.com:7071/service/admin/soap \
                                  -e ZIMBRA_USER=admin@example.com \
                                  -e ZIMBRA_PASSWORD=secret mdlee/zimbra-rest-api
# Try it
$ curl -I http://127.0.0.1:5000/users
```
