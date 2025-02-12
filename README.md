# Multi-Agent Design Analysis Platform

A powerful design analysis platform that uses multiple AI agents to provide comprehensive analysis of design images.

## Features

- 👁️ Vision Analysis: Evaluates visual hierarchy, color schemes, typography, and composition
- 🔍 UX Analysis: Assesses user flows, accessibility, and interaction design
- 📊 Market Research: Analyzes market trends and competitive positioning
- 📄 PDF Report Generation: Creates detailed analysis reports

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your Gemini API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Launch the application
2. Enter your Gemini API key in the sidebar
3. Upload a design image
4. Click "Start Analysis" to generate insights
5. View analysis results in respective tabs
6. Generate and download a comprehensive PDF report

## Requirements

- Python 3.8+
- Gemini API key (obtain from https://makersuite.google.com/app/apikey)
- Internet connection for API calls

## Project Structure

- `app.py`: Main Streamlit application
- `agents.py`: AI agent implementations
- `requirements.txt`: Project dependencies
- `.env`: Environment variables (create this file)
