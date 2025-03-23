### Design Notes

---

#### 3-21-2025

**Functionality:**

- static pages containing grammar notes (conjugations, particles, etc)
- front page is a **search**: basically a limited version of jisho, but with tags
  - search result products a list of results, or redirects to the page of the 1 result
  - info displayed on list items is an abbreviated version of the data on each page; can navigate to the page of each result for more info
  - **search for kanji**: searching "kanji:先" will display information about the kanji 先: meaning, readings w/examples, words containing 先 (with links), any tags (with links), notes
    - similar to https://jisho.org/search/%E5%85%88%E3%80%80%23kanji
    - maybe for later: search for multiple kanji
  - **search for words containing a kanji**: searching "先" (no qualifier) will return a list of words containing 先 
    - similar to: https://jisho.org/search/%E5%85%88
  - **search for words**: searching "月曜日" will redirect to vocab page: contains information about 月曜日: meaning, links to constituent kanji, any tags (with links), part of speech, conjugation group + conjugations (if any), notes/usage examples
    - similar to: https://jisho.org/search/%E6%9C%88%E6%9B%9C%E6%97%A5
    - maybe for later: have search match kana readings in addition to kanji (so you don't need to know the kanji)
  - **search for tag**: searching "tag:day" will return a list of everything tagged "day"
    - could include kanji (日) and words (月曜日, etc), need to display them both as list items in some fixed order 
- form pages to **add words and kanji** to the database

**Database Sketch**:

- main tables will contain **words** and **kanji**
- words and kanji can both have multiple **tags**
  - two joins: words/tags (M-M) and kanji/tags (M-M)
- words can have multiple **conjugations** and **kanji**
  - two joins: words/conjugations (1-M) and words/kanji (M-M, w/order column so kanji appear in order on the words page)
- kanji can have multiple **readings**
  - one join: kanji/readings with a type column (on/kun-yomi)

#### 3-23-2025

**Routes**:

- `/`: search page w/search field
  - `GET`: just returns the search page
  - `POST`: searches, returns search page w/rendered results
- `/kanji/{kanji}`: page for a single kanji
  - `GET`: returns the page
- `/word/{word}`: page for a single word
  - `GET`: returns the page
- `/kanji/add`: page w/form to add kanji to db
  - `GET`: returns the blank form
  - `POST`: adds the kanji to db (barring validation), returns to search page
- `/kanji/{kanji}/edit`: page w/form to edit kanji
  - `GET`: returns the edit page
  - `POST`: updates the kanji in db (barring validation), returns to search page
  - `POST`: deletes kanji from db, returns to search page
- `/word/add`: page w/form to add word to db
  - `GET`: returns the blank form
  - `POST`: adds the word to db (barring validation), returns to search page
- `/word/{word}/edit`: page w/form to edit word
  - `GET`: returns the edit page
  - `POST`: updates the word in db (barring validation), returns to search page
  - `POST`: deletes word from db, returns to search page
- `/notes`: page w/links to static content
  - possible example routes: `/notes/verbs`, `/notes/adjectives`, `/notes/particles` etc

**DBD sketch**

![dbd sketch](/dbd.png)

Created in dbdiagram.io:

```
table words {
  id integer [primary key]
  word varchar [not null]
  pronunciation varchar [not null]
  part_of_speech int [not null]
  meaning varchar [not null]
  sentence varchar [not null]
  conjugation_group int
}

table conjugation_groups {
  id integer [primary key]
  conjugation_group varchar [not null]
}

table parts_of_speech {
  id integer [primary key]
  part_of_speech varchar [not null]
}

table kanji {
  id integer [primary key]
  kanji varchar [not null]
  meaning varchar [not null]
}

table readings {
  id integer [primary key]
  kanji_id integer [not null]
  reading_type int [not null]
}

table reading_types {
  id integer [primary key]
  reading_type varchar [not null]
}

table kanji_words {
  id integer [primary key]
  word_id integer [not null]
  kanji_id integer [not null]
  word_order integer [not null]
}

table tags {
  id integer [primary key]
  tag varchar [not null]
}

table tags_words {
  id integer [primary key]
  tag_id integer [not null]
  word_id integer [not null]
}

table tags_kanji {
  id integer [primary key]
  tag_id integer [not null]
  kanji_id integer [not null]
}

Ref words_parts_of_speech: words.part_of_speech > parts_of_speech.id
Ref words_conjugation_groups: words.conjugation_group > conjugation_groups.id
Ref kanji_readings: kanji.id < readings.kanji_id 
Ref reading_reading_types: readings.reading_type > reading_types.id
Ref words_kanji_words: words.id <> kanji_words.word_id
Ref kanji_kanji_words: kanji.id <> kanji_words.kanji_id
Ref tags_tags_words: tags.id < tags_words.tag_id
Ref tags_tags_kanji: tags.id < tags_kanji.tag_id
Ref words_tags_words: words.id < tags_words.word_id
Ref kanji_tags_words: kanji.id < tags_kanji.kanji_id
```