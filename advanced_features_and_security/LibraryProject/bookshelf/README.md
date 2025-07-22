# 🔐 Security Testing Checklist

## ✅ CSRF Protection
- Confirm CSRF tokens are required for all form submissions.
- Try submitting a form without a CSRF token → Should fail with 403 Forbidden.

## ✅ XSS (Cross-Site Scripting) Protection
- Enter this in input field: `<script>alert('XSS')</script>`
- Result: Should appear as plain text, **not** as a script popup.

## ✅ SQL Injection Protection
- Use any search or text field.
- Input: `1' OR 1=1`
- Result: Should not break query logic or expose data.

## ✅ Clickjacking Protection
- Open browser developer tools > Network > check headers.
- Confirm this header exists:
