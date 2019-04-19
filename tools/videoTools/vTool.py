import subprocess
import sys

def getVideo(ls):
    command="ffmpeg -threads 8 -i {0} -vcodec copy –an  {1}".format(ls[0],ls[1])
    print(command)
    return subprocess.Popen(command,shell=True)
def getAudio(ls):
    command="ffmpeg -threads 8 -i {0} -vn -y -async 1 -acodec copy {1}".format(ls[0],ls[1])
    print(command)
    return subprocess.Popen(command,shell=True)
def combineVideoAndAudio(ls):
    command="ffmpeg -threads 8 -i {0} -i {1} -vcodec copy -acodec copy {2}".format(ls[0],ls[1],ls[2])
    print(command)
    return subprocess.Popen(command,shell=True)
def contactVideo(ls):
    command="ffmpeg -threads 8 -f concat -i {0} -c copy -acodec copy {1} ".format(ls[0],ls[1])
    print(command)

    return subprocess.Popen(command,shell=True)
def sliceTrim(ls):
    command="ffmpeg  -i {0} -vcodec copy -acodec copy -ss {1} -to {2} {3} -y ".format(ls[0],ls[1],ls[2],ls[3])
    print(command)

    return subprocess.Popen(command,shell=True)
def main():
    funcDict={
        "getAudio":getAudio,
        "getVideo":getVideo,
        "combineVideoAndAudio":combineVideoAndAudio,
        "contactVideo":contactVideo,
        "sliceTrim":sliceTrim
    }
    f=funcDict[str(sys.argv[1])]
    if f is None:
        print("no operator named:"+str(sys.argv[1]))
        return
    f(sys.argv[2:]).wait()

if __name__ == "__main__":
    main()