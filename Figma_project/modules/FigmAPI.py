# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 23:42:13 2023

@author: arsko
"""
from FigmaRequester import FigmaRequester

class FigmAPI:
    def TryToken(self): #Проверка актуальности токена
        url = "https://api.figma.com/v1/me"
        return FigmaRequester.Get_Request(url,headers=self.headers)
        
    def __init__(self, token, user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"): #Конструктор класса
        self.headers = {"user-agent": user_agent,
                        "X-FIGMA-TOKEN":token
                        }
        
    def Get_File(self,file_key,version={},ids={},depth={},geometry={},plugin_data={},branch_data={}): #Получение структуры файла (дерева)
        url = "https://api.figma.com/v1/files/"+file_key
        params = {
            "version" :version,
            "ids":ids,
            "depth":depth,
            "geometry":geometry,
            "plugin_data":plugin_data,
            "branch_data":branch_data
        }
        return FigmaRequester.Get_Request(url,headers=self.headers,params=params)['document']
    
    def Get_FileNodes(self,file_key,ids,depth={},geometry={},version={},plugin_data={}): #Получение нод файла
        url = "https://api.figma.com/v1/files/"+file_key+"/nodes"
        params = {
            "version" :version,
            "ids":ids,
            "depth":depth,
            "geometry":geometry,
            "plugin_data":plugin_data
        }
        return FigmaRequester.Get_Request(url,headers=self.headers,params=params)
    
    def Get_Image(self,file_key,ids,version={},scale={},formatt={},use_absolute_bounds={}):
        url = "https://api.figma.com/v1/images/"+file_key
        params = {
            "version" :version,
            "ids":ids,
            "scale":scale,
            "format":formatt,
            "use_absolute_bounds":use_absolute_bounds
        }
        return FigmaRequester.Get_Request(url,headers=self.headers,params=params)