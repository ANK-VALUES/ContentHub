# ContentHub
## 概述

* 什么是内容中心？
* 为什么创造它？
* 如何加入？

### 约定

####    @符号
(@+数字)留于句尾表示绑定前面的句子.一般用斜体强调.

(@+数字)嵌于句中,表示引用对应的句子.
## 什么是内容中心

内容中心是与ANK_VALUES视频频道相关的文件和问题的集合.

> 什么是ANK_VALUES？

随着信息和知识的大量增长,人类需要找到一种正确的方法来检验命题的可信度,并加快知道（不掌握）不同领域知识的速度.*(@1)*

为了实现@1愿景,我们创建了一个媒体频道命名为ANK_VALUES.

我知道已经有一些商业平台将自己称为“知识市场”或“QA社区”,但我认为这仍远远不是我上面提到的目标.商业平台确实制作了非凡的视频或速读文本(相比于社区).但是,他们如何面对如今种类极其多的领域并保持自身客观性不受商业利益的干涉呢.在企业平均寿命如此之短的情况下,他们如何能够长期维护和跟进每个话题呢（例如'在XX上建立XXX模型的方法'和'XXX威权主义的利弊'等等).QA社区亦无法满足@1,因为解答即求证,QA的简单对话流何以支撑高精度命题的诞生和演进呢?一些问题本身的提法就蕴含谬误,回答过程的引用也缺乏标准,想提取论证结构图和依赖网络更是遥不可及.更何况本世纪的信息IO的形态趋向于可视化,音视频因其高效的信息表达能力将成为网络社会对话的主要方式.如果我们尽可能多地提供工具以支持Text->Video,同时保留结构化的文本以支持论证和演进,那么@1的愿景会有很大程度的实现可能性.

感谢Linus Torvalds,我们现在有了git.我们可以以社区方式轻松创建和维护每个话题.

以下额外的命题也驱使我创建ANK_VALUES:
* 社区可以提供更多领域的话题.
* 在社群监督下平台中的提供者可以提供高质量的话题.
* 使用git可以轻松且长期维护话题.

但是,如果我们简单地堆砌各种类型的话题可能会很杂乱烦人,这就是我对话题进行分类定义的原因.

人类语言有三个主要功能.

* 命令 - > CMD
* 声明 - > STM
* 表达情感 - > ESE

> STM和ESE有更多子类型

```JS

STM.THEORY //理论

STM.TECH //技术工程

STM.ARGUMENT //观点,STM.ARGUMENT和ESE.ARGUMENT之间的区别在于STM.ARGUMENT需要证据支持

ESE.EXCITED//欢欣

ESE.ANGRY //愤怒

ESE.SAD //悲

ESE.EXPECT //期望

ESE.LOATHE //厌恶

ESE.ARGUMENT //未证言论

```



话题是如下的数据结构
```JSON
{
    "name":"How to implement a suburban home defense system at low cost",
    "id":"8aaa07afad614586aefae434bd98489b",//名字的md5值
    "type":"STM.TECH",
    "credibility":0.5,//如果主题是STM.THEORY或STM.ARGUMENT，则需要在其上添加可信属性。它的范围是[0,1]。零意味着STM完全是一个不可信命题，否则这是事实。
    "innerRefers":[
        "dbe75952a4d4aa910db41d7bb10f9507",
        "a52504527ecb5467e9378d3f8ac7052c",
    ],//如果你在ANK_VALUES中引用了某个主题，只需将它们的ID添加到此列表中即可
    "outerRefers":[
        {
            "GB/T7714":[
            "Yang G X , Li F J . Investigation of Security and Defense System for Home Based on Internet of Things[C]// 2010 International Conference on Web Information Systems and Mining (WISM 2010). IEEE Computer Society, 2010."
            ]//使用格式名称作为属性并在列表中追加内容.
            ,
            "webPage":[
                "https://en.wikipedia.org/wiki/Thermographic_camera"
            ]//也可以将网页添加到此列表中.

        }
    ]
    "initialAuthor":{
        "name":"Kevin",
        "introduce":"Computer, mathematics, engineering",
        "location":"unknown, China",
        "email":"ankkevinluo@gmail.com",
        "avator":"./CAW.png"//你的头像url,如果你用videoTool去制作视频,那么请带上它,并把文件拷到/tools/videoTools/下.
    },
    "tags":["technology","computer vision",...],//您可以添加这些标签,以帮助人们了解你的主题
    
    //我知道你想说什么 - “如何找到我可以选择标签的标签系统？”.我必须说对不起.目前我还没有建成它,但很快就会到来,伙计.

    "for":["age12-22","primary"],//选择目标人群
    "notFor":["age0-12","senior"],//过滤器
    "warning":["possible hurt level-middle","bad language level-low"],//一些内容警告
    "log":"Why are we here? What are we doing?",//在结尾留下几秒钟的句子
    "videoUrl":"https://XXX.mov"//如果你制作了视频,那可真是太让人为之鼓舞了.请将视频云文件链接放在这.一般情况下它都会在ANK_VALUES频道中得到发布.
}
```
*(@2)*


## 为什么创建它

正如@1所言,ANK_VALUES希望创建一个*社区性,可信赖,可维护的*内容渠道,以推动社会认知更高速地发展.

如果您想要查找有关每个视频的更多数据或通过请求合并来更正某些错误,那么这是适合您的地方.

更重要的是,开源驱动我们更认真地创建话题.


## 如何加入
1.首先克隆此存储库.
```
Git clone https://github.com/ANK-VALUES/ContentHub.git
```
2.1 如果有一天你有奇思妙想,只需添加正确格式的自己的目录和文件.

> 如果你想纠正已经存在的东西,修改它并提交.

> 如果你只是对某些事情感到困惑,请在github上提出一个issue.



2.1.如果你甚至使用内置的videoTool制作了视频,你可以将你做好的视频的云文件链接放入配置文件@2中.一般来说,它都会在被merge后由ANK_VALUES发布.

3 请求合并
