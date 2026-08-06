---
name: Teal SaaS Director
colors:
  surface: '#f7f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f7f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#3d4947'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
  outline: '#6d7a77'
  outline-variant: '#bcc9c6'
  surface-tint: '#006a61'
  primary: '#00685f'
  on-primary: '#ffffff'
  primary-container: '#008378'
  on-primary-container: '#f4fffc'
  inverse-primary: '#6bd8cb'
  secondary: '#565e74'
  on-secondary: '#ffffff'
  secondary-container: '#dae2fd'
  on-secondary-container: '#5c647a'
  tertiary: '#4d5d73'
  on-tertiary: '#ffffff'
  tertiary-container: '#66768d'
  on-tertiary-container: '#fdfcff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#89f5e7'
  primary-fixed-dim: '#6bd8cb'
  on-primary-fixed: '#00201d'
  on-primary-fixed-variant: '#005049'
  secondary-fixed: '#dae2fd'
  secondary-fixed-dim: '#bec6e0'
  on-secondary-fixed: '#131b2e'
  on-secondary-fixed-variant: '#3f465c'
  tertiary-fixed: '#d3e4fe'
  tertiary-fixed-dim: '#b7c8e1'
  on-tertiary-fixed: '#0b1c30'
  on-tertiary-fixed-variant: '#38485d'
  background: '#f7f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Hanken Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.03em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
---

## Brand & Style

The brand personality is professional, precise, and high-performance, tailored for modern SaaS environments. It evokes a sense of refreshing clarity and technical competence through a sophisticated Modern Corporate aesthetic.

The design system utilizes a "High-End Utility" style: it balances extreme legibility with high-quality finishes. The interface feels established yet agile, utilizing whitespace and a signature vibrant teal to guide focus without overwhelming the user. The aesthetic is clean, systematic, and optimized for long-form data management and complex workflows.

## Colors

The palette is centered around a vibrant Teal (#0d9488) which serves as the primary action color. This seafoam-derived hue provides a professional "tech" feel that is more modern and refreshing than standard corporate blues.

- **Primary**: Used for main calls to action, active states, and brand highlights.
- **Secondary**: A deep Slate used for high-contrast typography and sidebars.
- **Neutral**: A cool-toned gray scale that ensures the teal accents remain the focal point.
- **Functional**: Success, warning, and error states should be clearly differentiated, with the Teal specifically reserved for intent and primary navigation.

## Typography

This design system uses a triple-font stack to differentiate roles:
1. **Hanken Grotesk** (Headlines): Sharp and contemporary, used to establish hierarchy and brand voice.
2. **Inter** (Body): Highly legible and neutral, used for all long-form text and general UI labels.
3. **Geist** (Labels/Technical): A monospaced-leaning sans used for data, labels, and small metadata to emphasize precision.

Scale adjustments for mobile focus on reducing the `display` and `headline-lg` sizes to prevent awkward line breaks while maintaining the same vertical rhythm.

## Layout & Spacing

The design system employs a **12-column fluid grid** for desktop and a **4-column grid** for mobile. 

- **Spacing Rhythm**: Based on a 4px baseline, with most components utilizing 8px (sm) or 16px (md) increments for internal padding.
- **Margins**: Desktop views should maintain generous 40px outer margins to create a high-end "Director" feel.
- **Reflow**: On tablet transitions (768px), horizontal navigation should collapse into a vertical drawer, and columns should stack from 12 to 6.

## Elevation & Depth

Visual hierarchy is achieved through **Tonal Layers** supplemented by **Ambient Shadows**.

- **Surface Levels**: The background uses `surface-muted`, while cards and primary containers use `surface` (White) to pop.
- **Shadows**: Use highly diffused, low-opacity shadows. A standard elevation shadow should be `0px 4px 12px rgba(15, 23, 42, 0.08)`.
- **Interactivity**: On hover, elements should slightly lift (increase shadow spread) or shift to a subtly lighter teal tint for primary actions. 
- **Borders**: Soft, low-contrast outlines (`#e2e8f0`) are preferred over heavy shadows for secondary containers.

## Shapes

The shape language is "Rounded," striking a balance between approachable and professional. 

- **Base Radius**: 0.5rem (8px) for standard buttons, input fields, and small components.
- **Large Radius**: 1rem (16px) for cards, modals, and main content containers.
- **Extra Large**: 1.5rem (24px) for featured hero sections or large promotional banners.

## Components

### Buttons
- **Primary**: Solid `#0d9488` background with white text. Hover state shifts to `#0f766e`.
- **Secondary**: Ghost style with `#0d9488` border and text. 
- **Soft**: Teal background at 10% opacity with teal text.

### Input Fields
- **Default**: White background, 1px border (`#e2e8f0`), 8px border-radius.
- **Focus**: Border color shifts to `#0d9488` with a 3px `focus-ring` (teal at 40% alpha).

### Chips & Badges
- Used for status and filtering. Use the `primary-soft` token for background and `primary_color_hex` for text to ensure legibility and a refined look.

### Cards
- Use 16px padding, a 1px soft border, and the standard ambient shadow. Headlines within cards should use `headline-md`.

### Lists
- Interactive list items should have a subtle background hover state (`#f1f5f9`) and a 2px teal left-border highlight when active.