import praw
loginfo = open("login.txt","r")
lines = loginfo.readlines()
username = lines[0].removesuffix('\n')
password = lines[1]
import pageviewapi.period as wiki
import pageviewapi
ua = "annoying wiki article provider by /u/alik2004 alik87932@gmail.com"
r = praw.Reddit(username=username, password=password, user_agent=ua)

for submission in r.subreddit("PoliticalCompassMemes").stream.submissions():

    if submission.score > 2000:
        print(submission.title)
        print(f"Score: {submission.score}")
        submission.comments.sort = 'top'
        submission.comments.replace_more()
        try:
            to_reply_to = submission.comments.list()[0]
            body = to_reply_to.body
            body = body.split(' ')
            popularity = []
            for term in body:
                try:
                    pop = wiki.avg_last("en.wikipedia", term, 30)
                    popularity.append(pop)
                except pageviewapi.client.ZeroOrDataNotLoadedException:
                    break
            most_irrelevant = body[popularity.index(min(popularity))]
            wiki_url = 'https://en.wikipedia.org/wiki/' + most_irrelevant
            msg = "This is a very _relevant_ wikipedia article \n" + wiki_url
            to_reply_to.reply(msg)
            print(msg)
        except IndexError: # when there's no comments
            pass
