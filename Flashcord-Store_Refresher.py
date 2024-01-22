from flashapi import *
import time
import random

API_Version = "2.01"
Copyright_Date = "2024"

Last_Update_Time = time.localtime()
Last_Update_String = f"{Last_Update_Time.tm_hour}:{Last_Update_Time.tm_min}:{Last_Update_Time.tm_sec} {Last_Update_Time.tm_mday}/{Last_Update_Time.tm_mon}/{Last_Update_Time.tm_year}"

# NOT recommended to modify, do this only if you know what you're doing! 
StoreTemplate = "store/templates/store_template.html"

# Don't touch this, it will get overwritten anyways but still. Don't touch just in case.
HTMLFile = ""


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
        Results = Results.replace("[","").replace("]","").replace('"','').replace(" ","").split(",")
        if Results != None:
            for cycle in range (len(API_Folders)):
                API_Folders[cycle] = API_Folders[cycle] + "-files"
                HTMLCode = HTMLCode + '<iframe class="Flashcord-Module_Embed" src="store/modules/' + Users[cycle] + Results[cycle] + '/embed.html"></iframe>\n'

    #HTMLCode = "<h3>It's bloody empty in here!\n"
    return HTMLCode

ModuleCode = GetCode("Modules")
print(ModuleCode)

"""
def HTMLConfigurator():
    print('[FlashCFG // HTML-CFG] Connecting to SGN servers...')
    MoreByCode = GetEmbedCode()
    print(f'[FlashCFG // HTML-CFG] The "More by" section will have:\n{MoreByCode}')
    

    with open(StoreTemplate, 'r', encoding='utf-8') as StoreTemplate_File:
        with open(EmbedTemplate, 'r', encoding='utf-8') as EmbedTemplate_File:
            with open(HTMLFile, 'w', encoding='utf-8') as EditHTML_File:
                EditHTML_File.write("")
            with open(HTMLFile, 'a', encoding='utf-8') as EditHTML_File:
                if Step == 0:
                    HTMLArray = StoreTemplate_File.readlines()
                elif Step == 1:
                    HTMLArray = EmbedTemplate_File.readlines()
                else:
                    print("[FlashCFG // HTML-CFG] WARNING: Sirius A was here and caused another Big Bang", '(What the fuck is Step "', Step, '"?!)')
                    print("[FlashCFG // HTML-CFG] Also how in the LIVING FUCK DID YOU TRIGGER THIS ERROR without triggering the previous one?")
                    return "FUCK"
                for line in range (len(HTMLArray)):
                    # print('[FlashCGG] Processing Line"', line, '" which is "', HTMLArray[line], '".')
                    HTMLArray[line] = HTMLArray[line].replace("[NAME]", Name)
                    HTMLArray[line] = HTMLArray[line].replace("[SHORT_DESC]", Short_Description)
                    HTMLArray[line] = HTMLArray[line].replace("[LONG_DESC]", Long_Description)
                    HTMLArray[line] = HTMLArray[line].replace("[VERSION]", Version)
                    HTMLArray[line] = HTMLArray[line].replace("[LICENSE_YEAR]", License_Year)
                    HTMLArray[line] = HTMLArray[line].replace("[LICENSE]", License)
                    HTMLArray[line] = HTMLArray[line].replace("[GITHUB_PROFILE]", GitHub_Profile)
                    HTMLArray[line] = HTMLArray[line].replace("[GITHUB_REPO]", GitHub_Repo)
                    HTMLArray[line] = HTMLArray[line].replace("[GITHUB_CONTRIBUTORS]", GitHub_Contributors)
                    HTMLArray[line] = HTMLArray[line].replace("[DISCORD_LINK]", Discord)
                    HTMLArray[line] = HTMLArray[line].replace("[THEME]", SNDL_Theme)
                    HTMLArray[line] = HTMLArray[line].replace("[EMBED_COLOR]", Embed_Color)
                    HTMLArray[line] = HTMLArray[line].replace("[STORE_PAGE_NAME]", Store_Page_Name)
                    HTMLArray[line] = HTMLArray[line].replace("[FOLDER_NAME]", Folder_Name)
                    HTMLArray[line] = HTMLArray[line].replace("[EMBED_FILENAME]", Embed_FileName)
                    HTMLArray[line] = HTMLArray[line].replace("[STORE_EMBED_FILENAME]", Store_Embed_FileName)
                    HTMLArray[line] = HTMLArray[line].replace("[STORE_USER_FOLDER]", UserFolderName)
                    HTMLArray[line] = HTMLArray[line].replace("[FLASHSTORE_API-EMBEDS]", MoreByCode)
                    EditHTML_File.write(HTMLArray[line])
                    ProcessingProgress = ((line+1)/len(HTMLArray))*100
                    print('[FlashCFG // HTML-CFG] Processed Line', line+1, '/', len(HTMLArray), '(', ProcessingProgress, '%).', StepFile)
                    # print('[FlashCGG] Processed Line is now "', HTMLArray[line], '".')

def FlashcordStoreConfig():
    print("[FlashCFG] Script initiated.")
    FileBackup("Store Page")
    HTMLConfigurator(0)
    FileBackup("Embed")
    HTMLConfigurator(1)
    print("[FlashCFG] Script complete.")
    return

FlashcordStoreConfig()
"""