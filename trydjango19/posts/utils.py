import re
import datetime

from django.utils.html import strip_tags

def count_words(html_string):
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words)
    print("count: {}".format(count))
    return count

def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = count / 200.0 # assuming read 200 words per min
    read_time_sec = read_time_min * 60
    print("SEC: {}".format(read_time_sec))
    read_time = str(datetime.timedelta(seconds=read_time_sec))
    print("DATETIME: {}".format(read_time))
    return read_time