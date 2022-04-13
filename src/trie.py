from document import Document


class TrieNode:
    def __init__(self):
        self.child = dict()
        self.pos = None

    def __getitem__(self, key: str):
        return self.child.get(key, None)

    def __setitem__(self, key: str, value):
        self.child[key] = value

    def __contains__(self, key: str):
        return key in self.child

    def __iter__(self):
        yield from self.child


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def add_document(self, doc: Document):
        for term in doc:
            positions = [(doc.doc_id, start, end) for start, end in doc[term]]
            self.add_term(term, positions)

    def add_term(self, term: str, positions):
        node = self.root
        for char in term:
            if char not in node:
                node[char] = TrieNode()
            node = node[char]
        if node.pos:
            node.pos += positions
        else:
            node.pos = positions

    def prefix_complete(self, prefix: str, node: TrieNode = None,
                        word: str = ''):
        if not node:
            node = self.root
        if prefix:
            char = prefix[0]
            if char in node:
                return self.prefix_complete(prefix[1:], node[char], word+char)
            else:
                return dict()
        pos = dict()
        if node.pos:
            pos[word] = node.pos
        for char in node:
            pos.update(self.prefix_complete('', node[char], word+char))
        return pos
