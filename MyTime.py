# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Written by TJ Guthrie
# Questions, comments, concerns? Contact tguthri1@mix.wvu.edu and/or 
# lcseehelpdesk@mail.wvu.edu 

import urllib2, cookielib, datetime, calendar, os, sys
from xml.dom.minidom import parseString

# Set Hosts
atsProd = 'atsprod.wvu.edu'
soapProd = 'soaprod.wvu.edu'
mapProd = 'mapprod.wvu.edu'

# Set User Agents
firefox = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:13.0) Gecko/20100101 Firefox/13.0.1'

# Set Accepts
html = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'

# Set Languages
english = 'en-us,en;q=0.5'

# Set Encodings
gzip = 'gzip, deflate'

# Set Connections
alive = 'keep-alive'

# Set Referers
ats = 'https://atsprod.wvu.edu/sso/pages/maplogin.jsp'
swf = 'https://esd.wvu.edu/otl/OTL_TIMECARD.swf'
esd = 'https://esd.wvu.edu/flexotllinks/OTLLinks.swf?nocache=0.3090389143550235'

# Set Content Types
xml = 'text/xml; charset=utf-8'

# Set SOAP Actions
getStatus = '\"http://wvumap/GET_TIMECARD_HEADER.wsdl/callGetTimecardHeader\"'
getTime = '\"http://wvuotlgettimecard/GET_TIMECARD_SERVICE.wsdl/callGetTimecard\"'
getName = '\"http://edu/wvu/common/WVU_LRS_GET_PERSON_DETAIL.wsdl/getPersonDetailXML\"'

# Set Up Cookies And Proxy
cookie_monster = cookielib.CookieJar()
cookie = urllib2.HTTPCookieProcessor(cookie_monster)
proxy = urllib2.ProxyHandler({'https': '157.182.36.121:3128'})
opener = urllib2.build_opener(proxy, cookie)
urllib2.install_opener(opener)

# Get Username And Password
def getCredentials():
    print "Input Username: ",
    username = raw_input()
    os.system("stty -echo")
    print "Input Password:",
    password = raw_input()
    os.system("stty echo")
    print "\n"
    credentials = username + ' ' + password
    return credentials

# Builds A urllib2 Request Given A URL And Headers
def buildRequest(url, data, host, userAgent, accept, acceptLanguage, acceptEncoding, connection, referer, contentType, soapAction):
    # If There Is Not Data GET, If There Is Data POST
    if (data == 'null'):
        request = urllib2.Request(url)
    else:
        request = urllib2.Request(url, data)
    # Add Headers
    if (host != 'null'):
        request.add_header('Host', host)
    if (userAgent != 'null'):
        request.add_header('User-Agent', userAgent)
    if (accept != 'null'):
        request.add_header('Accept', accept)
    if (acceptLanguage != 'null'):
        request.add_header('Accept-Language', acceptLanguage)
    if (acceptEncoding != 'null'):
        request.add_header('Accept-Encoding', acceptEncoding)
    if (connection != 'null'):
        request.add_header('Connection', connection)
    if (referer != 'null'):
        request.add_header('Referer', referer)
    if (contentType != 'null'):
        request.add_header('Content-Type', contentType)
    if (soapAction != 'null'):
        request.add_header('SOAPAction', soapAction)
    return request

# Builds Authentication Data In URL Encoded Format
def buildAuthData (username, password):
    authData = 'p_action=OK&v=v1.4&site2pstoretoken=v1.4%7E5246C911%7EACBB04A47935CAC2BF910F9C244E64E14A69B3575DB4209652508030075602B8F589690F8FC8E4DB31E6534E28D28F915898E5304FB0680459D80D4C0727B8892C74AF6634F99AE11F5535F92DFDC101A5E6F387A4E56DA71D92CA171CB56E7216125AD3F527FACBE2273D812AEAB3C1B32B3A360163F4D6DD0129849BCFDD73DE373AF2FA9B8A55954BE77452B9AB18DAD26AD120E0750325A2936B4B105F4D24F1B82D82A4D2C0CDFAE5A95EB96B6E442A3B59E20362D68168DEC93CF73198&appctx=&p_cancel_url=https%253A%252F%252Fmyapps.wvu.edu&locale=&ssousername='+ username + '&password=' + password
    return authData

# Builds SOAP Envelope For Status Request
def buildSOAPData (personID, startDate, endDate):
    soapDataTemplate = '''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <SOAP-ENV:Body>
    <tns0:callGetTimecardHeaderElement xmlns:tns0="http://wvumap/GET_TIMECARD_HEADER.wsdl/types/">
      <tns0:pPersonId>%s</tns0:pPersonId>
      <tns0:pPeriodStartDate>%s</tns0:pPeriodStartDate>
      <tns0:pPeriodEndDate>%s</tns0:pPeriodEndDate>
      <tns0:pAssignmentId>-1</tns0:pAssignmentId>
      <tns0:pSupervisorId>-1</tns0:pSupervisorId>
      <tns0:pAttribute1 xsi:nil="true"/>
      <tns0:pAttribute2 xsi:nil="true"/>
      <tns0:pAttribute3 xsi:nil="true"/>
    </tns0:callGetTimecardHeaderElement>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>'''
    soapData = soapDataTemplate%(personID, startDate, endDate)
    return soapData

# Builds SOAP Envelope For Times Request
def buildSOAPData2 (personID, startDate, endDate):
    soapDataTemplate = '''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <SOAP-ENV:Body>
    <tns0:callGetTimecardElement xmlns:tns0="http://wvuotlgettimecard/GET_TIMECARD_SERVICE.wsdl/types/">
      <pPersonId>%s</pPersonId>
      <pPeriodStartDate>%s</pPeriodStartDate>
      <pPeriodEndDate>%s</pPeriodEndDate>
      <pAssignmentId>-1</pAssignmentId>
      <pAttribute1 xsi:nil="true"/>
      <pAttribute2 xsi:nil="true"/>
      <pAttribute3 xsi:nil="true"/>
    </tns0:callGetTimecardElement>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>'''
    soapData = soapDataTemplate%(personID, startDate, endDate)
    return soapData

# Builds SOAP Envelope For Status Request
def buildSOAPData3 (personID, currentDate):
    soapDataTemplate = '''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <SOAP-ENV:Body>
    <tns0:getPersonDetailXMLElement xmlns:tns0="http://edu/wvu/common/WVU_LRS_GET_PERSON_DETAIL.wsdl/types/">
      <tns0:pPersonId>%s</tns0:pPersonId>
      <tns0:pDate>%s</tns0:pDate>
    </tns0:getPersonDetailXMLElement>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>'''
    soapData = soapDataTemplate%(personID, currentDate)
    return soapData

# Checks To See If Authentication Was Sucessfull
def authenticationCheck(authHTML):
    authCheck = 'OK'
    if (authHTML[0:6] != '<html>'):
        authCheck = 'FAIL'
    return authCheck

# Get The Dates In The Correct Format
def getDates():
    dates = []
    # Get The Current Date
    now = datetime.datetime.now()
    year = str(now.year)
    month =  str(now.month)
    day = str(now.day)
    # Get The Last Day Of The Month
    lastDayOfMonth = str(calendar.monthrange(now.year,now.month)[1])
    # Add A Zero If Month Or Day Is Only One Character
    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day
    # Put The Dates In XML Date Data Type Format
    if (now.day >= 1 and now.day <= 15):
        startDate = year + '-' + month + '-' + '01Z'
        endDate = year + '-' + month + '-' + '15Z'
    else:
        startDate = year + '-' + month + '-' + '16Z'
        endDate = year + '-' + month + '-' + lastDayOfMonth + 'Z'
    currentDate = year + '-' + month + '-' + day + 'Z'
    # Add The Dates To A List
    dates.append(currentDate)
    dates.append(startDate)
    dates.append(endDate)
    return dates

# Gets The Person ID, Used To Identify User, Not Secure
def getPersonID(SSOData):
    personID = SSOData[SSOData.find("<personId>")+10:SSOData.find("</personId>")]
    return personID

# Gets The Status Of A Time Card
def getStatus(soapEnvelope):
    xml = parseString(soapEnvelope)
    xmlTag = xml.getElementsByTagName('ns0:employeeStatus')[0].toxml()
    timeCardStatus = xmlTag.replace('<ns0:employeeStatus>','').replace('</ns0:employeeStatus>','')
    return timeCardStatus

# Gets Total Hours Worked For Pay Period
def getTotal(soapEnvelope):
    xml = parseString(soapEnvelope)
    xmlTag = xml.getElementsByTagName('regularCumm')
    data = []
    for tag in xmlTag:
        strippedData = tag.toxml().replace('<regularCumm>','').replace('</regularCumm>','')
        if (strippedData[0] != '<'):
            data.append(strippedData)
    if len(data) != 0: 
        largestNumber = data[len(data) - 1]
    else:
        largestNumber = '0'
    return largestNumber

# Get A List Of Dates And Times
def getTimes(soapEnvelope):
    timeList = []
    count = 0
    # Format XML Stream
    xml = parseString(soapEnvelope)
    formattedXML = xml.toprettyxml()
    words = formattedXML.split()
    # Traverse Formatted XML Stream
    for word in words:
        # If Date Found
        if (word[0:9] == '<workDate'):
            # Add Date To List
            timeList.append(word[10:] + ' ' + words[count + 1][:3])
        # If Start Time Found
        if (word[0:10] == '<startTime'):
            # If Next Word Contains AM or PM
            if (words[count + 1][:2] == 'AM' or words[count + 1][:2] == 'PM'):
                # Add Start And Stop Times To List, The Stop Times Appear First In Envelope
                timeList.append(word[11:] + ' ' + words[count + 1][:2])
                timeList.append(stopTime)
        # If End Time Found
        if (word[0:9] == '<stopTime'):
            # If Next Word Contains AM or PM
            if (words[count + 1][:2] == 'AM' or words[count + 1][:2] == 'PM'):
                # Set Stop Time
                stopTime = word[10:] + ' ' + words[count + 1][:2]
        count = count + 1
    return timeList

# Gets The Name 
def getName(soapEnvelope):
    nameList = []
    # Parse XML
    xml = parseString(soapEnvelope)
    xmlTag = xml.getElementsByTagName('FULL_NAME')
    if len(xmlTag) != 0:
        xmlTag = xmlTag[0].toxml()
        strippedData = xmlTag.replace('<FULL_NAME>','').replace('</FULL_NAME>','')
        names = strippedData.split()
        if (len(names) == 4):
            # First Name
            nameList.append(names[1])
            # Middle Name
            nameList.append(names[2])
            # Last Name
            nameList.append(names[0][0:len(names[0]) -1])
            # Suffix
            nameList.append(names[3])            
        if (len(names) == 3):
            # First Name
            nameList.append(names[1])
            # Middle Name
            nameList.append(names[2])
            # Last Name
            nameList.append(names[0][0:len(names[0]) -1])
        if (len(names) == 2):
            # First Name
            nameList.append(names[1])
            # Last Name
            nameList.append(names[0][0:len(names[0]) -1])
    return nameList

# Prints Clocked Entries, Attempt Comprehension At Own Risk!
# If Anyone Needs To Understand It, Might As Well Rewrite It In A Cleaner Way
# If Anyone Does Rewrite It, Be Sure To Keep It "Sexy"
def printTimes(timeList):
    output = ''
    output = output +  '       Date              Start           End    \n'
    output = output +  ' -----------------------------------------------\n'
    dateLine = ''
    lastCount = 0
    line = ''
    count = 0
    firstLine = True
    for time in timeList:
        timeCount = count
        if(len(time) == 14):
            if (not firstLine and count + 1 != len(timeList)):
                output = output + '|                   |              |            |\n'
            firstLine = False
            dateLine = time
            if (count + 1 != len(timeList) and len(timeList[timeCount + 1]) == 14):
                output = output + '| '  + dateLine + ':' + '   |   NO TIME    |   NO TIME' + '  |\n'
            printCount = 0
            line = ''
            lastCount = count
            while (lastCount + 1 != len(timeList) and lastCount + 1 != len(timeList) and len(timeList[timeCount + 1]) != 14):
                printCount = printCount + 1
                lastCount = lastCount + 1
                line = line + '   |   ' + timeList[timeCount + 1]
                if (printCount == 2):
                    output = output +  '| ' + dateLine + ':' + line + ' |\n'
                    printCount = 0
                    line = ''
                timeCount = timeCount + 1
        count = count + 1
        if (count == len(timeList) and len(timeList[count - 1]) == 14):
            output = output + '|                   |              |            |\n'
            dateLine = time
            output = output + '| '  + dateLine + ':' + '   |   NO TIME    |   NO TIME' + '  |\n'
    output = output + ' -----------------------------------------------\n'
    print output

# Prints Time Card Status, Total Hours In Pay Period, And The Name
def printInfo(timeCardStatus, totalHours, nameList):
    nameString = ''
    output = ''
    for name in nameList:
        nameString = nameString + ' ' + name
    output = output + 'Hello' + nameString + '\n'
    if (totalHours != ''):
        output = output + 'You have worked a total of ' + totalHours + ' hours this pay period' + '\n' 
    output = output + 'The status of your time card is: ' + timeCardStatus + '\n'
    print output

def formatToStream(timeList, timeCardStatus, totalHours, nameList):
    mobileData = ''
    for time in timeList:
        mobileData = mobileData + '&' + time
    mobileData = mobileData + '*' + timeCardStatus + '%' + totalHours + '-'
    for name in nameList:
        mobileData = mobileData + ' ' + name
    return mobileData

def main(argv):
    # If Being Called From A PC
    if (len(argv) == 0):
        # Get The Users Credentials Via Standard Input
        credentials = getCredentials()
        credentialsList = credentials.split()
        username = credentialsList[0]
        password = credentialsList[1]
    # If This Is A Mobile Application
    elif (len(argv) == 2):
        # The Credentials Were Passed In The Argument
        username = argv[0]
        password = argv[1]
    else:
        print "This Script Was Not Designed To Be Called Directly"
        sys.exit()
    
    # Format And Save Dates
    dates = getDates()
    currentDate = dates[0]
    startDate = dates[1]
    endDate = dates[2]

    # Build And Send Authentication Request
    authData = buildAuthData(username, password)
    authRequest = buildRequest('https://atsprod.wvu.edu/sso/auth', authData, atsProd, firefox, html, english, gzip, alive, ats, 'null', 'null')
    authResponse = opener.open(authRequest)
    authHTML = authResponse.read()
    
    # Check If Authentication Was Successful
    authCheck = authenticationCheck(authHTML)
    # If Authentication Failed
    if (authCheck == 'FAIL'):
        # If Being Called From A PC                                                                                
        if (len(argv) == 0):
            print 'Authentication Failure'
            print ''
            sys.exit()
        # If This Is A Mobile Application                                                                          
        if (len(argv) == 2):
            mobileData = 'Authentication Failure'
            # print mobileData
            return mobileData
            sys.exit()
    
    # Build And Send Requests To Get Person ID
    SSORequest = buildRequest('https://soaprod.wvu.edu/WvuSSOEbizService/wvussoebizservice', 'null', soapProd, firefox, html, english, 'null', alive, esd, 'null', 'null')
    SSOResponse = opener.open(SSORequest)
    SSOData = SSOResponse.read()
    personID = getPersonID(SSOData)
    
    # Get The Status WSDL, Response Needed For Setting The JSESSION Cookie
    requestWSDL = buildRequest('https://soaprod.wvu.edu/WvuOTLTimecardHeaderWs/GET_TIMECARD_HEADERSoapHttpPort?WSDL', 'null', soapProd, firefox, html, english, gzip, alive, swf, 'null', 'null')
    responseWSDL = opener.open(requestWSDL)

    # Build And Send The SOAP Request For Status
    soapData = buildSOAPData(personID, startDate, endDate)
    soapRequest = buildRequest('https://soaprod.wvu.edu/WvuOTLTimecardHeaderWs/GET_TIMECARD_HEADERSoapHttpPort', soapData, soapProd, firefox, html, english, 'null', alive, swf, xml, getStatus)
    soapResponse = opener.open(soapRequest)
    soapEnvelope = soapResponse.read()

    # Get Time Card Status From Raw XML
    timeCardStatus = getStatus(soapEnvelope)

    # Get The Times WSDL, Response Needed For Setting The JSESSION Cookie
    requestWSDL2 = buildRequest('https://soaprod.wvu.edu/WvuOTLGetTimecardWs/GET_TIMECARD_SERVICESoapHttpPort?WSDL', 'null', soapProd, firefox, html, english, gzip, alive, swf, 'null', 'null')
    responseWSDL2 = opener.open(requestWSDL2)

    # Build And Send The SOAP Request For Times
    soapData2 = buildSOAPData2(personID, startDate, endDate)
    soapRequest2 = buildRequest('https://soaprod.wvu.edu/WvuOTLGetTimecardWs/GET_TIMECARD_SERVICESoapHttpPort', soapData2, soapProd, firefox, html, english, 'null', alive, swf, xml, getTime)
    soapResponse2 = opener.open(soapRequest2)
    soapEnvelope2 = soapResponse2.read()

    # Get Time List And Cummulative Hours From Raw XML, Then Print In Formatted Version
    timeList = getTimes(soapEnvelope2)
    totalHours = getTotal(soapEnvelope2)

    # Build And Send The SOAP Request For Name
    soapData3 = buildSOAPData3 (personID, currentDate)
    soapRequest3 = buildRequest('https://soaprod.wvu.edu/WvuGetPersonDetailWs/WVU_LRS_GET_PERSON_DETAILSoapHttpPort', soapData3, soapProd, firefox, html, english, 'null', alive, swf, xml, getName)
    soapResponse3 = opener.open(soapRequest3)
    soapEnvelope3 = soapResponse3.read()

    # Get The Name
    nameList = getName(soapEnvelope3)

    # # If Being Called From A PC
    if (len(argv) == 0):
        # Print Time Card
        printTimes(timeList)

    # If Being Called From A PC
    if (len(argv) == 0):
        # Print Name, Status, And Total Hours
        printInfo(timeCardStatus, totalHours, nameList)

    # If This Is A Mobile Application
    if (len(argv) == 2):
        mobileData = formatToStream(timeList, timeCardStatus, totalHours, nameList)
        # print mobileData;
        return mobileData
        sys.exit()
if __name__ == "__main__":
    main(sys.argv[1:])
