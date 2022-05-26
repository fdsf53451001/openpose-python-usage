# put this file in yolo directory to run
import detect as dt
import os

dataset_path = 'F:/Github/LSTM-action-detection/dataset/'
save_path = 'F:/Github/LSTM-action-detection/dataset_yolo/'
weights = 'F:/Github/yolo_volleyball/runs/train/exp6/weights/best.pt'
data = 'F:/Github/yolo_volleyball/data/volleyball.yaml'

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


def run_yolo(dataset_path,save_path,res,weights,data):
    for no in res:
        for action_series in res[no]:
            dt.run(weights=weights, 
                data=data,
                source=os.path.join(dataset_path,no,action_series),
                project=os.path.join(save_path,no),
                name=action_series,
                save_txt=True,
                nosave=True
                )

if __name__ == '__main__':
    res = walk_dir(dataset_path)
    print(res)
    run_yolo(dataset_path,save_path,res,weights,data)

