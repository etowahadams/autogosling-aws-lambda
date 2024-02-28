FROM public.ecr.aws/lambda/python:3.12

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY main.py ${LAMBDA_TASK_ROOT}
COPY marker.py ${LAMBDA_TASK_ROOT}
COPY object_detection.py ${LAMBDA_TASK_ROOT}
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY assemble.py ${LAMBDA_TASK_ROOT}
COPY utils.py ${LAMBDA_TASK_ROOT}

RUN yum install wget -y
RUN wget -O ${LAMBDA_TASK_ROOT}/best.onnx https://drive.google.com/file/d/1x_e4V9LDgjsZhMWCnONbiQXK4Zfw6t27/view?usp=share_link


# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]