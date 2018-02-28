'''
Author: Zixuan Chen
mail: scutczx@gmail.com
Requirements: PIL
'''

__author__="Zixuan Chen"

from PIL import Image

class sewImage(object):
	def __init__(self,imagePath=[]):
		self.__imgPath = imagePath
		self.__imgdatas = []
		self.__width = -1
		self.__height = -1
		self.__curr = 0

	#打开图片
	def __openImages(self):
		if(len(self.__imgPath)<2):
			raise ValueError("图片数量小于2张")
		for path in self.__imgPath:
			img = Image.open(path)
			img_RGB = img.convert("RGB")
			imgdata = img_RGB.getdata()
			#判断尺寸是否一致
			if(self.__width==-1):
				self.__width,self.__height = img_RGB.size
			else:
				w,h = img_RGB.size
				if(w!=self.__width or h != self.__height):
					raise ValueError("图片尺寸不一致")
			self.__imgdatas.append(imgdata)

	#寻找相同的头部 
	def __findHead(self,hitRate=0.9): #hitRate：一行中超过hitRate*width个相同的像素即认为该行相同
		imgdatas = self.__imgdatas
		curr = self.__curr
		width = self.__width
		if(curr>=len(imgdatas)-1):
			return
		equalPixel = 0
		head=self.__height #相同头的位置，默认为height
		imgdata1=imgdatas[curr]
		imgdata2=imgdatas[curr+1]

		for h in range(head):
			for w in range(width):#比对一行
				r1,g1,b1 = imgdata1[width*h+w]
				r2,g2,b2 = imgdata2[width*h+w]
				if(abs(r1-r2)<25 and abs(g1-g2)<25 and abs(b1-b2)<25):
					equalPixel +=1
			if(equalPixel<width*hitRate):
				head = h
				break
			equalPixel=0
		self.__curr+=1
		return head

	#拼接两张图
	def __getNewImgData(self):	
		newHeight = self.__height
		newImgData = list(self.__imgdatas[0])
		width = self.__width
		height = self.__height
		for i in range(len(self.__imgdatas)-1):
			equalPixel=0
			tail = newHeight
			imgdata2 = list(self.__imgdatas[i+1])
			head = self.__findHead()

			offsetLine = 15 #同时检查offsetLine行是否一致
			for h in range(newHeight-offsetLine)[::-1]:
				for w in range(width):
					r1,g1,b1 = imgdata2[w+width*head]
					r2,g2,b2 = newImgData[w+width*h]

					r3,g3,b3 = imgdata2[w+width*(head+offsetLine)]
					r4,g4,b4 = newImgData[w+width*(h+offsetLine)]

					if(r1==r2 and g1==g2 and b1==b2 and r3==r4 and g3==g4 and b3==b4):
						equalPixel+=1

				if(h < newHeight-height): #没有找到相同行
					break
				if(equalPixel==width):
					tail = h
					break
				equalPixel=0

			newImgData = newImgData[:width*tail]
			newImgData.extend(imgdata2[width*head:])
			newHeight = tail + (height - head)
		return (newImgData,newHeight)

	def sew(self,imagePath=[]):
		if(imagePath!=[]):
			self.__imgPath = imagePath
		self.__curr = 0
		self.__openImages() #加载图片	
		newImgData,newHeight = self.__getNewImgData()
		newImg = Image.new('RGB',(self.__width,newHeight))
		newImg.putdata(newImgData)
		print('拼图完成！')
		return newImg

sewImg = sewImage()
img = sewImg.sew(["pic1.png","pic2.png","pic3.png"])
img.save('new.png')