# Design System: DATA ENGINEERING DASHBOARD COCKPIT (OLED MODE)

## 1. Core Palette (Slate-900 OLED)

| Token | Hex | Tailwind | Usage |
|-------|-----|----------|-------|
| `--bg-app` | `#020617` | slate-950 | Main application background (Deepest) |
| `--bg-panel` | `#0F172A` | slate-900 | Cards, Sidebar, Modals |
| `--bg-surface` | `#1E293B` | slate-800 | Inputs, Hover states |
| `--primary` | `#3B82F6` | blue-500 | Primary actions, Links, Active states |
| `--accent` | `#F97316` | orange-500 | CTAs, Highlights, Badges |
| `--text-main` | `#F8FAFC` | slate-50 | Headings, Primary text |
| `--text-muted` | `#94A3B8` | slate-400 | Subtitles, Secondary text |
| `--border` | `#334155` | slate-700 | Dividers, Card borders |
| `--success` | `#10B981` | emerald-500 | Trends (+), Valid status |
| `--danger` | `#EF4444` | red-500 | Trends (-), Errors |

## 2. Typography (Code-Centric)

**Headings (Display):** `Fira Code`
- Weights: 600 (Bold), 500 (Medium)
- Usage: Page Titles, Card Headers, Metrics

**Body (Readability):** `Fira Sans`
- Weights: 400 (Regular), 300 (Light)
- Usage: Paragraphs, Descriptions, Labels

## 3. Component Styles

### Cards (`.card`)
- Background: `var(--bg-panel)`
- Border: `1px solid var(--border)`
- Radius: `8px`
- Shadow: `0 4px 6px -1px rgba(0, 0, 0, 0.5)`
- Hover: `transform: translateY(-2px); border-color: var(--primary);`

### Buttons (`.stButton button`)
- **Primary**: Gradient Blue (`bg-gradient-to-r from-blue-600 to-blue-500`)
- **Secondary**: Transparent border (`border border-slate-700 hover:bg-slate-800`)

## 4. Layout
- **Global**: Wide mode
- **Sidebar**: Collapsed (Custom implementation)
- **Grid**: 3-column default for metrics
