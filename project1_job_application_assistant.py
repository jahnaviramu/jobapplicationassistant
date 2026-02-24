"""
Project 1: AI Job Application Assistant
========================================
Analyzes job descriptions and helps candidates tailor their applications.

Features:
- Job Description Analyzer: Extract structured job details
- Resume Improvement Suggestions: Generate tailored improvements
- Cover Letter Generator: Create professional cover letters
"""

from typing import List
from pydantic import BaseModel, Field
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.runnables import RunnablePassthrough


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class JobDetails(BaseModel):
    """Structured job details extracted from job description."""
    job_title: str = Field(..., description="The job title")
    required_skills: List[str] = Field(..., description="List of required technical skills")
    experience_required: int = Field(..., description="Years of experience required")
    tools: List[str] = Field(..., description="Tools and technologies mentioned")
    soft_skills: List[str] = Field(..., description="Required soft skills")


class ResumeSuggestions(BaseModel):
    """Resume improvement suggestions based on job requirements."""
    missing_skills: List[str] = Field(..., description="Skills to add to resume")
    improvement_points: List[str] = Field(..., description="Specific improvements to resume")
    overall_fit_summary: str = Field(..., description="Overall fit assessment (0-100%)")


# ============================================================================
# FEATURE 1: JOB DESCRIPTION ANALYZER
# ============================================================================

class JobDescriptionAnalyzer:
    """Extract structured information from job descriptions."""
    
    def __init__(self, model_name: str = "mistral"):
        """Initialize with Ollama LLM."""
        self.llm = Ollama(model=model_name, temperature=0.3)
        self.output_parser = PydanticOutputParser(pydantic_object=JobDetails)
        self._setup_prompt()
    
    def _setup_prompt(self):
        """Setup the prompt template with format instructions."""
        format_instructions = self.output_parser.get_format_instructions()
        
        self.prompt = PromptTemplate(
            input_variables=["job_description"],
            template="""Analyze the following job description and extract structured information.

Job Description:
{job_description}

{format_instructions}

Provide the extracted information in the specified JSON format.""",
            partial_variables={"format_instructions": format_instructions},
        )
    
    def analyze(self, job_description: str) -> JobDetails:
        """
        Analyze job description and return structured job details.
        
        Args:
            job_description: The job description text
            
        Returns:
            JobDetails object with extracted information
        """
        chain = self.prompt | self.llm | self.output_parser
        result = chain.invoke({"job_description": job_description})
        return result


# ============================================================================
# FEATURE 2: RESUME IMPROVEMENT SUGGESTIONS
# ============================================================================

class ResumeSuggestionGenerator:
    """Generate tailored resume improvement suggestions."""
    
    def __init__(self, model_name: str = "mistral"):
        """Initialize with Ollama LLM."""
        self.llm = Ollama(model=model_name, temperature=0.5)
        self.output_parser = PydanticOutputParser(pydantic_object=ResumeSuggestions)
        self._setup_prompt()
    
    def _setup_prompt(self):
        """Setup the prompt template with format instructions."""
        format_instructions = self.output_parser.get_format_instructions()
        
        self.prompt = PromptTemplate(
            input_variables=["job_details", "current_resume"],
            template="""Based on the job requirements and current resume, generate improvement suggestions.

Job Requirements:
- Title: {job_details}
- Skills needed: {required_skills}
- Experience: {experience_required} years
- Tools: {tools}

Current Resume:
{current_resume}

{format_instructions}

Provide structured suggestions to improve the resume for this job position.""",
            partial_variables={"format_instructions": format_instructions},
        )
    
    def generate_suggestions(
        self, 
        job_details: JobDetails, 
        current_resume: str
    ) -> ResumeSuggestions:
        """
        Generate resume improvement suggestions.
        
        Args:
            job_details: JobDetails object from analyzer
            current_resume: Current resume text
            
        Returns:
            ResumeSuggestions object with tailored recommendations
        """
        chain = self.prompt | self.llm | self.output_parser
        result = chain.invoke({
            "job_details": job_details.job_title,
            "required_skills": ", ".join(job_details.required_skills),
            "experience_required": job_details.experience_required,
            "tools": ", ".join(job_details.tools),
            "current_resume": current_resume,
        })
        return result


# ============================================================================
# FEATURE 3: COVER LETTER GENERATOR
# ============================================================================

class CoverLetterGenerator:
    """Generate professional cover letters."""
    
    def __init__(self, model_name: str = "mistral"):
        """Initialize with Ollama LLM."""
        self.llm = Ollama(model=model_name, temperature=0.7)
        self.output_parser = StrOutputParser()
        self._setup_prompt()
    
    def _setup_prompt(self):
        """Setup the prompt template."""
        self.prompt = PromptTemplate(
            input_variables=[
                "candidate_name", 
                "job_title", 
                "company_name",
                "key_achievements",
                "job_requirements"
            ],
            template="""Write a professional cover letter for the following position:

Candidate Name: {candidate_name}
Job Title: {job_title}
Company: {company_name}

Key Achievements:
{key_achievements}

Job Requirements:
{job_requirements}

Instructions:
- Write a compelling cover letter (300-400 words)
- Highlight relevant experience
- Match key requirements from job description
- Use professional tone
- Include specific examples from achievements
- Output only the cover letter text, no JSON or formatting markers

Cover Letter:"""
        )
    
    def generate(
        self,
        candidate_name: str,
        job_title: str,
        company_name: str,
        key_achievements: str,
        job_requirements: str
    ) -> str:
        """
        Generate a professional cover letter.
        
        Args:
            candidate_name: Name of the candidate
            job_title: Position applied for
            company_name: Company name
            key_achievements: Candidate's key achievements
            job_requirements: Key requirements from job description
            
        Returns:
            Generated cover letter as plain text
        """
        chain = self.prompt | self.llm | self.output_parser
        result = chain.invoke({
            "candidate_name": candidate_name,
            "job_title": job_title,
            "company_name": company_name,
            "key_achievements": key_achievements,
            "job_requirements": job_requirements,
        })
        return result


# ============================================================================
# MAIN EXECUTION & EXAMPLES
# ============================================================================

def main():
    """Run all features of the Job Application Assistant."""
    
    print("\n" + "=" * 80)
    print("PROJECT 1: AI JOB APPLICATION ASSISTANT")
    print("=" * 80)
    
    # Sample job description
    job_description = """
    Senior Python Developer
    
    We are looking for a Senior Python Developer with 5+ years of experience.
    
    Required Skills:
    - Python (Django, FastAPI, Flask)
    - PostgreSQL and Redis
    - Docker and Kubernetes
    - AWS (EC2, S3, Lambda)
    - RESTful API design
    
    Responsibilities:
    - Design and develop scalable web applications
    - Lead code reviews and mentor junior developers
    - Optimize database performance
    - Collaborate with DevOps team
    
    Soft Skills:
    - Strong communication
    - Team player
    - Problem-solving
    - Leadership experience
    """
    
    # Sample resume
    sample_resume = """
    JOHN DOE
    john.doe@email.com | linkedin.com/in/johndoe
    
    EXPERIENCE:
    Python Developer at Tech Corp (3 years)
    - Developed REST APIs using Flask
    - Worked with MySQL databases
    - Basic Docker experience
    
    Junior Developer at Startup (2 years)
    - Built web applications
    - Fixed bugs and optimized code
    
    SKILLS:
    - Python, JavaScript
    - Flask, Django
    - MySQL
    - Git
    """
    
    # ========== FEATURE 1: JOB DESCRIPTION ANALYZER ==========
    print("\n" + "-" * 80)
    print("FEATURE 1: JOB DESCRIPTION ANALYZER")
    print("-" * 80)
    
    try:
        analyzer = JobDescriptionAnalyzer(model_name="mistral")
        job_details = analyzer.analyze(job_description)
        
        print("\n✅ Extracted Job Details:")
        print(f"   Job Title: {job_details.job_title}")
        print(f"   Experience Required: {job_details.experience_required} years")
        print(f"   Required Skills: {', '.join(job_details.required_skills)}")
        print(f"   Tools: {', '.join(job_details.tools)}")
        print(f"   Soft Skills: {', '.join(job_details.soft_skills)}")
        
    except Exception as e:
        print(f"❌ Error in Job Description Analyzer: {e}")
        return
    
    # ========== FEATURE 2: RESUME IMPROVEMENT SUGGESTIONS ==========
    print("\n" + "-" * 80)
    print("FEATURE 2: RESUME IMPROVEMENT SUGGESTIONS")
    print("-" * 80)
    
    try:
        suggestion_gen = ResumeSuggestionGenerator(model_name="mistral")
        suggestions = suggestion_gen.generate_suggestions(job_details, sample_resume)
        
        print("\n✅ Resume Improvement Suggestions:")
        print(f"\n   Missing Skills to Add:")
        for skill in suggestions.missing_skills:
            print(f"      • {skill}")
        
        print(f"\n   Improvement Points:")
        for point in suggestions.improvement_points:
            print(f"      • {point}")
        
        print(f"\n   Overall Fit Summary: {suggestions.overall_fit_summary}")
        
    except Exception as e:
        print(f"❌ Error in Resume Suggestion Generator: {e}")
        return
    
    # ========== FEATURE 3: COVER LETTER GENERATOR ==========
    print("\n" + "-" * 80)
    print("FEATURE 3: COVER LETTER GENERATOR")
    print("-" * 80)
    
    try:
        cover_letter_gen = CoverLetterGenerator(model_name="mistral")
        cover_letter = cover_letter_gen.generate(
            candidate_name="John Doe",
            job_title="Senior Python Developer",
            company_name="Tech Corp",
            key_achievements="""
            - Led development of 3 REST APIs serving 100K+ users
            - Optimized database queries reducing response time by 40%
            - Mentored 2 junior developers
            - Implemented CI/CD pipelines using Docker
            """,
            job_requirements="Python, Django, FastAPI, PostgreSQL, Redis, Docker, AWS"
        )
        
        print("\n✅ Generated Cover Letter:")
        print("\n" + "-" * 80)
        print(cover_letter)
        print("-" * 80)
        
    except Exception as e:
        print(f"❌ Error in Cover Letter Generator: {e}")
        return
    
    print("\n" + "=" * 80)
    print("✅ PROJECT 1 COMPLETED SUCCESSFULLY!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
