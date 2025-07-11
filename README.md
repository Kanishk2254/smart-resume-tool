# 🎯 Smart Resume Tool

A comprehensive AI-powered resume analysis and creation tool that combines resume analysis, job matching, and resume generation in one unified interface.

## 🌟 Features

### 🔍 **Resume Analysis**
- **Job Match Scoring**: Compare your resume against job descriptions using TF-IDF similarity
- **Missing Keywords**: Identify important keywords your resume is missing
- **Skill Categorization**: Automatically categorize and highlight your skills
- **Visual Feedback**: Get color-coded feedback on your resume's job match score

### 📝 **Resume Creation**
- **Interactive Form**: Fill out a user-friendly form with your information
- **PDF Generation**: Create professional PDF resumes instantly
- **Download Ready**: Get your resume in PDF format ready for applications

### 🚀 **All-in-One Interface**
- **Sidebar Navigation**: Easy switching between tools
- **Single Application**: No need to run multiple programs
- **Streamlined Workflow**: Analyze and create resumes in one place

## 🛠️ **Enhanced Skill Categories**

The tool recognizes skills across **9 major categories**:

- **Programming**: Python, Java, C++, JavaScript, TypeScript, PHP, Ruby, Go, Rust, Kotlin, Swift
- **Data Science**: Machine Learning, Pandas, NumPy, TensorFlow, PyTorch, Tableau, Power BI, SQL
- **Web Development**: React, Angular, Vue, Django, Flask, Node.js, Express, Laravel, Spring
- **Cloud & DevOps**: AWS, Azure, Docker, Kubernetes, Git, Jenkins, Terraform, Ansible
- **Mobile Development**: Android, iOS, React Native, Flutter, Xamarin, Ionic
- **Database**: SQL, NoSQL, MongoDB, PostgreSQL, MySQL, Redis, Elasticsearch
- **Testing**: Selenium, Jest, PyTest, JUnit, Cypress, Automation Testing
- **Project Management**: Agile, Scrum, Jira, Kanban, Leadership, Team Management
- **Soft Skills**: Communication, Leadership, Teamwork, Problem Solving, Creativity

## 🚀 **Quick Start**

### **Installation**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/smart-resume-tool.git
   cd smart-resume-tool
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run Smart_Resume_Tool.py
   ```

### **Usage**

1. **Open your browser** and go to `http://localhost:8501`

2. **Choose your tool** from the sidebar:
   - **Resume Analyser**: Upload resume and job description PDFs
   - **Resume Creator**: Fill out form and generate resume

## 📊 **Resume Analysis Features**

### **Job Match Scoring**
- Uses TF-IDF vectorization for accurate similarity calculation
- Provides percentage match score between resume and job description
- Color-coded feedback for easy interpretation

### **Keyword Analysis**
- Identifies missing keywords from job descriptions
- Highlights matching keywords in your resume
- Helps optimize resume for ATS systems

### **Skill Detection**
- Automatically categorizes skills into relevant domains
- Comprehensive skill database across multiple industries
- Visual presentation of detected skills

## 📄 **Resume Creation Features**

### **User-Friendly Form**
- **Personal Information**: Name, email, phone, address
- **Education**: Academic background and qualifications
- **Work Experience**: Professional history and achievements
- **Skills**: Technical and soft skills
- **Projects**: Notable projects and accomplishments

### **PDF Generation**
- Professional formatting
- Clean, readable layout
- Instant download capability
- Ready for job applications

## 🔧 **Technical Details**

### **Technologies Used**
- **Streamlit**: Web application framework
- **scikit-learn**: Machine learning for text analysis
- **pdfplumber**: PDF text extraction
- **FPDF**: PDF generation
- **TF-IDF**: Text similarity calculation

### **Requirements**
- Python 3.7+
- streamlit
- scikit-learn
- pdfplumber
- fpdf2
- pandas
- numpy

## 📁 **Project Structure**

```
smart-resume-tool/
├── Smart_Resume_Tool.py    # Main application
├── requirements.txt        # Dependencies
├── README.md              # Documentation
├── .gitignore            # Git ignore file
└── generated_resumes/    # Output directory (created automatically)
```

## 🎯 **Use Cases**

### **For Job Seekers**
- Analyze resume compatibility with job postings
- Identify missing skills and keywords
- Create professional resumes quickly
- Optimize applications for ATS systems

### **For Career Counselors**
- Help clients improve their resumes
- Identify skill gaps for career development
- Generate professional documents efficiently

### **For Recruiters**
- Assess candidate-job fit
- Understand skill distributions
- Generate standardized resume formats

## 🔒 **Privacy & Security**

- **No data storage**: Files are processed locally and not stored
- **Temporary processing**: PDFs are only used during analysis
- **User control**: All data remains on your machine

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📊 **Performance**

- **Fast Processing**: Optimized algorithms for quick analysis
- **Memory Efficient**: Handles large PDFs without memory issues
- **Scalable**: Can process multiple resumes in sequence

## 🛠️ **Troubleshooting**

### **Common Issues**

1. **PDF extraction errors**:
   - Ensure PDFs are not password-protected
   - Verify PDFs contain selectable text
   - Check file size (recommended < 10MB)

2. **Installation issues**:
   - Use Python 3.7 or higher
   - Install dependencies in a virtual environment
   - Update pip: `pip install --upgrade pip`

3. **Performance issues**:
   - Close other applications to free memory
   - Use smaller PDF files for testing
   - Restart the application if needed

## 🎨 **Future Enhancements**

- [ ] **Multiple file format support** (Word, txt)
- [ ] **Batch processing** for multiple resumes
- [ ] **Resume templates** with different styles
- [ ] **ATS compatibility scoring**
- [ ] **Industry-specific keyword suggestions**
- [ ] **Resume improvement recommendations**

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- Built with ❤️ using Streamlit
- Powered by scikit-learn for ML capabilities
- PDF processing by pdfplumber
- Resume generation with FPDF

## 📞 **Support**

For questions, issues, or feature requests:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

---

**Transform your resume game today! 🚀**

*Made with ❤️ for job seekers everywhere*
