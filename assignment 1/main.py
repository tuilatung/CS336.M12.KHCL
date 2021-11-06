import lucene
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
doc = Document()
field = StringField('field','Modern Computer Architecture', Field.Store.YES)
author = TextField('author','James Harrison', Field.Store.YES)
content = TextField('content', 'computer architecture, modern RAM, CPU speed, hard drive capacity, easy to use.', Field.Store.NO)
doc.add(field)
doc.add(author)
doc.add(content)
writer.addDocument(doc)

doc = Document()
field = StringField('field','Fashion in Use', Field.Store.YES)
author = TextField('author','James Smith', Field.Store.YES)
content = TextField('content', 'white shirt, hard hat, modern hair styles, easy to work', Field.Store.NO)
doc.add(field)
doc.add(author)
doc.add(content)
writer.addDocument(doc)


doc = Document()
field = StringField('field','Safety in Transportation', Field.Store.YES)
author = TextField('author','Smith Johnson', Field.Store.YES)
content = TextField('content', 'drunk driver, high speed vehicle architectures, carelessly drive, modern designed cars, smith', Field.Store.NO)
doc.add(field)
doc.add(author)
doc.add(content)
writer.addDocument(doc)
writer.close()

reader = DirectoryReader.open(directory)
searcher = IndexSearcher(reader)
parser = QueryParser('content', analyzer)
query = parser.parse('modern author:James')
doclist = searcher.search(query, 3)
docs = doclist.scoreDocs

for item in docs:
    doc = searcher.doc(item.doc)
    print(doc.get('field'), doc.get('author'), item.score)