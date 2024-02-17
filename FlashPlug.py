import urllib.request, json 
from Flashcord_API_Client import Flashcord_API_Client

def Replugged_API(GetWhat):
    if GetWhat == "Plugins":
        RepluggedAPI = "https://replugged.dev/api/store/list/plugin?page=1&items=100"
    else:
        RepluggedAPI = "https://replugged.dev/api/store/list/theme?page=1&items=100"
    API = urllib.request.Request(
        RepluggedAPI, 
        data=None, 
        headers={'User-Agent': 'Flashplug-Store/1.2'}
    )
    API_Result = json.load(urllib.request.urlopen(API))
    API_ResultKey = API_Result["results"]

    Current_Year = "2024"

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
            Addon_Contributors = []
            for subcycle in range (len(Addon_AuthorKey)):
                if subcycle == 1:
                    Addon_AuthorSubKey = Addon_AuthorKey[subcycle]
                    Addon_Author = Addon_AuthorSubKey["name"]
                else:
                    Addon_AuthorSubKey = Addon_AuthorKey[subcycle]
                    Addon_Contributors.append(Addon_AuthorSubKey["name"])
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
        """
        print(Addon_Name)
        print(Addon_Description)
        print(Addon_Version)
        print(Addon_Author)
        print(Addon_AuthorGitHub)
        print(Addon_Contributors)
        print(Addon_Image)
        print(Addon_GitHubRepo)
        print(Addon_ID)
        print(Addon_Install)
        print(Addon_Page)
        print("\n")
        """
        HTMLCode = HTMLCode + f'                    <div class="Replugged-Addon" id="{Addon_ID}">\n\
                            <img class="Replugged-Addon_Banner" src="{Addon_Image}" crossorigin="anonymous" referrerpolicy="no-referrer"></img>\n\
                            <div class="Flashcord-Module_Info">\n\
                                <div class="SNDL-Quick_FlexGrid"><a onclick="{AddStat_Views}" target="_blank" href="{Addon_Page}"><h1>{Addon_Name}</h1></a><a onclick="{AddStat_Views}" target="_blank" href="{Addon_GitHubRepo}"><h1>💿</h1></a></div>\n\
                                <div class="SNDL-Quick_FlexGrid"><a target="_blank" href="{Addon_AuthorGitHub}"><h2>{Addon_Author}</h2></a><h5>👀: {Addon_Views} // ⬇️: {Addon_Installs}</h5></div>\n\
                                <h5>Contributors: {Addon_Contributors}</h5><h3 class="Flashcord-Module_Version">Version: {Addon_Version}</h3>\n<p>{Addon_Description}</p>\n\
                                <button class="SNDL-BC_Info" onclick="{AddStat_Installs}"><a href="{Addon_Install}" target="_blank"><p>⬇️ Install</p></a></button>\n\
                                <a target="_blank" href="{Addon_GitHubRepo}"><p class="SNDL-Copyright">{Addon_Author} © {Current_Year} - {Addon_Name} | {Addon_License}</p></a>\n\
                            </div>\n\
                    </div>\n'
    return HTMLCode