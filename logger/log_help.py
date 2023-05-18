import datetime


logFile=""

def writeLog(logString, severity, log_file):
    
    global logFile
    # print( logString)


    tstamp = datetime.datetime.now()
    if severity == 'SUCCESS':
        inString = str(tstamp) + ' ' +  severity + '     ' + logString + '\n'
    
    else:
        inString = str(tstamp) + ' ' +  severity + ' ' + logString + '\n'
    try:
        fHandle = open(log_file,'a+')
        fHandle.write(inString)
        fHandle.close()
    except:
        print( 'Problem writing to log' )
        return

    return