def get_posts_details(rss=None):
  
    """
    Take link of rss feed as argument
    """
    if rss is not None:
      
          # import the library only when url for feed is passed
        import feedparser
        
        # parsing blog feed
        blog_feed = blog_feed = feedparser.parse(rss)
        
        # getting lists of blog entries via .entries
        posts = blog_feed.entries
        
        # dictionary for holding posts details
        posts_details = {"Blog title" : blog_feed.feed.title,
                        "Blog link" : blog_feed.feed.link}
        
        post_list = []
        
        # iterating over individual posts
        for post in posts:
            for i in post:
                print(i)
            temp = dict()
            
            # if any post doesn't have information then throw error.
            try:
                temp["title"] = post.title
                temp["link"] = post.link
                temp["pubDate"] = post.published
            except:
                pass
            
            post_list.append(temp)
        
        # storing lists of posts in the dictionary
        posts_details["posts"] = post_list 
        
        return posts_details # returning the details which is dictionary
    else:
        return None

if __name__ == "__main__":
    import json
    url="https://isthereanydeal.com/feeds/IN/giveaways.rss"        
    data = get_posts_details(rss = url) # return blogs data as a dictionary
    
    if data:
        # printing as a json string with indentation level = 2
        print(json.dumps(data, indent=2)) 
    else:
        print("None")