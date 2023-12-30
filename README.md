# WikiNest
#### Video Demo:  <https://youtu.be/JnTWxK1tgcs>
#### Description:
##### Over View: 
WikiNest is an advanced wiki platform designed to harness the power of semantic search and graph databases. Unlike traditional wikis that rely solely on keyword matching, WikiNest provides users with a richer, more contextually relevant search experience.

##### Key Features:

1. **User Registration and Authentication:** Users can securely register and log in to WikiNest, ensuring personalized experiences and data security.
2. **Interactive Dashboard:** Accessible via the navigation bar, the dashboard empowers users to seamlessly add documents of interest directly to the database.
3. **Semantic Search Capability:** At the heart of WikiNest is its semantic search engine. When users enter a query, the system doesn't just match keywords; it understands the context and meaning behind the query. This ensures more accurate and contextually relevant search results.
4. **Graph Database Abstraction:** WikiNest abstracts SQL behind a graph interface to mimic graph databases in order to establish relationships between documents. When a user accesses a particular document, WikiNest showcases related documents, providing a comprehensive view of interconnected information.

##### Benefits:
1. **Knowledge Exploration:** The graph database integration promotes exploration by presenting related documents, allowing users to delve deeper into topics of interest.
2. **Personalized Interaction:** With the ability to add documents to the database, users can curate content tailored to their needs, enhancing their overall experience.


##### Project File Structure and Description:
1. **database:**
   - Uses SQLAlchemy to interact with and store models in the database.

2. **graph_sql:**
   - A wrapper around the database that abstracts it as a graph database.

3. **graph:**
   - Implements a graph data structure for performing algorithms. It's capable of handling weighted graphs and automatically dropping edges below a specified threshold.

4. **fast search:**
   - Implements or uses TF-IDF and Sentence BERT for document retrieval.
   - Contains classes: FastSearchMethod for individual methods and MixedFastSearchMethod that combines TF-IDF and Sentence BERT.
   - Overcame challenges with long document searches by adjusting the weight of TF-IDF based on the target document's size.
   - Wraps these methods in a FastSearch class.
   - Capable of preprocessing and computing similarity matrices of documents, as well as finding top-relevant documents to a given query.

5. **app.py:**
   - Manages web app route redirections, including functionalities for user registration, login, adding new documents, and navigation.

6. **Other files for production and libraries:**
   - scripts/dev.py: Runs yarn dev.
   - static folder: Contains generated CSS and JS file bundles.
   - templates folder: Includes HTML files:
     - 404
     - apology
     - dashboard: Allows users to add new documents with title, primary, and secondary content.
     - index: Home page where users can submit search queries.
     - layout
     - login
     - register
     - result: Page displaying individual documents with related documents listed at the bottom.
     - results: Displays top search results.
   - **Other miscellaneous files:**
     - imports.js
     - imports.styles.js
     - main.css
     - package.json
     - Pipfile
     - postcss.config.cjs
     - rollup.config.js
     - search_engine.py
     - tailwind.config.js
