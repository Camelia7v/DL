import warnings
import nltk.translate.bleu_score as bleu
warnings.filterwarnings('ignore')


reference = [
    'He who wakes up early in the morning and eats breakfast will get far away'.split()
]

translation = 'Whoever wakes up early in the morning and eats breakfast gets far'.split()
print('BLEU score: {}'.format(bleu.sentence_bleu(reference, translation)))
