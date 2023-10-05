# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 23:45:18 2023

@author: arsko
"""
from FigmAPI import FigmAPI
import dearpygui.dearpygui as dpg
import pickle
import numpy as np
import pandas as pd

def CheckChildrensCounting(doc,res): # Смотрим сколько всего детей
  if 'children' not in doc:
    return res
  for children in doc['children']:
    res +=1
    res = CheckChildrensCounting(children,res)
  return res

def GetChangedParamsCount(doc_1,doc_2,all_keys):
  if 'children' not in doc_1 and 'children' not in doc_2:
    return all_keys
  if 'children' not in doc_1 and 'children' in doc_2:
    change = CheckChildrensCounting(doc_2,0)
    if "struct" not in all_keys:
      all_keys["struct"] = 0
    all_keys["struct"] += change
    return all_keys
  if 'children' in doc_1 and 'children' not in doc_2:
    change = CheckChildrensCounting(doc_1,0)
    if "struct" not in all_keys:
      all_keys["struct"] = 0
    all_keys["struct"] += change
    return all_keys
  childrens_1 = doc_1['children']
  childrens_2 = doc_2['children']
  childrens_1.sort(key=lambda dictionary: dictionary['type']) # Сортируем элементы по типу children
  childrens_2.sort(key=lambda dictionary: dictionary['type']) # Сортируем элементы по типу children
  if len(childrens_1) > len(childrens_2):
    j = 0
    for i in range(0, len(childrens_1)):
      try:
        if childrens_1[i]['type'] == childrens_2[j]['type']:
          for key,value in childrens_1[i].items():
            if key == 'children':
              continue
            if key not in childrens_2[j]:
              if key not in all_keys:
                all_keys[key] = 0
              all_keys[key]+=1
              continue
            if value != childrens_2[j][key]:
              if key not in all_keys:
                all_keys[key] = 0
              all_keys[key] +=1
          all_keys = GetChangedParamsCount(childrens_1[i],childrens_2[j],all_keys)
        else:
          change = CheckChildrensCounting(childrens_1[i],0)
          if "struct" not in all_keys:
            all_keys["struct"] = 0
          all_keys["struct"] += change
          i+=1
          all_keys = GetChangedParamsCount(childrens_1[i],childrens_2[j],all_keys)
        j+=1
      except IndexError:
        continue
  else:
    i = 0
    for j in range(0, len(childrens_2)):
      try:
        if childrens_1[i]['type'] == childrens_2[j]['type']:
          for key,value in childrens_2[j].items():
            if key == 'children':
              continue
            if key not in childrens_1[i]:
              if key not in all_keys:
                all_keys[key] = 0
              all_keys[key]+=1
              continue
            if value != childrens_1[i][key]:
              if key not in all_keys:
                all_keys[key] = 0
              all_keys[key] +=1
          all_keys = GetChangedParamsCount(childrens_1[i],childrens_2[j],all_keys)
        else:
          change = CheckChildrensCounting(childrens_2[j],0)
          if "struct" not in all_keys:
            all_keys["struct"] = 0
          all_keys["struct"] += change
          j+=1
          all_keys = GetChangedParamsCount(childrens_1[i],childrens_2[j],all_keys)
        i+=1
      except IndexError:
        continue
  return all_keys

def GetParamsCount(doc_1,doc_2,params_num,diff):
  if 'children' not in doc_1 or 'children' not in doc_2:
    return (params_num,diff)
  childrens_1 = doc_1['children']
  childrens_2 = doc_2['children']
  childrens_1.sort(key=lambda dictionary: dictionary['type']) # Сортируем элементы по типу children
  childrens_2.sort(key=lambda dictionary: dictionary['type']) # Сортируем элементы по типу children
  if len(childrens_1) > len(childrens_2):
    j = 0
    for i in range(0, len(childrens_1)):
      try:
        if childrens_1[i]['type'] == childrens_2[j]['type']:
          for key,value in childrens_1[i].items():
            if key not in childrens_2[j] or value != childrens_2[j][key]:
              diff +=1
            params_num +=1
          params_num,diff = GetParamsCount(childrens_1[i],childrens_2[j],params_num,diff)
        else:
          i+=1
          params_num,diff = GetParamsCount(childrens_1[i],childrens_2[j],params_num,diff)
        j+=1
      except IndexError:
        continue
  else:
    i = 0
    for j in range(0, len(childrens_2)):
      try:
        if childrens_1[i]['type'] == childrens_2[j]['type']:
          for key,value in childrens_2[j].items():
            if key not in childrens_1[i] or value != childrens_1[i][key]:
              diff +=1
            params_num +=1
          params_num,diff = GetParamsCount(childrens_1[i],childrens_2[j],params_num,diff)
        else:
          j+=1
          params_num,diff = GetParamsCount(childrens_1[i],childrens_2[j],params_num,diff)
        i+=1
      except IndexError:
        continue
  return (params_num,diff)

def CompareNodeIDS(doc_1,doc_2):
    for i in range(0, len(doc_1['children'])):
        if len(doc_1['children'][i]['id']) - len(doc_2['children'][i]['id']) >= 2:
            return "First"
        if len(doc_2['children'][i]['id']) - len(doc_1['children'][i]['id']) >= 2:
            return "Second"
    
def GetNeededParametersData(files_difference,params):
  needed_parameters = ["id","backgroundColor","absoluteBoundingBox","absoluteRenderBounds","componentId","overrides","struct","styles","transitionNodeID","name","clipsContent","background","fills","prototypeStartNodeID","flowStartingPoints","componentPropertyDefinitions","style","prototypeDevice","styleOverrideTable","componentProperties","fillOverrideTable","connectorStart","connectorEnd","exposedInstances"]
  row = []
  for parameter in needed_parameters:
      if parameter in files_difference:
          row.append(files_difference[parameter]/params)
      else:
          row.append(0)
  return np.array(row)

def GetMaxClusterSize(label):
  res = 0
  max_count = 0
  for i in range(0,9):
    iterRes =0
    for el in label:
      if el == i:
        iterRes +=1
    if iterRes > res :
      res = iterRes
      max_count = i
  return max_count

def GetPredict(data):
    with open('models/pca_model_1.pickle', 'rb') as f1:
        pca_model_1 = pickle.load(f1)
        data_transformed=pca_model_1.transform(data)
        with open('models/kmean_model_1.pickle', 'rb') as f2:
            kmean_model_1 = pickle.load(f2)
            expected_predict = GetMaxClusterSize(kmean_model_1.labels_)
            pred = kmean_model_1.predict(data_transformed)
            if expected_predict != pred[0]:
                return False
    with open('models/pca_model_2.pickle', 'rb') as f1:
        pca_model_2 = pickle.load(f1)
        data_transformed=pca_model_2.transform(data)
        with open('models/kmean_model_2.pickle', 'rb') as f2:
            kmean_model_2 = pickle.load(f2)
            expected_predict = GetMaxClusterSize(kmean_model_2.labels_)
            pred = kmean_model_2.predict(data_transformed)
            if expected_predict != pred[0]:
                return False
    return True
#3V3WnH4b4yHmtPyAmcoAMg,Daefc5zuc1JMzLzCIU76YQ
def Compare_Files(file_key_1,file_key_2):
    figma_token = "figd_ZeDu4ByR9phQUNRMD88P-X-jrEoxDCUBTQNkWrbJ"
    figma = FigmAPI(figma_token)
    figma_file_1 = figma.Get_File(file_key_1)
    figma_file_2 = figma.Get_File(file_key_2)
    changedParameters = GetChangedParamsCount(figma_file_1,figma_file_2,{})
    params,changed = GetParamsCount(figma_file_1,figma_file_2,0,0)
    data = GetNeededParametersData(changedParameters,params)
    df = pd.DataFrame(data=[data],columns = ["id","backgroundColor","absoluteBoundingBox","absoluteRenderBounds","componentId","overrides","struct","styles","transitionNodeID","name","clipsContent","background","fills","prototypeStartNodeID","flowStartingPoints","componentPropertyDefinitions","style","prototypeDevice","styleOverrideTable","componentProperties","fillOverrideTable","connectorStart","connectorEnd","exposedInstances"])
    with open('data.pickle', 'wb') as f:
        pickle.dump(df, f)
    verdict = GetPredict(df)
    if verdict is True:
        #copy_is = CompareNodeIDS(figma_file_1,figma_file_2)
        return "Result: These layouts are the same"
        #return f"{copy_is} is the copy"
    else:
        return "Result: These layouts are too different"

def CompareLayouts(sender,app_data):
    file_key_1 = dpg.get_value("file_key_1")
    file_key_2 = dpg.get_value("file_key_2")
    res = Compare_Files(file_key_1,file_key_2)
    dpg.add_text(res,parent = "main_window")

# DYJLzGz2haGq2sPZEiZgjg B0dZ6Z4LyrXbsaLxTdH5ok
dpg.create_context() # создаем контекст для запуска приложения
dpg.create_viewport(title='Figma Comparer App', width=1000, height=600,x_pos = 400,y_pos = 150) # создаем приложение
with dpg.window(label="Stock viewer",tag="main_window", width=1920, height=1280): # создаем окно внутри приложения
    dpg.add_text("file_key_1")
    dpg.add_input_text(tag = "file_key_1")
    dpg.add_text("file_key_2")
    dpg.add_input_text(tag = "file_key_2") # добавляем кнопку для открытия таблицы
    dpg.add_button(label="Compare",tag="compare_layouts",callback=CompareLayouts) # добавляем кнопку для добавления пустой строки в таблицу
dpg.setup_dearpygui() # сетап приложения
dpg.set_primary_window("main_window", True)
dpg.show_viewport() # отображаем приложение
dpg.start_dearpygui() # запускаем приложение
dpg.destroy_context() # удаляем данные приложения при закрытии окна