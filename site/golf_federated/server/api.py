# -*- coding: utf-8 -*-
# @Author             : GZH
# @Created Time       : 2022/5/18 17:15
# @Email              : guozh29@mail2.sysu.edu.cn
# @Last Modified By   : GZH
# @Last Modified Time : 2022/10/25 3:35
import zipfile
from flask import Flask, jsonify, abort, make_response, send_from_directory, render_template
from flask import request, Response
import json
import redis
import os
import time
import numpy as np
from golf_federated.server.token import create_token, verify_token
from golf_federated.strategy.encryption.myRSA import CreateRSAKeys
from golf_federated.utils.log import loggerhear
from golf_federated.utils.model import load_model_file, get_model_parameter

# Initialize flask app and basic variables
from golf_federated.utils.zip import read_zip

app = Flask(__name__)
MY_URL = '/api/'
TOKEN = 'token'
#
# """General API"""
#
#
# @app.errorhandler(404)
# def not_found(*args):
#     """
#     This API processing the 404 error
#     :return: The information in JSON form including " 'error':'Not found') "
#     """
#     return make_response(jsonify({'error': 'Not found'}), 404)
#
#
# """Page Jump API"""
#
#
# @app.route('/')
# def hello_world():
#     return "hello world"
#
#
# @app.route('/home/', methods=['GET', 'POST'])
# def Home():
#     """
#     This API can jump to the home page
#     :return:
#     """
#     tem_dic = request.args.to_dict()
#     username = tem_dic['username']
#     return render_template('homepage.html', name=username, token=TOKEN)
#
#
# @app.route('/regist/', methods=['GET', 'POST'])
# def Regist():
#     """
#     This API can jump to the regist page
#     :return:
#     """
#     return render_template('regist.html')
#
#
# @app.route('/login/', methods=['GET', 'POST'])
# def Login():
#     """
#     This API can jump to the login page
#     :return:
#     """
#     return render_template('login.html')
#
#
# @app.route('/fp/', methods=['GET', 'POST'])
# def Fp():
#     """
#     This API can jump to the retrieve password page
#     :return:
#     """
#     return render_template('forgetpassword.html')
#
# # ----------------------Add these new homepage api--------------------------------
# @app.route('/home/', methods=['GET', 'POST'])
# def Home():
#     return render_template('homepage_2.html', name=Username, token=TOKEN)
#
#
# @app.route('/homepage_1/', methods=['GET', 'POST'])
# def Homepage_1():
#     return render_template('homepage_1.html', name=Username, token=TOKEN)
#
#
# @app.route('/homepage_2/', methods=['GET', 'POST'])
# def Homepage_2():
#     return render_template('homepage_2.html', name=Username, token=TOKEN)
#
#
# @app.route('/homepage_3/', methods=['GET', 'POST'])
# def Homepage_3():
#     return render_template('homepage_3.html', name=Username, token=TOKEN)
#
#
# @app.route('/homepage_4/', methods=['GET', 'POST'])
# def Homepage_4():
#     return render_template('homepage_4.html', name=Username, token=TOKEN)
#
#
# @app.route('/homepage_5/', methods=['GET', 'POST'])
# def Homepage_5():
#     return render_template('homepage_5.html', name=Username, token=TOKEN)
#
#
# @app.route('/homepage_clientinfo/', methods=['GET', 'POST'])
# def Homepage_client():
#     return render_template('homepage_clientinfo.html', name=Username, token=TOKEN)
#
#
# # -----------------Delete this api-----------------------
# # @app.route('/tasklist/', methods=['GET', 'POST'])
# # def tasklist_test():
# #     """
# #     This API can jump to the task list page
# #     :return:
# #     """
# #     tem_dic = request.args.to_dict()
# #     username = tem_dic['username']
# #     return render_template('tasklist.html', name=username, token=TOKEN)
#
#
# """Login and Registration API"""
#
#
# # @app.route(MY_URL + 'login/', methods=['POST'])
# # def login():
# #     """
# #     This API provide a interface for clients to login.
# #     It can account authentication based on the database,
# #     convert the output to JSON for a response.
#
# #     The url refers to:
# #         http://127.0.0.1:5000/api/login
#
# #     :param:
# #         username
# #         password
# #     :return:
# #         The information in JSON form including 'code','message' and 'token'
# #         (token is prepared for identity verification)
# #     """
# #     data = request.get_data()
# #     data = json.loads(data.decode("utf-8"))
# #     try:
# #         username = data.get('username')
# #         password = data.get('password')
# #     except Exception:
# #         abort(404)
# #     dbhere = app.config['Database']
# #     TorF = dbhere.table_match(
# #         tablename='USER_INFO',
# #         query_fields=['username'],
# #         query_contents=[username],
# #         match_fields=['password'],
# #         match_contents=[password]
# #     )
# #     if TorF:
# #         token = create_token(username)
# #         global TOKEN
# #         TOKEN = token
# #         data = {
# #             "code": 201,
# #             "message": "Successful",
# #             "token": token
# #         }
# #         ret_json = json.dumps(data)
# #     else:
# #         data = {
# #             "code": 422,
# #             "message": "Failed"
# #         }
# #         ret_json = json.dumps(data)
#
# #     return ret_json
#
#
# @app.route(MY_URL + 'login/', methods=['POST'])
# def login():
#     data = request.get_data()
#     data = json.loads(data.decode("utf-8"))
#     try:
#         global Username
#         Username = data.get('username')
#         password = data.get('password')
#     except Exception:
#         abort(404)
#
#     dbhere = app.config['Database']
#     TorF = dbhere.table_match(
#         tablename='USER_INFO',
#         query_fields=['username'],
#         query_contents=[username],
#         match_fields=['password'],
#         match_contents=[password]
#     )
#     if TorF:
#         token = create_token(Username)
#         global TOKEN
#         TOKEN = token
#         data = {
#             "code": 201,
#             "message": "Success",
#             "token": token
#         }
#         ret_json = json.dumps(data)
#     elif not TorF:
#         data = {
#             "code": 422,
#             "message": "False"
#         }
#         ret_json = json.dumps(data)
#
#     return ret_json
#
#
# @app.route(MY_URL + 'regist/', methods=['POST'])
# def regist():
#     """
#     This API provide a interface for clients to regist.
#     It can account authentication based on the database,
#     convert the output to JSON for a response.
#
#     The url refers to:
#         http://127.0.0.1:5000/api/login
#
#     :param:
#         username
#         password
#     :return:
#         The information in JSON form including 'code','message' and 'token'
#         (token is prepared for identity verification)
#     """
#     data = request.get_data()
#     data = json.loads(data.decode("utf-8"))
#
#     try:
#         username = data.get('username')
#         password = data.get('password')
#     except Exception:
#         abort(404)
#     dbhere = app.config['Database']
#     TorF = dbhere.table_insert(
#         tablename='USER_INFO',
#         fields=['username', 'password'],
#         contents=[username, password]
#     )
#     if TorF:
#         token = create_token(username)
#         global TOKEN
#         TOKEN = token
#
#         data = {
#             "code": 201,
#             "message": "Successful",
#             "token": token
#         }
#     else:
#         data = {
#             "code": 422,
#             "message": "Failed"
#         }
#
#     ret_json = json.dumps(data)
#     return ret_json
#
#
# """Request and Publish API"""
#
#
# @app.route(MY_URL + 'home_source/', methods=['GET', 'POST'])
# def home_source():
#     """
#     This API porvide a interface for Filter to verify token and it can
#     query the USER_INFO table to return the username for a response.
#
#     The url refers to:
#         http://127.0.0.1:5000/api/home_source
#
#     :param:
#         token
#         username
#     :return:
#         The information in JSON form including
#                 'code', 'message' and 'username'.
#     """
#     data = request.get_data()
#     data = json.loads(data.decode("utf-8"))
#     token = data.get('token')
#
#     try:
#         data = verify_token(token)
#     except Exception:
#         abort(404)
#     dbhere = app.config['Database']
#     TorF = dbhere.table_find(
#         tablename='USER_INFO',
#         fields=['username'],
#         contents=[data['username']]
#     )['flag']
#
#     if TorF:
#         username = data["username"]
#         data = {
#             "code": 201,
#             "message": "Successful",
#             "username": username
#         }
#     else:
#         data = {
#             "code": 401,
#             "message": "Failed"
#         }
#
#     ret_json = json.dumps(data)
#     return ret_json
#
#
# # @app.route(MY_URL + 'service_visualize/', methods=['GET', 'POST'])
# # def service_visualize():
# #     """
# #     This API porvide a interface for Filter to verify token and it can
# #     query the SERVICE_INFO table to show the service details.
#
# #     The url refers to:
# #         http://127.0.0.1:5000/api/service_visualize
#
# #     :param:
# #         token
# #         username
# #     :return:
# #         The information about the queried service details including
# #                 'servicename', 'servicebrief' and 'servicedetail'.
# #     """
# #     data = request.get_data()
# #     data = json.loads(data.decode("utf-8"))
# #     token = data.get('token')
#
# #     try:
# #         data = verify_token(token)
# #     except Exception:
# #         abort(404)
# #     dbhere = app.config['Database']
# #     TorF = dbhere.table_find(
# #         tablename='USER_INFO',
# #         fields=['username'],
# #         contents=[data['username']]
# #     )['flag']
#
# #     if TorF:
# #         service_info = dbhere.table_get(tablename='SERVICE_INFO')
# #         length = len(service_info)
#
# #         data = {
# #             "servicename": service_info[length - 1][0],
# #             "servicebrief": service_info[length - 1][1],
# #             "servicedetail": service_info[length - 1][2],
# #             "next": "0",
# #             "nextdata": "null"
# #         }
# #         for i in range(length - 1):
# #             data = {
# #                 "servicename": service_info[length - i - 2][0],
# #                 "servicebrief": service_info[length - i - 2][1],
# #                 "servicedetail": service_info[length - i - 2][2],
# #                 "next": "1",
# #                 "nextdata": data
# #             }
# #         data = {
# #             "code": 200,
# #             "message": "Successful",
# #             "data": data
# #         }
# #     elif not TorF:
# #         data = {
# #             "code": 400,
# #             "message": "Failed"
# #         }
#
# #     ret_json = json.dumps(data)
# #     return ret_json
#
#
# @app.route(MY_URL + 'service_visualize/', methods=['GET','POST'])
# def service_visualize():
#     data = request.get_data()
#     data = json.loads(data.decode("utf-8"))
#     token = data.get('token')
#
#     try:
#         data = verify_token(token)
#     except Exception:
#         abort(404)
#     dbhere = app.config['Database']
#     TorF = dbhere.table_find(
#         tablename='USER_INFO',
#         fields=['username'],
#         contents=[data['username']]
#     )['flag']
#
#     if TorF:
#         service_info = dbhere.table_get(tablename='SERVICE_INFO')
#         length = len(service_info)
#
#         def get_data(servicename: str, servicebrief: str, servicedetail: str, next: str, nextdata):
#             return {
#                 "servicename": servicename,
#                 "servicebrief": servicebrief,
#                 "servicedetail": servicedetail,
#                 "next": next,
#                 "nextdata": nextdata
#             }
#
#         data = get_data(service_info[length - 1][0], service_info[length - 1][1], service_info[length - 1][2], "0",
#                         "null")
#         for i in range(length - 1):
#             data = get_data(service_info[length - i - 2][0], service_info[length - i - 2][1],
#                             service_info[length - i - 2][2], "1", data)
#
#         data = {
#             "code": 200,
#             "message": "Successful",
#             "data": data
#         }
#     elif not TorF:
#         data = {
#             "code": 400,
#             "message": "Failed"
#         }
#
#
#     ret_json = json.dumps(data)
#     return ret_json
#
#
# @app.route(MY_URL + 'service_request/', methods=['GET', 'POST'])
# def service_request():
#     """
#     This API provide a interface for clients to request service.
#     It can account authentication based on the database.
#     Based on SSE(Streaming SIMD Extensions) scheme to
#     publish information in the channel named 'event',
#     convert the status information to JSON for a response.
#     The url refers to:
#         http://127.0.0.1:5000/api/service_request
#
#     :param:
#         token
#         servicename
#     :return:
#         Publish information in the channel named 'event'
#         The information in JSON form including 'code','message'
#     """
#     data = request.get_data()
#     data = json.loads(data.decode("utf-8"))
#
#     try:
#         token = data.get('token')
#         data = verify_token(token)
#         servicename = data.get('servicename')
#     except Exception:
#         abort(404)
#     dbhere = app.config['Database']
#
#     TorF1 = dbhere.table_find(
#         tablename='USER_INFO',
#         fields=['username'],
#         contents=[data['username']]
#     )['flag']
#
#     TorF2 = dbhere.table_find(
#         tablename='SERVICE_INFO',
#         fields=['servicename'],
#         contents=[servicename]
#     )['flag']
#
#     TorF = TorF1 & TorF2
#
#     if TorF:
#         data = {
#             "code": 200,
#             "message": "Publish Successful",
#         }
#     else:
#         data = {
#             "code": 400,
#             "message": "Publish Failed"
#         }
#     # red = redis.StrictRedis(
#     #     host=app.config['REDIS_HOST'],
#     #     port=app.config['REDIS_PORT'],
#     #     db=app.config['REDIS_DB']
#     # )
#     red = redis.StrictRedis(host='localhost', port=6379, db=6)
#     red.publish('event', u'[Code:201 Message:Publish Begin]')
#     time.sleep(10)
#     red.publish('event', u'[Code:202 Message:Successful] [Userid]:%s [Event]:%s [Data]:%s [Retry]:%s' % (
#         "id", 'event', "None", 'None'))
#
#     ret_json = json.dumps(data)
#     return ret_json
#
#
# @app.route(MY_URL + 'sse_message/', methods=['GET', 'POST'])
# def sse_message():
#     """
#     This API use the function event_stream()
#     to get the real-time data in channel named 'event',
#     and Return the real-time data to the client with the
#     mimetype = "text/event-stream"
#
#     The url refers to:
#         http://127.0.0.1:5000/api/sse_message/
#
#     :param: None
#     :return:
#         real-time data in channel named 'event'
#         Form -> JSON
#     """
#     data = event_stream()
#     # print(data)
#     return Response(data, mimetype="text/event-stream")
#
#
# # @app.route(MY_URL + '/model_download/<filename>', methods=['POST', 'GET'])
# # def model_download(filename):
# #     """
# #     This API provide a interface for clients to client models.
# #     It can account authentication based on the database with token，
# #     get the model corresponding to the parameters contain username
# #     and servicename.Return the model with the from of file stream
# #
# #     The url refers to:
# #         http://127.0.0.1:5000/api/sse_message/
# #
# #     :param:
# #         token
# #         servicename
# #         username
# #     :return:
# #         real-time data in channel named 'event'
# #         Form -> JSON
# #     """
# #     data = request.get_data()
# #     data = json.loads(data.decode("utf-8"))
# #     token = data.get('token')
# #     servicename = data.get('servicename')
# #
# #     data = verify_token(token)
# #
# #     dbhere = app.config['Database']
# #     TorF1 = dbhere.table_find(
# #         tablename='USER_INFO',
# #         fields=['username'],
# #         contents=[data['username']]
# #     )['flag']
# #     TorF2 = dbhere.table_find(
# #         tablename='SERVICE_INFO',
# #         fields=['servicename'],
# #         contents=[servicename]
# #     )['flag']
# #
# #     TorF = TorF1 & TorF2
# #
# #     if TorF:
# #         DOWNLOAD_PATH = os.path.join(os.path.dirname(__file__), 'client')
# #         DOWNLOAD_PATH = os.path.join(DOWNLOAD_PATH, filename)
# #         data = {
# #             "code": 200,
# #             "message": "Successful",
# #         }
# #
# #         def send_chunk():
# #             with open(DOWNLOAD_PATH, 'rb') as target_file:
# #                 while True:
# #                     chunk = target_file.read(2 * 1024 * 1024)
# #                     if not chunk:
# #                         break
# #                     yield chunk
# #     else:
# #         data = {
# #             "code": 200,
# #             "message": "Failed"
# #         }
# #
# #     ret_json = json.dumps(data)
# #     return Response(send_chunk(), content_type='application/octet-stream')
#
#
# """Strategy Set and Training transfer API """
#
#
# @app.route(MY_URL + 'strategy_set/', methods=['GET', 'POST'])
# def strategy_set():
#     """
#     This API provide a interface for clients to set the parameters of strategy.
#     It can account authentication based on the database with token，set the
#     strategy and update the GLOBAL_MODEL_INFO table with the contents in strategies.
#     Publish the new model in the channel 'event',and return the status.
#
#     The url refers to:
#         http://127.0.0.1:5000/api/strategy_set/
#
#     :param:
#         token
#         servicename
#         'strategies',dictionary contain global model's informatin
#     :return:
#         the new model in channel named 'event'
#         the status with the form JSON
#     """
#     data = request.get_data()
#     data = json.loads(data.decode("utf-8"))
#
#     token = data.get('token')
#     servicename = data.get('servicename')
#     strategies = data.get('strategies')
#
#     try:
#         data = verify_token(token)
#     except Exception:
#         abort(404)
#
#     dbhere = app.config['Database']
#     TorF = dbhere.table_find(
#         tablename='USER_INFO',
#         fields=['username'],
#         contents=[data['username']]
#     )['flag']
#
#     if TorF:
#         # json生成
#         data = {
#             "code": 200,
#             "message": "Token Verify = Successful",
#         }
#
#         dbhere.table_update(
#             tablename='GLOBAL_MODEL_INFO',
#             query_fields=['servicename'],
#             query_contents=[servicename],
#             update_fields=['modelversion', 'maxround', 'aggregationtiming', 'epsilon', 'batchsize', 'lr'],
#             update_contents=[0, strategies['maxround'], strategies['aggregationtiming'],
#                              strategies['epsilon'], strategies['batchsize'], strategies['lr']]
#         )
#         # red = redis.StrictRedis(
#         #     host=app.config['REDIS_HOST'],
#         #     port=app.config['REDIS_PORT'],
#         #     db=app.config['REDIS_DB']
#         # )
#         red = redis.StrictRedis(host='localhost', port=6379, db=6)
#         red.publish('event', u'[Code:200 Message:Publish Begin]')
#         time.sleep(10)
#         red.publish('event', u'[Code:200 Message:Successful] [Userid]:%s [Event]:%s [Data]:%s [Retry]:%s' % (
#             "id", 'event', "None", 'None'))
#
#     else:
#         data = {
#             "code": 400,
#             "message": "Token Verify = Failed"
#         }
#
#     ret_json = json.dumps(data)
#     return ret_json
#
#
# # @app.route(MY_URL + 'task_visualize/', methods=['GET', 'POST'])
# # def task_visualize():
# #     """
# #     This API porvide a interface for Filter to verify token and it can
# #     query the SERVICE_INFO table and GLOBAL_MODEL_INFO table to show the task details.
# #     The url refers to:
# #         http://127.0.0.1:5000/api/task_visualize
#
# #     :param:
# #         token
# #         username
# #     :return:
# #         The information about the queried task details including
# #                 'servicename', 'servicebrief', 'servicedetail' and 'strategies'.
# #     """
# #     data = request.get_data()
# #     data = json.loads(data.decode("utf-8"))
# #     token = data.get('token')
#
# #     try:
# #         data = verify_token(token)
# #     except Exception:
# #         abort(404)
#
# #     dbhere = app.config['Database']
# #     TorF = dbhere.table_find(
# #         tablename='USER_INFO',
# #         fields=['username'],
# #         contents=[data['username']]
# #     )['flag']
#
# #     if TorF:
# #         service_info = dbhere.table_get(tablename='SERVICE_INFO')
# #         length = len(service_info)
#
# #         global_model_info = dbhere.table_find(
# #             tablename='GLOBAL_MODEL_INFO',
# #             fields=['servicename'],
# #             contents=[service_info[length - 1][0]]
# #         )['data']
#
# #         data = {
# #             "servicename": service_info[length - 1][0],
# #             "servicebrief": service_info[length - 1][1],
# #             "servicedetail": service_info[length - 1][2],
# #             "strategies": {
# #                 "maxround": global_model_info[0][2],
# #                 "aggregationtiming": global_model_info[0][3],
# #                 "epsilon": global_model_info[0][4],
# #                 "batchsize": global_model_info[0][5],
# #                 "lr": global_model_info[0][6]
# #             },
# #             "next": "0",
# #             "nextdata": "null"
# #         }
# #         for i in range(length - 1):
# #             global_model_info = dbhere.table_find(
# #                 tablename='GLOBAL_MODEL_INFO',
# #                 fields=['servicename'],
# #                 contents=[service_info[length - i - 2][0]]
# #             )['data']
#
# #             data = {
# #                 "servicename": service_info[length - i - 2][0],
# #                 "servicebrief": service_info[length - i - 2][1],
# #                 "servicedetail": service_info[length - i - 2][2],
# #                 "strategies": {
# #                     "maxround": global_model_info[0][2],
# #                     "aggregationtiming": global_model_info[0][3],
# #                     "epsilon": global_model_info[0][4],
# #                     "batchsize": global_model_info[0][5],
# #                     "lr": global_model_info[0][6]
# #                 },
# #                 "next": "1",
# #                 "nextdata": data
# #             }
#
# #         data = {
# #             "code": 200,
# #             "message": "Successful",
# #             "data": data
# #         }
# #     elif TorF == False:
# #         data = {
# #             "code": 200,
# #             "message": "Failed"
# #         }
#
# #     ret_json = json.dumps(data)
# #     return ret_json
#
#
# @app.route(MY_URL + 'task_visualize/', methods=['GET', 'POST'])
# def task_visualize():
#     data = request.get_data()
#     data = json.loads(data.decode("utf-8"))
#     token = data.get('token')
#     id = int(data.get('id'))
#
#     try:
#         data = verify_token(token)
#     except Exception:
#         abort(404)
#
#     dbhere = app.config['Database']
#     TorF = dbhere.table_find(
#         tablename='USER_INFO',
#         fields=['username'],
#         contents=[data['username']]
#     )['flag']
#
#     if TorF:
#         service_info = mysql_sql.SERVICE_INFO_get()
#
#         global_model_info = dbhere.table_find(
#             tablename='GLOBAL_MODEL_INFO',
#             fields=['servicename'],
#             contents=[service_info[id - 1][0]]
#         )['data']
#
#         data = {
#             "servicename": service_info[id - 1][0],
#             "servicebrief": service_info[id - 1][1],
#             "servicedetail": service_info[id - 1][2],
#             "strategies": {
#                 "maxround": global_model_info[0][2],
#                 "aggregationtiming": global_model_info[0][3],
#                 "epsilon": global_model_info[0][4],
#                 "batchsize": global_model_info[0][5],
#                 "lr": global_model_info[0][6]
#             },
#             "next": "0",
#             "nextdata": "null"
#         }
#
#         data = {
#             "code": 200,
#             "message": "Successful",
#             "data": data
#         }
#     elif not TorF:
#         data = {
#             "code": 400,
#             "message": "Failed"
#         }
#
#     ret_json = json.dumps(data)
#     return ret_json
#
#
# """Information List API"""
#
#
# @app.route(MY_URL + 'info_visualize/', methods=['GET', 'POST'])
# def info_visualize():
#     """
#     This API provide a interface for clients to visualize the info.
#     （Jump to another web page）
#     The url refers to:
#         http://127.0.0.1:5000/api/info_visualize/
#
#     :param:
#         token
#         username
#     :return:
#         the status with the form JSON
#     """
#     data = request.get_data()
#     data = json.loads(data.decode("utf-8"))
#
#     try:
#         token = data.get('token')
#         data = verify_token(token)
#     except Exception:
#         abort(404)
#
#     dbhere = app.config['Database']
#     TorF = dbhere.table_find(
#         tablename='USER_INFO',
#         fields=['username'],
#         contents=[data['username']]
#     )['flag']
#
#     if TorF:
#         data = {
#             "code": 200,
#             "message": "Successful",
#         }
#     else:
#         data = {
#             "code": 400,
#             "message": "Failed"
#         }
#
#     ret_json = json.dumps(data)
#     return ret_json
#
#
# @app.route(MY_URL + 'userpage_source/', methods=['GET', 'POST'])
# def userpage_source():
#     """
#     This API provide a interface for clients to visualize the page of users' source.
#     （Jump to another web page）
#     The url refers to:
#         http://127.0.0.1:5000/api/userpage_source/
#
#     :param:
#         token
#         username
#     :return:
#         the status with the form JSON
#     """
#     data = request.get_data()
#     data = json.loads(data.decode("utf-8"))
#
#     try:
#         token = data.get('token')
#         data = verify_token(token)
#     except Exception:
#         abort(404)
#
#     dbhere = app.config['Database']
#     TorF = dbhere.table_find(
#         tablename='USER_INFO',
#         fields=['username'],
#         contents=[data['username']]
#     )['flag']
#
#     if TorF:
#         data = {
#             "code": 200,
#             "message": "Successful",
#             "username": str(data['username'])
#         }
#     else:
#         data = {
#             "code": 400,
#             "message": "Failed"
#         }
#
#     ret_json = json.dumps(data)
#     return ret_json
#
#
# @app.route(MY_URL + 'pubkey_send/', methods=['GET', 'POST'])
# def pubkey_send():
#     """
#     This API aim to send a RSA public key to the client.
#     When method is 'GET', the url refers to :
#         http://127.0.0.1:5000/api/pubkey_send?filename=keys/my_rsa_public.pem
#     The client can receive the public key in the form of text information.
#     When method is 'POST', the url refers to :
#         http://127.0.0.1:5000/api/pubkey_send
#     The client can client the public key to the directory named 'pubkey'.
#     :return:
#         When method is 'GET', return the text that public key shows.
#         When method is 'POST', return the message in
#             json form that show whether the public ket is downloaded successfully.
#     """
#     CreateRSAKeys()
#     if request.method == 'GET':
#         full_file_name = request.args.get('filename')
#         full_file_name_list = full_file_name.split('/')
#         file_name = full_file_name_list[-1]
#         file_path = full_file_name.replace('/%s' % file_name, '')
#         # show the content of pubkey
#         response = make_response(send_from_directory(file_path, file_name, as_attachment=True))
#         response.headers["Content-Disposition"] = "attachment; filename={}".format(
#             file_path.encode().decode('latin-1'))
#         return send_from_directory(file_path, file_name, as_attachment=True)
#
#     if request.method == 'POST':
#
#         try:
#             file_dir = os.path.join(os.path.dirname(__file__), 'pubkey')
#             public_key = request.files['filename']
#             file_path = os.path.join(file_dir, public_key.filename)
#             public_key.save(file_path)
#             data = {
#                 "message": "Receive and client public key successfully!"
#             }
#             ret_json = json.dumps(data)
#             return ret_json
#         except:
#             data = {
#                 "message": "Fail to receive and client public key! "
#             }
#             ret_json = json.dumps(data)
#             return ret_json
#
# # ----------------------Add these new api--------------------------------
# """部署任务功能"""
# @app.route(MY_URL + 'upload_file/', methods=['GET','POST'])
# def upload_file():
#
#     data = request.get_data()
#     data = json.loads(data.decode("utf-8"))
#     file_info = data.get('file_info')
#
#     # 获取 token servicename 并校验 token
#     try:
#         token = data.get('token')
#         data = verify_token(token)
#     except Exception:
#         abort(404)
#
#     # 检查匹配
#     TorF = mysql_sql.USER_INFO_find(data['username'])['flag']
#     if TorF:
#         mysql_sql.UPLOADED_FILE_INFO_insert(file_info['filename'], file_info['time'])
#         # json生成
#         data = {
#             "code": 200,
#             "message": "Success"
#         }
#     elif not TorF:
#         data = {
#             "code": 400,
#             "message": "False"
#         }
#
#     ret_json = json.dumps(data)
#     return ret_json
#
# @app.route(MY_URL + 'uploadfile_info/', methods=['GET','POST'])
# def uploadfile_info():
#
#     data = request.get_data()
#     data = json.loads(data.decode("utf-8"))
#
#     # 获取 token servicename 并校验 token
#     try:
#         token = data.get('token')
#         data = verify_token(token)
#     except Exception:
#         abort(404)
#
#     # 检查匹配
#     TorF = mysql_sql.USER_INFO_find(data['username'])['flag']
#     if TorF:
#         info_data = mysql_sql.UPLOADED_FILE_INFO_get()
#         # json生成
#         data = {
#             "code": 200,
#             "message": "Success",
#             "data": info_data
#         }
#     elif not TorF:
#         data = {
#             "code": 400,
#             "message": "False"
#         }
#
#     ret_json = json.dumps(data)
#     return ret_json
#
#
# @app.route(MY_URL + 'create_file/', methods=['GET','POST'])
# def create_file():
#
#     data = request.get_data()
#     data = json.loads(data.decode("utf-8"))
#     file_info = data.get('file_info')
#
#     # 获取 token servicename 并校验 token
#     try:
#         token = data.get('token')
#         data = verify_token(token)
#     except Exception:
#         abort(404)
#
#     # 检查匹配
#     TorF = mysql_sql.USER_INFO_find(data['username'])['flag']
#     if TorF:
#         mysql_sql.CREATED_FILE_INFO_insert(file_info['filename'], file_info['time'])
#         # json生成
#         data = {
#             "code": 200,
#             "message": "Success"
#         }
#     elif not TorF:
#         data = {
#             "code": 400,
#             "message": "False"
#         }
#
#     ret_json = json.dumps(data)
#     return ret_json
#
#
# @app.route(MY_URL + 'createfile_info/', methods=['GET','POST'])
# def createfile_info():
#
#     data = request.get_data()
#     data = json.loads(data.decode("utf-8"))
#
#     # 获取 token servicename 并校验 token
#     try:
#         token = data.get('token')
#         data = verify_token(token)
#     except Exception:
#         abort(404)
#
#     # 检查匹配
#     TorF = mysql_sql.USER_INFO_find(data['username'])['flag']
#     if TorF:
#         info_data = mysql_sql.CREATED_FILE_INFO_get()
#         # json生成
#         data = {
#             "code": 200,
#             "message": "Success",
#             "data": info_data
#         }
#     elif not TorF:
#         data = {
#             "code": 400,
#             "message": "False"
#         }
#
#     ret_json = json.dumps(data)
#     return ret_json
#
#
#
# @app.route(MY_URL + 'logout/', methods=['GET','POST'])
# def logout():
#     data = request.get_data()
#     data = json.loads(data.decode("utf-8"))
#
#     # 获取 token servicename 并校验 token
#     try:
#         token = data.get('token')
#         data = verify_token(token)
#     except Exception:
#         abort(404)
#
#     # 检查匹配
#     TorF = mysql_sql.USER_INFO_find(data['username'])['flag']
#     if TorF:
#
#         # 清空 UPDATED_FILE_INFO 和 CREATED_FILE_INFO 表
#         mysql_sql.ALL_TABLE_CLEAR()
#         # json生成
#         data = {
#             "code": 200,
#             "message": "Success"
#         }
#     elif not TorF:
#         data = {
#             "code": 400,
#             "message": "False"
#         }
#
#     ret_json = json.dumps(data)
#     return ret_json


##############################################################


""" 接收client发送的模型参数 """


@app.route(MY_URL + '/ReceiveLocalModel', methods=['POST', 'GET'])
def receive_local_model():
    data = request.get_data()
    # server_id = data['server_id']
    # task_name = data['task_name']
    server_id = 'server1'
    task_name = 'MultiDeviceTest'
    serverhere = app.config['SERVER_ID_' + server_id + '_' + task_name]

    global_update_time = serverhere.aggregate_time
    if global_update_time is not None and time.time() - global_update_time < 1:
        loggerhear.log("Server Info  ", "%s Gives Up a Model!" % server_id)
        return 'Continue'
    data = request.get_data()
    # aggregation_data = data['aggregation_data']
    aggregation_data = data
    version_latest = serverhere.version_latest

    # 接收传过来的参数并解压出模型参数文件（.h5/.pt/.pth/.pkl）
    binfile_last = open('./server/return.zip', 'wb')
    binfile_last.write(aggregation_data)
    binfile_last.close()
    serverhere.currentround_cc += len(read_zip('./server/return.zip'))
    # 过度解压
    fz = zipfile.ZipFile('./server/return.zip', 'r')
    for file in fz.namelist():
        fz.extract(file, 'server')
        if '_dict.npy' in file:
            info_dict = np.load('./server/' + file, allow_pickle=True).item()
        else:
            model_name = file
    fz.close()
    model_library = info_dict['model_library']
    client_model = load_model_file(filepath='./server/' + model_name, library=model_library)
    client_w = get_model_parameter(model=client_model, library=model_library)
    index = serverhere.receive_and_judge(info_dict=info_dict, client_w=client_w)
    """ 判断是否需要全局更新 """
    if index == 'Update':
        # red = redis.StrictRedis(
        #     host=app.config['REDIS_HOST'],
        #     port=app.config['REDIS_PORT'],
        #     db=app.config['REDIS_DB']
        # )
        red = redis.StrictRedis(host='localhost', port=6379, db=6)
        red.publish('server', u'Update')
    elif index == 'Stop':
        # red = redis.StrictRedis(
        #     host=app.config['REDIS_HOST'],
        #     port=app.config['REDIS_PORT'],
        #     db=app.config['REDIS_DB']
        # )
        red = redis.StrictRedis(host='localhost', port=6379, db=6)
        red.publish('server', u'Stop')
    elif index == 'Wait':
        # red = redis.StrictRedis(
        #     host=app.config['REDIS_HOST'],
        #     port=app.config['REDIS_PORT'],
        #     db=app.config['REDIS_DB']
        # )
        red = redis.StrictRedis(host='localhost', port=6379, db=6)
        red.publish('server', u'Wait')
    elif index == 'Continue':
        # red = redis.StrictRedis(
        #     host=app.config['REDIS_HOST'],
        #     port=app.config['REDIS_PORT'],
        #     db=app.config['REDIS_DB']
        # )
        red = redis.StrictRedis(host='localhost', port=6379, db=6)
        red.publish('server', u'Continue')
    return index


""" sse监听接口 """


@app.route(MY_URL + '/stream')
def stream():
    return Response(server_stream(), mimetype="text/event-stream")


# @app.route(MY_URL + '/startnewtask', methods=['POST', 'GET'])
# def start_new_task():
#     index = True
#     try:
#         data = request.get_data()
#         server_id = data.server_id
#         task_name = data.task_name
#         app.config['SERVER_ID_' + server_id + '_' + task_name] = data
#     except:
#         index = False
#     return index


""" 模型下载请求接口 """


@app.route(MY_URL + "/model_download/<filename>", methods=['POST', 'GET'])
def model_download(filename):
    # 存放模型在当前文件夹下
    DOWNLOAD_PATH = './model/' + filename
    server_id = 'server1'
    task_name = 'MultiDeviceTest'
    serverhere = app.config['SERVER_ID_' + server_id + '_' + task_name]
    serverhere.currentround_cc += os.stat(DOWNLOAD_PATH).st_size

    # print(DOWNLOAD_PATH)
    # 流式读取

    def send_chunk():
        with open(DOWNLOAD_PATH, 'rb') as target_file:
            while True:
                chunk = target_file.read(2 * 1024 * 1024)  # 每次读取2mb大小
                if not chunk:
                    break
                yield chunk

    return Response(send_chunk(), content_type='application/octet-stream')


@app.route(MY_URL + "/image_download/<filename>", methods=['POST', 'GET'])
def image_download(filename):
    # 存放模型在当前文件夹下
    DOWNLOAD_PATH = './docker/' + filename

    # print(DOWNLOAD_PATH)
    # 流式读取

    def send_chunk():
        with open(DOWNLOAD_PATH, 'rb') as target_file:
            while True:
                chunk = target_file.read(2 * 1024 * 1024)  # 每次读取2mb大小
                if not chunk:
                    break
                yield chunk

    return Response(send_chunk(), content_type='application/octet-stream')


def server_stream():
    # red = redis.StrictRedis(
    #     host=app.config['REDIS_HOST'],
    #     port=app.config['REDIS_PORT'],
    #     db=app.config['REDIS_DB']
    # )
    red = redis.StrictRedis(host='localhost', port=6379, db=6)
    pubsub = red.pubsub()
    pubsub.subscribe('server')
    for message in pubsub.listen():
        '''
        if message['data'] == 1:
            pass
        else:
            print(message)
            print(type(message['data']))
            '''
        yield 'data: %s\n\n' % message['data']


def event_stream():
    """
    This function serving funciton "def sse_message()"
    It can provide the real-time data in channel named 'event'

    :param: None
    :return:
        the real-time data in channel named 'event'
    """
    # red = redis.StrictRedis(
    #     host=app.config['REDIS_HOST'],
    #     port=app.config['REDIS_PORT'],
    #     db=app.config['REDIS_DB']
    # )
    server_id = 'server1'
    task_name = 'MultiDeviceTest'
    serverhere = app.config['SERVER_ID_' + server_id + '_' + task_name]
    red = redis.StrictRedis(host=serverhere.url, port=6379, db=6)
    pubsub = red.pubsub()
    pubsub.subscribe('event')
    for message in pubsub.listen():
        yield 'data: %s\n\n' % message['data']


def add_config(title, content):
    app.config[title] = content
    print()

