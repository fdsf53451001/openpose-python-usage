from dis import dis
import os
import json
import numpy as np

openpose_txt_path = 'example/openpose_txt/'
yolo_txt_path = 'example/yolo_txt/'
saveback_txt_path = 'example/saveback_txt/'

# the index of person in yolo result
yolo_person_index = '0'

# the output format of openpose is pixel coordinate
# but the output format of yolo is 0-1 scaled coordinate
# use the following photo size to convert
photo_size_x = 1280
photo_size_y = 720

# when 0.5 of openpose keypoint in yolo box, return valid
accept_inbox_rate = 0.5    
# select 3 nearest yolo box to check 
# (the nearest box is not aloways correct one, so the other near box is also checked)
max_try_count = 3

# loop the file in dir
def check_dir(dir_path):
    for root,dirs,files in os.walk(dir_path):
        for file in files:
            load_keypoint(file)

# for each file, load openpose and yolo file
def load_keypoint(file_name):
    print(file_name,end=' ')
    with open(openpose_txt_path+file_name,'r') as f:
        op = json.load(f)
        op = json.loads(op)
    
    with open(yolo_txt_path+file_name,'r') as f:
        yolo = f.readlines()
        tmp = []
        for line in yolo:
            if line.split(' ')[0] == yolo_person_index:
                yolo_pos = line.split(' ')
                tmp.append([
                            float(yolo_pos[1])*photo_size_x,
                            float(yolo_pos[2])*photo_size_y,
                            float(yolo_pos[3])*photo_size_x,
                            float(yolo_pos[4])*photo_size_y
                            ])
        yolo = tmp
        yolo.sort(key=lambda x:(x[0],x[1]))

    saveback_list = []
    valid_person = 0
    for person_index in range(len(op)):
        index = openpose_compare_yolo(op[person_index],yolo)
        if index!=-1:
            valid_person+=1
            saveback_list.append(op[person_index])
    print(valid_person,'/',len(op))

    # save back to json file
    saveback_json = json.dumps(saveback_list)
    with open(saveback_txt_path+file_name,'w') as f:
        json.dump(saveback_json,f)

# compare two file of openpose and yolo (the same image)         
def openpose_compare_yolo(person,yolo):
    valid_point = []
    for keypoint in person:
        if keypoint[0] == 0 and keypoint[1] == 0:
            valid_point.append(0)
        else:
            valid_point.append(1)
    
    try:
        basic_point_index = valid_point.index(1)
    except AttributeError:
        # all 25 points in openpose are (0,0,0)
        return -1

    # calculate distance between basic point and yolo box
    distance = []
    for pos in yolo:
        distance.append(np.sqrt((pos[0]-person[basic_point_index][0])**2+(pos[1]-person[basic_point_index][1])**2))

    for _ in range(max_try_count):
        mindis = min(distance)
        index = distance.index(mindis)

        valid_count = 0
        inbox_count = 0
        for j in range(len(valid_point)):
            if valid_point[j] == 1:
                valid_count+=1
                if check_inbox(person[j][0],person[j][1],yolo[index][0],yolo[index][1],yolo[index][2],yolo[index][3]):
                    inbox_count+=1

        # if the valid rate > accept rate, return ok
        if inbox_count/valid_count >= accept_inbox_rate:
            return index
        distance[index] = max(distance)
    return -1

# check if the point is in the box
def check_inbox(ox,oy,yx,yy,yw,yh):
    if ox<yx-(yw/2) or ox>yx+(yw/2):
        return False
    if oy<yy-(yh/2) or oy>yy+(yh/2):
        return False
    return True

def run(openpose_txt_path_input,yolo_txt_path_input,saveback_txt_path_input):
    openpose_txt_path = openpose_txt_path_input
    yolo_txt_path = yolo_txt_path_input
    saveback_txt_path = saveback_txt_path_input
    check_dir(openpose_txt_path)

if __name__ == '__main__':
    check_dir(openpose_txt_path)