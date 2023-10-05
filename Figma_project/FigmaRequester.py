# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 23:39:10 2023

@author: arsko
"""
import requests
import json

class BadRequestError(Exception):
  def __init__(self, message="Parameters are invalid or malformed. Please check the input formats"):
    self.message = message
    super().__init__(self.message)

class NotFoundError(Exception):
  def __init__(self, message="The requested file or resource was not found."):
    self.message = message
    super().__init__(self.message)

class RateLimitError(Exception):
  def __init__(self, message="In some cases API requests may be throttled or rate limited. Please wait a while before attempting the request again (typically a minute)."):
    self.message = message
    super().__init__(self.message)

class InternalServerError(Exception):
  def __init__(self, status_code, message="This most commonly occurs for very large image render requests, which may time out our server and return a 500. Please reduce the number and size of objects requested."):
    self.message = message
    super().__init__(self.message)
    
class FigmaRequester:
  def Get_Request(url,headers={},params={},data={}):
      response = requests.get(url,headers=headers,params=params,data=data)
      if response.status_code == 200:
        return json.loads(response.text)
      if response.status_code == 400:
        raise BadRequestError()
      if response.status_code == 404:
        raise NotFoundError()
      if response.status_code == 429:
        raise RateLimitError()
      if response.status_code == 500:
        raise InternalServerError()
      
  def Post_Request(url,headers={},params={},data={}):
      response = requests.post(url,headers=headers,params=params,data=data)
      if response.status_code == 200:
        return json.loads(response.text)
      if response.status_code == 400:
        raise BadRequestError
      if response.status_code == 404:
        raise NotFoundError
      if response.status_code == 429:
        raise RateLimitError
      if response.status_code == 500:
        raise InternalServerError