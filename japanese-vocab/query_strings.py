# query is the db query
# col_groups tell get_result_list how to parse the columns
# if the value is none, then the column is a single value
# if the value is a list, then the column should be a nested dict
# w/the id as the key, and the list elements as keys
vocab_query = {
  "query": """
    SELECT
      w.id id,
      w.word,
      wm.id word_meaning_id,
      wm.meaning,
      wm.example,
      ps.part_of_speech,
      cg.conjugation_group,
      kw.id kanji_id,
      k.kanji,
      kw.word_order kanji_word_order,
      wf.id word_furigana_id,
      wf.word_part,
      wf.word_order furigana_word_order,
      wf.furigana,
      t.id tag_id,
      t.tag
    FROM words w
    JOIN words_meanings wm
    ON w.id = wm.word_id
    LEFT JOIN conjugation_groups cg
    ON wm.conjugation_group_id = cg.id
    JOIN parts_of_speech ps
    ON wm.part_of_speech_id = ps.id
    JOIN words_furigana wf
    ON w.id = wf.word_id
    JOIN kanji_words kw
    ON w.id = kw.word_id
    JOIN kanji k
    ON kw.kanji_id = k.id
    JOIN tags_words tw
    ON tw.word_id = w.id
    JOIN tags t
    ON tw.tag_id = t.id
    WHERE w.word LIKE (?)
    ORDER BY w.id
    """,
  "col_groups": {
    "id": None,
    "word": None,
    "word_meaning_id": 
      ["meaning", "example", "part_of_speech", "conjugation_group"],
    "word_furigana_id":
      ["word_part", "furigana", "furigana_word_order"],
    "kanji_id":
      ["kanji", "kanji_word_order"],
    "tag_id":
      ["tag"]
  }
}

kanji_query = {
  "query": """
    SELECT
      k.id id,
      k.kanji,
      k.meaning,
      r.id reading_type_id,
      r.reading,
      rt.reading_type,
      t.id tag_id,
      t.tag tag,
      kw.word_id word_id,
      w.word word
    FROM kanji k
    JOIN readings r
    ON k.id = r.kanji_id
    JOIN reading_types rt
    ON r.reading_type_id = rt.id
    LEFT JOIN tags_kanji tk
    ON k.id = tk.kanji_id
    LEFT JOIN tags t
    ON tk.tag_id = t.id
    JOIN kanji_words kw
    ON k.id = kw.kanji_id
    JOIN words w
    ON kw.word_id = w.id
    WHERE k.kanji LIKE (?)
  """,
  "col_groups": {
    "id": None,
    "kanji": None,
    "meaning": None,
    "reading_type_id":
      ["reading", "reading_type"],
    "word_id":
      ["word"],
    "tag_id":
      ["tag"]
  }
}

tag_query = {
  "query": [
    {
      "query": """
        SELECT
          w.id id,
          w.word,
          wm.id word_meaning_id,
          wm.meaning,
          wm.example,
          ps.part_of_speech,
          cg.conjugation_group,
          kw.id kanji_id,
          k.kanji,
          kw.word_order kanji_word_order,
          wf.id word_furigana_id,
          wf.word_part,
          wf.word_order furigana_word_order,
          wf.furigana,
          t.id tag_id,
          t.tag
        FROM words w
        JOIN words_meanings wm
        ON w.id = wm.word_id
        LEFT JOIN conjugation_groups cg
        ON wm.conjugation_group_id = cg.id
        JOIN parts_of_speech ps
        ON wm.part_of_speech_id = ps.id
        JOIN words_furigana wf
        ON w.id = wf.word_id
        JOIN kanji_words kw
        ON w.id = kw.word_id
        JOIN kanji k
        ON kw.kanji_id = k.id
        JOIN tags_words tw
        ON tw.word_id = w.id
        JOIN tags t
        ON tw.tag_id = t.id
        WHERE t.tag = ?
        ORDER BY w.id
        """,
      "col_groups": vocab_query['col_groups']
    },
    {
      "query": """
        SELECT
          k.id id,
          k.kanji,
          k.meaning,
          r.id reading_type_id,
          r.reading,
          rt.reading_type,
          t.id tag_id,
          t.tag tag,
          kw.word_id word_id,
          w.word word
        FROM kanji k
        JOIN readings r
        ON k.id = r.kanji_id
        JOIN reading_types rt
        ON r.reading_type_id = rt.id
        LEFT JOIN tags_kanji tk
        ON k.id = tk.kanji_id
        LEFT JOIN tags t
        ON tk.tag_id = t.id
        JOIN kanji_words kw
        ON k.id = kw.kanji_id
        JOIN words w
        ON kw.word_id = w.id
        WHERE t.tag = ?
        """,
      "col_groups": kanji_query['col_groups']
    }
  ]
}