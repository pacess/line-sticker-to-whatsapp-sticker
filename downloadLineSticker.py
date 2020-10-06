##----------------------------------------------------------------------------------------
##  Download LINE Sticker v3.00
##----------------------------------------------------------------------------------------
##  Platform: macOS Mojave + Python 3.7
##  Written by Pacess HO
##  Copyrights Pacess Studio, 2018-2020.  All rights reserved.
##----------------------------------------------------------------------------------------

import os
import json
import urllib.request
from PIL import Image, ImageFile

##----------------------------------------------------------------------------------------
## 	Sample META data for Xcode  {
## 		"identifier": "com.pacess.line6",
## 		"name": "Go Go Tomboy Sally!",
## 		"publisher": "LINE Store",
## 		"tray_image_file" : "_line6_tray.webp",
## 		"publisher_website" : "",
## 		"privacy_policy_website" : "",
## 		"license_agreement_website" : "",
## 		"stickers": [
## 			{"image_file": "_line6_00001.webp", "emojis": []},
## 			{"image_file": "_line6_00002.webp", "emojis": []},
## 			{"image_file": "_line6_00003.webp", "emojis": []},
## 			{"image_file": "_line6_00004.webp", "emojis": []},
## 			{"image_file": "_line6_00005.webp", "emojis": []},
## 			{"image_file": "_line6_00006.webp", "emojis": []},
## 			{"image_file": "_line6_00007.webp", "emojis": []},
## 			{"image_file": "_line6_00008.webp", "emojis": []},
## 			{"image_file": "_line6_00009.webp", "emojis": []},
## 			{"image_file": "_line6_00010.webp", "emojis": []},
## 			{"image_file": "_line6_00011.webp", "emojis": []},
## 			{"image_file": "_line6_00012.webp", "emojis": []},
## 			{"image_file": "_line6_00013.webp", "emojis": []},
## 			{"image_file": "_line6_00014.webp", "emojis": []},
## 			{"image_file": "_line6_00015.webp", "emojis": []},
## 			{"image_file": "_line6_00016.webp", "emojis": []},
## 			{"image_file": "_line6_00017.webp", "emojis": []},
## 			{"image_file": "_line6_00018.webp", "emojis": []},
## 			{"image_file": "_line6_00019.webp", "emojis": []},
## 			{"image_file": "_line6_00020.webp", "emojis": []},
## 			{"image_file": "_line6_00021.webp", "emojis": []},
## 			{"image_file": "_line6_00022.webp", "emojis": []},
## 			{"image_file": "_line6_00023.webp", "emojis": []},
## 			{"image_file": "_line6_00024.webp", "emojis": []}
## 		]
## 	},

##----------------------------------------------------------------------------------------
##  Sticker Store URL:
##  https://store.line.me/home/en
##
##  Sticker Pack URL:
##  https://store.line.me/stickershop/product/9773/en
##
##  Sample Sticker URL:
##  https://stickershop.line-scdn.net/stickershop/v1/sticker/8573819/ANDROID/sticker.png;compress=true
##  https://stickershop.line-scdn.net/stickershop/v1/sticker/8573819/IOS/sticker@2x.png;compress=true
## 
## 	http://dl.stickershop.line.naver.jp/products/0/0/1/2046/iphone/productInfo.meta
## 
## 	Preview url:
## 	http://dl.stickershop.line.naver.jp/products/0/0/1/2046/android/preview.png
## 
## 	Main icon url (180 x 180):
## 	http://dl.stickershop.line.naver.jp/products/0/0/1/2046/android/main.png
## 
## 	Thumbnail url:
## 	http://dl.stickershop.line.naver.jp/products/0/0/1/2046/android/thumbnail.png
## 
## 	Tab icon url:
## 	http://dl.stickershop.line.naver.jp/products/0/0/1/2046/android/tab_on.png
## 
## 	貼圖打包：
## 	http://dl.stickershop.line.naver.jp/products/0/0/1/2046/iphone/stickerpack@2x.zip
##
##  Reference
##  http://max-everyday.com/2013/02/line-sticker-meta-data-info-html/

_stickerPackIDArray = [3312]

_tabURL = "http://dl.stickershop.line.naver.jp/products/0/0/1/####/iphone/tab_on@2x.png"
_metaURL = "http://dl.stickershop.line.naver.jp/products/0/0/1/####/iphone/productInfo.meta"
_stickerURL = "https://stickershop.line-scdn.net/stickershop/v1/sticker/####/IOS/sticker@2x.png;compress=false"

##  Max 100KB
_stickerFileSizeLimit = (1000*98)
_trayImageFileSizeLimit = (1024*48)
_trayImageSize = (96, 96)
_stickerLimitPerPack = 30

##----------------------------------------------------------------------------------------
_metaArray = []
for stickerPackID in _stickerPackIDArray:

	##----------------------------------------------------------------------------------------
	##  Get meta data
	url = _metaURL.replace("####", str(stickerPackID))
	inputFile = urllib.request.urlopen(url)
	data = inputFile.read()
	inputFile.close()

	##  Extract JSON data
	jsonObject = json.loads(data)
	title = jsonObject["title"]["en"]
	stickerArray = jsonObject["stickers"]

	directory = str(stickerPackID)+"/"
	if not os.path.isdir(directory):
		os.makedirs(directory)

	##----------------------------------------------------------------------------------------
	##  Download stickers
	print("\nDownloading ["+str(stickerPackID)+"] "+title+" from LINE Store:")
	size = (512, 512)
	outputStickerArray = []
	count = 0
	for stickerDictionary in stickerArray:
	
		stickerID = stickerDictionary["id"]
		print("  Downloading sticker image with ID #"+str(stickerID)+"...", end="")
	
		url = _stickerURL.replace("####", str(stickerID))
		inputFile = urllib.request.urlopen(url)
		data = inputFile.read()
		inputFile.close()
		print("done")
	
		##  Save PNG
		outputID = str(stickerPackID)+"_"+str(stickerID)
		filename = outputID+".png"
		filePath = directory+filename
		outputFile = open(filePath, "wb")
		outputFile.write(data)
		outputFile.close()
		
		##  Scale up to 512x512 pixels
		ImageFile.LOAD_TRUNCATED_IMAGES = True
		image = Image.open(filePath)
		
		scaleW = size[0]/image.size[0]
		scaleH = size[1]/image.size[1]
		scale = scaleW
		if (scaleW > scaleH):
			scale = scaleH
	
		newWidth = int(image.size[0]*scale)
		newHeight = int(image.size[1]*scale)
		scaleSize = (newWidth, newHeight)
		
		image = image.convert("RGBA")
		scaledImage = image.resize(scaleSize, Image.ANTIALIAS)	
		outputImage = Image.new("RGBA", size, (255, 255, 255, 0))
		outputImage.paste(scaledImage, (int((size[0]-scaledImage.size[0])/2), int((size[1]-scaledImage.size[1])/2)))
		
		#filename = outputID+"_512x512.png"
		#outputImage.save(directory+filename)
	
		##  Convert to WEBP
		quality = 100
		filename = outputID+".webp"
		filePath = directory+filename
		outputImage.save(filePath, "webp", quality=quality)

		##  Make sure WEBP is under 100KB limit
		fileSize = os.path.getsize(directory+filename)
		while (fileSize >= _stickerFileSizeLimit):
			
			quality = quality-2
			outputImage.save(directory+filename, "webp", quality=quality)
			fileSize = os.path.getsize(directory+filename)
			print("    File size reach limit, saving quality "+str(quality)+"%")
			
			##  Force quit
			if (quality < 50):
				fileSize = 0
		
		##  Create output meta data
		##  {"image_file": "_line6_00001.webp", "emojis": []},
		singleStickerDictionary = {}
		singleStickerDictionary["image_file"] = outputID+".webp"
		singleStickerDictionary["emojis"] = []
		outputStickerArray.append(singleStickerDictionary)
		
		##----------------------------------------------------------------------------------------
		##  Convert first sticker to tray image
		count = count+1
		if (count == 1):
			
			croppedBox = image.getbbox()
			croppedImage = image.crop(croppedBox)
			croppedImage.save("cropped.png")
			
			##  Scale down to 96x96 pixels
			scaleW = _trayImageSize[0]/croppedImage.size[0]
			scaleH = _trayImageSize[1]/croppedImage.size[1]
			scale = scaleW
			if (scaleW > scaleH):
				scale = scaleH
			
			newWidth = int(croppedImage.size[0]*scale)
			newHeight = int(croppedImage.size[1]*scale)
			scaleSize = (newWidth, newHeight)
			scaledImage = croppedImage.resize(scaleSize, Image.ANTIALIAS)	
			
			##  Create tray image
			filename = str(stickerPackID)+"_tray.png"
			filePath = directory+filename
			outputImage = Image.new("RGBA", _trayImageSize, (255, 255, 255, 0))
			outputImage.paste(scaledImage, (int((_trayImageSize[0]-scaledImage.size[0])/2), int((_trayImageSize[1]-scaledImage.size[1])/2)))
			outputImage.save(filePath)

			##  Convert to WEBP
			quality = 100
			filename = str(stickerPackID)+"_tray.webp"
			filePath = directory+filename
			outputImage.save(filePath, "webp", quality=quality)
	
			##  Make sure WEBP within size limit
			filesize = os.path.getsize(filePath)
			while (filesize > _trayImageFileSizeLimit):
		
				quality = quality-2
				outputImage.save(filePath, "webp", quality=quality)
				filesize = os.path.getsize(filePath)
				print("    Tray image file size reach limit, saving quality "+str(quality)+"%")
	
	##----------------------------------------------------------------------------------------
	##  Prepare meta data for Xcode
	metaArray = {}
	metaArray["identifier"] = "line.store."+str(stickerPackID)
	metaArray["name"] = title
	metaArray["publisher"] = "LINE Store"
	metaArray["tray_image_file"] = str(stickerPackID)+"_tray.webp"
	metaArray["publisher_website"] = "https://store.line.me/home/ja"
	metaArray["privacy_policy_website"] = "https://store.line.me/home/ja"
	metaArray["license_agreement_website"] = "https://store.line.me/home/ja"

	##  Each stick pack can contains max. 30 stickers
	stickerCount = len(outputStickerArray)
	if (stickerCount <= _stickerLimitPerPack):
		
		metaArray["stickers"] = outputStickerArray
		_metaArray.append(metaArray)
		
		filename = directory+str(stickerPackID)+"_meta.txt"
		with open(filename, "w") as outfile:
			json.dump(metaArray, outfile)
	else:
		
		partNo = 1
		stickerIndex = 0
		while (stickerIndex < stickerCount):
		
			array = outputStickerArray[stickerIndex:stickerIndex+20]

			metaArray = {}
			metaArray["identifier"] = "line.store."+str(stickerPackID)+"."+str(chr(97-1+partNo))
			metaArray["name"] = title+" Pt."+str(partNo)
			metaArray["publisher"] = "LINE Store"
			metaArray["tray_image_file"] = str(stickerPackID)+"_tray.webp"
			metaArray["publisher_website"] = "https://store.line.me/home/ja"
			metaArray["privacy_policy_website"] = "https://store.line.me/home/ja"
			metaArray["license_agreement_website"] = "https://store.line.me/home/ja"
			metaArray["stickers"] = array
			_metaArray.append(metaArray)
	
			filename = directory+str(stickerPackID)+"_meta_"+str(partNo)+".txt"
			with open(filename, "w") as outfile:
				json.dump(metaArray, outfile)
		
			partNo = partNo+1
			stickerIndex = stickerIndex+20

##----------------------------------------------------------------------------------------
##  Save meta
filename = "line_sticker_meta.txt"
with open(filename, "w") as outfile:
	json.dump(_metaArray, outfile)

##----------------------------------------------------------------------------------------
##  Finally
print("\nDone\n")