import os
import re
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
stateFlagValue = 4


def getLatestManifestValue():
    steamdb = requests.get("https://steamdb.info/depot/620981/manifests/", headers=headers)
    html = BeautifulSoup(steamdb.content, features="html.parser")
    manifestIndex = html.select_one("th:-soup-contains('ManifestID')").fetchPreviousSiblings().__len__() + 1
    manifestTable = html.select_one("th:-soup-contains('ManifestID')").find_parent("table")
    manifestValue = manifestTable.select("tr")[1].select_one(f"td:nth-child({manifestIndex})").text
    return manifestValue


def getManifestPath():
    systemDrive = os.getenv("SystemDrive")
    manifestFile = os.path.join(systemDrive, os.sep, "Program Files (x86)", "Steam", "steamapps", "appmanifest_620980.acf")
    return manifestFile


def replaceParameter(string, paramName, replacement):
    return re.sub(rf'({paramName}"\t\t")([0-9]+)', rf'\g<1>{replacement}', string)


def replaceManifestParameters(manifestValue):
    manifestFilePath = getManifestPath()
    with open (manifestFilePath, "r") as manifest:
        data=manifest.read()

    data = replaceParameter(data, 'manifest', manifestValue)
    data = replaceParameter(data, 'StateFlags', stateFlagValue)
    with open(manifestFilePath, 'w') as manifest:
        manifest.write(data)
    return data


replaceManifestParameters(getLatestManifestValue())