import qbittorrentapi
import time
import yaml
import os
from loguru import logger

logger.add('./logs/log.log', rotation="20 MB",encoding='utf-8')

def get_config():
    with open('./config.yml', mode="r", encoding='utf-8') as f:
        yaml_config = yaml.safe_load(f)
    config = {}
    # 获取环境变量值，如果环境变量为空字符串则尝试从 YAML 配置文件中读取对应值
    qb_host_env = os.environ.get('QB_HOST')
    if qb_host_env != "" and qb_host_env is not None:
        config['QB_HOST'] = os.environ.get('QB_HOST')
        print(config['QB_HOST'])
    else:
        config['QB_HOST'] = yaml_config['QB_HOST']

    qb_port_env = os.environ.get('QB_PORT')
    if qb_port_env != "" and qb_port_env is not None:
        config['QB_PORT'] = qb_port_env
    else:
        config['QB_PORT'] = yaml_config['QB_PORT']

    qb_username_env = os.environ.get('QB_USERNAME')
    if qb_username_env != "" and qb_username_env is not None:
        config['QB_USERNAME'] = qb_username_env
    else:
        config['QB_USERNAME'] = yaml_config['QB_USERNAME'] 

    qb_password_env = os.environ.get('QB_PASSWORD')
    if qb_password_env != "" and qb_password_env is not None:
        config['QB_PASSWORD'] = qb_password_env
    else:
        config['QB_PASSWORD'] = yaml_config['QB_PASSWORD']

    return config

# qBittorrent配置
config = get_config()
QB_HOST = config['QB_HOST']
QB_PORT = config['QB_PORT']
QB_USERNAME = config['QB_USERNAME'] 
QB_PASSWORD = config['QB_PASSWORD']


# 连接到qBittorrent客户端
def connect_to_qb():
    try:
        qb = qbittorrentapi.Client(host=QB_HOST, port=QB_PORT, username=QB_USERNAME, password=QB_PASSWORD)
        qb.auth_log_in()
        logger.info("qBittorrent登录成功")
        return qb
    except qbittorrentapi.LoginFailed as e:
        logger.warning("qBittorrent登录失败："+ e + ", 10秒后重新连接")
        time.sleep(10)
        return connect_to_qb()

def main():
    qb = connect_to_qb()
    # 无限循环检查错误种子状态
    while True:
        time.sleep(1)
        try:
            # 获取qb所有下载中的任务
            torrents = qb.torrents_info()
            for torrent in torrents:
                # logger.info(torrent.name)
                # 检查是否有种子是否处于错误状态
                if torrent.state_enum.is_errored:
                    logger.info(f'发现错误状态种子，将强制继续种子{torrent.name}')
                    # 强制继续种子
                    qb.torrents.resume(torrent.hash)


        except Exception as e:
            #logger.exception('qb出现异常: %s', str(e))
            logger.warning("处理qBittorrent错误种子失败，10秒后重新连接...")
            time.sleep(10)
            qb = connect_to_qb()
            continue
        
        # 暂停一段时间再次检查
        time.sleep(10)


if __name__ == "__main__":
    main()
