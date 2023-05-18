import json,csv,copy,os
import sys
import requests
import urllib3 
import datetime
from logger.log_help import writeLog


from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings()

if hasattr(sys, 'frozen'):
    basis = sys.executable
else:
    basis = sys.argv[0]
dir_path = os.path.split(basis)[0]

# dir_path = os.path.dirname(os.path.realpath(__file__))
log_file = dir_path + "\APP_RESUBMIT.Log"


def stLogin(basicAuth,stUrl, session):

    url = stUrl + 'myself'

    authString = 'Basic ' + basicAuth

    headers = {'Referer': referer,
               'Accept': 'application/json',
               'Authorization': authString}

    try:
        response = session.post(url, headers=headers, verify=False, timeout=stTimeout)
    except requests.ConnectionError as ec:
        print('I cannot connect to ' + stUrl + ' ' + str(ec))
        sys.exit(1)
    except requests.exceptions.HTTPError as eh:
        print('HTTP Error ' + str(eh))
        sys.exit(1)
    except requests.exceptions.Timeout as et:
        print('Timeout Error:' + str(et))
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print('Unknown Error ' + str(e))
        sys.exit(1)
    else:
       
        print('Session Mgt Login using /myself: SUCCESS')
        writeLog("Session Mgt Login using /myself: SUCCESS","INFO",log_file)

        return True

def If_Account_exist(referer,sturl,session,timeout,account_name):
    account_exist = False
    url = sturl + 'accounts/' + account_name
    headers = {'Referer': referer,
               'Accept': 'application/json',
               'Content-Type' :'application/json'}
    try:
        response = session.head(url, headers=headers, verify=False, timeout=timeout)
    except requests.ConnectionError as ec:
        print('I cannot connect to ' + stUrl + ' ' + str(ec))
        sys.exit(1)
    except requests.exceptions.HTTPError as eh:
        print('HTTP Error' + str(eh))
        sys.exit(1)
    except requests.exceptions.Timeout as et:
        print('Timeout Error:' + str(et))
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print('Unknown Error' + str(e))
        sys.exit(1)
    else:
        if (response.status_code ==200):
            # print(f"account exist")
            account_exist =True
            writeLog(f"{account_name} exists","SUCCESS", log_file)
        else:
            # print(f"Account does not exist {response.status_code}")
            writeLog(f"Account doesn't exist, error code is {response.status_code}, for account {account_name}","ERROR", log_file)
        # print(response.json())

    return account_exist


def If_Application_exist(referer,sturl,session,timeout,application_name):
    app_exist = False
    
    url = sturl + 'applications/' + application_name
    headers = {'Referer': referer,
               'Accept': 'application/json',
               'Content-Type' :'application/json'}
    try:
        response = session.head(url, headers=headers, verify=False, timeout=timeout)
    except requests.ConnectionError as ec:
        print('I cannot connect to ' + stUrl + ' ' + str(ec))
        sys.exit(1)
    except requests.exceptions.HTTPError as eh:
        print('HTTP Error' + str(eh))
        sys.exit(1)
    except requests.exceptions.Timeout as et:
        print('Timeout Error:' + str(et))
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print('Unknown Error' + str(e))
        sys.exit(1)
    else:
        if (response.status_code ==200):
            # print(f"application exist")
            app_exist = True
            writeLog(f"{application_name} application exists on ST","SUCCESS", log_file)
        else:
            writeLog(f"{application_name} doesn't application exists on ST","ERROR", log_file)

            # print(f"somthing nasty occured , error code is {response.status_code}")
            # writeLog(f"somthing nasty occured , error code is {response.status_code}, for account {account_name}","ERROR", logFile)
        # print(response.json())

    return app_exist


def createAccount(referer,sturl,session,timeout,post_req):
    
    account_created = False
    url = sturl +'accounts/'
    headers = {'Referer': referer,
               'Content-Type' :'application/json',
               'Accept': 'application/json'}
    try:
        response = session.post(url, json=post_req, headers=headers, verify=False, timeout=timeout)
    except requests.ConnectionError as ec:
        print('I cannot connect to ' + stUrl + ' ' + str(ec))
        sys.exit(1)
    except requests.exceptions.HTTPError as eh:
        print('HTTP Error' + str(eh))
        sys.exit(1)
    except requests.exceptions.Timeout as et:
        print('Timeout Error:' + str(et))
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print('Unknown Error' + str(e))
        sys.exit(1)
    else:
        if (response.status_code ==201):
            account_created = True
            print(f"account creation success for account {post_req['name']}")
            writeLog(f"account creation success for account {post_req['name']}", "INFO", log_file)
            
        else:
            print(f"somthing nasty occured , error code is {response.status_code} for account {post_req['name']}")
            writeLog(f"account creation success for account {post_req['name']}", "ERROR", log_file)
            
        # print(response.json())

        return account_created 


def createSubscription(referer,sturl,session,timeout,post_req):
    subscription_created = False
    url = sturl +'subscriptions/'
    headers = {'Referer': referer,
               'Content-Type' :'application/json',
               'Accept': 'application/json'}
    try:
        response = session.post(url, json=post_req, headers=headers, verify=False, timeout=timeout)
    except requests.ConnectionError as ec:
        print('I cannot connect to ' + stUrl + ' ' + str(ec))
        sys.exit(1)
    except requests.exceptions.HTTPError as eh:
        print('HTTP Error' + str(eh))
        sys.exit(1)
    except requests.exceptions.Timeout as et:
        print('Timeout Error:' + str(et))
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print('Unknown Error' + str(e))
        sys.exit(1)
    else:
        if (response.status_code ==201):
            subscription_created = True
            print(f"subscription creation success for account {post_req['account']}, subscription name {post_req['folder']}")
            writeLog(f"subscription creation success for account {post_req['account']}, subscription name {post_req['folder']}", "INFO", log_file)
            
        else:
            print(f"somthing nasty occured , error code is {response.status_code} for account {post_req['account']}, {post_req['folder']}")
            writeLog(f"subscription creation failed for account {post_req['account']}, subscription name {post_req['folder']}, ERROR CODE is {response.status_code}", "INFO", log_file)
            
        # print(response.json())

        return subscription_created 


def CreateUserClass(referer,sturl,session,timeout,post_req):
    UC_created = False
    url = sturl +'userClasses/'
    headers = {'Referer': referer,
               'Content-Type' :'application/json',
               'Accept': 'application/json'
               }
    try:
        response = session.post(url, json=post_req, headers=headers, verify=False, timeout=timeout)
    except requests.ConnectionError as ec:
        print('I cannot connect to ' + stUrl + ' ' + str(ec))
        sys.exit(1)
    except requests.exceptions.HTTPError as eh:
        print('HTTP Error' + str(eh))
        sys.exit(1)
    except requests.exceptions.Timeout as et:
        print('Timeout Error:' + str(et))
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print('Unknown Error' + str(e))
        sys.exit(1)
    else:
        if(response.status_code == 201):
            UC_created=True
            print(f"User Class {post_req['className']} created! ")
            writeLog(f"User Class {post_req['className']} created! ", "INFO", log_file)
        else:
            print(f"Failed to  create UserClass {post_req['className']} , error code is {response.status_code}")
            print(f"{response.json()}")
            writeLog(f"Failed to  create UserClass {post_req['className']} , error code is {response.status_code}","INFO", log_file)

            
    return UC_created


#GET LOG TRANSFERS

def getFailedTransfer(referer,sturl,session,timeout,timeafter,timebefore):
    AnyFailedTransfers = False
    url = sturl + 'logs/transfers?status=Failed&startTimeAfter=' + timeafter +'&startTimeBefore=' +timebefore
    headers = {'Referer': referer,
               'Accept': 'application/json',
               'Content-Type' :'application/json'}
    try:
        response = session.get(url, headers=headers, verify=False, timeout=timeout)
    except requests.ConnectionError as ec:
        print('I cannot connect to ' + stUrl + ' ' + str(ec))
        sys.exit(1)
    except requests.exceptions.HTTPError as eh:
        print('HTTP Error' + str(eh))
        sys.exit(1)
    except requests.exceptions.Timeout as et:
        print('Timeout Error:' + str(et))
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print('Unknown Error' + str(e))
        sys.exit(1)
    else:
        if (response.status_code ==200):
            # print(f"account exist")
            AnyFailedTransfers =True
            writeLog(f" Failed Transfers in place","SUCCESS", log_file)
        else:
            # print(f"Account does not exist {response.status_code}")
            writeLog(f"No Failed Transfers","WARN", log_file)
        # print(response.json())

    return response.json()


#Resubmit Files On ST:

def resubmitFiles(referer,sturl,session,timeout,url_rep):
    resubmit_success = False
    url = sturl +'logs/transfers/' + url_rep + '/operations?operation=resubmit'
    headers = {'Referer': referer,
               'Content-Type' :'application/json',
               'Accept': 'application/json'
               }
    try:
        response = session.post(url, headers=headers, verify=False, timeout=timeout)
    except requests.ConnectionError as ec:
        print('I cannot connect to ' + stUrl + ' ' + str(ec))
        sys.exit(1)
    except requests.exceptions.HTTPError as eh:
        print('HTTP Error' + str(eh))
        sys.exit(1)
    except requests.exceptions.Timeout as et:
        print('Timeout Error:' + str(et))
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print('Unknown Error' + str(e))
        sys.exit(1)
    else:
        if(response.status_code == 200):
            resubmit_success=True
            print(f"resubmitted successfully , respone code : {response.status_code}")
            # writeLog(f"resubmitted successfully for url representation {url_rep}", "INFO", log_file)
            writeLog(f"{response.json()}","RESPONSE", log_file)
        else:
            print(f"resubmission failed , error code is {response.status_code}")
            # print(f"{response.json()}")
            writeLog(f"resubmission failed , error code is {response.status_code}","ERROR", log_file)

            
    return response.json()



#USED FOR DIRECT USE 

stTimeout = 120  # in seconds
referer = 'arpit'
stUrl = 'https://st-jdp-lab:8444/api/v2.0/'
basicAuth = "YWRtaW46YXh3YXk="  # from echo -n user:pass | base64
sessionMgt = requests.Session()

# with open('sample-requests/sample-subscription-request.json','r') as subscriptions:
#     sub = json.load(subscriptions)

# print(sub)
# stLogin(basicAuth, sessionMgt)
# createSubscription(referer,stUrl,sessionMgt,stTimeout,sub)

# with open('sample-requests/sample-userclass-request.json','r') as uc:
#     userclass = json.load(uc)

# print(userclass)
# CreateUserClass(referer,stUrl,sessionMgt,stTimeout,userclass)