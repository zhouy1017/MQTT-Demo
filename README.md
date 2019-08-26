MarsProbe Demo

Marsprobe.py simulates the clients of a bidirectional communication system based on MQTT/EMQX.  It sends a random number in range 0-1000 for 10 times and expects responses in one of marks of A, B, C.  Then the client will print the number-mark in correct pair.

Robot_comm is the standalone package to support the MQTT communication.  It could be easily integrated into other kinds of service.

Emqx.py is the simulation of the backend of the server, acts as the Sysclient.

A running emqx broker instance is required in this demo.

This demo aims at building a framework that support MQTT communication between multiple clients and a 'server' (SysClient is not an acutal MQTT server, it's a super client of the network and could provide expandable management backend functions.)  The MQTT messaging functions are placed in stand-alone package so just need to design new message protocol to support new services.

Note:
The demo assumes that the network connection is in premium which means the top priority is to minimize the usage of bandwidth.  Thus some implementations consume more local resources to save bandwidth.

MarsProbe 模拟双向通讯用户端，连续十次向服务器发送0-1000随机数（指代Data）并获得A,B,C三种回复，并打印随机数与回复。 
Robot_comm 为通讯模块包，支持建立mqtt通讯。可适配其它业务逻辑。
Emqx为模拟服务器端，充当SysClient。
另外需一台emqx服务器作为通讯服务器。

应用场景示例：客户端采集图像数据（代替随机数）传送至SysClient，由服务器处理（如OCR识别）后结果发回（代替ABC）。
