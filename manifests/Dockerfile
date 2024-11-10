FROM crpi-zlribkwyirjztfmd.cn-shenzhen.personal.cr.aliyuncs.com/lei-test/simplemodel:2.5.0-cud

WORKDIR /simplemodel

COPY ./manifests ./manifests
#COPY . .
RUN pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple -r ./manifests/requirements.txt 

COPY . . 
RUN chmod +x run_gunicorn.sh

EXPOSE 8080
CMD ["./run_gunicorn.sh"]