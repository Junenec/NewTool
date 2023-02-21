# -*- coding: utf-8 -*-
"""
:Responsible: Jessie Zhang
:Reviewed by: ()

Test case description
---------------------
Polarion ID: TODO
Check GUI menus

Test parameters
---------------------

Revision
--------
:$URL: $
:$Date: 2022-11-30 11:46:00 +0800 $
:$Revision: $
"""
import time
import json
import os
import re
from Products.CM44xPlatform.Sampler.ScriptTemplate.ScriptTemplateSampler import ScriptTemplateSampler
from Products.CM44xPlatform.Sampler.Transmitter.Sampler import PumpTypes
from Products.ProductsCommon.Libraries.ControlInterface.ControlInterfaceFactory import ControlInterfaceFactory
from Products.ProductsCommon.Libraries_V2.LibFactory import LibFactory
import Products.ProductsCommon.Libraries.Reporting.Imports as Reporting


class Check_HMI_Blocks(ScriptTemplateSampler):
    def __init__(self, relativeFilePath):
        super().__init__(__doc__)
        # Define instance for device control
        self.controlInterface = None
        self.rebootLib = None
        # Define the result table set
        self.NotAccessiblePaths = []
        self.ResultingErrorList = []
        self.NotFoundItemsList = []
        self.UnexpectedItemsList = []
        self.IncorrectPageTypeList = []
        self.UnresolvedConditionList = []
        self.UnmappedParameterUUIDsList = []
        self.UnresolvedSpecificationList = []
        self.CheckFailures = []
        # define internal definition data sheet
        self.__relativeFilePath = relativeFilePath
        self.__menuUUID = None
        self.__parameterDict = {}
        self.__SysetemParameterDict = {}
        self.__DeviceUiParameterDict = {}
        self.__WebUiParameterDict = {}
        self.__MenuUiLocalDisplayDict = {}
        self.__MenuStructureDict = {}

    def setup(self):
        # Configure error handling: do not stop test on first failed testcase
        self.ErrorHandling.MsgFailedErrorEnabled = False

    def cleanupTest(self):
        self.__testMenuData()
        # # postprocessing:
        # self.R.addComment('\n### Navigation errors:')
        # for entry in self.ResultingErrorList:
        #     self.R.addComment(entry)
        # self.R.addComment('\n### Not accessible paths:')
        # for entry in self.NotAccessiblePaths:
        #     self.R.addComment(entry)
        # self.R.addComment('\n### Not found items:')
        # for entry in self.NotFoundItemsList:
        #     self.R.addComment(entry)
        # self.R.addComment('\n### Unexpected items:')
        # for entry in self.UnexpectedItemsList:
        #     self.R.addComment(entry)
        # self.R.addComment('\n### Wrong page types:')
        # for entry in self.IncorrectPageTypeList:
        #     self.R.addComment(entry)
        # self.R.addComment('\n### Unresolved conditions:')
        # for entry in self.UnresolvedConditionsList:
        #     self.R.addComment(entry)
        # self.R.addComment('\n### Unmapped parameter uuids:')
        # # for entry in self.UnmappedParameterUUIDsList:
        # #     self.R.addComment(entry)
        # self.R.addComment('\n### Unresolved specifications:')
        # for entry in self.UnresolvedSpecificationList:
        #     self.R.addComment(entry)
        # self.R.addComment('\n### Failed checks:')
        # for entry in self.CheckFailures:
        #     self.R.addComment(entry)
        #
        # sumOfFailures = len(self.ResultingErrorList) + len(self.NotAccessiblePaths) + len(
        #     self.NotFoundItemsList) + len(self.CheckFailures)
        #
        # self.R.addCheck(sumOfFailures == 0,
        #                 'Menu structure consistent with specification [{0}]'.format(self.PathToFile))


    @Reporting.ReportTestCase("Start condition")
    def __startCondition(self):
        # Retrieve testable Menu Data
        self.__retrieveJSONFile()
        self.__restructureMenuUiLDData()
        self.__restructureParameterData()
        self.__testMenuData()
        # Create control interface
        self.controlInterface = ControlInterfaceFactory.getControlInterface(self.samplerProxy)
        self._tdHMI = self.controlInterface._tdHMI
        # Initialize rebootLib
        self.rebootLib = LibFactory.getRebootLib(self.controlInterface, self.R)

    @Reporting.ReportTestCase("Check menu structure")
    def __checkMenuStructure(self):
        # 1. Navigate to root page
        self._tdHMI.navigateToRootPage()
        time.sleep(2)
        self._tdHMI.pressKeyForPageChange(1)
        # TODO: verify menu structure based on menu data
        for uuid in self.__MenuStructureDict:
            self.R.addComment('Start to verify menu: {}'.format(self.__MenuStructureDict[uuid]['Name']))
            if self.__MenuStructureDict[uuid]['type'] == 'SingleSelect':
                self.__checkMenuSingleSelect(uuid)
            self.R.addComment('End to verify menu: {}'.format(self.__MenuStructureDict[uuid]['Name']))

    def runTest(self):
        # Call test cases
        self.__startCondition()
        self.__checkMenuStructure()

    """
    Define internal usage function for Menu Data retrieve in following part
    """
    # Retrieve raw data from JSON file
    def __retrieveJSONFile(self):
        # Load JSON data from json file
        self.PathToFile = os.path.join('%ATS_SCRIPTING_DIR%', self.__relativeFilePath)
        self.PathToFile = os.path.expandvars(self.PathToFile)
        with open(self.PathToFile) as jsonFile:
            jsonData = json.load(jsonFile)
        # Retrieve Parameter Primitives data
        for data in jsonData['ParameterPrimitives']['data']:
            self.__getParameterPrimitiveData(data, self.__parameterDict)
        # Retrieve System Setup Parameter data
        for data in jsonData['UiSystemSetup']['data']:
            self.__getParameterPrimitiveData(data, self.__SysetemParameterDict)
        # Retrieve Menu Ui Local Display data
        for data in jsonData['UiLocalDisplay']['data']:
            if data['type'] == 'MenuPage':
                self.__menuUUID = data['uuid']
                for child in data['childs']:
                    self.__getMenuUiLocalDisplayData(child)
        # for uuid in self.__MenuUiLocalDisplayDict:
        #     print("{}\n".format(self.__MenuUiLocalDisplayDict[uuid]))
        # TODO: Wizard Ui Local Display data

    # define recursive function to get Parameter Primitive attributes
    def __getParameterPrimitiveData(self, data, datalist):
        if data.get('childs'):
            for entry in data['childs']:
                self.__getParameterPrimitiveData(entry, datalist)
        else:
            if(self.__evaluatePPData(data)):
                uuid = data['uuid']
                # Add currentValue for parameter as default value
                if data['type'] in ['Integer', 'Real', 'Text', 'DateTime']:
                    data['currentValue'] = data['Default']
                elif data['type'] == "Enum":
                    if len(data['DefaultKeysArr']) == 0:
                        data['currentValue'] = None
                    if len(data['DefaultKeysArr']) == 1:
                        data['currentValue'] = data['DefaultKeysArr'][0]
                    if len(data['DefaultKeysArr']) > 1:
                        data['currentValue'] = str(data['DefaultKeysArr'][0])
                        for i in range(1, len(data['DefaultKeysArr'])):
                            data['currentValue'] = data['currentValue'] + " " + str(data['DefaultKeysArr'][i])
                elif data['type'] == "Duration":
                    data['currentValue'] = {}
                    data['currentValue']['DefaultHour'] = data['DefaultHour']
                    data['currentValue']['DefaultMin'] = data['DefaultMin']
                    data['currentValue']['DefaultSec'] = data['DefaultSec']
                # Add Source for parameter as Input Source
                data['Source'] = {'System': [], "Web UI": [], "Device UI": []}
                # Update Parameter to make it can be reused as variable identifier
                data['Name'] = data['Name'].replace(":","_")
                datalist[uuid] = data

    # TODO: NOT sure what kind of evaluation required for Parameter Primitive
    def __evaluatePPData(self, data):
        if data['Name'] is None:
            return False
        elif data['type'] is None:
            return False
        else:
            return True

    # define recursive function to get Menu Ui Local Display attributes
    def __getMenuUiLocalDisplayData(self, data):
        if(self.__evaluateMenuUiLDData(data)):
            uuid = data['uuid']
            self.__MenuUiLocalDisplayDict[uuid] = data
            if data.get('childs'):
                for entry in data['childs']:
                    self.__getMenuUiLocalDisplayData(entry)
            else:
                return

    # TODO: NOT sure what kind of evaluation required for Ui Local Display
    # TODO: 1. only 1 Steering Control Groups can be placed under one parent
    # TODO: 2. only 1 Steering Confirm Action can be placed under one ViewCondition parent
    def __evaluateMenuUiLDData(self, data):
        if data['type'] != "ViewCondition" and data['type'] != "SteeringControlsGroup":
            if (not data.get('Label_en') ):
                self.R.addComment("Menu {} does NOT have Label_en attribute".format(data['Name']))
                return False
            elif data['Label_en'] == "":
                self.R.addComment("Menu {} has an EMPTY Label_en attribute".format(data['Name']))
                return False
            else:
                return True
        else:
            return True

    def __setConditions(self, condition, currentMenu):
        if not currentMenu.get('Conditions'):
            currentMenu['Conditions']=[]
        currentMenu['Conditions'].append(condition)
        if currentMenu.get('childs'):
            for entry in currentMenu['childs']:
                self.__setConditions(condition, entry)
        else:
            return

    def __findConditions(self, uuid):
        if self.__MenuStructureDict[uuid].get("Conditions"):
            return self.__MenuStructureDict[uuid]["Conditions"]

    def __checkParentType(self, uuid):
        parentuuid = self.__MenuUiLocalDisplayDict[uuid]["parent"]
        if parentuuid != self.__menuUUID:
            return self.__MenuUiLocalDisplayDict[parentuuid]["type"]
        else:
            return None

    def __setMenuPath(self, uuid):
        if self.__MenuUiLocalDisplayDict[uuid].get('Label_en'):
            menuPath = '\\' + self.__MenuUiLocalDisplayDict[uuid]['Label_en']
        else:
            menuPath = None
        currentMenu = self.__MenuUiLocalDisplayDict[uuid]
        if currentMenu.get('parent'):
            while currentMenu['parent'] != self.__menuUUID:
                currentMenu = self.__MenuUiLocalDisplayDict[currentMenu['parent']]
                if currentMenu['type'] in ["ViewCondition", "SteeringControlsGroup", "SteeringConfirmAction"]:
                    continue
                else:
                    if menuPath != None:
                        menuPath = '\\' + currentMenu['Label_en'] + menuPath
                    else:
                        menuPath = '\\' + currentMenu['Label_en']
        return menuPath

    def __findChildItemforCondition(self, conditionMenu, firstLevelChild):
        if conditionMenu.get('childs'):
            for child in conditionMenu['childs']:
                if child['type'] == 'ViewCondition':
                    self.__findChildItemforCondition(child, firstLevelChild)
                elif child['type'] in ['SteeringControlsGroup','SteeringConfirmAction']:
                    continue
                else:
                    firstLevelChild.append({"Name": child['Name'], "uuid": child["uuid"], "uuid": child["uuid"]})
        else:
            return

    def __findMenuPath(self, menuPath):
        targetuuid = None
        for uuid in self.__MenuStructureDict:
            if self.__MenuStructureDict[uuid]['Menu_path'] == menuPath:
                targetuuid = uuid
                break
            else: continue
        return targetuuid

    def __restructureMenuUiLDData(self):
        for uuid in self.__MenuUiLocalDisplayDict:
            # 1. Retrieve all conditions for all child menus
            if self.__MenuUiLocalDisplayDict[uuid]["type"] == "ViewCondition":
                if self.__MenuUiLocalDisplayDict[uuid].get('childs'):
                    for child in self.__MenuUiLocalDisplayDict[uuid]["childs"]:
                        condition = self.__MenuUiLocalDisplayDict[uuid]['Condition']
                        self.__setConditions(condition, child)
            elif self.__MenuUiLocalDisplayDict[uuid]['type'] == "SteeringControlsGroup":
                if self.__checkParentType(uuid) != "SteeringConfirmAction":
                    parentuuid = self.__MenuUiLocalDisplayDict[uuid]["parent"]
                    # 2. Retrieve all initializations exact menu page
                    if len(self.__MenuUiLocalDisplayDict[uuid]["InitializerList"]) > 0:
                        if not self.__MenuUiLocalDisplayDict[parentuuid].get('Initialization'):
                            self.__MenuUiLocalDisplayDict[parentuuid]['Initialization'] = []
                        for InitializeEntry in self.__MenuUiLocalDisplayDict[uuid]["InitializerList"]:
                            if self.__parameterDict[InitializeEntry[0]]['type'] in ['Integer', 'Enum']:
                                InitializeEntry[1] = int(InitializeEntry[1] )
                            self.__MenuUiLocalDisplayDict[parentuuid]['Initialization'].append(InitializeEntry)
                    # 3. Retrieve all web parameter input in exact menu page
                    if  self.__MenuUiLocalDisplayDict[uuid].get('childs'):
                        if not self.__MenuUiLocalDisplayDict[parentuuid].get('Input'):
                            self.__MenuUiLocalDisplayDict[parentuuid]['Input'] = []
                        for webInput in self.__MenuUiLocalDisplayDict[uuid]["childs"]:
                            self.__MenuUiLocalDisplayDict[parentuuid]['Input'].append(webInput)
            # 4. Retrieve web confirmation input in exact menu page
            elif self.__MenuUiLocalDisplayDict[uuid]['type'] == "SteeringConfirmAction":
                parentuuid = self.__MenuUiLocalDisplayDict[uuid]["parent"]
                parenttype = self.__MenuUiLocalDisplayDict[parentuuid]["type"]
                if parentuuid != self.__menuUUID and parenttype == "ViewCondition":
                    grandparentuuid = self.__MenuUiLocalDisplayDict[parentuuid]["parent"]
                    SteeringControlsGroupFind = False
                    for child in self.__MenuUiLocalDisplayDict[grandparentuuid]["childs"]:
                        if child['type'] == "SteeringControlsGroup":
                            SteeringControlsGroupFind = True
                            break
                        else:
                            continue
                    if self.__MenuUiLocalDisplayDict[uuid].get('childs'):
                        for child in self.__MenuUiLocalDisplayDict[uuid]['childs']:
                            if child['type'] == 'SteeringControlsGroup':
                                if len(child['InitializerList']) > 0:
                                    if not self.__MenuUiLocalDisplayDict[uuid].get('ConfirmationInilization'):
                                        self.__MenuUiLocalDisplayDict[uuid]['ConfirmationInilization'] = []
                                    for InitializeEntry in child['InitializerList']:
                                        self.__MenuUiLocalDisplayDict[uuid]['ConfirmationInilization'].append(InitializeEntry)
                    if SteeringControlsGroupFind:
                        if not self.__MenuUiLocalDisplayDict[grandparentuuid].get("Confirmation"):
                            self.__MenuUiLocalDisplayDict[grandparentuuid]["Confirmation"] = []
                        self.__MenuUiLocalDisplayDict[grandparentuuid]["Confirmation"].append(self.__MenuUiLocalDisplayDict[uuid])

        # 5. Copy all Menu data to __MenuStructureDict
        for uuid in self.__MenuUiLocalDisplayDict:
            if self.__MenuUiLocalDisplayDict[uuid]["type"] in ["ViewCondition", "SteeringControlsGroup", "SteeringConfirmAction"]:
                continue
            elif self.__MenuUiLocalDisplayDict[uuid]["type"] in ["IntegerValueInput","RealValueInput","TextValueInput","SingleSelect","MultiSelect","DatePicker","TimeValueInput","Duration","IPv4AddressInput"]:
                if self.__checkParentType(uuid) == "SteeringControlsGroup":
                    continue
                else:
                    self.__MenuStructureDict[uuid] = self.__MenuUiLocalDisplayDict[uuid].copy()
            else:
                self.__MenuStructureDict[uuid] = self.__MenuUiLocalDisplayDict[uuid].copy()

        # 6. Find full menu path
        for uuid in self.__MenuStructureDict:
            self.__MenuStructureDict[uuid]['Menu_path'] = self.__setMenuPath(uuid)

        # 7. Reconstruct Ui Local Dispaly data with only first level child
        for uuid in self.__MenuStructureDict:
            if self.__MenuStructureDict[uuid].get('childs'):
                firstLevelChild = []
                for child in self.__MenuStructureDict[uuid]['childs']:
                    if child['type'] in ['SteeringControlsGroup','SteeringConfirmAction']:
                        continue
                    elif child['type'] == 'ViewCondition':
                       self.__findChildItemforCondition(child, firstLevelChild)
                    else:
                        firstLevelChild.append({"Name": child['Name'], "uuid": child["uuid"]})
                self.__MenuStructureDict[uuid]['childs'] = firstLevelChild

    def __restructureParameterData(self):
        # 1. First identify System Parameter
        for uuid in self.__SysetemParameterDict:
            ppuuid = self.__SysetemParameterDict[uuid]['ValuePrimitive']
            if self.__parameterDict.get(ppuuid):
                self.__parameterDict[ppuuid]['Source']['System'].append('Yes')
        for uuid in self.__MenuUiLocalDisplayDict:
            if self.__MenuUiLocalDisplayDict[uuid]['type'] in ['IntegerValueInput', 'RealValueInput', 'TextValueInput', 'SingleSelect', 'MultiSelect', 'DatePicker', 'TimeValueInput', 'DurationValueInput', 'IPv4AddressInput']:
                #2 Identify Web UI Parameter
                if self.__checkParentType(uuid) == 'SteeringControlsGroup':
                    ppuuid = self.__MenuUiLocalDisplayDict[uuid]['ValuePrimitive']
                    parentuuid = self.__MenuUiLocalDisplayDict[uuid]['parent']
                    if self.__checkParentType(parentuuid) == 'MenuSubpage':
                        if self.__parameterDict.get(ppuuid):
                            self.__parameterDict[ppuuid]['Source']['Web UI'].append(self.__setMenuPath(parentuuid))
                # 3 Identify Device UI
                else:
                    if self.__MenuUiLocalDisplayDict[uuid]['Editable'] == True:
                        ppuuid = self.__MenuUiLocalDisplayDict[uuid]['ValuePrimitive']
                        if self.__parameterDict.get(ppuuid):
                            self.__parameterDict[ppuuid]['Source']['Device UI'].append(self.__setMenuPath(uuid))

    # def __restructureParameterData(self):
    #     # 1. First identify System Parameter
    #     for uuid in self.__SysetemParameterDict:
    #         ppuuid = self.__SysetemParameterDict[uuid]['ValuePrimitive']
    #         if self.__parameterDict.get(ppuuid):
    #             if not self.__parameterDict[ppuuid].get('Source'):
    #                 self.__parameterDict[ppuuid]['Source'] = []
    #             self.__parameterDict[ppuuid]['Source'].append('System')
    #     for uuid in self.__MenuUiLocalDisplayDict:
    #         if self.__MenuUiLocalDisplayDict[uuid]['type'] in ['IntegerValueInput', 'RealValueInput', 'TextValueInput', 'SingleSelect', 'MultiSelect', 'DatePicker', 'TimeValueInput', 'DurationValueInput', 'IPv4AddressInput']:
    #             #2 Identify Web UI Parameter
    #             if self.__checkParentType(uuid) == 'SteeringControlsGroup':
    #                 ppuuid = self.__MenuUiLocalDisplayDict[uuid]['ValuePrimitive']
    #                 parentuuid = self.__MenuUiLocalDisplayDict[uuid]['parent']
    #                 if self.__checkParentType(parentuuid) == 'MenuSubpage':
    #                     if self.__parameterDict.get(ppuuid):
    #                         if not self.__parameterDict[ppuuid].get('Source'):
    #                             self.__parameterDict[ppuuid]['Source'] = []
    #                         self.__parameterDict[ppuuid]['Source'].append('Web UI:{}'.format(self.__setMenuPath(parentuuid)))
    #             # 3 Identify Device UI
    #             else:
    #                 if self.__MenuUiLocalDisplayDict[uuid]['Editable'] == True:
    #                     ppuuid = self.__MenuUiLocalDisplayDict[uuid]['ValuePrimitive']
    #                     if self.__parameterDict.get(ppuuid):
    #                         if not self.__parameterDict[ppuuid].get('Source'):
    #                             self.__parameterDict[ppuuid]['Source'] = []
    #                         self.__parameterDict[ppuuid]['Source'].append('Device UI:{}'.format(self.__setMenuPath(uuid)))

    def __testMenuData(self):
        for uuid in self.__MenuStructureDict:
            print("{}\n".format(self.__MenuStructureDict[uuid]))

        for uuid in self.__parameterDict:
            print("{}\n".format(self.__parameterDict[uuid]))

    """
    Define internal usage function for Menu Entry Checking in following part
    """
    # TODO: define a function to go to specifici menu and do initialization
    def __initializeforMenuEntry(self, uuid):
        if self.__MenuStructureDict[uuid]['Menu_path'] != None:
            menuPath = self.__MenuStructureDict[uuid]['Menu_path']
            menuList = menuPath[1:].split("\\")
            iterMenu = ''
            for menuEntry in menuList:
                iterMenu = iterMenu + "\\" + menuEntry
                iteruuid = self.__findMenuPath(iterMenu)
                if iteruuid:
                    if self.__MenuStructureDict[iteruuid].get("Initialization"):
                        for InitializationEntry in self.__MenuStructureDict[iteruuid]["Initialization"]:
                            self.__setParameterData(InitializationEntry[0],InitializationEntry[1])

    def __setParameterData(self, uuid, value):
        self.R.addComment("Set parameter [{}] as [{}]".format(self.__parameterDict[uuid]['Name'], value))
        self.__parameterDict[uuid]['currentValue'] = value

    # TODO: define a function check the condition list for specfic menu
    def __checkConditions(self, uuid) -> bool:
        conditionChecking = True
        if self.__MenuStructureDict[uuid].get("Conditions"):
            for condition in self.__MenuStructureDict[uuid]["Conditions"]:
                if self.__validateConditionFormat(condition):
                    # Replace true as True, false as False in condition string
                    condition = condition.replace('false', 'False')
                    condition = condition.replace('true', 'True')
                    # Replace uuid as parameter name in condition string
                    start_index = [i.start() for i in re.finditer('{', condition)]
                    end_index = [i.start() for i in re.finditer('}', condition)]
                    ppuuidlist = []
                    for i in range(len(start_index)):
                        ppuuidlist.append(condition[start_index[i]:end_index[i] + 1])
                    for ppuuid in ppuuidlist:
                        ppname = self.__parameterDict[ppuuid]['Name']
                        if self.__parameterDict[ppuuid]['currentValue'] is None:
                            print("Check Condition for uuid {}, result as False".format(uuid))
                            return False
                        else:
                            locals()[ppname] = self.__parameterDict[ppuuid]['currentValue']
                            condition = condition.replace(ppuuid, ppname)
                    re1 = eval(condition)
                    if re1:
                        continue
                    else:
                        print("Check Condition for uuid {}, result as False".format(uuid))
                        return False
                else:
                    continue
        print("Check Condition for uuid {}, result as {}".format(uuid, conditionChecking))
        return conditionChecking

    # Validate the format of condition
    # If the format of condition can be ensured by Factory app, we can then remove this function
    def __validateConditionFormat(self, condition):
        symbollist = []
        for i in condition:
            if i in ['{', "("]:
                symbollist.append(i)
            elif i == "}" and len(symbollist) != 0:
                if symbollist[-1] == "{":
                    symbollist.pop()
                else:
                    return False
            elif i == "}" and len(symbollist) == 0:
                return False
            elif i == ")" and len(symbollist) != 0:
                if symbollist[-1] == "(":
                    symbollist.pop()
                else:
                    return False
            elif i == ")" and len(symbollist) == 0:
                return False
            else:
                continue
        if len(symbollist) == 0:
            return True
        else:
            return False


    def __checkMenuSingleSelect(self, uuid):
        menu_path = self.__MenuStructureDict[uuid]['Menu_path']
        if menu_path != None and self.__checkConditions(uuid):
            # self.__initializeforMenuEntry(uuid)
            # self.__checkConditions(uuid)
            result = self._tdHMI.navigateToMenuItem(menu_path)
            # 1. First verify if specified menu existing
            if result != '0':
                self.NotAccessiblePaths.append(menu_path)
                return
            # 2. If operator can go to specific page, set the initializaion
            self.__initializeforMenuEntry(uuid)
            # 3. Then verify if page type correct or not
            pageType = self._tdHMI.getPageType()
            if pageType != 'List':
                self.IncorrectPageTypeList.append(
                    pageType + ' at path ' + menu_path + ', expected List (SingleSelect page)')
                self._tdHMI.pressKeyForPageChange(1)  # leave selection page # TODO: check if this works
            # 4. Verify



if __name__ == '__main__':
    relativeFilePath = "Products\\CM44xPlatform\\Sampler\\ScriptTemplate\\DemoScripts\\GUI_Description\\CSF28_new.json"
    # relativeFilePath = "Products\\CM44xPlatform\\Sampler\\ScriptTemplate\\DemoScripts\\GUI_Description\\TestingProject_v2.json"
    # relativeFilePath = "Products\\CM44xPlatform\\Sampler\\ScriptTemplate\\DemoScripts\\GUI_Description\\TestCondition.json"
    HMI_blocks = Check_HMI_Blocks(relativeFilePath)
    HMI_blocks.run()