#to accessed API through HTTP verbs we have use request library
import requests
#urllib helps us in fetching data across the web.
import urllib
#for sentimental analysis we use textblob library
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

#saving of Access Token and Base URL in global variables.
APP_ACCESS_TOKEN='5698893486.4e0aecd.73cf6f9f84a345d09e0441bb2ce082f4'
BASE_URL = 'https://api.instagram.com/v1/'

#Function declaration to get self information
def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s')%(APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    '''
    JSON response is similar to a dictionary . hence we can read data from it in a similar way that we used for the dictionary.
    '''
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            # to get the username, number of follower, posts and people we follow from
            print 'Username is: %s' % (user_info['data']['username'])
            print 'No. of followers are: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
         print 'Status code other than 200 received!'

#Function declaration to get the ID of a user and returns users id in return
def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()
    #To check if the user that we have searched for exists or not, we check the status code of response and fetch the user ID if response received is 200.
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            print"user doesn't exist"
            return None
    else:
         print 'Status code other than 200 received!'
         exit()

#Function declaration to get the info of a user by username and returns the information of the user
def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username is: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
         print 'Status code other than 200 received!'

#Function declaration to get your recent post and returns the image
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()
    #check for status code of the request
    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
            return own_media['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
         print 'Status code other than 200 received!'
    return None

#Function declaration to get the recent post of a user by username and returns the id of the most recent most
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
            return user_media['data'][0]['id']
        else:
            print "There is no recent post!"
    else:
         print "Status code other than 200 received!"
    return None

#Function declaration to get the ID of the recent post of a user by username
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    #get request
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()

#Function declaration to like the recent post of a user
def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    '''
    POST request which takes the request url and the data as input.
    data being send with the post request is called payload
    '''
    post_a_like = requests.post(request_url, payload).json()
    '''
   check for status code that is our like was successfull or not
    '''

    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'error!Your like was unsuccessful. Try again!'

#function declaration to comment the recent post of a user
def post_a_comment(insta_username):
    #to get id of a post
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()
    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"

#function declaration to get the list of comments on a post .it accepts the user's username
def get_comment_list(insta_username):
    #use of function get_post_id to get madia_id
    media_id=get_post_id(insta_username)
    request_url=(BASE_URL+"media/%s/comments?access_token=%s")%(media_id,APP_ACCESS_TOKEN)
    print 'get request url:%s'%(request_url)
    get_list=requests.get(request_url).json()
    if get_list['meta']['code'] == 200:
        i=0
        while(i<len(get_list['data'])):
            print "commented by %s and comment is %s "%(get_list['data'][i]['from']['username'],get_list['data'][i]['text'])
            i=i+1
        if(len(get_list['data'])>0):
           #printing of meesage on getting all comments
           print"yipee!comments are fetched successfully"
        else:
            print"no comments on the post"
    else:
        print" error!status code other then 200 received"

#function declaration to get a list of people who likes the recent post
def get_like_list(insta_username):
    #use of function get_post_id to get madia_id
    media_id=get_post_id(insta_username)
    request_url=(BASE_URL+"media/%s/likes?access_token=%s")%((media_id,APP_ACCESS_TOKEN))
    print"get request url:%s"%(request_url)
    get_list=requests.get(request_url).json()
    if get_list['meta']['code'] == 200:
        i=0
        while(i<len(get_list['data'])):
            print "liked by %s"%(get_list['data'][i]['username'])
            i=i+1
        if(len(get_list['data'])>0):
            #printing of meesage on getting all user that liked
            print " yipeeee! username who liked post are fetched successfully."
        else:
            print"no likes on the post"
    else:
        print" error!status code other then 200 received"

#function declaration to get the recent media liked  by the user
def recent_media_liked():
    request_url=(BASE_URL+"users/self/media/liked?access_token=%s")%(APP_ACCESS_TOKEN)
    print"get request url:%s" % (request_url)
    media_liked=requests.get(request_url).json()
    if media_liked['meta']['code']==200:
        if len(media_liked['data']):
            image_name = media_liked['data'][0]['id'] + '.jpeg'
            image_url = media_liked['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
            return media_liked['data'][0]['id']
        else:
            print "There is no recent post!"
    else:
        print "Status code other than 200 received!"
    return None

#function declaration to delete negative comments from a given user's post. It should accept the users' username as the input parameters.
def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #ask the user for the word that they want to search and delete comment for.
            desired_word = raw_input(" if you want to delete a comment which have specific word then enter that word ")
            #code to delete a comment
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                words=[]
                words=comment_text.split()
                for i in range(0,len(words)):
                    if desired_word==words[i]:
                        print" %s this is a comment which user want to delete"%(comment_text)
                        delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                        # make a delete call to delete the comment with desired word
                        delete_info = requests.delete(delete_url).json()
                        print"comment that user want to delete %s is successfully deleted"%(comment_text)
                #analyse the intent using the TextBlob library and look for comments with negative intent.
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    #make a delete call to delete the comment with negative intent
                    delete_info = requests.delete(delete_url).json()
                    #printing of meaningfull msg on the successfull deletion of negative comment
                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                        #error in deleting comment
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
         print 'Status code other than 200 received!'

#function declaration to iterate through the negative comments on a post which gets userss post.
def iterate_through_negative_comments(media_id):
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code'] == 200:
        if (len(comment_info['data'])):
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                #analyse the intent using the TextBlob library and look for comments with negative intent.
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment is : %s' % (comment_text)
        else:
             print"no negative comments"

#function definition to find the post with minimum number of likes
def minimum_number_of_likes(insta_username):
    user_id=get_user_id(insta_username)
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url: %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        #condition to check that account have post or not
        if len(user_media['data']):
            like=[]
            i=0
            while(i<len(user_media['data'])):
               likes_on_post=user_media['data'][i]['likes']['count']
               like.append(likes_on_post)
               i=i+1
            min_like= min(like)
            j=0
            while(j<len(like)):
                if(like[j]==min_like):
                    image_name = user_media['data'][j]['id'] + '.jpeg'
                    image_url = user_media['data'][j]['images']['standard_resolution']['url']
                    urllib.urlretrieve(image_url, image_name)
                    print image_url
                    print 'the post comtaining minimum munber of likes is open on clicking above link.Your image has been downloaded!'
                j=j+1
        else:
            print"this account have zero post"
    else:
        print"status code other then 200 received"

#function definition to find the post with particular caption.
def caption(insta_username):
    user_id =get_user_id(insta_username)
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url: %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            #caption has a particular text
            texts=raw_input("enter the particular text for which you want to search post")
            i=0
            while(i<len(user_media['data'])):
                caption_of_post = user_media['data'][i]['caption']['text']
                print caption_of_post
                words = []
                words = caption_of_post.split()
                j = 0
                while(j<len(words)):
                    if (words[j] == texts):
                        image_name = user_media['data'][i]['id'] + '.jpeg'
                        image_url = user_media['data'][i]['images']['standard_resolution']['url']
                        urllib.urlretrieve(image_url, image_name)
                        print image_url
                        print 'the post comtaining desired caption is open on clicking above link.Your image has been downloaded!'
                    j = j + 1
                i=i+1

        else:
            print"no post on this account"

#function declaration to start the boot
def start_bot():
    while True:
        print '\n'
        print 'Hey there! Welcome to instaBot!(*_*).This bot will be capable of getting the information of users, liking their posts, deleting and making comments and much more'
        request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
        user_info = requests.get(request_url).json()
        if user_info['meta']['code'] == 200:
            if len(user_info['data']):
                #The bot should ask the username for which you want to perform any of the action.
                print "%s are you want to perform action for yourself or another user" % (user_info['data']['username'])
                print"please choose option from here"
                print"a.for yourself operation"
                print"b.for another user operation"
                choose = raw_input("choose from a or b\n")
                if (choose == 'a'):
                    # menu to choose which task is to be performed
                    insta_username=user_info['data']['username']
                    print "1.Get your own details\n"
                    print "2.Get your own recent post\n"
                    print "3.to get the recent media liked by the user.\n"
                    print "6.Get a list of people who have liked the recent post of a your\n"
                    print "7.Like the recent post of your\n"
                    print "8.Get a list of comments on the recent post of a your\n"
                    print "9.Make a comment on the recent post of a your\n"
                    print "10.Delete negative comments from the recent post of a your\n"
                    print"11.to iterate through the negative comments on a post"
                    print"12.to find the post with minimum number of likes on a post\n"
                    print"13.to find the post with particular caption"
                    print "14.exit"
                elif (choose == 'b'):
                    # menu to choose which task is to be performed
                    print("my sanbox users are")
                    print("astha_rc_")
                    print("ruchikagarg764")
                    insta_username = raw_input("enter the username of the user")
                    #The bot should ask the user of what they want to do for the username already provided.
                    print "4.Get details of a user by username\n"
                    print "5.Get the recent post of a user by username\n"
                    print "6.Get a list of people who have liked the recent post of a user\n"
                    print "7.Like the recent post of a user\n"
                    print "8.Get a list of comments on the recent post of a user\n"
                    print "9.Make a comment on the recent post of a user\n"
                    print "10.Delete negative comments from the recent post of a user\n"
                    print"11.to iterate through the negative comments on a post"
                    print"12.to find the post with minimum number of likes on a post"
                    print "14.Exit"
                else:
                    print("wrong choice")
                    exit()

                choice = raw_input("Enter you choice: ")
                if choice == "1":
                    self_info()
                elif choice == "2":
                    get_own_post()
                elif choice == "3":
                    recent_media_liked()
                elif choice == "4":
                    get_user_info(insta_username)
                elif choice == "5":
                    get_user_post(insta_username)
                elif choice == "6":
                    get_like_list(insta_username)
                elif choice == "7":
                    like_a_post(insta_username)
                elif choice == "8":
                    get_comment_list(insta_username)
                elif choice == "9":
                    post_a_comment(insta_username)
                elif choice == "10":
                    delete_negative_comment(insta_username)
                elif choice=="11":
                    media_id=get_post_id(insta_username)
                    iterate_through_negative_comments(media_id)
                elif choice=='12':
                    minimum_number_of_likes(insta_username)
                elif choice=="13":
                    caption(insta_username)
                elif choice=="14":
                    exit()
                else:
                    print "wrong choice"

#function calling to sart the boot
start_bot()
