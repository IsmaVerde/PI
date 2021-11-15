FROM python
	WORKDIR /app
	COPY ./mrworldwide/requirements.txt .
	RUN pip install -r requirements.txt
	COPY mrworldwide .
	EXPOSE 80
	CMD ["./manage.py", "runserver", "0.0.0.0:80"]
