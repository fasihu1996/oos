#let lecture_report(lecture_data) = {{
  set document(title: lecture_data.title, author: "Studentenverwaltung")
  set page(
    paper: "a4",
    margin: (x: 2.5cm, y: 2cm),
    header: align(right)[Lecture Report],
    numbering: "1",
  )

  align(center)[
    #block(text(weight: "bold", size: 20pt, lecture_data.title))
    #v(1em)
    #text(style: "italic", lecture_data.description)
    #v(2em)
  ]

  heading(level: 1, "Lecture Details")

  let info = table(
    columns: (auto, 1fr),
    inset: 10pt,
    stroke: none,
    [*Title:*], [#lecture_data.title],
    [*Description:*], [#lecture_data.description],
    [*Total Students:*], [#str(lecture_data.student_count)]
  )

  info
  v(1em)

  heading(level: 1, "Enrolled Students")

  if lecture_data.student_count == 0 {{
    [No students are currently enrolled in this lecture.]
  }} else {{
    lecture_data.table_rows
  }}
}}

#lecture_report(
{typst_data}
)