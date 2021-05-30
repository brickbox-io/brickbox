[![Code Quality](https://github.com/brickbox-io/brickbox/actions/workflows/pylint.yml/badge.svg)](https://github.com/brickbox-io/brickbox/actions/workflows/pylint.yml)

Framework: Django

# Getting Started

```
apt-get install python3-venv -y
python3 -m venv brickbox-env

source brickbox-env/bin/activate
python3 -m pip install -r requirements.txt
```

To update requirements.txt after a new package is installed 
```
python3 -m pip freeze -l >requirements.txt

