import os.path
import json

#definition to get list of itemtypes
def getitemtype():
    if os.path.isfile("storedetail.json"):
        a=os.path.abspath(os.getcwd())+"\storedetail.json"
        f=open(a)
        data=json.load(f)
        itype=data["itemtype"]
    else:
        itype=[]
    return itype

#definition to get seed license number
def getlicno(itemtype):
    if os.path.isfile("storedetail.json"):
        a=os.path.abspath(os.getcwd())+"\storedetail.json"
        f=open(a)
        data=json.load(f)
        return data[itemtype]
    else:
        return "lic no not found"

#def to get tin no
def gettinno():
    if os.path.isfile("storedetail.json"):
        a=os.path.abspath(os.getcwd())+"\storedetail.json"
        f=open(a)
        data=json.load(f)
        return data["tinno"]
    else:
        return "tin no not found"

#def to get data
def getdata(val):
    if os.path.isfile("storedetail.json"):
        a=os.path.abspath(os.getcwd())+"\storedetail.json"
        f=open(a)
        data=json.load(f)
        return data[val]
    else:
        return ("No data for "+val)