# 系统包
import json
import logging

# 第三方包
from flask import Flask, request

# 自己的包
import conf
from utils import connects, util

app = Flask(__name__)


@app.route("/image_making", methods=['POST'])
def image_making():
    try:
        if request.method == 'POST':
            request_data = str(request.get_data(), encoding='utf-8')
            request_data = eval(request_data)
            request_type = request_data.get('type', None)
            request_data['reg_count'] = 0
            try:
                if request_type:  # 精彩图片合成
                    r_object.lpush_content(conf.res_wonderful_gen_name, json.dumps(request_data))
                else:  # 图片打标
                    media_id = request_data.get('media_id', None)
                    res_code = r_object.sadd_content(conf.redis_image_making_set_name, media_id)
                    if res_code == 1:
                        r_object.lpush_content(conf.redis_image_making_list_name, json.dumps(request_data))
            except Exception as e:
                logging.exception(e)
                return json.dumps(conf.status_code['37'])
            return json.dumps(conf.status_code['00'])
        else:
            return json.dumps(conf.status_code['28'])
    except Exception as e:
        logging.exception(e)
        return json.dumps(conf.status_code['35'])


if __name__ == '__main__':
    # 创建日志
    util.makedirs("./log")
    util.init_logging(
        "log/deep_learning_server_api.log", log_filelevel=logging.INFO, log_streamlevel=logging.INFO, daily=False)
    local_ip = util.get_local_ip()
    env_code = conf.env_manage.get(local_ip, 0)
    logging.info("获取到的脚本运行环境代码为: {}".format(env_code))
    account_conf = conf.AccountConf(env_code=env_code)
    # 连接redis
    r_object = connects.ConnectRedis(
        account_conf.res_host, account_conf.res_port, account_conf.res_decode_responses, account_conf.res_password)

    # 启动 flask 进程
    app.run(host='127.0.0.1', port=8081, debug=True)
