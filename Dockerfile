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

RUN curl -o ${LAMBDA_TASK_ROOT}/best.onnx "https://autogosling.s3.us-east-2.amazonaws.com/best.onnx?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEAsaCXVzLWVhc3QtMSJIMEYCIQCmqPfRRw8%2BVYmKnGMnw2ncHOa6bIG6TNSIQSmPEMJ9XAIhAMX0vnoSbw85AZB3KXRcsuB2XvwaA9uQb%2BFz62rqKl6HKvkDCPP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNzY1MTM5MTczNzg1Igw%2BjlAYfZ5kKziN35YqzQMdL3hdHXm0ESBSv2M%2FIXSK8ipBmm6q%2FS4eR7ECfxvAWMU0Z%2BNbuBjohXfD4JolehKCc4%2FJCKqDVd9xABMxQvTshK%2FwNPwmjkC4ONGK5Ip6cxEqOhe80GkltqVb%2Fh4MtGDRt78lXLE1NZbhwEWg0%2FIKecj5sxSqWh%2BtGsWsy1T%2BOq0%2B3v7Jx6C72Jjfoe8bQLWNBi%2FvN3DWWF5tZpBMkg7jWIR%2FhcOk8%2BKbt6ukFTXVN84V66MMwpPIet6Zklo493Yx5ErZyvy3sNQlDywYPFvKWp%2BvX6IxD7jQKFjLtOEZEzs%2Fsynv%2Bifi3QU5Ox9yHzmZKuDEFznO3JeF136F4D%2F9QEQ0%2F6dXjHZ119dCQzG0IcPb%2FtbjGXSk6O%2BXPtLiRBsIh%2FC%2FrUxF4%2FbLJtma1twk5C7Fu2HwgBN7Y%2BEY5ZkX4QAKK6IqzyQRl0W66PIrOv6Qd%2F7K8hmN7ypWRKo1jF4Wr9%2Bhxy1fSXQI9aERuEVfKb5M%2BjmaDRQkciYrGgtiCCRaBeRDM1vMwh5Rm2q4fRtnjzhbNWdQpfA0cp%2BIukIC%2F8jnzIMaC5gCkodD2053StQTlzYTTKzYLM%2BnRQ4p5HRnBfps0LHhW%2Fn2ElonqDCvzv2uBjqTAi3y%2BP%2Fcz40ISriTD7mOhE2DTpChTv7b809%2FTkiYqYM9P7RMqBbkSkxWtMtlowzsnCyXmIaw8vcIeSeQMVXiML1g8YOojULo3q%2FUDA%2FNqsJm%2FfZkUo4SDZORqZRQS8MR4LZbIidxfDALHaeQDH5%2FwPeOiF9xxj%2BlQ3txJYWXDKVP22PfQKXoXAvoVl%2FtWrtptQSyDvHg0LmzJ%2BfvWrR08rFYt8uPjvvec4yXOZdclYH70HHx8x69af3yulC1tmSFVX3Uw6NkHDRh%2B1jlSHhQ6mRXtltIs4cwhMOXE8QbqCGWjb5h3HoBoMyWyDQ%2Fi8BWQ6LbeJtEOlKAV%2FGGjOgN14jcxcbEBGbaE0tMmsLjjp1gOtwd&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240228T182223Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA3EJOZIGMQAVDWA4P%2F20240228%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Signature=4d6e06692be57f850d5ab8693174b3122a9d87317df1ad0096c1f54d6f442dfe"


# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]