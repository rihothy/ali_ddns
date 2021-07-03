# ali_ddns
### Install libraries
```
pip3 install aliyun-python-sdk-core
pip3 install aliyun-python-sdk-domain
pip3 install aliyun-python-sdk-alidns
```

### Fill in the AccessKey and SecretKey
```
line 48| client = AcsClient(AccessKey, SecretKey)
```

### Run
```
python3 ddns.py
```
