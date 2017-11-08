# DevOps

`DevOps` for `AppDev` projects

## Getting Started

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables

If your project involves sensitive information, keep that information as environment
variables.  Place a `.env` in the subdirectory you're working in and have your variables
setup the following way in that file:

```bash
export MY_FIRST_VARIABLE=first_variable
export MY_SECOND_VARIABLE=second_variable
...
```
