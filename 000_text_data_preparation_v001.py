# This program demonstrates the capabilities of Python
# for processing text... data munging. The typical web
# page contains tagged text, references to css formatting,
# and calls to JavaScript programs. Extracting meaningful
# text from web pages is a big job... a job made easier
# with the capabilities of Python modules re for regular
# expressions and Beautiful Soup for html text parsing.

# Bring in Python modules for file and text manipulation
from bs4 import BeautifulSoup  # DOM html manipulation
import os  # operating system commands
import re  # regular expressions
import nltk  # draw on the Python natural language toolkit

# define list of codes to be dropped from document
# carriage-returns, line-feeds, tabs
codelist = ['\r', '\n', '\t']    

# there are certain words we will ignore in subsequent
# text processing... these are called stop-words 
# and they consist of prepositions, pronouns, and 
# conjunctions, interrogatives, ...
# we begin with the list from the natural language toolkit
nltk.download('stopwords')
# let's look at that list 
print(nltk.corpus.stopwords.words('english'))

# remove negations from standard stopwords list
# negations can be important in sentiment analysis
negations = ['no', 'nor', 'not']
oldlist = nltk.corpus.stopwords.words('english')
newlist = [x for x in oldlist if x not in negations ]

# there are also extensions and character strings 
# common to web pages that we will ingore
# note that many additional words and character strings
# could be added to this list....
my_stoplist = ['js','url','png','jpg','jpeg','gif','hover','em','px','pdf',\
    'header','footer','padding','ie','tm']
stoplist = newlist + my_stoplist   

# web page parsing function for creating text document 
def page_parse(string):
    # replace non-alphanumeric with space 
    temp_string = re.sub('[^a-zA-Z]', '  ', string)    
    # replace codes with space
    for i in range(len(codelist)):
        stopstring = ' ' + codelist[i] + '  '
        temp_string = re.sub(stopstring, '  ', temp_string)      
    # replace single-character words with space
    temp_string = re.sub('\s.\s', ' ', temp_string)   
    # convert uppercase to lowercase
    temp_string = temp_string.lower()    
    # replace selected character strings/stop-words with space
    for i in range(len(stoplist)):
        stopstring = ' ' + stoplist[i] + ' '
        temp_string = re.sub(stopstring, ' ', temp_string)        
    # replace multiple blank characters with one blank character
    temp_string = re.sub('\s+', ' ', temp_string)    
    return(temp_string)    

# initialize count of results files
nfiles = 0
# identify all of the directory names 
dir_names = [name for name in 
    os.listdir('/Users/northwestern/Desktop/435_Assignment_5_Text_Clustering/data_from_web_analytics_blogs/')
    if os.path.isdir(os.path.join('/Users/northwestern/Desktop/435_Assignment_5_Text_Clustering/data_from_web_analytics_blogs/', name))]
print('\nInput Directory Names')   
# create a directory for the results... called results
os.mkdir('/Users/northwestern/Desktop/000_html_work_v003/' + 'results') 
print(dir_names)
for input_dir in dir_names:
    # indentify all html files in this directory
    html_names = None  # initialize file name list for this directory
    html_names = [name for name in 
        os.listdir(os.path.join('/Users/northwestern/Desktop/435_Assignment_5_Text_Clustering/data_from_web_analytics_blogs/', input_dir)) 
        if name.endswith('.html')]
    print('\nWorking on directory: ')
    print(input_dir)
    print(html_names)
    # work on files one at a time
    for input_file in html_names:
        # read in the html file
        this_dir = os.path.join('/Users/northwestern/Desktop/435_Assignment_5_Text_Clustering/data_from_web_analytics_blogs/', input_dir)
        with open(os.path.join(this_dir, input_file),'r') as my_html:
            my_stuff = BeautifulSoup(my_html)
            
            # remove JavaScript code from Beautiful Soup page object
            [x.extract() for x in my_stuff.find_all('script')]
                        
#            # extract information within paragraph tags	
#            my_paragraphs = my_stuff.find_all('p')
            
            # create text string from the paragraphs
            my_page_text = BeautifulSoup.get_text(my_stuff) 
            
            # parse the text to prepare for subsequent document processing
            my_document = page_parse(my_page_text)
           
            # write text to new files with extension .txt
            blog_id = re.sub('nodejs_opinion_crawler_v', 'blog_', input_dir) 
            output_file_name = blog_id + '_' + re.sub('.html', '.txt', input_file)
            output_file = '/Users/northwestern/Desktop/435_Assignment_5_Text_Clustering/results/' + output_file_name
            with open(output_file, 'wt') as f:
                f.write(str(my_document))
                nfiles = nfiles + 1
                
print('\n\nRUN COMPLETE ' + str(nfiles) + ' files in total (see directory <results>)')                