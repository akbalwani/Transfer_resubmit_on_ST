from STAPIs import *
import urllib.parse
from datetime import datetime,timedelta
from email import utils 
from pytz import timezone
#GLOBAL CONFIGs
stTimeout = 120  # in seconds
referer = 'arpit'
stUrl = 'https://st-jdp-lab:8444/api/v2.0/'
basicAuth = "YWRtaW46YXh3YXk="  # from echo -n user:pass | base64
sessionMgt = requests.Session()

resubmit_list = []
#PARAMS FOR THIS SCRIPT
stLogin(basicAuth,stUrl,sessionMgt)


def default_func():
    print("Not a valid choice.")

def getFailedTransferAndResubmit(timeafter,timebefore):
    
    failedtransfers = getFailedTransfer(referer,stUrl,sessionMgt,stTimeout,timeafter,timebefore)
    
    #######CODE TO GET RESUBMIT ELIGIBLE FILES
    for i in range(0,failedtransfers["resultSet"]["returnCount"]):

        try:
            resubmit = failedtransfers["result"][i]["metadata"]["links"]["resubmit"]
        except KeyError:
            resubmit = None
        if resubmit:
            # resubmit_list.append(resubmit)
            resubmitted_already = {failedtransfers ["result"][i]["resubmitted"]}
            print(f'is file already resubmitted ? {failedtransfers ["result"][i]["resubmitted"]}')
            url_rep = resubmit[48:172]
            print(url_rep)
            print(f'filename : {failedtransfers ["result"][i]["filename"]}')
            if failedtransfers ["result"][i]["resubmitted"] == False :
                feedback = resubmitFiles(referer,stUrl,sessionMgt,stTimeout,url_rep)
                print(feedback["message"])
            else:
                pass
                # print("the transfer is already resubmitted.")

def last_5_minutes():
    timebefore_utc = datetime.now()
    timebefore = timebefore_utc.astimezone(timezone('US/Arizona'))
    timebefore = utils.format_datetime(timebefore)
    print(f"plain text timebefore :  {timebefore}")
    timebefore = urllib.parse.quote(timebefore)

    timeafter_utc = datetime.now()+timedelta(minutes=-5)
    timeafter = timeafter_utc.astimezone(timezone('US/Arizona')) 
    timeafter = utils.format_datetime(timeafter) 
    print(f"plain text timeafter :  {timeafter}")
    timeafter = urllib.parse.quote(timeafter)
    getFailedTransferAndResubmit(timeafter,timebefore)
    

def last_1_hour():
    timebefore_utc = datetime.now()
    timebefore = timebefore_utc.astimezone(timezone('US/Arizona'))
    timebefore = utils.format_datetime(timebefore)
    print(f"plain text timebefore :  {timebefore}")
    timebefore = urllib.parse.quote(timebefore)

    timeafter_utc = datetime.now()+timedelta(hours=-1)
    timeafter = timeafter_utc.astimezone(timezone('US/Arizona')) 
    timeafter = utils.format_datetime(timeafter) 
    print(f"plain text timeafter :  {timeafter}")
    timeafter = urllib.parse.quote(timeafter)
    getFailedTransferAndResubmit(timeafter,timebefore)

def last_1_day():
    timebefore_utc = datetime.now()
    timebefore = timebefore_utc.astimezone(timezone('US/Arizona'))
    timebefore = utils.format_datetime(timebefore)
    print(f"plain text timebefore :  {timebefore}")
    timebefore = urllib.parse.quote(timebefore)

    timeafter_utc = datetime.now()+timedelta(days=-1)
    timeafter = timeafter_utc.astimezone(timezone('US/Arizona')) 
    timeafter = utils.format_datetime(timeafter) 
    print(f"plain text timeafter :  {timeafter}")
    timeafter = urllib.parse.quote(timeafter)
    getFailedTransferAndResubmit(timeafter,timebefore)

interval_choice = input("resubmit interval decision :\n1. last 5 mins \n2. last 1 hour\n3. last 1 day \nplease enter choice now:")

match interval_choice:
    case "1":
        last_5_minutes()

    case "2":
        last_1_hour()

    case "3":
        last_1_day()

    case _:
        default_func()






       
