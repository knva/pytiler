import math
import os
import sys

from PIL import Image

def save_images(imagelist,filename='result'):
    if not os.path.exists(filename):
        os.mkdir(filename)

    for data in imagelist:
        image = data['img']
        image.save('./{}/{}_{}_{}.png'.format(filename,data['z'],data['x'],data['y']),'PNG')


def fill_image(origin_image:Image.Image,size,zoom,tiles,tile_size):
    img = Image.new('RGB', (int(size),int(size)), (255, 255, 255,0))
    if origin_image.width > origin_image.height:
        width,height = img.width,img.width * origin_image.height // origin_image.width
    else:
        height,width = img.height,img.height * origin_image.width // origin_image.height

    if width < origin_image.width or height < origin_image.height:
        # 缩小
        img = origin_image.resize((width,height),Image.LANCZOS)
    else:
        # 放大
        img = origin_image.resize((width,height),Image.BICUBIC)

    imglist=  []

    for i in range(tiles):
        for j in range(tiles):
            # print(i,j)
            box = (tile_size * i, tile_size * j, tile_size * (i+1), tile_size * (j+1))
            # print(box)
            region = img.crop(box)
            imglist.append( {'z':zoom,'x':j,'y':i,'img':region})
    return imglist

def get_max_zoom(width,height,tile_size):
    res  =math.ceil(math.log(max(width, height) / float(tile_size)) + 1)
    print('图片宽度:{},图片高度:{},切片尺寸:{},最大缩放:{}'.format(width,height,tile_size,res))
    return  res


if __name__=='__main__':
    file_path = sys.argv[1]
    tile_size = 256
    if len(sys.argv)==3:
        tile_size = int(sys.argv[2])
    if (file_path.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff'))):
        print(file_path)
    else:
        print('请选择正确的图片格式')
        sys.exit(0)

    image = Image.open(file_path)# type: Image.Image
    max_zoom = get_max_zoom(image.width,image.height,tile_size)

    for i in range(max_zoom+1):
        tiles = math.pow(2.0,i)
        print('切',tiles)
        size = tiles * tile_size
        imglist = fill_image(image,size,i,int(tiles),tile_size)
        save_images(imglist,file_path.split('.')[0])