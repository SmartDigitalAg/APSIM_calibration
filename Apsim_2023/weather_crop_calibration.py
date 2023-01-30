# -*- coding: utf-8 -*-

import os,subprocess
import shutil
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


out_list = []

'''met 파일 불러오기 (from. met_list.csv)'''
met_list = pd.read_csv('met_list.csv', index_col=False)
# print(met_list.met_list[0])
met_list = met_list['met_list'].values
print('met 리스트 : \n', met_list)


inpath = 'C:/code/Apsim_2023/'
os.chdir(inpath)

'''apsim 파일 불러오기'''
wheat_tree = ET.parse('run.apsim')
root = wheat_tree.getroot()

'''run.apsim 파일 내 met 경로 변경'''
for i in range(len(met_list)):
    for node in root.iter('simulation'):
        node.attrib['name'] = met_list[i][23:-4]

        for metfile in node.iter('filename'):
            metfile.text = met_list[i]

    wheat_tree.write('run.apsim')                                                           # apsim 파일 덮어 씌우기
    apsim_exe = 'C:/Program Files (x86)/APSIM710-r4218/Model/Apsim.exe "run.apsim"'         # apsim exe 경로 및 apsim 파일 선언
    subprocess.run(apsim_exe, stdout=open(os.devnull, 'wb'))                                # apsim 파일 실행

    '''그래프 그리기'''
    out_list = met_list[i][23:-4]
    out_file = pd.read_csv(f'C:/code/Apsim_2023/{out_list}.out',sep="\\s+" ,skiprows=[0, 1, 3],parse_dates=['Date'], infer_datetime_format=True)
    # print(out_file)

    index = np.arange(len(out_file["Date"].dt.year))
    plt.figure(figsize=(15, 10))
    plt.barh(index, out_file['yield'])
    plt.title(f'{out_list} yield', fontsize=15)
    plt.xlabel('yield (kg/ha)', fontsize=15)
    plt.ylabel('Year', fontsize=15)
    plt.yticks(index, out_file["Date"].dt.year, fontsize=15)
    plt.savefig(f'C:/code/Apsim_2023/graph/{out_list}.png')

###########################################################################################################################################
# 폴더 정리

"""폴더선택"""
dir_path = 'C:\code\Apsim_2023'

"""폴더내파일검사"""

global_cache = {}

def cached_listdir(path):
    res = global_cache.get(path)
    if res is None:
        res = os.listdir(path)
        global_cache[path] = res
    return res


def moveFile(ext):
    if item.rpartition(".")[2] == ext:
        """폴더이동"""
        # print(ext + "확장자를 가진 " + item)

        tDir = dir_path + '/' + ext
        # print(dir_path + '/' + item)

        if not os.path.isdir(tDir):
            os.mkdir(tDir)

        filePath = dir_path + '/' + item
        finalPath = tDir + '/' + item

        if os.path.isfile(filePath):
            shutil.move(filePath, finalPath)


if __name__ == '__main__':

    cached_listdir(dir_path)

    for item in global_cache[dir_path]:

        """추가할 확장자를 수동으로 리스트에 추가"""
        extList = ["sum", "out"]

        for i in range(0, len(extList)):
            moveFile(extList[i])
