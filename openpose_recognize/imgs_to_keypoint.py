# in order to work, you need to install openpose (compile with python)
# put this file in openpose/python directory
# and make sure that the below link to pyd file is correct

import sys
import cv2
import os
from sys import platform
import argparse
import time
import json

dataset_path = 'F:\\Github\\LSTM-action-detection\\dataset\\'
save_path = 'F:\\Github\\LSTM-action-detection\\dataset_op\\'

dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Change these variables to point to the correct folder (Release/x64 etc.)
    sys.path.append(dir_path + '/../bin/python/openpose/Release')
    os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../x64/Release;' +  dir_path + '/../bin;'
    import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

def walk_dir(dataset_path):
    res = {}
    for no in os.listdir(dataset_path):    # dataset/run
        datas = []
        for action_series in os.listdir(dataset_path+no): # dataset/run/1
            if os.path.isfile(dataset_path+no+'/'+action_series):
                continue
            # data = []
            # for action_photos in os.listdir(dataset_path+no+'/'+action_series): # dataset/run/1/1-10
            #     data.append(dataset_path+no+'/'+action_series+'/'+action_photos)
            datas.append(action_series)
        res[no] = datas
    return res
    
def run_openpose(dataset_path,save_path,res):
     for no in res:
        for action_series in res[no]:
            os.makedirs(os.path.join(save_path,no,action_series), exist_ok=True)
            openpose(image_dir=os.path.join(dataset_path,no,action_series),
                     save_txt_dir=os.path.join(save_path,no,action_series)
                    )

def openpose(image_dir='../examples/media/',save_image_dir='',save_txt_dir='',no_display=False):
    # Flags
    parser = argparse.ArgumentParser()
    # parser.add_argument("--image_dir", default=image_dir, help="Process a directory of images. Read all standard formats (jpg, png, bmp, etc.).")
    # parser.add_argument("--save_image_dir", default=save_image_dir, help="The directory to save result photo")
    # parser.add_argument("--save_txt_dir", default=save_txt_dir, help="The directory to save result txt")
    # parser.add_argument("--no_display", default=no_display, help="Enable to disable the visual display.")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "F:\\Github\\openpose\\models\\"

    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item

    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Read frames on directory
    imagePaths = op.get_images_on_directory(image_dir)
    start = time.time()

    # Process and display images
    for imagePath in imagePaths:
        datum = op.Datum()
        imageToProcess = cv2.imread(imagePath)                  # load image
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))        # compute

        print('Processing : '+imagePath)
        # print("Body keypoints: \n" + str(datum.poseKeypoints))  # text result

        if datum.poseKeypoints is None:
            # no keypoint in this photo
            continue

        if not no_display:
            cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)  # image result 
            key = cv2.waitKey(15)
            if key == 27: break

        # file_name = imagePath.split('\\')[-1].split('.')[0]
        file_name = os.path.basename(imagePath).split('.')[0]
        if save_image_dir != "":
            cv2.imwrite(save_image_dir+file_name+".jpg",datum.cvOutputData)

        if save_txt_dir != "":
            res = datum.poseKeypoints.tolist()
            res = json.dumps(res)
            with open(os.path.join(save_txt_dir,file_name+".txt"),'w') as f:
                json.dump(res,f)

    end = time.time()
    print("OpenPose demo successfully finished. Total time: " + str(end - start) + " seconds")
    

if __name__ == '__main__':

    try:
        res = walk_dir(dataset_path)
        print(res)

        run_openpose(dataset_path,save_path,res)

    except Exception as e:
        print(e)
        sys.exit(-1)