FROM public.ecr.aws/lambda/python:3.10

COPY requirements.txt .

RUN pip3 install -r requirements.txt -U --no-cache-dir

COPY ./app ${LAMBDA_TASK_ROOT}

CMD [ "main.handler" ]
