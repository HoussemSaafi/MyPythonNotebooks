# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def scrape_comments(yt_link):
    import import_ipynb
    api_key = "AIzaSyB2l7HPFPTUboybjsqY-0cp_XlRG0PVuAM"
    from googleapiclient.discovery import build
    youtube = build('youtube', 'v3', developerKey=api_key)

    import pandas as pd

    ID = "aB6fL5LWefo"  # Replace this YouTube video ID with your own.

    box = [['Name', 'Comment', 'Time', 'Likes', 'Reply Count']]

    def scrape_comments_with_replies():
        data = youtube.commentThreads().list(part='snippet', videoId=ID, maxResults='100',
                                             textFormat="plainText").execute()

        for i in data["items"]:

            name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
            comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
            published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
            likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
            replies = i["snippet"]['totalReplyCount']

            box.append([name, comment, published_at, likes, replies])

            totalReplyCount = i["snippet"]['totalReplyCount']

            if totalReplyCount > 0:

                parent = i["snippet"]['topLevelComment']["id"]

                data2 = youtube.comments().list(part='snippet', maxResults='100', parentId=parent,
                                                textFormat="plainText").execute()

                for i in data2["items"]:
                    name = i["snippet"]["authorDisplayName"]
                    comment = i["snippet"]["textDisplay"]
                    published_at = i["snippet"]['publishedAt']
                    likes = i["snippet"]['likeCount']
                    replies = ""

                    box.append([name, comment, published_at, likes, replies])

        while ("nextPageToken" in data):

            data = youtube.commentThreads().list(part='snippet', videoId=ID, pageToken=data["nextPageToken"],
                                                 maxResults='100', textFormat="plainText").execute()

            for i in data["items"]:
                name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
                comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
                published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
                likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
                replies = i["snippet"]['totalReplyCount']

                box.append([name, comment, published_at, likes, replies])

                totalReplyCount = i["snippet"]['totalReplyCount']

                if totalReplyCount > 0:

                    parent = i["snippet"]['topLevelComment']["id"]

                    data2 = youtube.comments().list(part='snippet', maxResults='100', parentId=parent,
                                                    textFormat="plainText").execute()

                    for i in data2["items"]:
                        name = i["snippet"]["authorDisplayName"]
                        comment = i["snippet"]["textDisplay"]
                        published_at = i["snippet"]['publishedAt']
                        likes = i["snippet"]['likeCount']
                        replies = ''

                        box.append([name, comment, published_at, likes, replies])

        df = pd.DataFrame({'Name': [i[0] for i in box], 'Comment': [i[1] for i in box], 'Time': [i[2] for i in box],
                           'Likes': [i[3] for i in box], 'Reply Count': [i[4] for i in box]})

        df.to_csv('youtube-comments.csv', index=False, header=False)

        print("Successful! Check the CSV file that you have just created.")

    scrape_comments_with_replies()


def scrape_video(yt_link):
    # Use a breakpoint in the code line below to debug your script.

    from pytube import YouTube

    # where to save.
    # link of the video to be downloaded
    # Replace with the Youtube video link you want to download.
    destination = "C:/Users/Houssem S/Downloads/"


    try:
        video = YouTube(yt_link)
        # filtering the audio. File extension can be mp4/webm
        # You can see all the available streams by print(video.streams)
        audio = video.streams.filter(only_audio=True, file_extension='mp4').first()
        audio.download(destination)
        print('Download Completed!')

    except:
        print("Connection Error")  # to handle exception


# # Press the green button in the gutter to run the script.
if __name__ == '__main__':
     import time
     start_time = time.time()
     yt_link = "https://www.youtube.com/watch?v=rFKxMRTBnUM"
     scrape_video(yt_link)
     scrape_comments(yt_link)
     print("---The execution time is %s seconds ---" % (time.time() - start_time))
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
