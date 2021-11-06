import lucene
import os
from java.nio.file import Paths, Path
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.analysis.core import StopAnalyzer
from org.apache.lucene.search import IndexSearcher, TopDocs, ScoreDoc
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import FSDirectory, RAMDirectory

lucene.initVM()
directory = FSDirectory.open(Paths.get('./lucene/index'))
# directory = RAMDirectory()

analyzer = StopAnalyzer()
cf = IndexWriterConfig(analyzer)
cf.setOpenMode(IndexWriterConfig.OpenMode.CREATE)

writer = IndexWriter(directory, cf)

"""*** START CODE HERE ***"""
CRANFIELD_DIR = './Cranfield'
idx = 0
for file in os.listdir(CRANFIELD_DIR):
    idx += 1
    f = open(os.path.join(CRANFIELD_DIR, file))
    text = f.read()
    doc = Document()
    index = StringField('index', str(idx), Field.Store.YES)
    content = TextField('content', text, Field.Store.YES)
    doc.add(index)
    doc.add(content)
    writer.addDocument(doc)

"""*** END CODE HERE ***"""
writer.close()

reader = DirectoryReader.open(directory)
searcher = IndexSearcher(reader)
parser = QueryParser('content', analyzer)

keywords = [
    'what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft .',
    'what are the structural and aeroelastic problems associated with flight of high speed aircraft .'
]

for keyword in keywords:
    print('======================')
    print('Querying <', keyword, '> ... ', sep='')
    query = parser.parse(keyword)
    doclist = searcher.search(query, 50)
    docs = doclist.scoreDocs

    for item in docs:
        doc = searcher.doc(item.doc)
        print(doc.get('index'), item.score)
    print()