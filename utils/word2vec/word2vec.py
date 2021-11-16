import multiprocessing
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import hjson
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=str,
        default='./word2vec.hjson',
        help="The config path.",
    )
    parser.add_argument(
        "--train_files", type=list, default=['train.txt'], help="train tokenizer files."
    )
    parser.add_argument(
        "--embedding_size",
        type=int,
        default=128,
        help=( "vector size")
    )
    parser.add_argument(
        "--min_count",
        type=int,
        default=10,
        help=( "minist word frequence")
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=0,
        help=( "0 means use all cpus")
    )
    parser.add_argument(
        "--window",
        type=int,
        default=6,
        help=( "window size")
    )
    parser.add_argument(
        "--sg",
        type=bool,
        default=0,
        help=( "use skip gram or not. if set to 0 use cbow")
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=15,
        help=( "training epochs")
    )
    parser.add_argument(
        "--embedding_file",
        type=str,
        default='embedding.txt',
        help=( "embedding file")
    )
    args = parser.parse_args()
    if args.config:
        config_json = hjson.load(open(args.config), object_pairs_hook=dict)
        for key, value in config_json.items():
           setattr(args, key, value) 
    if not args.workers:
        args.workers = multiprocessing.cpu_count()
    # print(args)

    lines = []
    for file in args.train_files:
        lines = lines + list(LineSentence(file))

    model = Word2Vec(lines, vector_size=args.embedding_size, window=args.window, min_count=args.min_count, workers=args.workers, epochs=args.epochs, sg=args.sg)
    model.save(args.model_file)
    model.wv.save_word2vec_format(args.embedding_file, binary=False)