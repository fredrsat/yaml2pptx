"""Script to create the default template. Run once: python scripts/create_default_template.py"""

from pptx import Presentation

# The default Presentation() already contains standard layouts:
# [0] Title Slide, [1] Title and Content, [2] Section Header,
# [3] Two Content, [4] Comparison, [5] Title Only,
# [6] Blank, [7] Content with Caption, [8] Picture with Caption, etc.
prs = Presentation()
prs.save("templates/default.pptx")
print("Created templates/default.pptx")
