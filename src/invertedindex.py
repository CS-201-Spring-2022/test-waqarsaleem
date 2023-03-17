import math
from document import Document


class InvertedIndex:
    def __init__(self, docs: [Document]):
        index = dict()
        for doc in docs:
            doc_id = doc.doc_id
            tf_vector = self.get_tf_vector(doc, normalize=True)
            for t, f in tf_vector:
                index[t] = {**index.get(t, dict()), doc_id: f}
        idf_vector = self.get_idf_vector(index, len(docs))
        for t, idf in idf_vector:
            for doc_id in index[t]:
                index[t][doc_id] *= idf
        self.index = index

    def get_tf_vector(self, doc: Document, normalize: bool = True):
        terms = list(doc)
        tf = [len(doc[term]) for term in terms]
        if normalize:
            tf_total = sum(tf)
            tf = [f/tf_total for f in tf]
        return zip(terms, tf)

    def get_idf_vector(self, index: dict, n: int):
        df_vector = [(t, len(docs)) for t, docs in index.items()]
        return [(t, math.log(n/df, 10)) for t, df in df_vector]

    def query(self, terms: str, k: int):
        terms = terms.strip().split()
        relevance = dict()
        for term in terms:
            if term not in self.index:
                continue
            for doc, score in self.index[term].items():
                relevance[doc] = relevance.get(doc, 0) + score
        result = list(map(lambda x:(x[1],x[0]), relevance.items()))
        result = sorted(result, reverse=True)
        return [(i+1, pair[1]) for i, pair in enumerate(result)][:k]
