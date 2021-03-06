import requests
import time


def get_upload_url(api_url):
    response = requests.get(api_url+"upload-url")
    print("get_upload_url response = " + str(response.json()))
    assert response.status_code == 200
    print ('get_upload_url passed')
    return response.json()


def upload_file(upload_url,file_path):
    headers = {"Content-Type":"text/csv"}
    with open(file_path,"rb") as file:
        response = requests.put(upload_url,data=file,headers=headers)
    print( "upload_file response status" + str(response.status_code))
    print( "upload_file response" + response.text)
    assert response.status_code == 200
    print ('upload_file passed')
    print(file.name + " has been uploaded to S3")


def get_summary(api_url,file_key):
    for i in range(60):
        response = requests.get(api_url+"results?filekey="+file_key)
        lambda_status_code = int(response.status_code)
        if lambda_status_code == 204:
            time.sleep(5)
            continue
        if lambda_status_code == 200:
            print ('get_summary passed')
            print("get_summary request {} response = ".format(i) + str(response.json()))
            return response.json()
    #Raise an exception if results were not returned after 6 tries
    raise Exception("Results were not returned after requesting 6 times")

    

base_url = 'https://8k7ni4cse1.execute-api.us-west-2.amazonaws.com/github-deploy-test/'



upload_url_response = get_upload_url(base_url) 
upload_url = upload_url_response['uploadurl']
file_key = upload_url_response['filekey']

file_path = "./Backend/Tests/test_upload_session/testfile.csv"

upload_file(upload_url,file_path)
summary_response = get_summary(base_url,file_key)
