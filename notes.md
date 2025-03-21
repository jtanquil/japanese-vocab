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