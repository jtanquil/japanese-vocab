aggregate_cols = {
  "word_meaning_id": 
    ["meaning", "example", "part_of_speech", "conjugation_group"],
  "word_furigana_id":
    ["word_part", "furigana", "furigana_word_order"],
  "kanji_word_id":
    ["kanji", "kanji_word_order"],
  "reading_type_id":
    ["reading", "reading_type"]
}

get_vocab = """
  SELECT
    w.id word_id,
    w.word,
    wm.id word_meaning_id,
    wm.meaning,
    wm.example,
    ps.part_of_speech,
    cg.conjugation_group,
    kw.id kanji_word_id,
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
  """

get_kanji = """
  SELECT
    k.id kanji_id,
    k.kanji,
    k.meaning,
    r.id reading_type_id,
    r.reading,
    rt.reading_type,
    t.id tag_id,
    t.tag tag,
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
"""

get_tag = """"""

vocab = {
  "get_result_list": """
    SELECT * FROM words
    WHERE word LIKE (?)
    """,
  "joins": [
    """
    SELECT
      GROUP_CONCAT(wm.meaning, ', ') meaning,
      GROUP_CONCAT(wm.example, ', ') example,
      GROUP_CONCAT(p.part_of_speech, ', ') part_of_speech
    FROM words_meanings wm
    JOIN parts_of_speech p
    ON p.id = wm.part_of_speech_id
    WHERE wm.word_id = (?)
    GROUP BY wm.word_id
    """,
    """
    SELECT
      GROUP_CONCAT(k.kanji, ', ') kanji
    FROM kanji k
    JOIN kanji_words kw
    ON k.id = kw.kanji_id
    WHERE kw.word_id = (?)
    GROUP BY kw.word_id
    """,
    """
    SELECT
      GROUP_CONCAT(wf.word_part, ', ') word_part,
      GROUP_CONCAT(wf.furigana, ', ') furigana
    FROM words_furigana wf
    JOIN words w
    ON wf.word_id = w.id
    WHERE w.id = (?)
    GROUP BY w.id
    ORDER BY wf.word_order
    """,
    """
    SELECT
      GROUP_CONCAT(t.tag, ', ') tag
    FROM tags t
    JOIN tags_words tw
    ON t.id = tw.tag_id
    WHERE tw.word_id = (?)
    """
  ]
}

kanji = {
  "get_result_list": """
    SELECT * FROM kanji
    WHERE kanji LIKE (?)
    """,
  "joins": [
    """
    SELECT
      GROUP_CONCAT(r.reading, ', ') reading,
      rt.reading_type
    FROM readings r
    JOIN reading_types rt
    ON r.reading_type_id = rt.id
    WHERE r.kanji_id = (?)
    GROUP BY reading_type
    """,
    """
    SELECT
      GROUP_CONCAT(t.tag, ', ') tag
    FROM tags t
    JOIN tags_kanji tk
    ON t.id = tk.tag_id
    WHERE tk.kanji_id = (?)
    """,
    """
    SELECT
      w.word
    FROM kanji k
    JOIN kanji_words kw
    ON k.id = kw.kanji_id
    JOIN words w
    ON kw.word_id = w.id
    WHERE k.id = (?)
    """
  ]
}

tag = {
  "get_result_list": """
    SELECT * FROM tags
    WHERE tag = (?)
    """,
  "joins": [
  ]
}

