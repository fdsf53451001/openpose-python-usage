import os
import json

openpose_txt_path = ''
yolo_txt_path = ''
yolo_person_index = '0'

def check_dir(dir_path):
    for root,dirs,files in os.walk(dir_path):
        for file in files:
            load_keypoint(file)

def load_keypoint(file_name):
    with open(openpose_txt_path+file_name,'r') as f:
        op = json.load(f)
    
    with open(yolo_txt_path+file_name,'r') as f:
        yolo = f.readlines()
        tmp = []
        for line in yolo:
            if line.split(' ')[0] == yolo_person_index:
                tmp.append(line.split(' ')[1:5])
        yolo = tmp

    for person in op:
        inbox_count = 0
        for keypoint in person:
            # add compare code here
            pass

    # save back to json file
            

if __name__ == '__main__':
    check_dir(openpose_txt_path)