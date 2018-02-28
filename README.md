# sewImage
## 前言
可能很多安卓手机都会自带拼接长截图的功能，可是对于iOS只能通过第三方的app拼接了。于是我想将拼接的功能做成微信小程序，这样会比较方便，无奈实现过程中发现用JavaScript实现性能存在很大问题，识别率也很低，于是打算先用python实现，以测试算法的正确性。

我写得可能不是很好，欢迎指正！


## 用法
请保持两张图片重复部分的高度超过15px


```
sewImg = sewImage()
img = sewImg.sew(["pic1.png","pic2.png","pic3.png"])
img.save('new.png')
```

## 效率问题
目前效率并不是太好，拼接三张图需要1.8秒左右
我的想法是通过hash将图片压缩后再进行识别比对，但目前没有想到比较好的hash算法
如果有更好更快的算法欢迎交流

效果图在最后

## 效果图
![pic1.png](https://github.com/ZitionChan/sewImage/blob/master/pic1.png)
![pic2.png](https://github.com/ZitionChan/sewImage/blob/master/pic2.png)
![pic3.png](https://github.com/ZitionChan/sewImage/blob/master/pic3.png)
拼成下图
![new.png](https://github.com/ZitionChan/sewImage/blob/master/new.png)

