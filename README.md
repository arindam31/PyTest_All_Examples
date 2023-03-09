## How to run tests:

The tests optionally can be passed a config file to be present with configurations of device under test.
The '--cfg' argument can be used to pass the name of the ini file.
Default: config.ini

```
pytest test_practise.py --cfg=some_config.ini
```

If user does not pass the above param, a default value is considered: (config.ini)

## For running tests with coverage:
```
python3 -m pytest --cov
```

## Reports.
Reports can be found in the report directory. 
Everytime you run the test, two reports are generated. One by default, and another a custome designed report using Jinja.