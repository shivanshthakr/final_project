import array
import string
import operator

#Natural Language Processing Libraries
import nltk
#nltk.download() 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

from urllib.request import urlopen


#from gensim.summarization import summarize
from flask import Flask, render_template, request #Used to render .html templates


#spacy summarizer
from spacy_summarizer import text_summarizer
from sumy_summarizer import sumy_summarization

#bert summarizer
from bs4 import BeautifulSoup

#for newspaper stuff
from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import pandas as pd
app=Flask(__name__)

class summarize:

	def get_summary(self, input, max_sentences):
		sentences_original = sent_tokenize(input)

		#Remove all tabs, and new lines
		if (max_sentences > len(sentences_original)):
			print ("Error, number of requested sentences exceeds number of sentences inputted")
			#Should implement error schema to alert user.
		s = input.strip('\t\n')
		
		#Remove punctuation, tabs, new lines, and lowercase all words, then tokenize using words and sentences 
		words_chopped = word_tokenize(s.lower())
		
		sentences_chopped = sent_tokenize(s.lower())

		stop_words = set(stopwords.words("english"))
		punc = set(string.punctuation)

		#Remove all stop words and punctuation from word list. 
		filtered_words = []
		for w in words_chopped:
			if w not in stop_words and w not in punc:
				filtered_words.append(w)
		total_words = len(filtered_words)
		
		#Determine the frequency of each filtered word and add the word and its frequency to a dictionary (key - word,value - frequency of that word)
		word_frequency = {}
		output_sentence = []

		for w in filtered_words:
			if w in word_frequency.keys():
				word_frequency[w] += 1.0 #increment the value: frequency
			else:
				word_frequency[w] = 1.0 #add the word to dictionary

		#Weighted frequency values - Assign weight to each word according to frequency and total words filtered from input:
		for word in word_frequency:
			word_frequency[word] = (word_frequency[word]/total_words)

		#Keep a tracker for the most frequent words that appear in each sentence and add the sum of their weighted frequency values. 
		#Note: Each tracker index corresponds to each original sentence.
		tracker = [0.0] * len(sentences_original)
		for i in range(0, len(sentences_original)):
			for j in word_frequency:
				if j in sentences_original[i]:
					tracker[i] += word_frequency[j]

		#Get the highest weighted sentence and its index from the tracker. We take those and output the associated sentences.
		
		for i in range(0, len(tracker)):
			
			#Extract the index with the highest weighted frequency from tracker
			index, value = max(enumerate(tracker), key = operator.itemgetter(1))
			if (len(output_sentence)+1 <= max_sentences) and (sentences_original[index] not in output_sentence): 
				output_sentence.append(sentences_original[index])
			if len(output_sentence) > max_sentences:
				break
			
			#Remove that sentence from the tracker, as we will take the next highest weighted freq in next iteration
			tracker.remove(tracker[index])
		
		sorted_output_sent = self.sort_sentences(sentences_original, output_sentence)
		return (sorted_output_sent)

	# @def sort_senteces:
	# From the output sentences, sort them such that they appear in the order the input text was provided.
	# Makes it flow more with the theme of the story/article etc..
	def sort_sentences (self, original, output):
		sorted_sent_arr = []
		sorted_output = []
		for i in range(0, len(output)):
			if(output[i] in original):
				sorted_sent_arr.append(original.index(output[i]))
		sorted_sent_arr = sorted(sorted_sent_arr)

		for i in range(0, len(sorted_sent_arr)):
			sorted_output.append(str(original[sorted_sent_arr[i]]))
		return sorted_output











######   --------------  home page   ------------------   #####
@app.route('/',methods=['GET','POST'])
def hello_world():
	if request.method=='GET':
		return render_template('index.html',enter=True)
	else:
		text=request.form['originalText'] #Get text from html
		max_value=sent_tokenize(text)
		num_sent = int(request.form['num_sentences']) #Get number of sentence required in summary
		summary=text_summarizer(text,num_sent)
		print(summary)
		return render_template('index.html',t1=request.form['originalText'],value=False,output_summary=summary)


######    ----------------compare page --------------------     ######
@app.route('/compare_summarizer',methods=['GET','POST'])
def comparsion():
	if request.method=='GET':
		return render_template('comparsion.html' ,enter=True)
	else:
		inputtext=request.form['summCompare']
		sum2=summarize()
		nltk_list=sum2.get_summary(inputtext,3)
		nltk_summary=''.join(nltk_list)
		spacy_summary=text_summarizer(inputtext)
		sumy_summary=sumy_summarization(inputtext)
		return render_template('comparsion.html',original=inputtext,enter=False,gen_sum=nltk_summary,sp_sum=spacy_summary,sumy_sum=sumy_summary)

	  
########### ---------------newssummary--------------------------- ###########
@app.route('/news_summary', methods=['GET','POST'])
def urlandpdf():
	if request.method=='GET':
		return render_template('newsarticle.html',enter=True)
	else:
		googlenews=GoogleNews()
		googlenews.search(request.form['newsWord'])
		result=googlenews.result()
		df=pd.DataFrame(result)
		list=[]
		for ind in df.index:
			dict={}
			article = Article(df['link'][ind])
			article.download()
			article.parse()
			article.nlp()
			dict['Date']=df['date'][ind]
			dict['Media']=df['media'][ind]
			dict['Title']=article.title
			dict['Article']=article.text
			dict['Summary']=article.summary
			list.append(dict)
		return render_template('newsarticle.html',title=list[0]['Title'],text=list[0]['Article'],summ=list[0]['Summary'])




################--------------linkSummary----------------------- ##############
@app.route('/link_summary',methods=['GET','POST'])
def fetch_and_analayse():
	if request.method=='GET':
		return render_template('link_summary.html',enter=True)
	else:
		url=request.form['raw_url']
		page = urlopen(url)
		soup = BeautifulSoup(page)
		fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
		max_value = sent_tokenize(fetched_text)
		summary = text_summarizer(fetched_text, 3)
		return render_template('link_summary.html',enter=False,original_text = fetched_text, output_summary = summary)


if __name__=='__main__':
	app.run(debug=True)