query_strings = {
  "get_word_list": """
    SELECT * FROM words
    WHERE word LIKE (?)
    """,
  "get_word_meanings" : """
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
  "get_kanji_words": """
    SELECT
      GROUP_CONCAT(k.kanji, ', ') kanji
    FROM kanji k
    JOIN kanji_words kw
    ON k.id = kw.kanji_id
    WHERE kw.word_id = (?)
    GROUP BY kw.word_id
    """,
  "get_word_furigana": """
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
  "get_word_tags": """
    SELECT
      GROUP_CONCAT(t.tag, ', ') tag
    FROM tags t
    JOIN tags_words tw
    ON t.id = tw.tag_id
    WHERE tw.word_id = (?)
    """,
}