import deliciousapi
dapi = deliciousapi.DeliciousAPI()
url = "http://www.michael-noll.com/wiki/Del.icio.us_Python_API"
username = "go2delicious"

# web pages shown on the front page of Delicious.com aka the 'hotlist'
featured_links = dapi.get_urls()

# popular web pages tagged with "photography"
popular_photography_links = dapi.get_urls(tag="photography")

# web pages recently tagged with "web2.0", up to a maximum of
# 300 URLs if possible; note that get_urls() cannot guarantee
# that the list of URLs is free of duplicate items - this is
# due to the way Delicious.com generates the regular feeds for
# a given tag (i.e. /tag/<tag> as opposed to /popular/<tag>)
recent_web20_links = dapi.get_urls(tag="web2.0", popular=False, max_urls=300)

# DeliciousURL object, providing
#     .title : title of the web document as stored on delicious.com
#     .url   : URL of the corresponding web document
#     .total_bookmarks: total number of bookmarks/users for this url
#     .bookmarks  : list of (user, tags, comment, timestamp) tuples
#     .top_tags: list of (tag, tag_count) tuples, representing the
#                most popular tags of this url (up to 10)
#     .tags       : dict mapping tags to total tag count
#
#
# Note that by default, get_url() does only retrieve the
# 50 most recent bookmarks of a given url. You can control
# this behavior with the max_bookmarks parameter (see
# docstrings).
url_metadata = dapi.get_url(url)

print url_metadata
# output: [http://www.michael-noll.com/wiki/Del.icio.us_Python_API] 103 total bookmarks (= users), 187 tags (37 unique), 10 out of 10 max 'top' tags

# print url_metadata.title
# output: Del.icio.us Python API - Michael G. Noll

print url_metadata.bookmarks
# output: [
#  (u'neetij', [u'python', u'api', u'del.icio.us', u'programming'], None, datetime.datetime(2008, 8, 4, 0, 0)),
#  (u'jsf.online', [u'software', u'programming', u'free', u'development', u'del.icio.us', u'python', u'2008'], u'Python API - wraps the del.icio.us api for python', datetime.datetime(2008, 8, 4, 0, 0)),
#  (u'as11018', [u'python', u'api', u'programming'], None, datetime.datetime(2008, 7, 30, 0, 0)),
#  ...]
print url_metadata.top_tags
# output: [ (u'python', 91), (u'api', 73), (u'del.icio.us', 71), ... ]

print url_metadata.tags
# output : { u'is:api': 1, u'code': 6, u'toread': 1, ... }

# If get_user() is called with both username and password, the full
# bookmark collection of the user is returned, including any private
# bookmarks. Communication is encrypted via SSL. You can use get_user()
# for creating a backup of your Delicious.com bookmarks.
#
# If get_user() is called without password, only the most recent
# public bookmarks of the given user are returned (up to 100).
#
# DeliciousUser object, providing
#     .bookmarks  : list of (url, tags, title, notes, timestamp) tuples
#     .tags       : dict mapping tags to total tag count
#     .username   : name of the corresponding del.icio.us user
user_metadata = dapi.get_user(username)

print user_metadata
# output: [jsmith] 31 bookmarks, 78 tags (45 unique)

print user_metadata.bookmarks
# output: [ (u'http://www.twellow.com/', [u'mashup', u'tools', u'twitter'], u'Twellow.com :: Twitter users organized into business categories', u'Kind of yellow pages for Twitter, interesting.', datetime.datetime(2008, 6, 25, 0, 0, 0)), ... ]

# list of (tag, tag_count) tuples
user_tags = dapi.get_tags_of_user(username)
print user_tags
# output: { 'golf': 1, 'toread': 11, 'recipe': 1, 'rest': 4, ... }
