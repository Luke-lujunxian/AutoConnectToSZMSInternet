import time
import struct
import socket
import select
from selenium import webdriver
import selenium
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys
import sys
import re
import bs4
from selenium.webdriver.chrome.options import Options


'''copy from CSDN
https://blog.csdn.net/zhj082/article/details/80531628
'''
def chesksum(data):
    """
    校验
    """
    n = len(data)
    m = n % 2
    sum = 0
    for i in range(0, n - m ,2):
        sum += (data[i]) + ((data[i+1]) << 8)#传入data以每两个字节（十六进制）通过ord转十进制，第一字节在低位，第二个字节在高位
    if m:
        sum += (data[-1])
    #将高于16位与低16位相加
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16) #如果还有高于16位，将继续与低16位相加
    answer = ~sum & 0xffff
    #主机字节序转网络字节序列（参考小端序转大端序）
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

    '''
    连接套接字,并将数据发送到套接字
    '''
def raw_socket(dst_addr,imcp_packet):
    rawsocket = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.getprotobyname("icmp"))
    send_request_ping_time = time.time()
    #send data to the socket
    rawsocket.sendto(imcp_packet,(dst_addr,80))
    return send_request_ping_time,rawsocket,dst_addr

    '''
    request ping
    '''
def request_ping(data_type,data_code,data_checksum,data_ID,data_Sequence,payload_body):
    #把字节打包成二进制数据
    imcp_packet = struct.pack('>BBHHH32s',data_type,data_code,data_checksum,data_ID,data_Sequence,payload_body)
    icmp_chesksum = chesksum(imcp_packet)#获取校验和
    imcp_packet = struct.pack('>BBHHH32s',data_type,data_code,icmp_chesksum,data_ID,data_Sequence,payload_body)
    return imcp_packet
    '''
    reply ping
    '''
def reply_ping(send_request_ping_time,rawsocket,data_Sequence,timeout = 2):
    while True:
        started_select = time.time()
        what_ready = select.select([rawsocket], [], [], timeout)
        wait_for_time = (time.time() - started_select)
        if what_ready[0] == []:  # Timeout
            return -1
        time_received = time.time()
        received_packet, addr = rawsocket.recvfrom(1024)
        icmpHeader = received_packet[20:28]
        type, code, checksum, packet_id, sequence = struct.unpack(
            ">BBHHH", icmpHeader
        )
        if type == 0 and sequence == data_Sequence:
            return time_received - send_request_ping_time
        timeout = timeout - wait_for_time
        if timeout <= 0:
            return -1

    '''
    实现 ping 主机/ip
    '''
def ping(host):
    fail = 0
    data_type = 8 # ICMP Echo Request
    data_code = 0 # must be zero
    data_checksum = 0 # "...with value 0 substituted for this field..."
    data_ID = 0 #Identifier
    data_Sequence = 1 #Sequence number
    payload_body = b'abcdefghijklmnopqrstuvwabcdefghi' #data
    dst_addr = socket.gethostbyname(host)#将主机名转ipv4地址格式，返回以ipv4地址格式的字符串，如果主机名称是ipv4地址，则它将保持不变
    #print("正在 Ping {0} [{1}] 具有 32 字节的数据:".format(host,dst_addr))
    for i in range(0,4):
        icmp_packet = request_ping(data_type,data_code,data_checksum,data_ID,data_Sequence + i,payload_body)
        send_request_ping_time,rawsocket,addr = raw_socket(dst_addr,icmp_packet)
        times = reply_ping(send_request_ping_time,rawsocket,data_Sequence + i)
        if times > 0:
            'print("来自 {0} 的回复: 字节=32 时间={1}ms".format(addr,int(times*1000)))'
            #time.sleep(0.7)
            break
        else:
            fail += 1
            'print("请求超时。")'
    if fail <=3:
        print("[{0}] Success".format(time.asctime(time.localtime(time.time()))))
        return True
    else:
        print("**[{0}] Fail**".format(time.asctime(time.localtime(time.time()))))
        return False
'''Copy end'''

def login(Username, Password):
    browser.get("http://10.80.20.9:8080/portal/templatePage/20160111161839093/login_custom.jsp")
    time.sleep(1)
    retry_times = 0
    try:
        browser.find_element_by_name("id_userName").send_keys(Username)
        browser.find_element_by_name("id_userPwd").send_keys(Password)
        while True:
            try:
                browser.find_element_by_link_text("上线").click()
                time.sleep(0.5)
                if re.search('密码错误',bs4.BeautifulSoup(browser.page_source,"lxml").find_all(id="id_errorMessage").__str__()):
                    print("账号/密码错误")
                    input()
                    break
                if "http://10.80.20.9:8080/portal/templatePage/20160111161839093/login_custom.jsp" != browser.current_url:
                    break
            except UnexpectedAlertPresentException:
                browser.switch_to.alert.accept()
            except NoSuchElementException:
                if "http://10.80.20.9:8080/portal/templatePage/20160111161839093/login_custom.jsp" != browser.current_url:
                    break
                else:
                    if retry_times*0.5 > 5:
                        print("连接超时")
                        break
                    time.sleep(0.5)
                    retry_times += 1
    except NoSuchElementException:
        try:
            if re.search("ERR_INTERNET_DISCONNECTED", browser.find_element_by_class_name("error-code").text):
                print("未联网")
                input()
            elif re.search("ERR_CONNECTION_TIMED_OUT", browser.find_element_by_class_name("error-code").text) or re.search("HTTP ERROR 404", browser.find_element_by_class_name("error-code").text):
                print("网络错误")
                input()
        except NoSuchElementException:
            print("Unknown Error")




flag = False
def main(Mes,Username="zhchen", Password="zhchen"):
    global browser
    chrome_option = Options()
    chrome_option.add_argument('--headless')
    chrome_option.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_option)

    login(Username, Password)
    while True:
        if Mes.isSet() or flag or browser == -1:
            print("Process End")
            break
        if not ping("baidu.com"):
            login(Username, Password)
        time.sleep(3)
    shoutDown()


def shoutDown():
    try:
        browser.close()
    except NameError:
        print("并未上线")
    except WebDriverException:
        print("多次offline")
    print("已下线")


if __name__ == "__main__":
    main()
