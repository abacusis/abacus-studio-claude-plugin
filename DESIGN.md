---
name: Abacus Studio Local Dashboard
description: A restrained dark team map for recorded local AI development activity.
colors:
  bg: "#101112"
  surface: "#191b1d"
  hover: "#202427"
  line: "#373b3e"
  text: "#f0f2f1"
  muted: "#a8b0ad"
  mint: "#70e6aa"
  amber: "#f3ca73"
  red: "#f58e91"
  returned: "#b9d8c6"
  selected: "#181f1b"
  button-primary: "#eeeae3"
  button-ink: "#131714"
  button-hover: "#fff"
  button-line: "#6b7470"
  button-secondary-hover: "#242a26"
  agent-hover-line: "#66726b"
  notice-bg: "#22251f"
  notice-text: "#e0e6c9"
  notice-line: "#545e3c"
  request-bg: "#182a21"
  request-text: "#c6edda"
  request-line: "#376248"
typography:
  headline:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "32px"
    fontWeight: 650
    lineHeight: 1.2
    letterSpacing: "-.035em"
  title:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "23px"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "-.025em"
  body:
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "15px"
    lineHeight: 1.5
  agent-name:
    fontSize: "16px"
    fontWeight: 600
    lineHeight: 1.3
  label:
    fontSize: "13px"
    lineHeight: 1.4
  metadata:
    fontSize: "12px"
rounded:
  surface: "14px"
  notice: "10px"
  button: "9px"
spacing:
  compact: "8px"
  small: "12px"
  medium: "18px"
  large: "24px"
  workspace: "36px"
components:
  button-primary:
    backgroundColor: "{colors.button-primary}"
    textColor: "{colors.button-ink}"
    rounded: "{rounded.button}"
    padding: "12px 18px"
  button-primary-hover:
    backgroundColor: "{colors.button-hover}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.text}"
    rounded: "{rounded.button}"
    padding: "12px 18px"
  agent-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.surface}"
    padding: "22px 18px 17px"
  agent-card-selected:
    backgroundColor: "{colors.selected}"
  status-working:
    textColor: "{colors.mint}"
    typography: "{typography.label}"
  notice:
    backgroundColor: "{colors.notice-bg}"
    textColor: "{colors.notice-text}"
    rounded: "{rounded.notice}"
    padding: "12px 16px"
---

# Design System: Abacus Studio Local Dashboard

## Overview

**Creative North Star: "The Local Team Map"**

A simple black workspace makes a small authored-icon team legible at a glance. System sans typography, quiet borders and restrained status color support an operational interface, not a new expressive brand identity. The implementation is lightweight HTML, CSS and JavaScript served by Python, with no asset or framework dependency.

Recorded evidence leads: an active color must correspond to an actual state, and muted, stale or disconnected information must remain visibly distinct. Selection reveals detail without turning lifecycle activity into a claim that checks passed.

**Key Characteristics:**
- Quiet dark surfaces and thin structural lines.
- Small authored outline SVG icons.
- Mint working and selected states, amber attention, gray idle.
- Readable provenance and explicit local-versus-remote boundaries.

## Colors

The palette is near-black and neutral, with small functional signals rather than decorative washes. Frontmatter values are normative; CSS custom properties in `dashboard/style.css` are the implementation source.

### Primary
- **Signal Mint** (`mint`): working, fresh connection, passed findings, selected-card outline, selected-tab underline and keyboard focus. Selected cards use the quieter `selected` surface.

### Secondary
- **Attention Amber** (`amber`): attention, interrupted or stale states and unverified checks.
- **Failure Rose** (`red`): failed and blocked findings. Returned activity has its own subdued `returned` tint and is not a passed-check signal.

### Neutral
- **Black Workspace** (`bg`), **Graphite Surface** (`surface`) and **Raised Graphite** (`hover`): base, agent card and hover layers.
- **Structural Gray** (`line`): map connectors, panel divisions and surface outlines.
- **Soft White** (`text`) and **Metadata Gray** (`muted`): primary content and secondary evidence.
- **Warm Action White** (`button-primary`): the primary request action; it is not another status accent.
- Notice and request color families separate caution from queued-request feedback.

**The Evidence Color Rule.** Never use working mint or passed-check color to imply activity, independent verification or approval that has not been recorded.

## Typography

One native system sans stack serves the whole interface. No downloaded display font or monospace branding is introduced. Tight headline tracking gives hierarchy without spectacle.

- **Headline:** the page title uses the headline token; it reduces to (28px) at the narrowest breakpoint.
- **Title:** detail headings use the title token. The brand uses (23px, 650 weight) and reduces to (19px) on narrow screens.
- **Body:** the body token anchors the UI; project and detail summaries use (16px), with detail tasks increasing to (18px) on large desktops.
- **Agent name:** the agent-name token becomes (14px) at the compact-desktop breakpoint, (15px) on narrow screens and (17px) on large desktops.
- **Label:** status text uses the label token; tabs, event bodies and buttons use (13px). Primary and secondary buttons use (600 weight).
- **Metadata:** supporting counts, timestamps, provenance footers, Git notes and footnotes remain (12px) after the stylesheet's final readability overrides. Event times use tabular numerals.

## Layout

The dashboard has a (76px) top bar, then a flexible map beside a (350px) detail rail. Workspace padding is (32px 36px 24px); the map has a (1020px) maximum width. A centered orchestrator sits above eight specialists in four columns, connected by thin CSS lines. Specialist gaps are (30px 24px). The bottom local-change bar is a bordered horizontal region, not a fixed overlay.

- At **1500px and wider**, the detail rail becomes (420px), workspace padding (40px 46px), map top margin (42px), specialist gaps (36px 28px), and detail panel maximum height (510px).
- At **1150px and narrower**, the rail becomes (300px), workspace padding (28px 24px), specialist gaps (18px 14px), and the local label and explanatory Git note hide.
- At **850px and narrower**, the map and details stack; the rail becomes a bottom section with a top border. Workspace padding is (28px 22px); the detail panel uses (180px) minimum and (300px) maximum height. The change bar wraps. Selecting an agent focuses and scrolls to its detail heading.
- At **540px and narrower**, the top bar becomes (65px), specialists form two columns with (14px) gaps, most connector stems disappear, the introduction stacks, and both action buttons share the full available row.

Closing details returns the map to one column and restores focus to the selected agent. Long project names, agent names, tasks and file paths wrap rather than force horizontal overflow.

## Elevation & Depth

There are no shadows, gradients, glows or blur layers. Depth comes from flat tonal surfaces, thin borders, spacing and a selected outline. Agent hover changes background and border over (.16s ease); it does not move or lift the card. Reduced-motion preference removes transitions and animations.

**The Flat Map Rule.** Preserve the flat hierarchy: emphasis comes from state and placement, not decorative elevation.

## Shapes

Agent cards and local-change containers share gently rounded surface corners. Notices and action buttons use their smaller dedicated radii. Lines are (1px); state dots are (8px) circles. Authored SVGs use a (24 × 24) viewBox, no fill, current-color strokes, rounded caps and joins, and (1.6) stroke width. They render at (31px) in agent cards and (34px) in detail headings.

## Components

### Buttons

Quiet and explicit. Primary and secondary actions have (44px) minimum height, the button radius and (12px 18px) padding. Primary uses warm white with dark text and white hover; secondary is transparent with a gray outline and dark hover surface. Disabled controls use (.45) opacity and a not-allowed cursor. Keyboard focus uses a (2px) mint outline offset (5px). The close button is a muted, borderless × that brightens on hover.

The two bottom actions queue requests only. Retain the explanatory footnote and queued/error feedback; no visual state should suggest that Git operations or publication already happened.

### Agent cards and status

The entire card is a button with `aria-pressed`, not a decorative tile with a tiny target. Icon, name, textual state and optional two-line summary remain in that order. Base minimum height is (154px), or (174px) with a summary; responsive overrides adjust density. The centered orchestrator uses (216px) minimum width and (136px) minimum height at default desktop size.

Status combines a dot, a color and a plain-language label. Idle, queued, ended and not-required states remain muted; stale and interrupted are amber. A returned agent is not a passed check. Offline working cards render as stale.

### Detail navigation

Activity, Changes and Checks share a three-item tab strip. Inactive labels are muted; selected labels brighten and receive a (2px) mint bottom border. ARIA selection and roving tab order accompany Left/Right, Home and End keyboard navigation. Detail content scrolls within the bounded panel. Activity uses a (48px) timestamp column; file and finding rows use subtle separators.

### Notices and evidence

Caution notices and queued-request notices use distinct subdued fills, (1px) borders and the notice radius. Empty states remain plain muted copy, not fabricated charts or animation. Provenance distinguishes observed hook events from coordinator reports, and reported checks from independent execution.

### Local changes

A Git outline icon and two-line summary reveal a bounded list of paths. Preserve separate working-copy counts, cached-upstream commit counts, staged labels and unknown states. This read-only view must not imply that cached upstream information proves current GitHub state.

## Do's and Don'ts

### Do:
- Do use native system sans type and authored outline SVG icons.
- Do pair every status color with a readable label.
- Do preserve keyboard focus, tab navigation and reduced-motion behavior.
- Do keep local changes, cached upstream data and queued requests explicitly distinct.

### Don't:
- Don't add decorative glows, gradients, shadows or animated activity indicators.
- Don't equate a returned agent, idle state or delivered request with passed checks or approval.
- Don't replace unknown or disconnected state with reassuring live styling.
- Don't introduce an external asset, icon package or UI framework for this dashboard.
