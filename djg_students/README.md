# Requirements

__This project required typst for the pdf rendering!__ 

You will receive error messages, if typst is
not installed and not added to your PATH. You can find more information about installing typst directly on the
[Github Repo](https://github.com/typst/typst).

# Quick explainer

This is a very basic tech demo of dynamic pdf generation based on forms and models.
It expands on the students task presented to us in the lecture and uses those files as a base.

Using typst and a custom template, the information from the lectures and the registered
students is filled into the template. The completed template is then compiled using typst
and you receive a pdf as well as the typ file in the download folder in the app directory itself.
That pdf is also displayed inline in the browser to avoid double-downloading on Windows due to the
header values.