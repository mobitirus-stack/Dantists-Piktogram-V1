# EmailJS Integration Documentation

## Overview
The contact form has been integrated with EmailJS to send emails directly from the website without a backend server.

## Setup Instructions

### 1. Get Your EmailJS Credentials

1. Go to [EmailJS Dashboard](https://dashboard.emailjs.com/)
2. Sign up or log in to your account
3. Note down your **Public Key** from Account → General → API Keys

### 2. Update the contact.html File

Replace the placeholder values in `contact.html`:

```javascript
// Find this line in the <script> section:
emailjs.init("YOUR_PUBLIC_KEY"); // Replace with your EmailJS public key

// And this line:
emailjs.send('service_g38rlef', 'YOUR_TEMPLATE_ID', formData)
```

Replace:
- `YOUR_PUBLIC_KEY` with your actual EmailJS public key
- `YOUR_TEMPLATE_ID` with your template ID (see step 3)

### 3. Create Email Template

1. In EmailJS Dashboard, go to Email Templates
2. Create a new template with the following variables:

#### Template Content Example:

**Subject:**
Nauja žinutė iš Švytintys dantys svetainės - {{subject}}

**To:**
info@svytintysdantys.lt

**Message:**
Gavote naują žinutę iš kontakto formos.

Vardas: {{first_name}} {{last_name}}
El. paštas: {{email}}
Telefonas: {{phone}}
Tema: {{subject}}

Žinutė:
{{message}}

---

Siųsta iš: https://svytintysdantys.lt/kontaktai.html

### 4. Service Configuration

The service ID is already configured as: `service_g38rlef`

If you need to create a new service:
1. Go to Email Services in dashboard
2. Add your email service provider (Gmail, Outlook, etc.)
3. Follow the connection instructions
6. Note the new service ID if different

### 5. Test the Integration

1. Open `contact.html` in your browser
2. Fill out the form with test data
3. Submit the form
4. Check your email for the test message
5. Check browser console for any errors

## Form Fields Mapped to Email Template

| Form Field | Template Variable | Description |
|------------|-------------------|-------------|
| first_name | {{first_name}} | First name (required) |
| last_name | {{last_name}} | Last name (optional) |
| phone | {{phone}} | Phone number (required) |
| email | {{email}} | Email address (required) |
| subject | {{subject}} | Subject from dropdown (optional) |
| message | {{message}} | Message content (required) |

## Features Implemented

- ✅ Loading state with spinner animation
- ✅ Success message display
- ✅ Error handling with user-friendly messages
- ✅ Form validation
- ✅ Auto-reset after successful submission
- ✅ Lithuanian language messages

## Troubleshooting

### Common Issues:

1. **"EmailJS is not defined" error**
   - Ensure the EmailJS CDN script is loaded before your custom script

2. **"Public key is invalid" error**
   - Double-check your public key from EmailJS dashboard

3. **"Template ID not found" error**
   - Verify the template ID matches exactly in EmailJS

4. **No email received**
   - Check your spam folder
   - Verify the service is connected properly
   - Check EmailJS dashboard for send logs

### Debug Mode:
To enable debug mode, add this to your script:
```javascript
emailjs.init("YOUR_PUBLIC_KEY", { debug: true });
```

## Security Notes

- Your public key is safe to expose in client-side code
- The service limits sending to prevent abuse
- Consider adding reCAPTCHA if needed for production use