---
name: Kinetic Unity
colors:
  surface: '#f8f9ff'
  surface-dim: '#f1f5f9'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#414751'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#717782'
  outline-variant: '#c1c7d3'
  surface-tint: '#0260aa'
  primary: '#004b87'
  on-primary: '#ffffff'
  primary-container: '#0c63ad'
  on-primary-container: '#cadfff'
  inverse-primary: '#a3c9ff'
  secondary: '#805600'
  on-secondary: '#ffffff'
  secondary-container: '#fdaf16'
  on-secondary-container: '#694600'
  tertiary: '#00534f'
  on-tertiary: '#ffffff'
  tertiary-container: '#006d68'
  on-tertiary-container: '#78f0e8'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d3e4ff'
  primary-fixed-dim: '#a3c9ff'
  on-primary-fixed: '#001c38'
  on-primary-fixed-variant: '#004882'
  secondary-fixed: '#ffddb0'
  secondary-fixed-dim: '#ffba46'
  on-secondary-fixed: '#281800'
  on-secondary-fixed-variant: '#614000'
  tertiary-fixed: '#7ef6ed'
  tertiary-fixed-dim: '#5fd9d1'
  on-tertiary-fixed: '#00201e'
  on-tertiary-fixed-variant: '#00504c'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
  energy-gradient-start: '#f1a500'
  energy-gradient-end: '#e94b23'
  surface-light: '#f8fafc'
typography:
  display:
    fontFamily: Montserrat
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Montserrat
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-lg-mobile:
    fontFamily: Montserrat
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Montserrat
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-sm:
    fontFamily: Montserrat
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.05em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.2'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
  stack-sm: 12px
  stack-md: 24px
  stack-lg: 48px
---

## Brand & Style

The design system is engineered for a youth-focused NGO that balances institutional credibility with vibrant, grassroots energy. It bridges the gap between the structured authority of international organizations (UNICEF/UNDP) and the fluid, digital-native aesthetics of modern youth movements.

The visual style is **Corporate Modern with Kinetic Accents**. It utilizes a clean, professional foundation—heavy on whitespace and precise typography—interrupted by high-energy gradients and fluid geometric shapes. 

**Key Principles:**
- **Professionalism:** High-quality execution, generous margins, and a structured grid.
- **Energy:** Use of the signature "Energy Gradient" to highlight momentum, growth, and action.
- **Glassmorphism:** Strategic use of frosted glass overlays for navigation and modal elements to create depth and a modern, high-end feel.
- **Accessibility:** High contrast ratios and clear typographic hierarchies ensure inclusivity for all users.

## Colors

The palette is anchored by a **Deep Primary Blue**, providing a stable, NGO-standard foundation. This is contrasted by a **Vibrant Orange** and a secondary **Teal**, which are used to signify connectivity and "linkage."

The defining characteristic of this system is the **Energy Gradient**, transitioning from vibrant orange to a deep warm red. This gradient should be used sparingly for primary actions, decorative flourishes, and status indicators representing progress or momentum.

**Surface Strategy:**
- Use `surface-light` for secondary sections to break up long pages.
- Use `surface-dim` for subtle card backgrounds or inset UI elements.
- The default background remains pure white to maintain a premium, clean aesthetic.

## Typography

The typography strategy pairs the geometric strength of **Montserrat** for headings with the supreme legibility of **Inter** for body text.

- **Headlines:** Set in Montserrat with tighter letter spacing for a punchy, modern look. Use Semibold or Bold weights to establish a clear hierarchy.
- **Body:** Inter is used for all functional and long-form text. It provides a "systematic" feel that aligns with the professional NGO aesthetic.
- **Labels:** Small labels and "overlines" should use Inter in uppercase with increased letter spacing to differentiate them from body content and metadata.

## Layout & Spacing

The design system utilizes a **12-column fluid grid** for desktop and a **4-column grid** for mobile. 

**Layout Model:**
- **Rhythm:** An 8px base unit drives all padding, margins, and component sizing.
- **Whitespace:** Use generous `stack-lg` spacing between major sections to emphasize a premium, uncluttered experience.
- **Alignment:** Content is generally centered within a max-width container, though background fills (like `surface-light`) should bleed to the edge of the viewport to create distinct content "zones."
- **Reflow:** On mobile, margins reduce to 16px, and multi-column card layouts stack vertically into a single column.

## Elevation & Depth

Depth is created through a mix of **Tonal Layering** and **Glassmorphism**.

- **Surfaces:** Use flat surfaces with extremely soft, large-radius shadows (e.g., Blur: 30px, Opacity: 4%) to lift cards off the background. Avoid harsh shadows.
- **Glassmorphism:** Use for fixed navigation bars, dropdown menus, and modal overlays. These elements should have a backdrop-blur (12px - 20px) and a subtle 1px white border with 20% opacity to define the edge.
- **Z-Index Hierarchy:** 
  - Level 0: Main Background.
  - Level 1: Cards and content blocks (Subtle shadow).
  - Level 2: Floating Action Buttons and Navigation (Glassmorphism + Shadow).
  - Level 3: Modals and Overlays (Heavy backdrop blur).

## Shapes

The shape language is defined by **Large, Soft Radii** that evoke a friendly and approachable feel.

- **Standard Components:** Buttons and input fields use a `0.5rem` radius.
- **Containers:** Cards and section containers use a `1.5rem` (2xl) radius to create a distinct, modern look.
- **Decorative Elements:** Circular motifs from the logo are used as background patterns, often with low opacity or as part of the "Energy Gradient" swooshes.

## Components

### Buttons
- **Primary:** Features the Energy Gradient with white text. High impact, reserved for the main CTA.
- **Secondary:** Deep Blue (#0c63ad) with white text. Used for standard actions.
- **Ghost:** Transparent background with a 1.5px border in Primary Blue or White (if on dark background).

### Cards
Cards are the primary content vessel. They must have a `rounded-xl` (1.5rem) radius, a white background, and the "Ambient Shadow" defined in the Elevation section. For "Featured" cards, a 4px top-border using the Energy Gradient can be applied.

### Inputs & Form Fields
Fields should have a `surface-dim` background and a subtle 1px gray border. Focus states should transition the border to Primary Blue and add a soft blue outer glow.

### Navigation
The header should be a glassmorphic bar that remains fixed at the top of the viewport. It uses a semi-transparent white background with a backdrop filter to blur the content beneath it.

### Chips & Tags
Used for categories or status. They should use low-saturation versions of the brand colors (e.g., light teal background with dark teal text) to remain secondary to main buttons.

### List Items
Interactive lists should have a subtle hover state that changes the background to `surface-light` and shifts the item 4px to the right, emphasizing "forward movement."