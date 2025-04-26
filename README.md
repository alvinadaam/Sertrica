# SERTRICA Website

## Overview
This repository contains the source code for the **SERTRICA** website, a companion to the SERTRICA encryption tool. The website provides information about the tool, a live demo, and download links for the application.

## Website Features
- **Homepage**: Overview of SERTRICA's features and call-to-action buttons.
- **Demo Page**: Interactive demo for testing AES and AES+RSA encryption modes.
- **About Page**: Background and philosophy behind SERTRICA.
- **Download Page**: Links to download the application for Windows, macOS, and Linux.

## File Structure
The website's files are organized as follows:

```
Sretica/
├── assets/                # Static assets (icons, images, etc.)
│   ├── terminal-icon.svg  # Icon for macOS/Linux
│   ├── windows-icon.svg   # Icon for Windows
├── styles.css             # Global styles for the website
├── index.html             # Homepage
├── demo.html              # Demo page
├── demo.js                # JavaScript for the demo page
├── about.html             # About page
├── install.html           # Download page
└── README.md              # Documentation for the website
```

## Pages and Their Purpose
### 1. **Homepage (`index.html`)**
   - Provides an overview of SERTRICA's features.
   - Includes call-to-action buttons for downloading the app or viewing the GitHub repository.

### 2. **Demo Page (`demo.html`)**
   - Allows users to test AES and AES+RSA encryption modes.
   - Includes a live encryption/decryption interface powered by `demo.js`.

### 3. **About Page (`about.html`)**
   - Explains the philosophy and purpose behind SERTRICA.
   - Highlights the creator's vision for privacy and encryption.

### 4. **Download Page (`install.html`)**
   - Lists system requirements and provides download links for the app.
   - Includes troubleshooting tips for running the app on different platforms.

## Assets
- **Icons**: Located in the `assets/` directory, used for platform-specific download cards.
- **Styles**: `styles.css` contains global styles for consistent design across all pages.

## How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/xzeromin/SERTRICA.git
   ```
2. Navigate to the `Sretica` directory:
   ```bash
   cd Sretica
   ```
3. Open any `.html` file in your browser to view the corresponding page.

## Contributing
Feel free to submit issues or pull requests to improve the website.
