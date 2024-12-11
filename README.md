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
This language is focused around simplicity and scalability. Think of it as python and yaml colliding. It is a parameter focused langauge creating **configurations** and implementing them. Every line of code will have two elements **Keys** and **Values**. Keys are predefined identifers in the programming language and would require you to modify the interpreter itself inorder to change there name convention. Values are the values of the keys that you can set. 

These keys can be found in [**Key List**](#key_list) that comprise of the 4 main tokens: **config_capture**, **config_scan**, **capture**, and **scan**

### Key List (Tokens)
- **config_capture** 
- **config_scan**
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
`config_capture : <name_your_capture_configuration>

    interface : <name_of_interface>

    packets : <num_of_packets>
    
    ipv4 : <ipv4_address>
    
    json : <boolean>
    
    ek : <boolean>

capture : <name_of_capture_configuration>`





