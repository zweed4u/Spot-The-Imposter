#Parses user's DM and enters them for guac
#DM format: 
#                  FIRST_NAME LAST_NAME MOBILE_NUMBER ZIPCODE EMAIL
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from tweepy.streaming import StreamListener
import json,requests,urllib2

#enter the corresponding information from your Twitter application:
#make sure to set proper permissions for application (DMs included)
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

class StdOutListener( StreamListener ):
    #@staticmethod <- use if StdOutListener.bogo wanted rather than self
    def bogo(self,f,l,m,z,e):
        global response
        reqUrl='https://api-proxy.chipotle.com/ri2k17/reg'
        postHeaders={
            'Accept':'application/json',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.8',
            'Connection':'keep-alive',
            'Content-Type':'application/json',
            'Host':'api-proxy.chipotle.com',
            'Origin':'https://spottheimposter.chipotle.com',
            'Referer':'https://spottheimposter.chipotle.com/',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
        }

        payload={
            'f': f,
            'l': l,
            'm': m,
            's': "true",
            'z': z,
            'e': e,
            'es': "true"
        }
        print str(payload)
        session=requests.Session()
        response=session.post(reqUrl,data=json.dumps(payload),headers=postHeaders)
        #want {"status":"success","is_repeat":false}
        response=response.json()
        #if success and repeat false send success message api.direct message

    def __init__( self ):
        self.tweetCount = 0

    def on_connect( self ):
        print("Connection established!!")

    def on_disconnect( self, notice ):
        print("Connection lost!! : ", notice)

    def on_data( self, status ):
        global message,first,last,mobile,zipCode,email
        #unicode to string
        status = str(status)
        try:
            json_acceptable_string = status.replace('\\','')
            #string to dict
            status=json.loads(json_acceptable_string)
            #conditional for wanted message stream
            if 'direct_message' in status.keys():
                print '\n'
                print status[u'direct_message'][u'sender_screen_name'] +' sent: '+ status[u'direct_message'][u'text']
                flag=0
                if str(status[u'direct_message'][u'sender_screen_name'])=='jayzer1217':
                    flag=1
                message=str(status[u'direct_message'][u'text'])
                #makes sure the message is 6 words
                if len(message.split(' '))==6:
                    first=message.split(' ')[0]
                    last=message.split(' ')[1]
                    mobile=message.split(' ')[2]
                    mobile=mobile.replace('-','')
                    mobile=mobile.replace(' ','')
                    mobile=mobile.replace('(','')
                    mobile=mobile.replace(')','')
                    #mobile=message.split(' ')[2].replace('(','').replace(')','').replace('-','').replace(' ','')
                    if len(mobile)==10:
                        mobile='1'+mobile
                    zipCode=message.split(' ')[3]
                    email=message.split(' ')[4]
                    self.bogo(first,last,mobile,zipCode,email)
                    if flag == 0:
                        if 'error' in response.keys():
                            api.send_direct_message(user=str(status[u'direct_message'][u'sender_screen_name']),text='Request Failed! Response Error: '+response['error'])
                        elif 'success' in response.values():
                            if response['is_repeat']==True:
                                api.send_direct_message(user=str(status[u'direct_message'][u'sender_screen_name']),text='Request Succeeded But this number has already been used!')
                            else:
                                api.send_direct_message(user=str(status[u'direct_message'][u'sender_screen_name']),text='Yay! You should receive a message from Chipotle shortly!')

                    if 'error' in response.keys():
                        print response['error']
                    elif 'success' in response.values():
                        if response['is_offer_repeat'] == True:
                            print  'Number has already been used!'
                        else:
                            print 'Success!'

                    #if is_repeat==true then message this is a repeat
                    print '\n'
                elif len(message.split(' '))==5:
                    first=message.split(' ')[0]
                    last=message.split(' ')[1]
                    mobile=message.split(' ')[2]
                    mobile=mobile.replace('-','')
                    mobile=mobile.replace(' ','')
                    if len(mobile)==10:
                        mobile='1'+mobile
                    zipCode=message.split(' ')[3]
                    email=message.split(' ')[4]
                    self.bogo(first,last,mobile,zipCode,email)
                    if flag == 0:
                        if 'error' in response.keys():
                            api.send_direct_message(user=str(status[u'direct_message'][u'sender_screen_name']),text='Request Failed! Response Error: '+response['error'])
                        elif 'success' in response.values():
                            if response['is_offer_repeat']==True:
                                api.send_direct_message(user=str(status[u'direct_message'][u'sender_screen_name']),text='Request Succeeded But this number has already been used!')
                            else:
                                api.send_direct_message(user=str(status[u'direct_message'][u'sender_screen_name']),text='Yay! You should receive a message from Chipotle shortly!')

                    if 'error' in response.keys():
                        print response['error']
                    elif 'success' in response.values():
                        if response['is_offer_repeat'] == True:
                            print  'Number has already been used!'
                        else:
                            print 'Success!'

                    print '\n'

                else:
                    #message is not in designed format
                    #Implement Message back with example
                    if flag==0:
                        api.send_direct_message(user=str(status[u'direct_message'][u'sender_screen_name']),text='Message ill formed! Send as one line! eg. John Doe 18008675309 90210 johndoe@gmail.com')
                    print 'Message ill formed'
            else:
                #not direct message flow
                pass
        except:
            #not important flows - couldn't convert to json/not correct flow in stream
            pass
        return True

    def on_direct_message( self, status ):
        print("Entered on_direct_message()")
        try:
            print(status)#, flush = True)
            return True

        except BaseException as e:
            print("Failed on_direct_message()", str(e))

    def on_error( self, status ):
        #Verbose error code
        if status==200:
            print str(status)+' :: OK - Success!'
        elif status==304:
            print str(status)+' :: Not modified'
        elif status==400:
            print str(status)+' :: Bad request'
        elif status==401:
            print str(status)+' :: Unauthorized'
        elif status==403:
            print str(status)+' :: Forbidden'
        elif status==404:
            print str(status)+' :: Not found'
        elif status==406:
            print str(status)+' :: Not acceptable'
        elif status==410:
            print str(status)+' :: Gone'
        elif status==420:
            print str(status)+' :: Enhance your Calm - rate limited'
        elif status==422:
            print str(status)+' :: Unprocessable entity'
        elif status==429:
            print str(status)+' :: Too many requests'
        elif status==500:
            print str(status)+' :: Internal server error'
        elif status==502:
            print str(status)+' :: Bad gateway'
        elif status==503:
            print str(status)+' :: Service unavailable'
        elif status==504:
            print str(status)+' :: Gateway timeout'
        else:
            print str(status)+' :: Unknown'

def main():
    global api
    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.secure = True
        auth.set_access_token(access_token, access_token_secret)
        api = API(auth)
        print(api.me().name)
        stream = Stream(auth, StdOutListener())
        stream.userstream()

    except BaseException as e:
        print("Error in main()", e)


if __name__ == '__main__':
    main()
