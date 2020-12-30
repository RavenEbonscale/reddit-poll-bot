import praw

#This bot is dependt on the same format as Celebe battle so the names have to be seperated by "vs" and all non name things have to go before a :
#THis bot will need moderator privlegaes

def main():
    reddit = praw.Reddit(
        client_id="",
        client_secret="",
        user_agent="",
        username ="",
        password =""
            )
    print('Connecting to reddit')

    subreddit = reddit.subreddit("Your subreddit here Subreddit")

    for submission in subreddit.stream.submissions():
        #converts the submissions titles to names
        names =convert_to_names(submission)
        #This creates the poll after converting the title int names
        poll = create_poll(submission.title,names,reddit)
        #This locks the poll for comments, Posts the poll to the correct submsion and stickiesit
        post_poll(poll,reddit,submission)


def convert_to_names(sub):
    title = sub.title
    if ':' in title:
        substring = title.split(':',1)[1]
        nomerlized = substring.strip()
        names =  nomerlized.split('vs')
        return names
    else:
       nomerlized= title.strip()
       names =  nomerlized.split('vs')
       return names



def create_poll(title,names,reddit):
    if len(names) <= 7 and len(names) > 1:
          poll = reddit.subreddit("Poll Version Of Subreddit").submit_poll(
            title,selftext="",  options = names, duration =3
            )
          return poll
    else:
         print("not enought names")


def post_poll(poll,reddit,submission):
    tolock = reddit.submission(poll.id)
    tolock.mod.lock()
    comment = submission.reply(f'Vote here:{poll.shortlink}')
    comment = reddit.comment(comment.id)
    comment.mod.distinguish(how="yes",sticky=True)
main()