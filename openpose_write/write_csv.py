import json
import pandas as pd
import numpy as np
import glob


def getFilelist(path):
    filelist = glob.glob(path + "/*.json")
    filelist.sort()  # 時系列にしたい（openposeの出力はID振ってくれているのでその順番に直す）
    return filelist


def getCSV(files, face, hand):
    body = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist", "MidHip", "RHip", "RKnee",
            "RAnkle", "LHip", "LKnee", "LAnkle", "REye", "LEye", "REar", "LEar", "LBigToe", "LSmallToe", "LHeel",
            "RBigToe", "RSmallToe", "RHeel"]
    for_b_columns = []
    for t in range(len(body)):
        for_b_columns.append(body[t] + str("_X"))
        for_b_columns.append(body[t] + str("_Y"))
        for_b_columns.append(body[t] + str("_P"))

    # 使わなくても結合できるように空のデータフレームを定義しておく
    df_face = pd.DataFrame()
    df_Lhand = pd.DataFrame()
    df_Rhand = pd.DataFrame()
    df_all = pd.DataFrame()

    for i in range(len(files)):
        with open(files[i]) as f:
            data = json.load(f)
            persons = data['people']
            if persons:
                #             data_b= np.array(data['people'][0]['pose_keypoints_2d']).reshape(-1,3)
                data_b = np.array(persons['people'][-1]['pose_keypoints_2d']).reshape(1, -1)
                df_body = pd.DataFrame(data_b, columns=for_b_columns)
                if face == "1":
                    data_head = np.array(persons['people'][-1]['face_keypoints_2d']).reshape(1, -1)
                    df_face = parts(data_head, "face")

                if hand == "1":
                    data_L = np.array(persons['people'][-1]['hand_left_keypoints_2d']).reshape(1, -1)
                    df_Lhand = parts(data_L, "Lhand")
                    data_R = np.array(persons['people'][-1]['hand_right_keypoints_2d']).reshape(1, -1)
                    df_Rhand = parts(data_R, "Rhand")



                df_p = pd.concat([df_body, df_face, df_Lhand, df_Rhand], axis=1)
                df_all = pd.concat([df_all, df_p])

            else:
                non_person=pd.DataFrame("non_person")
                df_all=pd.concat([df_all,non_person])
    df_all.to_csv("./result.csv", index=False)
    print("done")


def parts(data, parts_name):
    for_column = []
    for t in range(data.shape[1] // 3):
        for_column.append(parts_name + "_" + str(t) + "_X")
        for_column.append(parts_name + "_" + str(t) + "_Y")
        for_column.append(parts_name + "_" + str(t) + "_P")

    return pd.DataFrame(data, columns=for_column)


def main():
    files = getFilelist(input("JSONのディレクトリのパスを入力:　"))
    parts_bool=input("頭・手の検出(スペース区切り・書き出す⇨1):").split()
    getCSV(files, parts_bool[0], parts_bool[1])

if __name__ == '__main__':
    main()