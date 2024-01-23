from flashapi import *
import time
import random
import math

StartTime = time.time()

API_Version = "2.01"
Copyright_Date = "2024"

Last_Update_Time = time.localtime()
Last_Update_String = f"{Last_Update_Time.tm_hour}:{Last_Update_Time.tm_min}:{Last_Update_Time.tm_sec} {Last_Update_Time.tm_mday}/{Last_Update_Time.tm_mon}/{Last_Update_Time.tm_year}"

# NOT recommended to modify, do this only if you know what you're doing! 
StoreTemplate = "store/templates/store_template.html"

# Don't touch this, it will get overwritten anyways but still. Don't touch just in case.
HTMLFile = ""

SplashText = [
    "Oh look, a splash text!",
    "Now built thanks to the Flashstore API!",
    "Still without Javascript!",
    "The Discount Replugged Store™️",
    "Without working search bars!",
    "now with more yaes than mikos! \n - Atacantul, 2024 (from GangChat)"
]
SplashText_Length = len(SplashText) - 1
SplashSeed = random.randint(0,SplashText_Length)
SplashText_Selected = SplashText[SplashSeed]



print(SplashText_Selected)

def GetAPILatency():
    InitTime = time.time()
    FlashClient_API_Request("GET")
    Latency = math.floor((time.time() - InitTime) * 1000)
    Latency_String = str(Latency) + "ms"
    return Latency_String
API_Latency = GetAPILatency()

def GetCode(GetWhat):
    HTMLCode = ''
    API_Folders = []
    def CallAPI(GetWhat, User):
        if GetWhat == "Modules":
            API_Request = "GET/" + "MODULES"
        elif GetWhat == "Plugins":
            API_Request = "GET/" + "PLUGINS"
        elif GetWhat == "Themes":
            API_Request = "GET/" + "THEMES"
        elif GetWhat == "Users":
            API_Request = "GET/" + "USERS"
        if GetWhat == "UserModules":
            API_Request = "GET/" + "MODULES/" + User
        elif GetWhat == "UserPlugins":
            API_Request = "GET/" + "PLUGINS/" + User
        elif GetWhat == "UserThemes":
            API_Request = "GET/" + "THEMES/" + User
        RequestResults = FlashClient_API_Request(API_Request)
        return RequestResults
    Users = CallAPI("Users", "None")
    Users = Users.replace("[","").replace("]","").replace("'","").replace(" ","").split(",")
    TotalX = []
    for cycle in range (len(Users)):
        time.sleep(1)
        if GetWhat == "Modules":
            Results = CallAPI("UserModules",str(Users[cycle]))
        elif GetWhat == "Plugins":
            Results = CallAPI("UserPlugins",str(Users[cycle]))
        elif GetWhat == "Themes":
            Results = CallAPI("UserThemes",str(Users[cycle]))
        if Results != None:
            Results = Results.replace("[","").replace("]","").replace('"','').replace(" ","").split(",")
            for subcycle in range (len(Results)):
                TotalX.append(Users[cycle] + "/" + Results[subcycle] + "-files")
    TotalX.sort()
    if GetWhat == "Modules":
        EmbedType = "modules"
    elif GetWhat == "Plugins":
        EmbedType = "plugins"
    elif GetWhat == "Themes":
        EmbedType = "themes"
    if TotalX != []:
        for cycle in range (len(TotalX)):
            HTMLCode = HTMLCode + '<iframe class="Flashcord-Module_Embed" src="store/' + EmbedType + '/' + TotalX[cycle] + '/embed.html"></iframe>\n'
    else:
        HTMLCode = "<h3>It's bloody empty in here!</h3>\n"
    return HTMLCode

ModuleCode = GetCode("Modules")
PluginCode = GetCode("Plugins")
ThemesCode = GetCode("Themes")
#print(ModuleCode)
#print(PluginCode)
#print(ThemesCode)

def HTMLConfigurator(ShowBuildTime):
    HTMLFile = "store.html"
    with open(StoreTemplate, 'r', encoding='utf-8') as StoreTemplate_File:
        if ShowBuildTime == False:
            with open(HTMLFile, 'w', encoding='utf-8') as EditHTML_File:
                EditHTML_File.write("")
            with open(HTMLFile, 'a', encoding='utf-8') as EditHTML_File:
                HTMLArray = StoreTemplate_File.readlines()
                for line in range (len(HTMLArray)):
                    # print('[FlashCGG] Processing Line"', line, '" which is "', HTMLArray[line], '".')
                    HTMLArray[line] = HTMLArray[line].replace("[SPLASH_TEXT]", SplashText_Selected)
                    HTMLArray[line] = HTMLArray[line].replace("[FLASHCORD_OFFICIAL-MODULES]", ModuleCode)
                    HTMLArray[line] = HTMLArray[line].replace("[REPLUGGED_PLUGINS]", PluginCode)
                    HTMLArray[line] = HTMLArray[line].replace("[NON-FLASHCORD_THEMES]", ThemesCode)
                    HTMLArray[line] = HTMLArray[line].replace("[API_VERSION]", API_Version)
                    HTMLArray[line] = HTMLArray[line].replace("[API_LATENCY]", API_Latency)
                    HTMLArray[line] = HTMLArray[line].replace("[LAST_UPDATE]", Last_Update_String)
                    HTMLArray[line] = HTMLArray[line].replace("[COPYRIGHT_DATE]", Copyright_Date)
                    EditHTML_File.write(HTMLArray[line])
                    ProcessingProgress = ((line+1)/len(HTMLArray))*100
                    print('[FlashCFG // HTML-CFG] Processed Line', line+1, '/', len(HTMLArray), '(', ProcessingProgress, '%).')
        else:
            with open(HTMLFile, 'r', encoding='utf-8') as EditHTML_File:
                BuildData = EditHTML_File.readlines()
            with open(HTMLFile, 'w', encoding='utf-8') as EditHTML_File:
                BuildTime = math.floor(time.time() - StartTime)
                BuildTime_String = str(BuildTime) + " seconds"
                BuildData[70] = f'                        <p>Build time: {BuildTime_String}</p>\n'
                EditHTML_File.writelines(BuildData)
HTMLConfigurator(False)
HTMLConfigurator(True)