# sign-to-text

Translate sign language (just the sign alphabet) to text and back in real-time.

## Setup and Running Locally

First, make sure you have a recent version of python 3 installed. (Tested with
python 3.10.) And make sure that you can run bash scripts. Then, the project
can be set up with:

```
./setup.sh  # If you are not training, you can skip the ASL download
```

Then grab a copy of `model.pkz` and put it in the root of the repository.

Finally, the application can be run as follows:

```
source ./venv/bin/activate  # For MacOS/Linux
python3 app/gui.py
```

## License

The contents of this project, unless stated otherwise, have been released under
the MIT license. See [LICENSE](./LICENSE) for details.
