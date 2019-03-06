from PIL import Image
import argparse
import os
from tqdm import tqdm

def crop(image_path, coords, saved_location):
	"""

	@param image_path: The path to the image to edit

	@param coords: A tuple of x/y coordinates (x1, y1, x2, y2)

    @param saved_location: Path to save the cropped image

    """
	image_obj = Image.open(image_path)		
	cropped_image = image_obj.crop(coords)
	cropped_image.save(saved_location)


if __name__ == "__main__":
	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-s", "--size", required=True, type=int,help="the size of the square cropped image in pixels")
	ap.add_argument("-p", "--position", type=int, default=0,help="position of the top left pixel of the cropped image")
	args = vars(ap.parse_args())
	
	READ_DIRECTORY = os.path.join(os.path.expanduser('~'), 'Desktop','Cours','OSY',"Projet d'option", 'DepthNet', 'stereo-tracking', 'scenario_0')
	SAVE_DIRECTORY = os.path.join(os.path.expanduser('~'), 'Desktop','Cours','OSY',"Projet d'option", 'DepthNet', 'stereo-tracking', 'scenario_0_'+str(args['size']))
	
	try:
		if not os.path.exists(SAVE_DIRECTORY):
			os.makedirs(SAVE_DIRECTORY)
	except OSError:
		print('Error creating directory'+SAVE_DIRECTORY)

	for filename in tqdm(os.listdir(READ_DIRECTORY)):
		if filename.endswith('.jpg'):
			image = READ_DIRECTORY+'/'+filename
			cropped = SAVE_DIRECTORY+'/'+filename
			if args['position']:
				crop(image, (args['position'], args['position'], args['position'] + args['size'], args['position'] + args['size']),cropped)
			else:
				x = 0
				while x < (1296-1296%args['size']):
					y = 0
					while y < (972-972%args['size']):
						crop(image, (x, y, x + args['size'], y + args['size']),cropped[:-4]+'_'+str(x)+'_'+str(y)+'.jpg')
						y = y + args['size']
					crop(image, (x, 972-args['size'] , x + args['size'], 972),cropped[:-4]+'_'+str(x)+'_'+str(972-args['size'])+'.jpg')
					x = x + args['size']
			for y in range(0,(972-972%args['size']), args['size']):
				crop(image, (1296-args['size'], y , 1296, y + args['size']),cropped[:-4]+'_'+str(1296-args['size'])+'_'+str(y)+'.jpg')
			crop(image, (1296-args['size'], 972-args['size'] , 1296, 972),cropped[:-4]+'_'+str(1296-args['size'])+'_'+str(972-args['size'])+'.jpg')
		
				
