Heavily copied from https://github.com/mivade/tornadose

Before deciding whether or not include that as dependency, I prefer rewrite "everything".
This is my preferred way to learn something "new".

Typical setup:

1) create a virtualenv
2) install the package
3) run
4) open localhost:8080

```
python3 -m venv .venv
pip install .
sse_example -p 8080 -vvv
```
