# Write Up

Unthink is an advanced, AI-powered diagnostic engine designed to evaluate and optimize social media marketing copy. Built with a sleek, responsive Streamlit interface, the application bridges the gap between deterministic linguistic metrics and generative AI analysis to give marketers actionable insights in seconds.

At its core, Unthink leverages the lightning-fast Groq API (powered by Llama 3 models) to perform a rigorous multi-dimensional evaluation of your content. It scores copy based on Hook Retention, Call-to-Action (CTA) Clarity, and Audience Resonance, while simultaneously identifying top strengths, areas for improvement, and the dominant emotional tone. To ensure content accessibility, a deterministic readability engine (via textstat) calculates the Flesch Reading Ease and Gunning Fog indices.

Beyond analysis, Unthink acts as an automated platform-native copywriter. It intelligently refactors your original text into perfectly optimized formats for LinkedIn, X (Twitter), and Instagram—automatically adjusting character limits, spacing, and hashtag strategies. Featuring seamless document ingestion (supporting both PDF parsing and image OCR via Tesseract) and a highly modular backend architecture, Unthink is a comprehensive tool for creators looking to elevate their digital presence.




# Social Media Content Analyzer ⚡

A production-ready Streamlit diagnostic engine for evaluating and adapting social media copy — powered by **Gemini 2.0 Flash**, **textstat**, and **Tesseract OCR**.

---

## Features

| Feature | Details |
|---|---|
| 🪝 Hook Retention | AI scores your opening line for curiosity and scroll-stopping power |
| 📢 CTA Clarity | Evaluates clarity, specificity, and friction of your call-to-action |
| 🎯 Audience Resonance | Assesses tone-audience fit and platform nativeness |
| 📖 Readability | Flesch Reading Ease, Gunning Fog, sentence stats via textstat |
| 🎭 Emotional Tone | AI-detected dominant emotional register |
| 🌐 Platform Adapter | Auto-refactors copy for LinkedIn, X (Twitter), and Instagram |
| 📄 PDF Extraction | pypdf for structured document parsing |
| 🖼️ OCR Extraction | pytesseract for image-based asset scanning |

---

## Setup

### 1. Prerequisites

**Install Tesseract** (required for image OCR):
```bash
brew install tesseract
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a Gemini API Key
Get a free key at [https://aistudio.google.com](https://aistudio.google.com)

### 4. Run the app
```bash
streamlit run app.py
```

---

## Usage

1. Enter your Gemini API key in the sidebar
2. Upload a **PDF**, **image** (PNG/JPG/WebP), or paste text directly
3. Click **⚡ Analyze Content**
4. View your full Content Intelligence Dashboard
5. Copy platform-adapted versions from the LinkedIn / X / Instagram tabs

---

## Tech Stack

- **UI**: Streamlit with custom CSS dark mode
- **AI**: Google Gemini 2.0 Flash (structured JSON output via `google-genai`)
- **Readability**: textstat (Flesch, Gunning Fog, SMOG)
- **PDF**: pypdf
- **OCR**: pytesseract + Pillow
