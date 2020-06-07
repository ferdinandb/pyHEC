"""
Natural Language Processing (NLP) with spaCy
--------------------------------------------

A simple example using spaCy to process a number of "documents". The more documents you
process in parallel, the greater the increase in processing speed.

You could also generate the spaCy NLP object in __name__ == '__main__' and pass it to the
parallel processing function as a keyword argument. Doing so comes with a significant
overhead and increases the processing time of the small dummy data set noticeable. If a
huge amount of data is processed, the overhead turns marginal.
"""

from pyhec import parallel_processing as pp
import spacy
import pandas as pd


def tokenize_files(docs):
    print(' - tokenize_output() called.')
    # The output will be returned as a list of lists. One list item per document and one
    # list item per token
    output = []

    #  Load the spaCy NLP object. In practice, we would also override the spaCy's default
    #  stop word list here and replace it with our own stopwords.
    nlp = spacy.load('en_core_web_sm')

    # We use spaCy's language processing pipelines to increase efficiency. Please see the
    # docs for more information: https://spacy.io/usage/processing-pipelines
    for doc in nlp.pipe(docs, disable=['tagger', 'parser', 'ner']):
        # Add the tokens to the output list
        output.append([token.text for token in doc])

    return output


if __name__ == '__main__':
    # We use a random eBook from the Project Gutenberg and paste the first few paragraphs
    # as a list. In reality, one list item would be represented by a TXT file and not a
    # single sentence. Source: http://www.gutenberg.org/files/62240/62240-0.txt
    DOCUMENTS = [
        'The condition of a nation, socially and politically, is to a great extent decided by the character of its religious teaching and worship.',
        'The history of our own country, and that of every other in the world, affords many striking illustrations of the fact.',
        'Many instances might be quoted where the connection is remarkably verified, and we venture to ascribe the proud position of England mainly to the operation of its Christian faith.',
        'The churches of Britain were the outbirths of its religious life. They were reared by the earnest piety of our forefathers.',
        'Their history presents an inviting sphere of investigation, from the valuable aid they furnish, in tracing the successive incidents and onward development of Christianity;',
        'which soon after its first promulgation, diffused a welcome light over the Pagan darkness, which enveloped the primeval inhabitants of our country.',
        'The subject of the first introduction of Christian truth into Britain, and who was the first herald employed by Providence in proclaiming it, is one of deep interest, and has long engaged the investigation of the learned.',
        'The theories which have been offered are conflicting, as to the time, and by whom, this great boon was conferred upon our country.',
        'But as all the varied traditions seem to point to the apostolic age, we may the more readily acquiesce, in not being able to fix upon the exact period and the actual instrument;',
        'especially when we remember, how many of the world’s benefactors have been unknown to those who are most indebted to them.'
    ]

    # Tokenize the text documents in parallel. We convert the list of documents to a pandas
    # series. Doing so keeps the chunk sizes bigger and makes the processing more efficient
    # in the given case. In reality, you have to test, which option is faster.
    tokenized_output = pp.parallelize(tokenize_files, pd.Series(DOCUMENTS))
    print(tokenized_output)


