FROM pytorch/pytorch:2.5.0-cuda12.4-cudnn9-devel

WORKDIR /simplemodel

COPY ./manifests ./manifests
#COPY . .
RUN pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple -r ./manifests/requirements.txt 

COPY . . 
RUN chmod +x run_gunicorn.sh

EXPOSE 8080
CMD ["./run_gunicorn.sh"]