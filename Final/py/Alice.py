"""****************************************************************************************
 ** FileName:       p2p_client.py
 ** Author:         Jiawei Hawkins
 ** Date:           2019-06-29 星期六 19:58:00
 ** Description:    实现对等方的客户端
 ****************************************************************************************"""

from p2p import p2p_client

tmp = p2p_client()



tmp.init("my_name_is_Alice", '127.0.0.1', 8989, (48512027864650021867681261707378924189222238041537180459913491423973706385315, 12347006614419446767777325628942602486721496981580611877273353936539536025074), '127.0.0.1', 9000)
while(True):
    tmp.negotiation_key('127.0.0.1', 10000, ddl='2020-02-10')
    tmp.run()