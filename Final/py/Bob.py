"""****************************************************************************************
 ** FileName:       p2p_server.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-06-29 星期六 19:57:16
 ** Description:    实现对等方的服务器端
 ****************************************************************************************"""



from p2p import p2p_server

tmp = p2p_server()
tmp.init("my_name_is_Bob", '127.0.0.1', 10000, '127.0.0.1', 8989, (48512027864650021867681261707378924189222238041537180459913491423973706385315, 12347006614419446767777325628942602486721496981580611877273353936539536025074))
while(True):
    tmp.negotiation_key('127.0.0.1', 9000, ddl='2020-05-09')
    tmp.run()