from atlas.apps.account.serializers import UserLinkedInSerializer
from atlas.apps.experience.models import OtherEducation, Position, User
from datetime import datetime
from django.db.models import Q

import requests
import json
import time

def get_all_linkedin_url(serializer, unique_url_list, url_list, user_list):
    # count = 0
    for i in serializer.data:
        # print(i)
        url = i.get('profile').get('linkedin_url')
        if url == None or url in unique_url_list:
            continue
        
        dict_url = {"url": url}
        user_id = i.get('id')
        user_name = i.get('first_name') + ' ' + i.get('last_name') # handle urutan respon != urutan user awal

        unique_url_list.append(url)
        url_list.append(dict_url.copy())
        user_list[user_name] = user_id

        # count += 1

        # if count == 6:
        #     break

def get_bright_data_response(url_list_json):
    bright_data_headers = {"Content-Type": "application/json", "Authorization": "Bearer a32e1e2a-018a-4f7d-a3b7-40c6e3c4fa24"}

    print("manggil api post")
    response_post = requests.post("https://api.brightdata.com/dca/trigger?collector=c_l3aehq022k7w15u2ad&queue_next=1", headers=bright_data_headers, data=url_list_json)
    
    if(response_post.status_code != 200):
        print('status code post: ' + str(response_post.status_code))
        raise Exception("Collector tidak dapat diakses")

    response_post_dict = json.loads(response_post.text)
    collection_id = response_post_dict.get('collection_id')

    print("manggil api get")
    response_get = requests.get("https://api.brightdata.com/dca/dataset?id=" + collection_id, headers=bright_data_headers)
    status_code = response_get.status_code

    while(status_code != 200):
        time.sleep(150)

        response_get = requests.get("https://api.brightdata.com/dca/dataset?id=" + collection_id, headers=bright_data_headers)
        status_code = response_get.status_code
        print(status_code)
    
    response_get = requests.get("https://api.brightdata.com/dca/dataset?id=" +\
         collection_id, headers=bright_data_headers)

    response_get_dict = json.loads(response_get.text)

    return response_get_dict

def save_user(url_list, response_get_dict, user_list):
    failed_url_list = []
    for i in range(len(url_list)):
        if response_get_dict[i].get("error") == None:
            id = ''
            linkedin_name = response_get_dict[i].get('name').lower()
            splt_ln_name = linkedin_name.split()
            print('ln: ' + linkedin_name)

            for user_name in user_list.keys(): # handle urutan respon != urutan user awal
                stat = True
                print(user_name)
                for name in splt_ln_name:
                    if name in user_name.lower():
                        stat = stat and True
                    else:
                        stat = stat and False
                if stat == True:
                    id = user_list[user_name]
                    break

            user = User.objects.get(pk=id)

            if response_get_dict[i].get("error") == None:
                # if user.is_from_sisidang == False:
                    # print("masuk false")
                    # delete experience yg udh ada dari db
                Position.objects.filter(Q(user_id=id) & Q(is_from_sisidang=False)).delete()
                OtherEducation.objects.filter(user_id=id).delete()

                experience_list = response_get_dict[i].get("experience")
                for experience in experience_list:
                    if experience.get("company") != None:
                        companyName = experience.get("company")
                        position_list = experience.get("positions")
                        for position in position_list:
                            title = position.get("title")

                            dateStartedStr = position.get("start_date")
                            # print(dateStartedStr)
                            if dateStartedStr != None:
                                try:
                                    if '.' in dateStartedStr:
                                        # print('masuk .')
                                        d = datetime.strptime(dateStartedStr, '%b. %Y')
                                    else:
                                        try:
                                            d = datetime.strptime(dateStartedStr, '%b %Y')
                                        except ValueError:
                                            d = datetime.strptime(dateStartedStr, '%Y')
                                    
                                    dateStarted = d.strftime('%Y-%m-%d') + ""
                                except ValueError:
                                    dateStarted = None

                                # print("dateStarted: " + dateStarted)
                            else:
                                dateStarted = None

                            dateEndedStr = position.get("end_date")
                            if dateEndedStr == "Present" or dateEndedStr == None:
                                dateEnded = None
                            elif dateEndedStr != None:
                                try:
                                    if '.' in dateEndedStr:
                                        # print('masuk .')
                                        d = datetime.strptime(dateEndedStr, '%b. %Y')
                                    else:
                                        try:
                                            d = datetime.strptime(dateEndedStr, '%b %Y')
                                        except ValueError:
                                            d = datetime.strptime(dateEndedStr, '%Y')
                                    
                                    dateEnded = d.strftime('%Y-%m-%d') + ""
                                except ValueError:
                                    dateEnded = None

                            industryName = "" # gaada di hasil bright data
                            locationName = "" # gaada di hasil bright data

                            p = Position(title=title, company_name=companyName, \
                                location_name=locationName, industry_name=industryName, \
                                    date_started=dateStarted, date_ended=dateEnded, user=user)
                            p.save()
                    
                    else:
                        companyName = experience.get("subtitle")
                        title = experience.get("title")

                        dateStartedStr = experience.get("start_date")
                        if dateStartedStr != None:
                            try:
                                if '.' in dateStartedStr:
                                    # print('masuk .')
                                    d = datetime.strptime(dateStartedStr, '%b. %Y')
                                else:
                                    try:
                                        d = datetime.strptime(dateStartedStr, '%b %Y')
                                    except ValueError:
                                        d = datetime.strptime(dateStartedStr, '%Y')
                                
                                dateStarted = d.strftime('%Y-%m-%d') + ""
                            except ValueError:
                                dateStarted = None

                            # print("dateStarted: " + dateStarted)
                        else:
                            dateStarted = None

                        dateEndedStr = experience.get("end_date")
                        if dateEndedStr == "Present" or dateEndedStr == None:
                            dateEnded = None
                        elif dateEndedStr != None:
                            try:
                                if '.' in dateEndedStr:
                                    # print('masuk .')
                                    d = datetime.strptime(dateEndedStr, '%b. %Y')
                                else:
                                    try:
                                        d = datetime.strptime(dateEndedStr, '%b %Y')
                                    except ValueError:
                                        d = datetime.strptime(dateEndedStr, '%Y')
                                
                                dateEnded = d.strftime('%Y-%m-%d') + ""
                            except ValueError:
                                dateEnded = None
                        
                        industryName = "" # gaada di hasil bright data
                        locationName = experience.get("location")

                        p = Position(title=title, company_name=companyName, \
                                location_name=locationName, industry_name=industryName, \
                                    date_started=dateStarted, date_ended=dateEnded, user=user)
                        p.save()
                            
                pos = Position.objects.filter(user_id=id)
                print(list(pos))

                education_list = response_get_dict[i].get("education")
                for education in education_list:
                    if education.get("title") == "University of Indonesia" or education.get("title") == "University of Indonesia (UI)" or education.get("title") == "Universitas Indonesia (UI)" or education.get("title") == "Universitas Indonesia" or education.get("degree") == "" or education.get("field") == "" or "SMA" in education.get("title") or "High School" in education.get("title"):
                        continue

                    university = education.get("title")
                    program = education.get("field")
                    degree_temp = education.get("degree")

                    if "Bachelor" in degree_temp:
                        degree = "S1"
                    elif "Master" in degree_temp:
                        degree = "S2"
                    elif "Doctor" in degree_temp:
                        degree = "S3"
                    else:
                        degree = "-"

                    classYear = education.get("start_year")
                    graduationYear = education.get("end_year")

                    current_year = datetime.now().year

                    # print(type(graduationYear))
                    # print(type(current_year))

                    if current_year >= int(graduationYear):
                        isGraduated = True
                    else:
                        isGraduated = False

                    country = "" # gaada di hasil bright data

                    oe = OtherEducation(country=country, university=university, \
                        program=program, degree=degree, class_year=classYear, \
                            is_graduated=isGraduated, graduation_year=graduationYear, user=user)
                    oe.save()
                
                edu = OtherEducation.objects.filter(user_id=id)
                print(list(edu))

                print('\n')

        else:
            print('user ini error')
            linkedin_url = response_get_dict[i].get("input").get("url")
            print(linkedin_url)
            dict_url = {"url": linkedin_url}
            failed_url_list.append(dict_url.copy())
            print("len failed url list " + str(len(failed_url_list)))
            print('\n')
    
    return failed_url_list


def run():
    print("mulai jalan script")
    serializer = UserLinkedInSerializer('json', User.objects.all(), many=True)
    serializer.is_valid()

    unique_url_list = []
    url_list = []
    user_list = {}
    failed_url_list = []

    get_all_linkedin_url(serializer, unique_url_list, url_list, user_list)

    print(user_list)

    url_list_json = json.dumps(url_list, indent=2)
    print(url_list_json)
    print("selesai for url list")

    response_get_dict = get_bright_data_response(url_list_json)

    print("masuk for loop save user")
    failed_url_list = save_user(url_list, response_get_dict, user_list)

    print("len failed url list " + str(len(failed_url_list)))

    count = 0
    while(len(failed_url_list)>0):
        url_list_json = json.dumps(failed_url_list, indent=2)
        print(url_list_json)
        print("selesai for url list")

        response_get_dict = get_bright_data_response(url_list_json)
        
        print("masuk for loop save user")
        failed_url_list = save_user(failed_url_list, response_get_dict, user_list)
        
        count+=1
        print("masuk while...")
        if count == 3:
            break
        