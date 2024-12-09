start api server
LLMS_Top_Student/app/
uvicorn api:app --reload

test api:
LLMS_Top_Student/app/app_test.py
run for unit tests.

https://fastapi-service-940454193602.us-central1.run.app


okay. 

in google cloud sdk shell:
docker build -t fastapi-app .
docker run -p 8000:8080 fastapi-app
docker tag fastapi-app gcr.io/llmtopstudent/fastapi-app
docker push gcr.io/llmtopstudent/fastapi-app

gcloud run deploy fastapi-service --image gcr.io/llmtopstudent/fastapi-app --platform managed --region us-central1 --allow-unauthenticated


C:\Users\mym24\Desktop\GITHUB\LLMs-top-student\app>uvicorn api:app --reload

