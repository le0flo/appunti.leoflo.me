# Notes website

A simple python program that generates a static website that hosts my [notes](https://github.com/le0flo/appunti).
It even has a `config.toml` that tweaks the website's generation.

### Usage

Download the repo:

```sh
git clone https://github.com/le0flo/appunti.leoflo.me
cd appunti.leoflo.me
git submodule update --init
```

Download the required dependencies:

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Available commands:

- `python generate.py .` generates the static website from a given root path
