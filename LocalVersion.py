import os, json, time, requests
"""
python发消息给微信(本地版记录Token)
"""
def Send2Wechat(AgentId, Secret, CompanyId, touser, message):
    """
    :param AgentId: 应用ID
    :param Secret: 应用Secret
    :param CompanyId: 企业ID
    :param touser : 接收人
    """
    # 通行密钥
    ACCESS_TOKEN = None
    # 如果本地保存的有通行密钥且时间不超过两小时，就用本地的通行密钥
    if os.path.exists('ACCESS_TOKEN.txt'):
        txt_last_edit_time = os.stat('ACCESS_TOKEN.txt').st_mtime
        now_time = time.time()
        print('ACCESS_TOKEN_time:', int(now_time - txt_last_edit_time))
        if now_time - txt_last_edit_time < 7200:  # 官方说通行密钥2小时刷新
            with open('ACCESS_TOKEN.txt', 'r') as f:
                ACCESS_TOKEN = f.read()
                # print(ACCESS_TOKEN)
    # 如果不存在本地通行密钥，通过企业ID和应用Secret获取
    if not ACCESS_TOKEN:
        r = requests.post(f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={CompanyId}&corpsecret={Secret}').json()
        ACCESS_TOKEN = r["access_token"]
        # print(ACCESS_TOKEN)
        # 保存通行密钥到本地ACCESS_TOKEN.txt
        with open('ACCESS_TOKEN.txt', 'w', encoding='utf-8') as f:
            f.write(ACCESS_TOKEN)
    # 要发送的信息格式
    data = {
        "touser": f"{touser}",
        "msgtype": "text",
        "agentid": f"{AgentId}",
        "text": {
            "content": f"{message}"
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    # 字典转成json，不然会报错
    data = json.dumps(data)
    # 发送消息
    r = requests.post(
        f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={ACCESS_TOKEN}',
        data=data)
    print(r.json())


if __name__ == '__main__':
    #以下参数替换为自己的
    # 应用ID
    AgentId_ = '100000X'
    # 应用Secret
    Secret_ = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    # 企业ID
    CompanyId_ = 'XXXXXXXXXXXXXXXXXX'
    # 接收人
    touser_ = 'XXXXXXXXXXXX'
    # 发送的消息
    message_ = 'Hello World！'
    Send2Wechat(AgentId_, Secret_, CompanyId_, touser_, message_)
