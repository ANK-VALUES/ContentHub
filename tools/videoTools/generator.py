import json
from pathlib import Path
import collections
import subprocess
import time
import os
import jinja2


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
        self.headerSlice="header.mp4"
        self.endingFile="ending.html"
        self.innerVideo="talk.mp4"
        self.flatReplaceDict=dict()
        self.ffThreadsNum=8
        self.middleTmpFile=dict()

        self.coverTime=2
        self.profileTime=2
        self.tagTime=2

        self.endingTime=4
        self.htmlDirName="__ANK_CACHE__"
        self.preserveTmpFile=False
        pass
    def askForSetting(self):
        inString=""
        inString=input("input payload video file name  (default talk.mp4)>")
        self.innerVideo=self.innerVideo if len(inString)==0 else inString
        # self.innerVideo=os.path.join(self.htmlDirName,self.innerVideo)

        inString=input("input cover page (default cover.html)>")
        self.coverFile=self.coverFile if len(inString)==0 else inString
        # self.coverFile=os.path.join(self.htmlDirName,self.coverFile)

        inString=input("input profile page (default profile.html)>")
        self.profileFile=self.profileFile if len(inString)==0 else inString
        # self.profileFile=os.path.join(self.htmlDirName,self.profileFile)

        inString=input("input ending page (default ending.html)>")
        self.endingFile=self.endingFile if len(inString)==0 else inString
        # self.endingFile=os.path.join(self.htmlDirName,self.endingFile)

        inString=input("input tag page (default tag.html)>")
        self.tagFile=self.tagFile if len(inString)==0 else inString
        # self.tagFile=os.path.join(self.htmlDirName,self.tagFile)

        inString=input("input header video name (default header.mp4)>")
        self.headerSlice=self.headerSlice if len(inString)==0 else inString

        inString=input("input output video name (default output.mp4)>")
        self.outputFileName=self.outputFileName if len(inString)==0 else inString

        inString=input("input cover time (default 2)>")
        self.coverTime=self.coverTime if len(inString)==0 else inString

        inString=input("input profile time (default 2)>")
        self.profileTime=self.profileTime if len(inString)==0 else inString

        inString=input("input tag time (default 2)>")
        self.tagTime=self.tagTime if len(inString)==0 else inString


        inString=input("input ending time (default 4)>")
        self.endingTime=self.endingTime if len(inString)==0 else inString

        inString=input("preserve tmp file ? input any char means yes(default No)>")
        self.preserveTmpFile=self.preserveTmpFile if len(inString)==0 else True
    def _readFileAsDict(self,fileName):
        d=None
        with open(fileName, encoding='utf-8') as f:
            lines = f.read()
            d = json.loads(lines)
            f.close()
        return d
    def _readFileAsString(self,fileName,preDir=""):
        lines=None
        if preDir=="":
            pass
        else:
            fileName=os.path.join(preDir,fileName)
        with open(fileName, encoding='utf-8') as f:
            lines = f.read()
            f.close()
        return lines

    def build(self):
        self.conf=self._readFileAsDict(self.confFileName)
        #handle cover
        coverOutHtml="tmp."+self.coverFile
        coverInHtmlString=self._readFileAsString(self.coverFile,self.htmlDirName)
        
        coverInHtmlString=jinja2.Template(coverInHtmlString).render(self.conf)
        writeStringToFile(coverInHtmlString,coverOutHtml)
        self.middleTmpFile["TMP.COVER"]=coverOutHtml
        self.middleTmpFile["TMP.COVER.PNG"]=coverOutHtml+".png"

        profileOutHtml="tmp."+self.profileFile
        profileInHtmlString=self._readFileAsString(self.profileFile,self.htmlDirName)
        profileInHtmlString=jinja2.Template(profileInHtmlString).render(self.conf)
        writeStringToFile(profileInHtmlString,profileOutHtml)


        self.middleTmpFile["TMP.PROFILE"]=profileOutHtml
        self.middleTmpFile["TMP.PROFILE.PNG"]=profileOutHtml+".png"

        tagOutHtml="tmp."+self.tagFile
        tagInHtmlString=self._readFileAsString(self.tagFile,self.htmlDirName)
        tagInHtmlString=jinja2.Template(tagInHtmlString).render(self.conf)
        writeStringToFile(tagInHtmlString,tagOutHtml)
        self.middleTmpFile["TMP.TAG"]=tagOutHtml
        self.middleTmpFile["TMP.TAG.PNG"]=tagOutHtml+".png"


        endingOutHtml="tmp."+self.endingFile
        endingInHtmlString=self._readFileAsString(self.endingFile,self.htmlDirName)
        endingInHtmlString=jinja2.Template(endingInHtmlString).render(self.conf)
        writeStringToFile(endingInHtmlString,endingOutHtml)
        self.middleTmpFile["TMP.END"]=endingOutHtml
        self.middleTmpFile["TMP.END.PNG"]=endingOutHtml+".png"
        # cover to pngs
        commandShell="wkhtmltoimage  --width 1920 --height 1080 "+ self.middleTmpFile["TMP.COVER"]+"  "+self.middleTmpFile["TMP.COVER.PNG"]
        pCover=subprocess.Popen(commandShell,shell=True)

        commandShell="wkhtmltoimage  --width 1920 --height 1080 "+ self.middleTmpFile["TMP.PROFILE"]+"  "+self.middleTmpFile["TMP.PROFILE.PNG"]
        pProfile=subprocess.Popen(commandShell,shell=True)

        commandShell="wkhtmltoimage  --width 1920 --height 1080 "+ self.middleTmpFile["TMP.TAG"]+"  "+self.middleTmpFile["TMP.TAG.PNG"]
        pTag=subprocess.Popen(commandShell,shell=True)

        commandShell="wkhtmltoimage  --width 1920 --height 1080 "+ self.middleTmpFile["TMP.END"]+"  "+self.middleTmpFile["TMP.END.PNG"]
        endTag=subprocess.Popen(commandShell,shell=True)

        pCover.wait()
        pProfile.wait()
        pTag.wait()
        endTag.wait()

        joinVideoCommandShell='ffmpeg \
-loop 1 -probesize 10MB -framerate 24 -t {} -i {} \
-loop 1 -probesize 10MB -framerate 24 -t {} -i {} \
-loop 1 -probesize 10MB -framerate 24 -t {} -i {} \
-i {} \
-loop 1 -probesize 10MB -framerate 24 -t {} -i {} \
-f lavfi -t 0.1 -i anullsrc \
-filter_complex " [0:v][5:a][1:v][5:a][2:v][5:a][3:v][3:a][4:v][5:a] concat=n=5:v=1:a=1 [v][a]" \
-map "[v]" -map "[a]" {}'.format(self.coverTime,self.middleTmpFile["TMP.COVER.PNG"],self.profileTime,self.middleTmpFile["TMP.PROFILE.PNG"],self.tagTime,self.middleTmpFile["TMP.TAG.PNG"],self.innerVideo,self.endingTime,self.middleTmpFile["TMP.END.PNG"],self.outputFileName)
# "+self.outputFileName
        print(joinVideoCommandShell)
        joinVideoP=subprocess.Popen(joinVideoCommandShell,shell=True)
        joinVideoP.wait()

        if self.preserveTmpFile:
            pass
        else:
            try:
                for k,v in self.middleTmpFile.items():
                    os.remove(v)
                    pass
            except Exception:
                pass
        # print(str(self.middleTmpFile))


if __name__ == "__main__":
    v=ANKVideo()
    v.askForSetting()
    v.build()