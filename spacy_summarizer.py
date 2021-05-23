# import spacy 
# nlp = spacy.blank('en')
# # Pkgs for Normalizing Text
# from spacy.lang.en.stop_words import STOP_WORDS
# from string import punctuation
# # Import Heapq for Finding the Top N Sentences
# from heapq import nlargest



# def text_summarizer(raw_docx):
#     raw_text = raw_docx
#     docx = nlp(raw_text)
#     stopwords = list(STOP_WORDS)
#     # Build Word Frequency # word.text is tokenization in spacy
#     word_frequencies = {}  
#     for word in docx:  
#         if word.text not in stopwords:
#             if word.text not in word_frequencies.keys():
#                 word_frequencies[word.text] = 1
#             else:
#                 word_frequencies[word.text] += 1


#     maximum_frequncy = max(word_frequencies.values())

#     for word in word_frequencies.keys():  
#         word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
#     # Sentence Tokens
#     sentence_list = [ sentence for sentence in docx.sents ]

#     # Sentence Scores
#     sentence_scores = {}  
#     for sent in sentence_list:  
#         for word in sent:
#             if word.text.lower() in word_frequencies.keys():
#                 if len(sent.text.split(' ')) < 30:
#                     if sent not in sentence_scores.keys():
#                         sentence_scores[sent] = word_frequencies[word.text.lower()]
#                     else:
#                         sentence_scores[sent] += word_frequencies[word.text.lower()]


#     summarized_sentences = nlargest(4, sentence_scores, key=sentence_scores.get)
#     final_sentences = [ w.text for w in summarized_sentences ]
#     summary = ' '.join(final_sentences)
#     return summary


import spacy
from spacy.lang.en.stop_words import STOP_WORDS
stopwords=list(STOP_WORDS)
from string import punctuation
punctuation=punctuation+ '\n'

def text_summarizer(raw_docx,num_sentence=3):
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(raw_docx)
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    from heapq import nlargest
    summary=nlargest(num_sentence, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    return summary
