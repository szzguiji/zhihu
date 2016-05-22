#coding=utf-8
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
def create_validate_code():

	# 随机字母:
	def rndChar():
		return chr(random.randint(65, 90))

	# 随机颜色:
	def rndColor():
		return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

	# 80 x 40:
	width = 20 * 4
	height = 40
	strs = ''
	image = Image.new('RGB', (width, height), (255,255,255))
	# 创建Font对象:
	font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
	# 创建Draw对象:
	draw = ImageDraw.Draw(image)
	# 填充每个像素:
	for x in range(width):
		for y in range(height):
			draw.point((x, y), fill=(204,204,204))
	# 输出文字:
	for t in range(4):
		randchar =  rndChar()
		strs = strs + randchar
		draw.text((20 * t + 5, 10), randchar, font=font, fill=rndColor())
	return image,strs