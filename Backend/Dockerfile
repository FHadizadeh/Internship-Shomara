# init a base image (Alpine is small Linux distro)
FROM python:3.8-alpine
# define the present working directory
WORKDIR /code
ENV FLASK_APP=api.py
ENV FLASK_RUN_HOST=0.0.0.0
# copy the contents into the working dir
ADD . .
# run pip to install the dependencies of the flask app
RUN pip install -r requirements.txt
EXPOSE 4000
# define the command to start the container
CMD ["python","api.py"]