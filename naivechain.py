# coding=utf-8
"""
Module Summary Here.
Authors: gorgeousdays@outlook.com
Create time:2021.9.26
"""
import json
import datetime
import hashlib
import logging

from flask import Flask,request
import json
 
app=Flask(__name__)


# set the format of logging
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
)

class Block(object):

    def __init__(self,index,hash,previousHash,timestamp,data):
        self.index=index
        self.hash=hash
        self.previousHash=previousHash
        self.timestamp=timestamp
        self.data=data


def templatePage(blockchain):
    page="<h1>Blockchain</h1>"
    for i in range(len(blockchain)):
        title="<h3>Block</h3>"
        index="<p>"+"index:"+str(blockchain[i].index)+"</p>"
        hash="<p>"+"hash:"+str(blockchain[i].hash)+"</p>"
        previousHash="<p>"+"previousHash:"+str(blockchain[i].previousHash)+"</p>"
        timestampe="<p>"+"timestamp:"+str(blockchain[i].timestamp)+"</p>"
        data="<p>"+"data:"+str(blockchain[i].data)+"</p>"
        page=page+title+index+hash+previousHash+timestampe+data
    return page

def calculateHash(index,previousHash,timestamp,data):
    hashData=hashlib.sha256(str(index).encode()+str(previousHash).encode()+str(timestamp).encode()+str(data).encode()).hexdigest()
    return hashData

def generateNextBlock(blockData,blockchain):
    previousBlock=getLastestBlock(blockchain)

    nextIndex=previousBlock.index+1
    nextTimestamp=int(datetime.datetime.now().timestamp())
    nextHash=calculateHash(nextIndex,previousBlock.hash,nextTimestamp,blockData)

    block=Block(nextIndex,nextHash,previousBlock.hash,nextTimestamp,blockData)
    return block

def getLastestBlock(blockchain):
    return blockchain[len(blockchain)-1]

def calculateHashForBlock(block):
    return calculateHash(block.index,block.previousHash,block.timestamp.block.data)

def gensisBlock():
    block=Block(0, '816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7', None, 1465154705, 'my genesis block!!')
    return block

def isValidNewBlock(newBlock,previousBlock):
    if previousBlock.index+1!=newBlock.index:
        logging.error("invalid index")
        return False
    elif previousBlock.hash!=newBlock.previousHash:
        logging.error("invalid previoushash")
        return False
    elif calculateHashForBlock(newBlock)!=newBlock.hash:
        logging.error("invalid hash:"+calculateHashForBlock(newBlock)+' '+newBlock.hash)
        return False
    return True

def isValidBlockStructure(block):
    intType=type(1)
    stringType=type('1')
    return type(block.index)==intType and type(block.hash)==stringType and type(block.previousHash)==stringType and type(block.timestamp)==intType and type(block.data)==stringType

def isValidGenesis(block):
    genBlock=gensisBlock()
    return block.index==genBlock.index and block.hash==genBlock.hash and block.previousHash==genBlock.previousHash and block.timestamp==genBlock.timestamp and block.data==genBlock.data

def isValidChain(blockChainToValidate):
    if isValidGenesis(blockChainToValidate[0])==False:
        return False
    for i in range(1,len(blockChainToValidate)):
        if isValidNewBlock(blockChainToValidate[i],blockChainToValidate[i-1])==False:
            return False
    return True

def replaceChain(newBlocks,blokchain):
    if isValidChain(newBlocks) and len(newBlocks)>len(blokchain):
        logging.info("Received blockchain is valid. Replacing current blockchain with received blockchain")
        blokchain=newBlocks
    else:
        logging.error("Received blockchain invalid")

@app.route("/blocks",methods=["GET"])
def blocks():
    blockchain.append(gensisBlock())
    logging.info(blockchain[-1].index)
    return  templatePage(blockchain)

@app.route("/mineBlock",methods=["POST","GET"])
def mineBlock():
    data = request.args.get("data")
    newBlock=generateNextBlock(data,blockchain)
    blockchain.append(newBlock)
    logging.info(blockchain[-1].index)
    return  templatePage(blockchain)

if __name__ == "__main__":
    blockchain=[]
    app.run(debug=True)