# NetSpectre

## Installation

#### NetSpectre requirements
- [python](https://www.python.org/downloads/) 3.9 or later version
- [wireshark](https://www.wireshark.org/download.html)
- [nmap](https://nmap.org/download.html)
    
Ensure that you set wireshark and nmap to Path/bin depending on what OS you are operating on

## Setup Environment
Once you have installed the necessities from [NetSpectre requirements](#netspectre-requirements) you can create your environment

#### Pip installations
`pip install python-nmap`

`pip install pyshark`

## Basics of the language
This language is focused around simplicity and scalability. Think of it as python and yaml colliding. It is a parameter focused langauge creating **configurations** and implementing them. Every line of code will have two elements **Keys** and **Values**. **Keys** are predefined identifers in the programming language and would require you to modify the interpreter itself inorder to change there value. **Values** are the values of the keys that you can set. 

These keys can be found in [**Key List**](#key-list-tokens) that comprise of the 4 main tokens: **config_capture**, **config_scan**, **capture**, and **scan**

### Key List (Tokens)
#### Configuration Keys (Tokens)
- **config_capture** 
- **config_scan**
#### Capture and Scan Keys (Tokens)
- **capture**
- **scan**

#### Config_capture Parameter Keys : explanation of value
- **interface** : the name of the network interface
- **packets** : the number of packets you want to capture
- **ipv4** : the IPv4 address you want to scope your packet captures around (optional)
- **json** : boolean value if you want output in json format (**ek and json can't both be set to TRUE**)
- **ek** : boolean value if you want output in ek format (**ek and json can't both be set to TRUE**)

#### Config_scan Parameter Keys
- **target** : ip/s you want to scan on the network
- **ports** : ports you want to check that status of on the ip/s set prior
- **arguments** : you can give the scan extra arguments (**for higher level expertise**) found in [nmap arguments](https://nmap.org/book/man-briefoptions.html) (optional)
- **verbose_levels** : an interger 1-5 the higher the value the more detail you will get in your output

### Code Structure
```
config_capture : <name_your_capture_configuration> //ex: cap1
    interface : <name_of_interface> //ex: Ethernet
    packets : <num_of_packets> //ex: 60
    ipv4 : <ipv4_address> //ex: 192.168.1.1
    json : <boolean> //ex: True
    ek : <boolean> //ex: False

capture : <name_of_capture_configuration> //ex: cap1

config_scan : <name_your_scan_configuration> //ex: hibbygibbyscan
    target : <ip4v_address> //ex: 192.168.1.1   /   192.168.1.1-10   /   192.168.1.0/24
    ports : <port/s_to_target> //ex: 80   /   79, 82    /   60-80
    arguments : <arguments_found_in_nmap_documentation> //ex: -T4 -F -A
    verbose_level : <int_1-5> //ex: 1

scan : <name_of_scan_configuration> //ex: hibbygibbyscan
```
Ensure that the configuration is created before it is called to

Make sure to have a line of space in between [**Key List Tokens**](#key-list-tokens)

### Code Sample
![Program Sample](assets/NetSpectreProgram.jpg)


### How the Interpreter Works
Runs through the program line by line when it comes aross a configuration token it parses the lines and establishes the parameters for that configuration and is stored to be called upon later by its proper reference token and value. When a **capture : <config_name>** is called, it runs a capture with the given parameters to the config **Value <config_name>** you assigned. Same for **scan : <config_name>**, it is called, then runs a scan with the parameters assigned to that configuration name.

### Future Modifications
Make the interpreter accessible from anywhere on the OS
```
NetSpectre program.ns
```

Right now you have to place your program into the programs folder then modify one of the last lines in the interpreter to call to your program

```
interpreter.interpret_file("programs/program.ns")
```

Make calls to the configurations with the **capture :** and **scan :** tokens able to be written anywhere in the program by having the interpreter read through the entire program create the configurations then address the captures and scans.


