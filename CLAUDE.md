# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static HTML website for "Švytintys dantys" (Healthy Teeth), a dental clinic website. The site is built with plain HTML, Tailwind CSS (via CDN), and includes basic JavaScript for interactivity.

## Site Structure

- **index.html** - Homepage with hero section, services preview, testimonials, and contact information
- **services.html** - Detailed services page showcasing dental treatments
- **doctors.html** - Doctors/staff page with team information
- **booking.html** - Appointment booking form with time slot selection

## Technology Stack

- **HTML5** - Semantic markup
- **Tailwind CSS** - Utility-first CSS framework (loaded via CDN)
- **Font Awesome** - Icons (loaded via CDN)
- **Vanilla JavaScript** - Basic interactivity (mobile menu, smooth scrolling, form interactions)

## Language and Content

- **Primary Language**: Lithuanian (lt)
- All content, navigation, and UI text are in Lithuanian
- Contact information targets Vilnius, Lithuania

## Common Development Tasks

### Running the Site
Since this is a static site, you can serve it locally using any static file server:
```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000

# Node.js (if available)
npx serve .

# Or simply open index.html directly in a browser
```

### Making Changes
- Edit HTML files directly for content changes
- Styles are implemented using Tailwind CSS classes in the HTML
- Custom CSS is embedded in `<style>` tags in each HTML file
- JavaScript is embedded in `<script>` tags at the bottom of each HTML file

### Navigation Menu Updates
When adding new pages, update the navigation menu in all HTML files:
- Desktop menu (around lines 43-51)
- Mobile menu (around lines 60-68)
- Update the active page highlighting (text-blue-500 font-semibold)

## Design Patterns

### Color Scheme
- Primary: Blue (blue-500, blue-600)
- Secondary: Purple gradient (gradient-bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%))
- Background: Gray (gray-50, gray-900 for footer)
- White for cards and content areas

### Common Components
- **Navigation**: Fixed top navigation with mobile hamburger menu
- **Service Cards**: Hover effects with translateY(-5px)
- **Form Inputs**: Focus states with transform and shadow effects
- **Buttons**: Consistent blue theme with hover states

### Responsive Design
- Mobile-first approach using Tailwind's responsive prefixes (md:, lg:)
- Hamburger menu for mobile navigation
- Grid layouts that stack on mobile

## File Organization

- All HTML files are self-contained with embedded CSS and JavaScript
- No external CSS or JS files (everything via CDN or embedded)
- **Photos Directory**: All images are stored in `Photos/` directory in WebP format
- .env file contains WordPress database configuration (unused in current static version)

## Contact Information
The site displays the following contact details (may need updating):
- Address: Lvivo g. 25, Vilnius
- Phone: +370 5 205 2405, +370 686 24050
- Email: info@sveikidantys.lt
- Hours: Pr-Pe: 9:00-18:00

## Browser Compatibility
The site uses modern CSS features (flexbox, grid, backdrop-filter) and should work in all modern browsers. Consider testing in older browsers if needed.