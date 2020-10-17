# Node-red running on Raspberry Pi

## Prerequisites
If you are using Raspbian, then you must have Raspbian Jessie as a minimum version. Raspbian Buster is the currently supported version.

Installing and Upgrading Node-RED
We provide a script to install Node.js, npm and Node-RED onto a Raspberry Pi. The script can also be used to upgrade an existing install when a new release is available.

Running the following command will download and run the script. If you want to review the contents of the script first, you can view it [here](https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered).

```shell script
bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
```
This script will work on any Debian-based operating system, including Ubuntu and Diet-Pi. You may need to run sudo apt install build-essential git first to ensure npm is able to build any binary modules it needs to install.
This script will:

* remove the pre-packaged version of Node-RED and Node.js if they are present
* install the current Node.js LTS release using the NodeSource. If it detects Node.js is already installed from NodeSource, it will ensure it is at least Node 8, but otherwise leave it alone
* install the latest version of Node-RED using npm
* optionally install a collection of useful Pi-specific nodes
* setup Node-RED to run as a service and provide a set of commands to work with the service

Node-RED has also been packaged for the Raspbian repositories and appears in their list of 'Recommended Software'. This allows it to be installed using apt-get install nodered and includes the Raspbian-packaged version of Node.js, but does not include npm.
While using these packages is convenient at first, we strongly recommend using our install script above instead.

## Running as a service
The install script for the Pi also sets it up to run as a service. This means it can run in the background and be enabled to automatically start on boot.

The following commands are provided to work with the service:

node-red-start - this starts the Node-RED service and displays its log output. Pressing Ctrl-C or closing the window does not stop the service; it keeps running in the background
node-red-stop - this stops the Node-RED service
node-red-restart - this stops and restarts the Node-RED service
node-red-log - this displays the log output of the service

You can also start the Node-RED service on the Raspbian Desktop by selecting the Menu -> Programming -> Node-RED menu option.
## Autostarting on boot
If you want Node-RED to run when the Pi is turned on, or re-booted, you can enable the service to autostart by running the command:
```shell script
sudo systemctl enable nodered.service
```
To disable the service, run the command:
```shell script
sudo systemctl disable nodered.service
```
## Securing Node-RED
By default, the Node-RED editor is not secured - anyone who can access its IP address can access the editor and deploy changes.

This is only suitable if you are running on a trusted network.

This guide describes how you can secure Node-RED. The security is split into three parts:
### Enabling HTTPS access
To enable access to the Node-RED Editor over HTTPS, rather than the default HTTP, you can use the https configuration option in your setting file.

The https option can be either a static set og configuration options, or since Node-RED 1.1.0, a function that returns the options.

The full set of options are documentd [here](https://nodejs.org/api/tls.html#tls_tls_createsecurecontext_options).

As a minimum, the options should include:
* key - Private key in PEM format, provided as a String or Buffer.
* cert - Cert chain in PEM format, provided as a String or Buffer.

For a guide on how to generate certificates, you can follow this [guide](https://it.knightnet.org.uk/kb/nr-qa/https-valid-certificates/).

### Install network packet capture for Node-RED
```shell script
sudo apt install libpcap-dev
npm install node-red-contrib-pcap # Please install customized node-red-contrib-pcap.
```

### Install NTP server
check this [paper](https://medium.com/@rishabhdevyadav/how-to-install-ntp-server-and-client-s-on-ubuntu-18-04-lts-f0562e41d0e1)
```
sudo apt-get install ntp
```

### Design workflow to interpret pcap
this is sample package formation
LINKTYPE_ETHERNET f0:18:98:ad:c2:8a -> 40:ee:dd:5d:bd:c4 IPv4 192.168.1.118 -> 13.250.177.223 flags [d] TCP 58666->443 seq 826836336 ack 534459785 flags [ar] win 2047 csum 13015 [.] len 0
LINKTYPE_ETHERNET 40:ee:dd:5d:bd:c4 -> f0:18:98:ad:c2:8a IPv4 203.205.255.221 -> 192.168.1.118 flags [d] TCP 443->58224 seq 3333002952 ack 4214607568 flags [ap] win 63 csum 14916 [.] len 184