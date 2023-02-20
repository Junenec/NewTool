import json
import os
from collections.abc import Iterable
import cv2
import numpy as np


def getMenuStructureData(menuStructure, path, data):
    if data.get('childs'):
        path = path + " -> " + data["Name"]
        for entry in data['childs']:
            getMenuStructureData(menuStructure, path, entry)
    else:
        path = path + " -> " + data["Name"]
        menuStructure.append(path)


def getMenuStructure(jsonData):
    menuStructure = []
    for data in jsonData['UiLocalDisplay']['data']:
        getMenuStructureData(menuStructure, '', data)
    return menuStructure


def loadJsonData():
    jsonData = {}
    ctDirName = "Products\\CM44xPlatform\\Sampler\\ScriptTemplate\\DemoScripts\\GUI_Description"
    menuModelFile = "CSF28_latest.json"  # "CSF28.json"
    PathToFile = os.path.join('%ATS_SCRIPTING_DIR%', ctDirName, menuModelFile)
    PathToFile = "C:\\Work\\NewTool\\Verification\\CSF28_latest.json"
    with open(PathToFile) as jsonFile:
        jsonData = json.load(jsonFile)
    return jsonData


def getParameterPrimitiveData(parameterDict, data):
    if data.get('childs'):
        for entry in data['childs']:
            getParameterPrimitiveData(parameterDict, entry)
    else:
        uuid = data['uuid']
        parameterDict[uuid] = data


def getParameterPrimitive(jsonData):
    parameterDict = {}
    for data in jsonData['ParameterPrimitives']['data']:
        # evaluate recursively
        getParameterPrimitiveData(parameterDict, data)
    for i in parameterDict:
        print("KEY is {}, VALUE is {}\n".format(i, parameterDict[i]))


if __name__ == '__main__':
    loadJsonData()