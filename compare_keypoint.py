from dis import dis
import os
import json
import numpy as np

class Compare_keypoint:

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
    def check_dir(self,dir_path):
        for root,dirs,files in os.walk(dir_path):
            for file in files:
                self.load_keypoint(file)

    # for each file, load openpose and yolo file
    def load_keypoint(self,file_name):
        print(file_name,end=' ')
        with open(os.path.join(self.openpose_txt_path,file_name),'r') as f:
            op = json.load(f)
            op = json.loads(op)
        
        with open(os.path.join(self.yolo_txt_path,file_name),'r') as f:
            yolo = f.readlines()
            tmp = []
            for line in yolo:
                if line.split(' ')[0] == self.yolo_person_index:
                    yolo_pos = line.split(' ')
                    tmp.append([
                                float(yolo_pos[1])*self.photo_size_x,
                                float(yolo_pos[2])*self.photo_size_y,
                                float(yolo_pos[3])*self.photo_size_x,
                                float(yolo_pos[4])*self.photo_size_y
                                ])
            yolo = tmp
            yolo.sort(key=lambda x:(x[0],x[1]))

        saveback_list = []
        valid_person = 0
        for person_index in range(len(op)):
            index = self.openpose_compare_yolo(op[person_index],yolo)
            if index!=-1:
                valid_person+=1
                saveback_list.append(op[person_index])
        print(valid_person,'/',len(op))

        # save back to json file
        saveback_json = json.dumps(saveback_list)
        with open(os.path.join(self.saveback_txt_path,file_name),'w') as f:
            json.dump(saveback_json,f)

    # compare two file of openpose and yolo (the same image)         
    def openpose_compare_yolo(self,person,yolo):
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

        for _ in range(self.max_try_count):
            mindis = min(distance)
            index = distance.index(mindis)

            valid_count = 0
            inbox_count = 0
            for j in range(len(valid_point)):
                if valid_point[j] == 1:
                    valid_count+=1
                    if self.check_inbox(person[j][0],person[j][1],yolo[index][0],yolo[index][1],yolo[index][2],yolo[index][3]):
                        inbox_count+=1

            # if the valid rate > accept rate, return ok
            if inbox_count/valid_count >= self.accept_inbox_rate:
                return index
            distance[index] = max(distance)
        return -1

    # check if the point is in the box
    def check_inbox(self,ox,oy,yx,yy,yw,yh):
        if ox<yx-(yw/2) or ox>yx+(yw/2):
            return False
        if oy<yy-(yh/2) or oy>yy+(yh/2):
            return False
        return True

    # run this file with default path
    def run(self):
        self.check_dir(self.openpose_txt_path)

    # run this method to setup the path, and excute compare_keypoint
    def run(self,openpose_txt_path,yolo_txt_path,saveback_txt_path):
        self.openpose_txt_path = openpose_txt_path
        print(self.openpose_txt_path)
        self.yolo_txt_path = yolo_txt_path
        self.saveback_txt_path = saveback_txt_path
        self.check_dir(openpose_txt_path)

    

def walk_dir(dataset_path):
    res = {}
    for no in os.listdir(dataset_path):    # dataset/run
        datas = []
        for action_series in os.listdir(dataset_path+no): # dataset/run/1
            if os.path.isfile(os.path.join(dataset_path,no,action_series)):
                continue
            # data = []
            # for action_photos in os.listdir(dataset_path+no+'/'+action_series): # dataset/run/1/1-10
            #     data.append(dataset_path+no+'/'+action_series+'/'+action_photos)
            datas.append(action_series)
        res[no] = datas
    return res

def run_compare(res,yolo_dataset_path,openpose_dataset_path,save_dataset_path):
    file_missing_count = 0
    for no in res:
        for action_series in res[no]:
            try:
                os.makedirs(os.path.join(save_dataset_path,no,action_series), exist_ok=True)

                ck = Compare_keypoint()
                ck.run( openpose_txt_path=os.path.join(openpose_dataset_path,no,action_series),
                        yolo_txt_path=os.path.join(yolo_dataset_path,no,action_series),
                        saveback_txt_path=os.path.join(save_dataset_path,no,action_series)
                        )
            except FileNotFoundError:
                file_missing_count+=1

    return file_missing_count

if __name__ == '__main__':  
    yolo_dataset_path = 'F:\\Github\\LSTM-action-detection\\dataset_yolo\\'
    openpose_dataset_path = 'F:\\Github\\LSTM-action-detection\\dataset_op\\'
    save_dataset_path = 'F:\\Github\\LSTM-action-detection\\dataset_filiter\\'
    res = walk_dir(yolo_dataset_path)
    file_missing_count = run_compare(res,yolo_dataset_path,openpose_dataset_path,save_dataset_path)

    print('finish!','missing count :',file_missing_count)
    