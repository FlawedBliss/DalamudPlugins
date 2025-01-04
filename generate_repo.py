import json
import requests
from time import time


DOWNLOAD_URL = '{}/releases/download/v{}/latest.zip'
GITHUB_RELEASES_API_URL = 'https://api.github.com/repos/{}/{}/releases/tags/v{}'


def load_plugins():
    with open("plugins.json", "r") as f:
        return json.load(f)

def set_updated(plugins):
    with open("repo.json", "r") as f:
        old_repo = json.load(f)
        
        for plugin in plugins:
            plugin['LastUpdate'] = str(int(time()))
            
            for old_plugin in old_repo:
                if old_plugin["InternalName"] != plugin["InternalName"]:
                    continue
                if plugin["AssemblyVersion"] == old_plugin["AssemblyVersion"]:
                    plugin["LastUpdate"] = old_plugin["LastUpdate"]
                break
        
if __name__ == '__main__':
    plugins = load_plugins()
    for plugin in plugins:
        url = DOWNLOAD_URL.format(plugin["RepoUrl"], plugin["AssemblyVersion"])
        plugin["DownloadLinkInstall"] = plugin["DownloadLinkTesting"] = plugin["DownloadLinkUpdate"] = url
    set_updated(plugins)
    
    with open("repo.json", "w") as f:
        json.dump(plugins, f, indent=4)