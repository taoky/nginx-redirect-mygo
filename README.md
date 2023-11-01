# nginx-redirect-mygo

将用户随机重定向至 MyGO!!!!! 在 B 站的切片视频之一的 nginx 配置，使用 lua 或 njs。

## 有什么用

可以调戏网站攻击者（大概），比如说加上这份配置：

```nginx
geo $abuse {
    default 0;
    # 下面的 IP 是瞎写的，测试的时候自己换一个
    194.100.67.223 1;
}
```

然后就可以：

```nginx
location /app {
    # ...
    if ($abuse) {
        rewrite ^(.+)$ /mygo-lua last;
        # 或者 rewrite ^(.+)$ /mygo-njs last;
    }
}
```

毕竟「拉黑不如消音」……啊不对，是「拉黑不如重定向」。

## 使用例

初始化：

```console
python gen.py
```



### Lua

需要 nginx 加载 lua 模块。然后将 `mygo-lua.conf` 复制到配置中。

```nginx
# 根据情况，可能需要手工加载 lua 模块
load_module "ngx_http_lua_module.so";

# ...

http {
    # ...
    server {
        include mygo-lua.conf;
        # ...
    }
}
```

`location` 如下：

```nginx
location /your-endpoint {
    rewrite ^(.+)$ /mygo-lua last;
}
```

一份完整的**测试**配置：

```nginx
error_log /dev/stdout info;
pid /tmp/nginx.pid;
# 根据你的配置修改下面的路径
load_module "/usr/lib/nginx/modules/ngx_http_lua_module.so";

events {
    worker_connections  1024;
}

http {
    include /etc/nginx/mime.types;
    client_body_temp_path /tmp/nginx/;
    fastcgi_temp_path /tmp/nginx/fastcgi/;
    uwsgi_temp_path /tmp/nginx/uwsgi/;
    scgi_temp_path /tmp/nginx/scgi/;
    access_log /tmp/access.log;
    types_hash_max_size 102400;

    server {
        listen 8000 default_server;
        listen [::]:8000 default_server ipv6only=on;
        root /tmp/;
        server_name localhost;
        client_max_body_size 100m;

        include mygo-lua.conf;
        location /your-endpoint {
            rewrite ^(.+)$ /mygo-lua last;
        }
    }
}
```

```console
> nginx -c $(pwd)/mygo.conf
2023/11/01 18:08:36 [alert] 3265033#3265033: detected a LuaJIT version which is not OpenResty's; many optimizations will be disabled and performance will be compromised (see https://github.com/openresty/luajit2 for OpenResty's LuaJIT or, even better, consider using the OpenResty releases from https://openresty.org/en/download.html)
2023/11/01 18:08:36 [notice] 3265033#3265033: using the "epoll" event method
2023/11/01 18:08:36 [notice] 3265033#3265033: nginx/1.24.0
2023/11/01 18:08:36 [notice] 3265033#3265033: OS: Linux 6.5.7-arch1-1
2023/11/01 18:08:36 [notice] 3265033#3265033: getrlimit(RLIMIT_NOFILE): 1024:524288
2023/11/01 18:08:36 [notice] 3265034#3265034: start worker processes
2023/11/01 18:08:36 [notice] 3265034#3265034: start worker process 3265035
> curl -v http://localhost:8000/your-endpoint/
*   Trying [::1]:8000...
* Connected to localhost (::1) port 8000
> GET /your-endpoint/ HTTP/1.1
> Host: localhost:8000
> User-Agent: curl/8.4.0
> Accept: */*
> 
< HTTP/1.1 302 Moved Temporarily
< Server: nginx/1.24.0
< Date: Wed, 01 Nov 2023 10:11:21 GMT
< Content-Type: text/html
< Content-Length: 145
< Connection: keep-alive
< Location: https://www.bilibili.com/video/BV18u4y1Q7pj/
< 
<html>
<head><title>302 Found</title></head>
<body>
<center><h1>302 Found</h1></center>
<hr><center>nginx/1.24.0</center>
</body>
</html>
* Connection #0 to host localhost left intact
```

### Njs

需要 nginx 加载 njs 模块。然后将 `mygo-njs.conf` 和 `mygo.js` 复制到配置中。

```nginx
# 根据情况，可能需要手工加载 njs 模块
load_module "ngx_http_js_module.so";

# ...

http {
    # ...
    server {
        include mygo-njs.conf;
        # ...
    }
}
```

`location` 如下：

```nginx
location /your-endpoint {
    rewrite ^(.+)$ /mygo-njs last;
}
```

一份完整的**测试**配置：

```nginx
error_log /dev/stdout info;
pid /tmp/nginx.pid;
# 根据你的配置修改下面的路径
load_module "/usr/lib/nginx/modules/ngx_http_js_module.so";

events {
    worker_connections  1024;
}

http {
    include /etc/nginx/mime.types;
    client_body_temp_path /tmp/nginx/;
    fastcgi_temp_path /tmp/nginx/fastcgi/;
    uwsgi_temp_path /tmp/nginx/uwsgi/;
    scgi_temp_path /tmp/nginx/scgi/;
    access_log /tmp/access.log;
    types_hash_max_size 102400;

    server {
        listen 8000 default_server;
        listen [::]:8000 default_server ipv6only=on;
        root /tmp/;
        server_name localhost;
        client_max_body_size 100m;

        include mygo-njs.conf;
        location /your-endpoint {
            rewrite ^(.+)$ /mygo-njs last;
        }
    }
}
```

```console
> nginx -c $(pwd)/mygo2.conf
2023/11/01 18:24:30 [notice] 3268407#3268407: using the "epoll" event method
2023/11/01 18:24:30 [notice] 3268407#3268407: nginx/1.24.0
2023/11/01 18:24:30 [notice] 3268407#3268407: OS: Linux 6.5.7-arch1-1
2023/11/01 18:24:30 [notice] 3268407#3268407: getrlimit(RLIMIT_NOFILE): 1024:524288
2023/11/01 18:24:30 [notice] 3268409#3268409: start worker processes
2023/11/01 18:24:30 [notice] 3268409#3268409: start worker process 3268410
> curl -v http://localhost:8000/your-endpoint/
*   Trying [::1]:8000...
* Connected to localhost (::1) port 8000
> GET /your-endpoint/ HTTP/1.1
> Host: localhost:8000
> User-Agent: curl/8.4.0
> Accept: */*
> 
< HTTP/1.1 302 Moved Temporarily
< Server: nginx/1.24.0
< Date: Wed, 01 Nov 2023 10:24:33 GMT
< Content-Type: text/html
< Content-Length: 145
< Connection: keep-alive
< Location: https://www.bilibili.com/video/BV14j41117VF/
< 
<html>
<head><title>302 Found</title></head>
<body>
<center><h1>302 Found</h1></center>
<hr><center>nginx/1.24.0</center>
</body>
</html>
* Connection #0 to host localhost left intact
2023/11/01 18:24:33 [info] 3268410#3268410: *1 client ::1 closed keepalive connection
```

## 性能

使用 siege 本机（笔记本）测试。nginx 和 njs 包来自 Arch，lua 包来自 Arch Linux CN。

### Lua

```console
> siege --no-follow --concurrent=1000 -t30S -b --no-parser http://localhost:8000/your-endpoint/
...
Lifting the server siege...
Transactions:		      240511 hits
Availability:		      100.00 %
Elapsed time:		       30.85 secs
Data transferred:	       33.26 MB
Response time:		        0.11 secs
Transaction rate:	     7796.14 trans/sec
Throughput:		        1.08 MB/sec
Concurrency:		      831.66
Successful transactions:      240512
Failed transactions:	           0
Longest transaction:	       27.66
Shortest transaction:	        0.00
> # Kill 之后再试一次
...
Lifting the server siege...
Transactions:		      227604 hits
Availability:		      100.00 %
Elapsed time:		       30.24 secs
Data transferred:	       31.47 MB
Response time:		        0.11 secs
Transaction rate:	     7526.59 trans/sec
Throughput:		        1.04 MB/sec
Concurrency:		      847.22
Successful transactions:      227606
Failed transactions:	           0
Longest transaction:	       27.78
Shortest transaction:	        0.00
```

### Njs

```console
> siege --no-follow --concurrent=1000 -t30S -b --no-parser http://localhost:8000/your-endpoint/
...
Lifting the server siege...
Transactions:		      242858 hits
Availability:		      100.00 %
Elapsed time:		       30.26 secs
Data transferred:	       33.58 MB
Response time:		        0.10 secs
Transaction rate:	     8025.71 trans/sec
Throughput:		        1.11 MB/sec
Concurrency:		      832.49
Successful transactions:      242858
Failed transactions:	           0
Longest transaction:	       29.80
Shortest transaction:	        0.00
> # Kill 之后再试一次
...
Lifting the server siege...
Transactions:		      229359 hits
Availability:		      100.00 %
Elapsed time:		       30.77 secs
Data transferred:	       31.72 MB
Response time:		        0.12 secs
Transaction rate:	     7453.98 trans/sec
Throughput:		        1.03 MB/sec
Concurrency:		      864.19
Successful transactions:      229361
Failed transactions:	           0
Longest transaction:	       27.71
Shortest transaction:	        0.00
```