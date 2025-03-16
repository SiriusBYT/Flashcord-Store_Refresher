import time, math, socket, urllib.request, json
from Flashcord_API_Client import *

# Logging System + Getting current time and date in preferred format
def GetTime():
    CTime = time.localtime()
    Time = f"{CTime.tm_hour:02d}:{CTime.tm_min:02d}:{CTime.tm_sec:02d}"
    Date = f"{CTime.tm_mday:02d}-{CTime.tm_mon:02d}-{CTime.tm_year}"
    return Time,Date
def WriteLog(Log):
    Time,Data = GetTime()
    PrintLog = f"[{Time}] {Log}"
    print(PrintLog)

# Fetch data from the Replugged API to insert Replugged Plugins/Themes to the Flashcord Store
def Replugged_API(GetWhat):
    WriteLog(f"Parsing Replugged {GetWhat}...")
    if GetWhat == "Plugins": Replugged_URL = "https://replugged.dev/api/store/list/plugin?page=1&items=100"
    else: Replugged_URL = "https://replugged.dev/api/store/list/theme?page=1&items=100"
    API = urllib.request.Request(
        Replugged_URL, 
        data=None, 
        headers={'User-Agent': 'Flashplug-Store/1.3-dev'}
    )
    API_Result = json.load(urllib.request.urlopen(API))
    API_ResultKey = API_Result["results"]

    CTime = time.localtime()
    Current_Year = str(CTime.tm_year)

    HTMLCode = ""
    Views_JSON = json.loads(Flashcord_API_Client("GET/VIEWS").replace("'", '"'))
    Installs_JSON = json.loads(Flashcord_API_Client("GET/INSTALLS").replace("'", '"'))
    
    for cycle in range (len(API_ResultKey)):
        Addon = Addon_Name = Addon_Description = Addon_Version = Addon_AuthorKey = Addon_Contributors = Addon_ImageKey = Addon_Image = Addon_GitHubRepo = Addon_ID = Addon_Install = Addon_Page = Addon_AuthorGitHub = ""

        Addon = API_ResultKey[cycle]
        Addon_Name = Addon["name"]
        Addon_Description = Addon["description"]
        Addon_Version = Addon["version"]
        Addon_AuthorKey = Addon["author"]
        try:
            Addon_Author = Addon_AuthorKey["github"]
            Addon_Contributors = "None"
        except:
            try:
                Dummy = Addon_AuthorKey[1]
                Addon_Contributors = []
                for subcycle in range (len(Addon_AuthorKey)):
                    if subcycle == 0:
                        Addon_AuthorSubKey = Addon_AuthorKey[subcycle]
                        Addon_Author = Addon_AuthorSubKey["name"]
                    else:
                        Addon_AuthorSubKey = Addon_AuthorKey[subcycle]
                        Addon_Contributors.append(Addon_AuthorSubKey["name"])
            except:
                Addon_AuthorSubKey = Addon_AuthorKey[0]
                Addon_Author = Addon_AuthorSubKey["name"]
                Addon_Contributors = "None"
        try:
            Addon_ImageKey = Addon["image"]
            if Addon_ImageKey[0] == "h":
                Addon_Image = Addon["image"]
            else:
                Addon_Image = Addon_ImageKey[0]
        except:
            Addon_Image = "https://sirio-network.com/sbin/This is fine.png"
        try:
            Addon_GitHubRepo = Addon["source"]
        except:
            Addon_GitHubRepo = "https://sirio-network.com/404"
        Addon_ID = Addon["id"]
        Addon_Install = f"https://replugged.dev/install?identifier={Addon_ID}"
        Addon_Page = f"https://replugged.dev/store/{Addon_ID}"
        Addon_AuthorGitHub = f"https://github.com/{Addon_Author}"
        Addon_License = Addon["license"]
        Addon_Contributors = str(Addon_Contributors)
        Addon_Contributors = Addon_Contributors.replace("[","").replace("]","").replace("'","")
        Addon_Views = Views_JSON[Addon_ID]
        Addon_Installs = Installs_JSON[Addon_ID]
        AddStat_Views = f"Flashcord_API_Client('ADD_STAT/VIEWS/{Addon_ID}')"
        AddStat_Installs = f"Flashcord_API_Client('ADD_STAT/INSTALLS/{Addon_ID}')"

        HTMLCode = HTMLCode + f'                    <div class="Replugged-Addon" id="{Addon_ID}">\n\
                            <img class="Replugged-Addon_Banner" src="{Addon_Image}" crossorigin="anonymous" referrerpolicy="no-referrer"></img>\
                            <div class="Flashcord-Module_Info">\
                                <div class="SNDL-Quick_FlexGrid"><a onclick="{AddStat_Views}" target="_blank" href="{Addon_Page}"><h1>{Addon_Name}</h1></a><a onclick="{AddStat_Views}" target="_blank" href="{Addon_GitHubRepo}"><h1>💿</h1></a></div>\
                                <div class="SNDL-Quick_FlexGrid"><a target="_blank" href="{Addon_AuthorGitHub}"><h2>{Addon_Author}</h2></a><h5>👀: {Addon_Views} // ⬇️: {Addon_Installs}</h5></div>\
                                <h5>Contributors: {Addon_Contributors}</h5><h3 class="Flashcord-Module_Version">Version: {Addon_Version}</h3>\n<p>{Addon_Description}</p>\
                                <button class="SNDL-BC_Info" onclick="{AddStat_Installs}"><a href="{Addon_Install}" target="_blank"><p>⬇️ Install</p></a></button>\
                                <a target="_blank" href="{Addon_GitHubRepo}"><p class="SNDL-Copyright">{Addon_Author} © {Current_Year} - {Addon_Name} | {Addon_License}</p></a>\
                            </div>\
                    </div>\n'
    return HTMLCode

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

while True:
    RefreshStore()
    print("\n[Flashcord Store Refresher} Now sleeping for 3600 seconds.\n")
    time.sleep(3600)