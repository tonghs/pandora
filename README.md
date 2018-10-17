## pandora

AD Data Dashboard


### 开发

只运行 app

```
docker-compose -f docker-compose.yml -f docker-compose.app.yml up -d
```


运行测试

```
docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm test
```
