import json
from pathlib import Path
import collections
import subprocess
import time

def flatten(d, parent_key='', sep='.',warp="$"):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            new_key=warp+new_key+warp
            items.append((new_key, v))
    return dict(items)

def writeStringToFile(content,fileName):
    f= open(fileName,"w+")
    f.write(content)
    f.close()


class ANKVideo():
    def __init__(self):
        self.confFileName="conf.json"
        self.outputFileName="output.mp4"
        self.confString=""
        self.conf=None
        self.coverFile="cover.html"
        self.profileFile="profile.html"
        self.tagFile="tag.html"

        self.flatReplaceDict=dict()
        self.ffThreadsNum=8
        self.middleTmpFile=dict()
        pass
    def askForSetting(self):
        inString=""
        inString=input("input cover page (default cover.html)>")
        self.coverFile=self.coverFile if len(inString)==0 else inString
        inString=input("input profile page (default profile.html)>")
        self.profileFile=self.profileFile if len(inString)==0 else inString        
        inString=input("input tag page (default tag.html)>")
        self.tagFile=self.tagFile if len(inString)==0 else inString   
        inString=input("input output video name (default output.mp4)>")
        self.outputFileName=self.outputFileName if len(inString)==0 else inString

    def _readFileAsDict(self,fileName):
        d=None
        with open(fileName, encoding='utf-8') as f:
            lines = f.read()
            d = json.loads(lines)
            f.close()
        return d
    def _readFileAsString(self,fileName):
        lines=None
        with open(fileName, encoding='utf-8') as f:
            lines = f.read()
            f.close()
        return lines

    def build(self):
        self.conf=self._readFileAsDict(self.confFileName)
        self.flatReplaceDict=flatten(self.conf)
        #handle cover
        coverOutHtml="tmp."+self.coverFile
        coverInHtmlString=self._readFileAsString(self.coverFile)
        for k,v in self.flatReplaceDict.items():
            coverInHtmlString=coverInHtmlString.replace(k,str(v))
        writeStringToFile(coverInHtmlString,coverOutHtml)
        self.middleTmpFile["TMP.COVER"]=coverOutHtml
        self.middleTmpFile["TMP.COVER.PNG"]=coverOutHtml+".png"

        profileOutHtml="tmp."+self.profileFile
        profileInHtmlString=self._readFileAsString(self.profileFile)
        for k,v in self.flatReplaceDict.items():
            profileInHtmlString=profileInHtmlString.replace(k,str(v))
        writeStringToFile(profileInHtmlString,profileOutHtml)
        self.middleTmpFile["TMP.PROFILE"]=profileOutHtml
        self.middleTmpFile["TMP.PROFILE.PNG"]=profileOutHtml+".png"

        tagOutHtml="tmp."+self.tagFile
        tagInHtmlString=self._readFileAsString(self.tagFile)
        for k,v in self.flatReplaceDict.items():
            tagInHtmlString=tagInHtmlString.replace(k,str(v))
        writeStringToFile(tagInHtmlString,tagOutHtml)
        self.middleTmpFile["TMP.TAG"]=tagOutHtml
        self.middleTmpFile["TMP.TAG.PNG"]=tagOutHtml+".png"

        # cover to pngs
        commandShell="wkhtmltoimage  --width 1920 --height 1080 "+ self.middleTmpFile["TMP.COVER"]+"  "+self.middleTmpFile["TMP.COVER.PNG"]
        pCover=subprocess.Popen(commandShell,shell=True)

        commandShell="wkhtmltoimage  --width 1920 --height 1080 "+ self.middleTmpFile["TMP.PROFILE"]+"  "+self.middleTmpFile["TMP.PROFILE.PNG"]
        pProfile=subprocess.Popen(commandShell,shell=True)

        commandShell="wkhtmltoimage  --width 1920 --height 1080 "+ self.middleTmpFile["TMP.TAG"]+"  "+self.middleTmpFile["TMP.TAG.PNG"]
        pTag=subprocess.Popen(commandShell,shell=True)

        pCover.wait()
        pProfile.wait()
        pTag.wait()

        print(str(self.middleTmpFile))
if __name__ == "__main__":
    v=ANKVideo()
    v.askForSetting()
    v.build()