import lemmatizer
from nltk.corpus import gutenberg

print(
    lemmatizer.lemmatize(
        gutenberg.raw("shakespeare-caesar.txt")[0:500]
    )
)