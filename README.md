# yaml2pptx

Generate PowerPoint presentations from YAML files. Define your slides declaratively — version-controlled, reproducible, and template-free.

## Installation

```bash
pip install -e .
```

## Quick Start

```bash
# Build a presentation using the component renderer (themed slides)
yaml2pptx build presentation.yaml

# Build and open immediately
yaml2pptx build presentation.yaml --open

# Use the template-based renderer
yaml2pptx gen presentation.yaml -t template.pptx

# Inspect a PowerPoint template's layouts
yaml2pptx inspect template.pptx
```

## Commands

| Command | Description |
|---------|-------------|
| `build` | Component-based renderer — builds slides from free-form shapes using a theme |
| `gen` | Template-based renderer — uses .pptx templates with placeholders |
| `inspect` | Shows layouts and placeholders in a .pptx template |
| `init` | Creates a starter YAML file |

## YAML Structure

```yaml
output: "output.pptx"             # Output filename
metadata:
  title: "Presentation Title"
  author: "Author Name"
  subject: "Subject"
theme: "default"                    # Theme name (default: "default")
theme_config:
  organization: "Organization"     # Footer organization name
  document_title: "Doc Title"      # Footer document title
  classification: "Internal"       # Footer classification label
  footer: "Custom footer text"     # Override entire footer

slides:
  - type: title_page
    # ... slide-specific fields
```

## Slide Types

yaml2pptx includes 14 slide types. Each type has its own layout and set of fields.

---

### `title_page`

Full-screen title slide with dark background and decorative elements.

```yaml
- type: title_page
  category: "CATEGORY LABEL"        # Small caps label above title
  title: "Main Title"               # Large title (54pt, white)
  subtitle: "Subtitle text"         # Below title (22pt, light blue)
  author: "Author Name"             # Below divider line
  date: "April 2026"                # Below author
```

---

### `agenda`

Numbered table-of-contents with title, description columns and separator lines.

```yaml
- type: agenda
  section: "AGENDA"
  title: "What we'll cover"
  subtitle: "Optional subtitle"
  items:
    - title: "First topic"
      description: "Brief description"
    - title: "Second topic"
      description: "Brief description"
      number: "02"                   # Optional custom number (auto-generated if omitted)
```

---

### `stat_cards`

Cards with large statistics (numbers), labels, and descriptions. Good for key figures.

```yaml
- type: stat_cards
  section: "SECTION LABEL"
  title: "Slide title"
  subtitle: "Optional subtitle"
  cards:
    - stat: "85%"                    # Large number/stat
      label: "of respondents"        # Small label below stat
      title: "Card title"           # Card heading
      description: "Longer text"     # Card body
  footnotes:                         # Optional footnotes at bottom
    - "[1] Source reference"
```

---

### `definition_cards`

Term cards with icon, subtitle, and description. Ideal for glossaries and key concepts.

```yaml
- type: definition_cards
  section: "SECTION"
  title: "Key concepts"
  subtitle: "Optional"
  cards:
    - term: "API"                    # Large term text
      icon: "gear"                   # Icon name (see Icons section)
      subtitle: "Application Programming Interface"
      description: "Explanation text"
      border_color: "#00A9A5"        # Optional custom border color
  callout:                           # Optional dark bar at bottom
    label: "CALLOUT LABEL"
    columns:
      - title: "Column 1"
        description: "Description"
      - title: "Column 2"
        description: "Description"
```

---

### `content_cards`

Feature cards with icon, title, subtitle, and description or bullet points.

```yaml
- type: content_cards
  section: "SECTION"
  title: "Features"
  subtitle: "Optional"
  cards:
    - title: "Card title"
      icon: "shield"                 # Icon name
      subtitle: "Card subtitle"
      description: "Or use description text"
      # OR use points:
      points:
        - "Bullet point 1"
        - "Bullet point 2"
  callout:                           # Optional callout bar
    label: "LABEL"
    columns:
      - title: "Title"
        description: "Text"
```

---

### `icon_cards`

Key message at top with accent-bordered cards below.

```yaml
- type: icon_cards
  section: "KEY MESSAGE"
  message: "The main message text displayed prominently at the top."
  cards:
    - title: "Card title"
      icon: "shield"
      description: "Card description"
```

---

### `two_panels`

Side-by-side panels (A/B comparison) with dark/light backgrounds.

```yaml
- type: two_panels
  section: "SECTION"
  title: "Two approaches"
  subtitle: "Optional"
  left_panel:
    letter: "A"                      # Large letter
    label: "OPTION A"               # Small caps label
    title: "Panel title"
    example: "Example text (italic)"
    dark: true                       # Dark background (default for left)
    points:
      - "Bullet point 1"
      - "Bullet point 2"
  right_panel:
    letter: "B"
    label: "OPTION B"
    title: "Panel title"
    example: "Example text"
    dark: false                      # Light background (default for right)
    points:
      - "Bullet point 1"
      - "Bullet point 2"
```

---

### `comparison`

Two panels with header bars and key-value rows. Good for before/after or side-by-side data.

```yaml
- type: comparison
  section: "SECTION"
  title: "Comparison"
  subtitle: "Optional"
  left_panel:
    header: "BEFORE"                 # Colored header bar text
    title: "Panel title"
    rows:
      - label: "METRIC"             # Key (colored, bold)
        value: "Description"        # Value text
  right_panel:
    header: "AFTER"
    title: "Panel title"
    rows:
      - label: "METRIC"
        value: "Description"
  footer_text: "Optional centered footer text"
```

---

### `section_divider`

Full dark background with large number and title. Use between sections.

```yaml
- type: section_divider
  number: "03"                       # Large number (96pt)
  title: "Section Title"            # Main title (40pt, white)
  subtitle: "Optional subtitle"     # Below title (light blue)
```

---

### `timeline`

Horizontal timeline with phases/milestones and optional items.

```yaml
- type: timeline
  section: "SECTION"
  title: "Project Timeline"
  subtitle: "Optional"
  phases:
    - label: "Q1 2026"              # Above timeline
      title: "Phase name"           # Below timeline
      active: true                   # Highlight this phase (accent color)
      description: "Phase description"
      # OR use items for bullet list:
      items:
        - "Task 1"
        - "Task 2"
```

---

### `process`

Numbered step-by-step process flow in connected cards.

```yaml
- type: process
  section: "SECTION"
  title: "Process Steps"
  subtitle: "Optional"
  steps:
    - number: "1"                    # Step number (auto-generated if omitted)
      icon: "search"                 # Optional icon
      title: "Step title"
      description: "Step description"
      items:                         # Optional sub-items
        - "Detail 1"
        - "Detail 2"
```

---

### `quote`

Large quote with attribution. Optional dark mode.

```yaml
- type: quote
  section: "SECTION"
  quote: "The quote text goes here."
  attribution: "— Speaker Name"
  source: "Publication, Year"
  dark: true                         # Dark background (optional)
```

---

### `key_metrics`

Dashboard-style metrics grid with trend indicators. Supports up to 8 metrics in a 2-row layout.

```yaml
- type: key_metrics
  section: "SECTION"
  title: "Key Metrics"
  subtitle: "Optional"
  metrics:
    - value: "99.9%"                 # Large number
      label: "System uptime"        # Metric label
      trend: "up"                    # "up", "down", or omit
      trend_label: "+0.2pp"         # Trend description
      color: "success"              # "primary", "accent", "success", "warning", "blue", "dark"
```

---

### `checklist`

Status checklist with colored indicators. Supports multi-column layout.

```yaml
- type: checklist
  section: "SECTION"
  title: "Action Items"
  subtitle: "Optional"
  columns: 2                         # 1, 2, or 3 columns
  items:
    - text: "Task description"
      status: "done"                 # "done" (✓), "in_progress" (●), "pending" (○), "blocked" (✗)
      note: "Optional note"         # Small italic text below
```

---

### `content` (fallback)

Simple bullet-point slide. Used for any unrecognized type or explicit `content` type.

```yaml
- type: content
  section: "SECTION"
  title: "Slide Title"
  subtitle: "Optional"
  content:
    - "Bullet point 1"
    - "Bullet point 2"
    - "Bullet point 3"
  # OR as a single string:
  content: "Paragraph text without bullets"
```

---

## Icons

Cards that support icons (`definition_cards`, `content_cards`, `icon_cards`, `process`) accept an `icon` field with a named icon:

```yaml
cards:
  - title: "Security"
    icon: "shield"
```

### Available Icons

| Category | Icons |
|----------|-------|
| **Security** | `shield`, `lock`, `key`, `unlock` |
| **Technology** | `gear`, `server`, `cloud`, `database`, `code`, `network`, `chip` |
| **People** | `people`, `person`, `mail`, `chat` |
| **Status** | `check`, `cross`, `warning`, `info`, `star`, `flag` |
| **Business** | `chart`, `target`, `trend`, `money`, `document`, `folder` |
| **Health** | `brain`, `heart`, `health`, `science`, `microscope` |
| **Energy** | `lightning`, `globe`, `sun`, `leaf` |
| **Navigation** | `arrow_right`, `arrow_left`, `arrow_up`, `arrow_down`, `search`, `link`, `clock`, `rocket` |
| **Shapes** | `circle`, `square`, `diamond`, `triangle` |

**Aliases:** `gpu`→chip, `ai`→brain, `security`→shield, `settings`→gear, `users`→people, `time`→clock, `data`→database, `success`→check, `error`→cross, `alert`→warning, `plus`→health

## Theme

The default theme uses:

- **Colors:** Navy blue (#003087), teal accent (#00A9A5), light blue (#6CACE4), dark navy (#001F5C)
- **Font:** Calibri throughout
- **Slide size:** 13.33" × 7.50" (widescreen 16:9)

### Theme Config

Override footer and organization info per presentation:

```yaml
theme_config:
  organization: "Company Name"
  document_title: "Document Title"
  classification: "Internal"
  footer: "Custom footer"           # Overrides auto-generated footer
```

## Examples

See the `examples/` directory:

| File | Description |
|------|-------------|
| `product_launch.yaml` | Product launch plan — stat_cards, timeline, checklist, two_panels, quote |
| `quarterly_review.yaml` | Quarterly business review — key_metrics, comparison, process, table |
| `tech_strategy.yaml` | Cloud migration strategy — definition_cards, process, timeline, comparison |

Build all examples:

```bash
yaml2pptx build examples/product_launch.yaml --open
yaml2pptx build examples/quarterly_review.yaml --open
yaml2pptx build examples/tech_strategy.yaml --open
```

## Template-Based Rendering (`gen`)

For standard PowerPoint templates with placeholders:

```yaml
template: "template.pptx"
output: "output.pptx"
metadata:
  title: "Title"
slides:
  - layout: title_slide
    title: "Presentation Title"
    subtitle: "Subtitle"
  - layout: content
    title: "Slide Title"
    content:
      - "Point with **bold** and *italic*"
      - text: "Indented point"
        level: 1
    speaker_notes: "Speaker notes here"
```

Supports inline Markdown formatting: `**bold**`, `*italic*`, `` `code` ``, `[link](url)`, `~~strikethrough~~`.

```bash
yaml2pptx gen presentation.yaml
yaml2pptx inspect template.pptx     # See available layouts
yaml2pptx init --name "My Deck"     # Generate starter YAML
```
