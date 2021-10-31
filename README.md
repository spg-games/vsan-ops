# vsan-ops
vSAN Ops tools.

## How to use

1. Download vSAN Management SDK for Python
```
cp bindings/vsanmgmtObjects.py ./
cp samplecode/vsanapiutils.py ./
```
2. pip install
```
pip3 install pyvmomi defusedxml tabulate
```
3. exec script
```
python3.7 get_Virtual_Objects.py --host $host -u administrator@vsphere.local -p $pass -c Cluster
```

[vSAN Management API入門してみました](https://webprog.spg-games.net/2021-10-31/vsan-management-api%E5%85%A5%E9%96%80%E3%81%97%E3%81%A6%E3%81%BF%E3%81%BE%E3%81%97%E3%81%9F/)
