# AI Job Application Assistant

An intelligent AI-powered tool that helps job seekers analyze job descriptions, improve their resumes, and generate professional cover letters using LangChain and Ollama.

## 📋 Overview

This project implements three key features to streamline the job application process:

1. **Job Description Analyzer** - Automatically extracts structured information from job postings
2. **Resume Improvement Suggestions** - Provides tailored recommendations to optimize resumes for specific positions
3. **Cover Letter Generator** - Creates compelling, personalized cover letters

## 🚀 Features

### 🔍 Job Description Analyzer
- Extracts job title, required skills, and experience level
- Identifies tools and technologies mentioned
- Captures soft skills requirements
- Structures information using Pydantic models for consistency

### 📄 Resume Improvement Suggestions
- Analyzes resume-job fit and provides improvement recommendations
- Identifies missing skills that should be added
- Suggests specific resume enhancements
- Provides overall fit assessment percentage

### ✉️ Cover Letter Generator
- Generates professional cover letters (300-400 words)
- Incorporates candidate's key achievements
- Matches job requirements with candidate experience
- Uses professional tone and compelling language

## 🛠️ Technology Stack

- **LangChain** - LLM orchestration and prompt management
- **Ollama** - Local LLM inference (default: Mistral model)
- **Pydantic** - Data validation and structured output parsing
- **Python 3.8+** - Core programming language

## 📦 Installation

1. Ensure Ollama is installed and running:
   ```bash
   ollama serve
   ```

2. Pull the required model:
   ```bash
   ollama pull mistral
   ```

3. Install Python dependencies:
   ```bash
   pip install langchain langchain-community pydantic
   ```

## 💻 Usage

### Basic Usage

```python
from project1_job_application_assistant import (
    JobDescriptionAnalyzer,
    ResumeSuggestionGenerator,
    CoverLetterGenerator
)

# Sample job description
job_desc = """
[Your job description text here]
"""

# Sample resume
resume = """
[Your resume text here]
"""

# 1. Analyze job description
analyzer = JobDescriptionAnalyzer()
job_details = analyzer.analyze(job_desc)

# 2. Get resume suggestions
suggestion_gen = ResumeSuggestionGenerator()
suggestions = suggestion_gen.generate_suggestions(job_details, resume)

# 3. Generate cover letter
cover_gen = CoverLetterGenerator()
cover_letter = cover_gen.generate(
    candidate_name="John Doe",
    job_title="Senior Python Developer",
    company_name="Tech Corp",
    key_achievements="Led development of REST APIs...",
    job_requirements="Python, Django, PostgreSQL..."
)
```

### Running the Complete Demo

Execute the script directly to see all features in action:

```bash
python project1_job_application_assistant.py
```

This will process sample job description and resume data, demonstrating all three features.

## 🔧 Configuration

### Model Selection

You can specify different Ollama models for each component:

```python
# Use different models for different features
analyzer = JobDescriptionAnalyzer(model_name="llama2")
suggestion_gen = ResumeSuggestionGenerator(model_name="codellama")
cover_gen = CoverLetterGenerator(model_name="mistral")
```

### Temperature Settings

Each component uses optimized temperature settings:
- **JobDescriptionAnalyzer**: 0.3 (balanced analysis)
- **ResumeSuggestionGenerator**: 0.5 (creative suggestions)
- **CoverLetterGenerator**: 0.7 (creative writing)

## 📊 Data Models

### JobDetails
```python
{
    "job_title": "string",
    "required_skills": ["string"],
    "experience_required": "integer",  # years
    "tools": ["string"],
    "soft_skills": ["string"]
}
```

### ResumeSuggestions
```python
{
    "missing_skills": ["string"],
    "improvement_points": ["string"],
    "overall_fit_summary": "string"  # e.g., "75% fit"
}
```

## ⚠️ Important Notes

- **AI-Generated Content**: Review and personalize all generated content before use
- **Privacy**: Be mindful of sharing sensitive resume information
- **Job Market**: AI suggestions should complement, not replace, professional career advice
- **Local Processing**: All processing happens locally using Ollama - no data is sent to external services

## 🏗️ Architecture

The system follows a modular architecture:

1. **JobDescriptionAnalyzer** - Handles structured job data extraction
2. **ResumeSuggestionGenerator** - Performs resume-job matching analysis
3. **CoverLetterGenerator** - Creates personalized application documents

Each component uses:
- LangChain prompt templates
- Pydantic output parsing
- Ollama LLM integration

## 🔍 Example Output

### Job Details
```
Job Title: Senior Python Developer
Experience Required: 5 years
Required Skills: Python, Django, FastAPI, Flask
Tools: PostgreSQL, Redis, Docker, Kubernetes, AWS
Soft Skills: Communication, Team player, Problem-solving, Leadership
```

### Resume Suggestions
```
Missing Skills to Add:
   • PostgreSQL database experience
   • AWS cloud services
   • Kubernetes orchestration

Improvement Points:
   • Add specific metrics to achievements
   • Include leadership experience
   • Highlight scalable system design

Overall Fit Summary: 70% fit - Good foundation with room for skill expansion
```

## 🎯 Use Cases

- **Job Seekers**: Optimize applications for better success rates
- **Career Counselors**: Provide data-driven resume improvement advice
- **HR Professionals**: Understand job requirement patterns
- **Students**: Learn about industry requirements and resume writing

## 🤝 Contributing

This is a demonstration project. For production use, consider additional validation and professional review processes.

## 📄 License

This project is provided as-is for educational and demonstration purposes.</content>
<parameter name="filePath">c:\Users\jhanv\OneDrive\Documents\ollama\README_project1.md