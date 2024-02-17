from Flashcord_API_Client import Flashcord_API_Client
from FlashPlug import Replugged_API
import time
#import random
import math
import socket

def RefreshStore():
    StartTime = time.time()
    API_Version = Flashcord_API_Client("GET/API_VERSION")
    Server_Version = Flashcord_API_Client("GET/SERVER_VERSION")
    Copyright_Date = "2021-2024"
    Hostname = socket.gethostname()

    Last_Update_Time = time.localtime()
    Last_Update_String = f"{Last_Update_Time.tm_hour:02d}:{Last_Update_Time.tm_min:02d}:{Last_Update_Time.tm_sec:02d} - {Last_Update_Time.tm_mday:02d}/{Last_Update_Time.tm_mon:02d}/{Last_Update_Time.tm_year}"

    StoreTemplate = "store/templates/store_template.html"
    HTMLFile = ""

    SplashText_Selected = Flashcord_API_Client("GET/SPLASH_TEXT").replace(">", "&gt").replace("<", "&lt").replace("\n","\A ")

    def GetCode():
        InitTime = time.time()
        Users = Flashcord_API_Client("GET/USERS")
        Users = (Flashcord_API_Client("GET/USERS").replace("[","").replace("]","").replace("'","").replace(" ","")).split(",")
        Users.sort()
        Latency = math.floor((time.time() - InitTime) * 1000)
        API_Latency = f"{Latency}ms (from {Hostname})"
        def CodeLoop(Type):
            ValidAddons = []
            HTMLCode = ""
            for cycle in range (len(Users)):
                match Type:
                    case "modules": Results = Flashcord_API_Client(f"GET/MODULES/{Users[cycle]}")
                    case "plugins": Results = Flashcord_API_Client(f"GET/PLUGINS/{Users[cycle]}")
                    case "themes": Results = Flashcord_API_Client(f"GET/THEMES/{Users[cycle]}")
                if len(Results) != 0 and Results != "NOT_FOUND" and Results != "[]":
                    Results = Results.replace("[","").replace("]","").replace('"','').replace(" ","").replace("'","").split(",")
                    for subcycle in range (len(Results)):
                        ValidAddons.append(Users[cycle] + "/" + Results[subcycle] + "-files")
                ValidAddons.sort()
            if ValidAddons != []:
                for cycle in range (len(ValidAddons)):
                    HTMLCode = HTMLCode + f'                    <iframe class="Flashcord-Module_Embed" src="store/{Type}/{ValidAddons[cycle]}/embed.html"></iframe>\n'
            else:
                HTMLCode = "<h1>It's bloody empty in here!</h1>\n"
            return HTMLCode
        ModuleCode = CodeLoop("modules")
        PluginCode = CodeLoop("plugins")
        ThemeCode = CodeLoop("themes")
        return ModuleCode,PluginCode,ThemeCode,API_Latency

    ModuleCode,PluginCode,ThemeCode,API_Latency = GetCode()
    Replugged_Plugins = Replugged_API("Plugins")
    Replugged_Themes = Replugged_API("Themes")
    #print(ModuleCode)
    #print(PluginCode)
    #print(ThemeCode)
    #print(API_Latency)

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
                        HTMLArray[line] = HTMLArray[line].replace("[FLASHCORD_PLUGINS]", PluginCode)
                        HTMLArray[line] = HTMLArray[line].replace("[NON-FLASHCORD_THEMES]", ThemeCode)
                        HTMLArray[line] = HTMLArray[line].replace("[SERVER_VERSION]", Server_Version)
                        HTMLArray[line] = HTMLArray[line].replace("[API_VERSION]", API_Version)
                        HTMLArray[line] = HTMLArray[line].replace("[API_LATENCY]", API_Latency)
                        HTMLArray[line] = HTMLArray[line].replace("[LAST_UPDATE]", Last_Update_String)
                        HTMLArray[line] = HTMLArray[line].replace("[COPYRIGHT_DATE]", Copyright_Date)
                        HTMLArray[line] = HTMLArray[line].replace("[REPLUGGED_PLUGINS]", Replugged_Plugins)
                        HTMLArray[line] = HTMLArray[line].replace("[REPLUGGED_THEMES]", Replugged_Themes)
                        EditHTML_File.write(HTMLArray[line])
                        ProcessingProgress = ((line+1)/len(HTMLArray))*100
                        print('[FlashCFG // HTML-CFG] Processed Line', line+1, '/', len(HTMLArray), '(', ProcessingProgress, '%).')
            else:
                with open(HTMLFile, 'r', encoding='utf-8') as EditHTML_File:
                    BuildData = EditHTML_File.readlines()
                with open(HTMLFile, 'w', encoding='utf-8') as EditHTML_File:
                    BuildTime = math.floor((time.time() - StartTime)*1000)
                    BuildTime_String = str(BuildTime) + " milliseconds"
                    BuildData[71] = f'                        <p>Build time: {BuildTime_String}</p>\n'
                    EditHTML_File.writelines(BuildData)
    HTMLConfigurator(False)
    HTMLConfigurator(True)
                    
RefreshStore()