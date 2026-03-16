Personal Are.na (fully local) vector search on my PDF/link/text blocks: it finds the most similar content I've saved based on an input PDF query. The more similar a document, the closer to the center.

1.) Install requirements.txt<br>
2.) add your [Are.na API](https://dev.are.na/documentation) ARENA_ACCESS_TOKEN and your ARENA_USER_ID to an environmental variable file<br>
3.) run `arena_vector_store.py` to create an embedding map of your are.na channels<br>
4.) run `arena_search.py` to serach text via CLI and `arena_search_gui.py` to drag and drop pdfs<br>
