# HateRadar

Coding weeks project to detect and analyse insults in the replies to a twitter user. This app provides several graphics representing the insult rate and the evolution of hatefull responses to the tweets of a given user.

All the programs are made to work with english only. 

## Team Members
+ Vianney Ruhlmann
+ Othman El Menjra-Saady
+ Julie Veschambre
+ Jonathan Poli
+ Mathilde Proust
+ Khadija Bouassida
## Installation

To install the dependencies do:

```bash
pip install -r requirements.txt
```

Add a file ```credentials.py``` where you replaced the KEYS by yours:
```bash
 # Twitter App access keys for @user

# Consume:
CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'

# Access:
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
ACCESS_SECRET = 'YOUR_ACCESS_SECRET'
```

## Usage

Execute main.py then enter the name of the user *ex:@user*.

After the server has started connect to the ip address printed in the terminal.

## Contributing
This project may not receive support after the end of the Coding Weeks i.e. after 20/11/20, although feel free to fork it if you want to extend the project.

## License
[MIT](https://choosealicense.com/licenses/mit/)
