# Notes website

A simple python program that generates a static website that hosts my [notes](https://github.com/le0flo/appunti).
It even has a `config.toml` to tweak the website's generation.

### Usage

Download the repo:

```sh
git clone https://github.com/le0flo/hermes.git
cd hermes
```

Initialize the submodule:

```sh
git submodule init
git submodule update --remote
```

Generate the website:

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python generate.py .
```
