import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
def sumy_summarization(rawtext):
    parser = PlaintextParser.from_string(rawtext,Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summ1 = summarizer(parser.document, 3)
    list=[]
    for s1 in summ1:
        list.append(str(s1))
    summary=''.join(list)
    return summary
