<br/>
<p align="center">
  <h1 align="center">AutoTrickster</h1>

  <p align="center">
    Automate the complete process of adding fleets to Trickest Community Edition!
    <br/>
    <br/>
    <a href="https://www.youtube.com/watch?v=_P20W7qHwps">View Demo</a>
    .
    <a href="https://github.com/SiddharthBharadwaj/AutoTrickster/issues">Report Bug</a>
    .
    <a href="https://github.com/SiddharthBharadwaj/AutoTrickster/issues">Request Feature</a>
  </p>
</p>

![Downloads](https://img.shields.io/github/downloads/SiddharthBharadwaj/AutoTrickster/total) ![Contributors](https://img.shields.io/github/contributors/SiddharthBharadwaj/AutoTrickster?color=dark-green) ![Issues](https://img.shields.io/github/issues/SiddharthBharadwaj/AutoTrickster) 

## Table Of Contents

* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [Authors](#authors)

## Getting Started

To get started with Trickest Community, you need a Trickest account from https://trickest.com/. And if you are willing to automate the complete process of creating cloud fleets then you will also need a Hetzner account from https://hetzner.cloud/?ref=U06IyeDqAwIB.

Incase you plan on using your own machines or VMs, Hetzner account is optional

### Prerequisites

These are some Prerequisities required for AutoTrickster to work.

##### Python3

```sh
sudo apt-get install python3
```

##### Hetzner Account (For Cloud Fleets)
Use https://hetzner.cloud/?ref=U06IyeDqAwIB to create a Hetzner Account and get €⁠20 in cloud credits.

### Installation

1. After creating a Hetzner account, Create a new project in Hetzner.

2. Get a API key from  [https://console.hetzner.cloud/projects/project-id/security/tokens](https://console.hetzner.cloud/projects/<project-id>/security/tokens)

2. Clone the repo

```sh
git clone https://github.com/SiddharthBharadwaj/AutoTrickster.git
```

2. Change directory to the cloned path

```sh
cd AutoTrickster
```
3. Install required python packages

```sh
pip3 install -r requirements.txt
```

4. Enter your Trickest credentials and Hetzner API key in `config.ini`

```ini
[trickest]
email = trickest email address
password = trickest password
[hetzner]
apikey = hetzner api key
```

## Usage

usage: python3 trickest.py [-h] [--create] [--delete] [--this]

Manage Trickest Community Machines.

options:
  -h, --help  show this help message and exit
  --create    Create and add cloud instances to Trickest fleets.
  --delete    Delete and remove instances from Trickest Fleets
  --this      Use the current machine as a fleet for Trickest Community

## Roadmap

See the [open issues](https://github.com/SiddharthBharadwaj/AutoTrickster/issues) for a list of proposed features (and known issues).

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.
* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/SiddharthBharadwaj/AutoTrickster/issues/new) to discuss it, or directly create a pull request after you edit the *README.md* file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Authors

* **Siddharth Bharadwaj**
* [Github](https://github.com/SiddharthBharadwaj)
* [Telegram](https://t.me/SiddharthBharadwaj)
* [X](https://x.com/____Siddharth__)