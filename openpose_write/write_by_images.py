import json
import pandas as pd
import numpy as np
import glob


def getFilelist(path):
    file_path = glob.glob(path + "/*.json")
    # filelist.sort()  # 時系列にしたい（openposeの出力はID振ってくれているのでその順番に直す）
    return file_path


def getCSV(path, face, hand):
    body = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist", "MidHip", "RHip", "RKnee",
            "RAnkle", "LHip", "LKnee", "LAnkle", "REye", "LEye", "REar", "LEar", "LBigToe", "LSmallToe", "LHeel",
            "RBigToe", "RSmallToe", "RHeel"]

    # 使わなくても結合できるように空のデータフレームを定義しておく
    df_face = pd.DataFrame()
    df_Lhand = pd.DataFrame()
    df_Rhand = pd.DataFrame()
    df_all = pd.DataFrame()


    with open(path[0]) as f:
        file_name=pd.DataFrame(path,columns=["file_name"])
        data = json.load(f)
        persons = data['people']
        if persons:
            #             data_b= np.array(data['people'][0]['pose_keypoints_2d']).reshape(-1,3)
            data_b = np.array(data['people'][0]['pose_keypoints_2d']).reshape(-1, 3)
            df_body = pd.DataFrame(data_b, columns=["X","Y","P"])
            df_body["parts"]=body
            if face == "1":
                data_head = np.array(data['people'][0]['face_keypoints_2d']).reshape(-1, 3)
                df_face = parts(data_head, "face")

            if hand == "1":
                data_L = np.array(data['people'][0]['hand_left_keypoints_2d']).reshape(-1, 3)
                df_Lhand = parts(data_L, "Lhand")
                data_R = np.array(data['people'][0]['hand_right_keypoints_2d']).reshape(-1, 3)
                df_Rhand = parts(data_R, "Rhand")



            df_p = pd.concat([df_body, df_face, df_Lhand, df_Rhand])

        else:
            non_person=pd.DataFrame("non_person")
            df_all=pd.concat([df_all,non_person])
    df_p.to_csv("./result.csv", index=False)
    print("done")


def parts(data, parts_name):
    for_parts = []
    for t in range(data.shape[0]):
        for_parts.append(parts_name+str(t))
    parts_df=pd.DataFrame(data,columns=["X","Y","P"])
    parts_df["parts"]=for_parts
    return parts_df


def main():
    files = getFilelist(input("JSONのディレクトリのパスを入力:　"))
    parts_bool=input("頭・手の検出(スペース区切り・書き出す⇨1):").split()
    getCSV(files, parts_bool[0], parts_bool[1])

if __name__ == '__main__':
    main()