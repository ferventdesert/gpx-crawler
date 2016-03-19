# gpx-crawler
a gpx format running/riding crawler from Chinese sports website


这是笔者一年多的跑步记录绘制的全图：
![image](https://github.com/ferventdesert/gpx-crawler/blob/master/img/final2.png)


##2.获取网站数据
登录之后，可以看出它是动态加载，当滚轮滚到最下时，自动加载后面的内容。本来是应该嗅探和分析http请求的。后来我懒惰了，采取折中方案，拖到底，全部加载完毕后，保存了当前的html文件。  
yidong.com

值得注意的是，因为下载时需要cookie，因此读者需要将自己在益动GPS的userid和登录的cookie都替换掉（这种网站不值得为它开发自动登录）。

接下来就是下载的过程，获取导出数据按钮的URL的XPath，构造一个带cookie的请求，然后保存文件即可，非常容易。

##3. 解析gpx数据

所谓gpx数据，是一种通用规范的GPS数据格式，详细的资料可自行搜索。

我们需要使用python的gpx解析器, gpxpy是个好选择，使用

pip3 install gpxpy 即可安装。

```
def readgpx(x):
     
    file= open(dir+x+'.gpx','r')
    txt=file.read()
    gpx=gpxpy.parse(txt)
    mv=gpx.get_moving_data()
    dat= {'移动时间':mv.moving_time,'静止时间':mv.stopped_time,'移动距离':mv.moving_distance,'暂停距离':mv.stopped_distance,'最大速度':mv.max_speed};
    dat['总时间']=(gpx.get_duration())
    dat['id']=str(x)
    updown=gpx.get_uphill_downhill()
    dat['上山']=(updown.uphill);
    dat['下山']=(updown.downhill)
    timebound=gpx.get_time_bounds();
    dat['开始时间']=(timebound.start_time)
    dat['结束时间']=(timebound.end_time)
    p=gpx.get_points_data()[0]
    dat['lat']=p.point.latitude
    dat['lng']=p.point.longitude
    file.close()
    return dat
```
