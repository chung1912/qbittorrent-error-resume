# qBittorrent自动强制继续

针对qBittorrent下载失败的种子，自动强制继续下载。

## 使用说明

```sh
docker run -it --name qbittorrent-error-resume \
-e QB_HOST="127.0.0.1" \
-e QB_PORT=12345 \
-e QB_USERNAME="your_username" \
-e QB_PASSWORD="your_password" \
--restart always \
chung1912/qbittorrent-error-resume:latest
```
