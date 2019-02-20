import argparse
import os
from tqdm import tqdm

READ_DIRECTORY = os.path.join(os.path.expanduser('~'), 'Desktop','Cours','OSY',"Projet d'option", 'Data', 'scenario_0_')

if __name__ == "__main__":

	ap = argparse.ArgumentParser()
	ap.add_argument("-s", "--size", required=True, type=int,help="the size of the square cropped image in pixels")
	args = vars(ap.parse_args())


	suffixes = [ ( x, 972-972%args["size"] ) for x in range(0,1296,args["size"]) ]
	
	suffixes.extend([ ( 1296-1296%args["size"], y ) for y in range(0,972,args["size"])])

	counter = 0

	for filename in tqdm(os.listdir(READ_DIRECTORY+str(args["size"]))):
		# print((int(filename.split('_')[1]),int(filename.split('_')[2][:-4])), '---', suffixes[0])
		if (int(filename.split('_')[1]),int(filename.split('_')[2][:-4])) in suffixes:
			os.remove(READ_DIRECTORY+str(args["size"])+'/'+filename)
			counter += 1
	print(counter, 'files have been removed!')