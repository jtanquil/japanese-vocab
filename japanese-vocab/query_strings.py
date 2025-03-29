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
