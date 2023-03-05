## How to run tests:

The tests expect a config file to be present with configurations of device under test.
The '--cfg' argument can be used to pass the name of the ini file.

```
pytest test_practise.py --cfg=some_config.ini
```

If user does not pass the above param, a default value is considered: (config.ini)