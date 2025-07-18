For generation py files from proto files (example):

While you are in root i.e product
> C:\Projects\PyTest_All_Examples\embedded_device_testing\product>
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/device.proto --pyi_out=.
```
Note: -I. tells protoc that the root of the .proto files is current dir (product/)

Running the server (be at product root):
```bash
python -m servers.device_server
```

Running tests:
```bash
python -m pytest
python -m pytest -k "test_get_sw_info"
```

Running tests with reports:
```bash
pytest --html=report.html
```

Running with Allure
On Windows, install scoop, then allure.
```powershell
Set-ExecutionPolicy RemoteSigned -scope CurrentUser
scoop install allure
python -m pytest --alluredir=allure-results
allure serve allure-results
```
