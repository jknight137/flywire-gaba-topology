# GitHub Pages Website Architecture

## Site Map

```
Home (index.md)
├── Methods (methods.md)
│   ├── Data Source
│   ├── Network Construction
│   ├── Topological Metrics
│   ├── Statistical Methods
│   └── Computational Implementation
│
├── Results (results.md)
│   ├── GABA Clustering
│   ├── Full NT Results
│   ├── Hub Composition
│   ├── Scale-Free Properties
│   ├── Sensitivity Analyses
│   └── Component Structure
│
├── Code (code.md)
│   ├── Repository Structure
│   ├── Prerequisites
│   ├── Running Analysis
│   ├── Script Details
│   ├── Data Files
│   └── Troubleshooting
│
└── About (about.md)
    ├── Research Context
    ├── Key Discoveries
    ├── Biological Implications
    ├── Data Sources
    ├── Technical Approach
    └── Contact Info
```

## Navigation Flow

```
┌─────────────────────────────────────────────────────────────┐
│  Header: GABA Topology Study                                 │
│  [Home] [Methods] [Results] [Code] [About] [GitHub]         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      HOME PAGE                               │
│  • Hero: Key message                                         │
│  • Finding Cards (3):                                        │
│    - 714× clustering difference                              │
│    - 100% GABA hub dominance                                 │
│    - Scale-free architecture                                 │
│  • Abstract                                                  │
│  • Data & Methods summary                                    │
│  • Results table                                             │
│  • Biological implications                                   │
│  • Resource links                                            │
│  • Citation                                                  │
└─────────────────────────────────────────────────────────────┘
           │              │              │              │
           ▼              ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
    │ METHODS  │   │ RESULTS  │   │   CODE   │   │  ABOUT   │
    │          │   │          │   │          │   │          │
    │ • Data   │   │ • Stats  │   │ • Setup  │   │ • Context│
    │ • Metrics│   │ • Tables │   │ • Scripts│   │ • Impact │
    │ • Stats  │   │ • Figures│   │ • Repro  │   │ • Team   │
    └──────────┘   └──────────┘   └──────────┘   └──────────┘
```

## File Dependencies

```
docs/
│
├── _config.yml ──────────────────┐
│   (Site configuration)          │
│                                  │
├── _layouts/                      │
│   └── default.html ←────────────┤─── All pages use this layout
│       (Custom template)          │
│                                  │
├── assets/                        │
│   └── css/                       │
│       └── style.scss ←───────────┤─── Imported by all pages
│           (Custom styling)       │
│                                  │
├── index.md ─────────────────────┤
├── methods.md ───────────────────┤
├── results.md ───────────────────┤
├── code.md ──────────────────────┤
└── about.md ─────────────────────┘
```

## Component Breakdown

### Header (in default.html)

```
┌────────────────────────────────────────┐
│  Project Title                         │
│  Project Tagline                       │
│  ┌──────────────────────────────────┐ │
│  │ [Home] [Methods] [Results] etc.. │ │
│  └──────────────────────────────────┘ │
└────────────────────────────────────────┘
```

### Content Area (markdown files)

```
┌────────────────────────────────────────┐
│  # Page Title                          │
│                                        │
│  Content section 1                     │
│  Content section 2                     │
│  ...                                   │
│                                        │
│  [← Previous] [Home] [Next →]         │
└────────────────────────────────────────┘
```

### Footer (in default.html)

```
┌────────────────────────────────────────┐
│  Maintained by: [Author]               │
│  Data: FlyWire (CC-BY 4.0)            │
│  Hosted on: GitHub Pages               │
└────────────────────────────────────────┘
```

## CSS Architecture

```
style.scss
├── Theme Import (@import "{{ site.theme }}")
│
├── Custom Styles
│   ├── Hero Section
│   │   • Gradient background
│   │   • White text
│   │   • Rounded corners
│   │
│   ├── Findings Grid
│   │   • 3-column responsive grid
│   │   • Card styling
│   │   • Hover effects
│   │
│   ├── Tables
│   │   • Styled headers
│   │   • Hover rows
│   │   • Responsive layout
│   │
│   ├── Buttons
│   │   • Resource links
│   │   • Navigation
│   │   • Hover animations
│   │
│   ├── Code Blocks
│   │   • Syntax highlighting
│   │   • Dark theme
│   │   • Scrollable
│   │
│   └── Responsive Design
│       • Mobile breakpoints
│       • Flexible grids
│       • Touch-friendly
```

## Data Flow

### User Visits Site

```
1. GitHub Pages receives request
   ↓
2. Jekyll builds site (if needed)
   ↓
3. Loads _config.yml settings
   ↓
4. Applies _layouts/default.html template
   ↓
5. Injects page content (markdown → HTML)
   ↓
6. Loads assets/css/style.scss
   ↓
7. Renders final HTML + CSS
   ↓
8. Delivers to user's browser
```

### Developer Updates Content

```
1. Edit .md file locally
   ↓
2. git commit -m "Update content"
   ↓
3. git push to GitHub
   ↓
4. GitHub Actions triggered
   ↓
5. Jekyll rebuilds site
   ↓
6. New version deployed
   ↓
7. Live in 1-2 minutes
```

## Color Palette

```
Primary Colors:
┌──────┐ ┌──────┐
│#667eea│ │#764ba2│  Gradient (purple)
└──────┘ └──────┘

Secondary Colors:
┌──────┐ ┌──────┐ ┌──────┐
│#f8f9fa│ │#e9ecef│ │#6c757d│  Grays
└──────┘ └──────┘ └──────┘

Accent Colors:
┌──────┐ ┌──────┐
│#5568d3│ │#282c34│  Hover + Code
└──────┘ └──────┘
```

## Typography Hierarchy

```
H1 (Page Titles)
├── Size: 2rem
├── Color: #1a202c
├── Border: 3px solid #667eea
└── Weight: 600

H2 (Major Sections)
├── Size: 1.75rem
├── Color: #2d3748
├── Border: 2px solid #e9ecef
└── Weight: 600

H3 (Subsections)
├── Size: 1.3rem
├── Color: #667eea
└── Weight: 600

Body Text
├── Size: 1rem
├── Color: #333
├── Line Height: 1.6
└── Font: System sans-serif

Code
├── Font: Monaco, Menlo
├── Size: 0.9em
└── Background: #f4f4f4
```

## Responsive Breakpoints

```
Desktop (>768px)
┌─────────────────────────────────┐
│  [─────── Content ────────]    │
│  3-column findings grid         │
│  Full navigation                │
└─────────────────────────────────┘

Mobile (≤768px)
┌──────────────┐
│   Content    │
│ 1-col grid   │
│ Stacked nav  │
└──────────────┘
```

## Performance Optimization

```
Assets
├── CSS: ~15KB (minified)
├── HTML: ~20KB per page
├── JS: MathJax from CDN (only when needed)
└── Images: None (can add optimized PNGs)

Load Time
├── First Paint: <1s
├── Interactive: <1.5s
└── Full Load: <2s

Optimizations
├── Static HTML (no server processing)
├── CDN delivery (GitHub Pages)
├── Minimal dependencies
└── Efficient CSS
```

## SEO Structure

```
<head>
├── <title>Page Title - GABA Topology</title>
├── <meta description="...">
├── <meta keywords="GABA, connectome, ...">
├── <link rel="canonical" ...>
├── <meta property="og:..." > (Open Graph)
└── <script type="application/ld+json"> (Schema)
```

## Access Pattern

```
Common User Journeys:

Researcher Looking for Methods:
Home → Methods → Code
└── Download repo

Paper Reviewer:
Home → Results → Methods
└── Verify analysis

Collaborator:
Home → About → GitHub
└── Contact via Issues

General Reader:
Home → Results → About
└── Share on social
```

## Maintenance Schedule

```
Regular Updates:
├── Content: As results update
├── Figures: When regenerated
├── Code examples: When scripts change
└── Links: Check annually

Dependencies:
├── Jekyll: Auto-updated by GitHub
├── Theme: Stable (minimal changes)
├── MathJax: CDN (always current)
└── Ruby gems: bundle update quarterly
```

---

This architecture provides:
✅ Clear content hierarchy
✅ Easy navigation
✅ Professional design
✅ Fast performance
✅ SEO optimization
✅ Mobile responsiveness
✅ Maintainability
✅ Accessibility
