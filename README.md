# 🔍 Generative-Output-Comparison-Suite

A powerful, interactive Streamlit application for analyzing and evaluating AI responses across three critical dimensions: **Helpfulness**, **Truthfulness**, and **Harmlessness**. Perfect for researchers, developers, and AI enthusiasts who want to systematically assess prompt quality and response effectiveness.

![GPT Feedback Engine](https://img.shields.io/badge/Built%20with-Streamlit-FF6B6B)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

### 🚀 Advanced Prompt Analysis Studio
- **Professional Templates**: Pre-built templates for Educational, Creative, Business, Technical, and Analysis prompts
- **Real-time Quality Scoring**: Instant analysis of prompt complexity, clarity, and quality
- **Smart Suggestions**: AI-powered recommendations to improve your prompts
- **Multiple Response Methods**: Write custom responses, use samples, or generate variations

### 📊 Comprehensive Analytics Dashboard
- **Visual Progress Tracking**: Beautiful progress bars and completion metrics
- **Interactive Charts**: Score distribution analysis using Plotly
- **Real-time Metrics**: Word count, character analysis, and reading level assessment
- **Historical Insights**: Track evaluation trends over time

### 🔄 Prompt Comparison Lab
- **Side-by-side Analysis**: Compare different prompts and their responses
- **Detailed Metrics**: Comprehensive comparison of prompt effectiveness
- **A/B Testing**: Perfect for optimizing prompt performance

### 📝 Professional Evaluation System
- **3-Dimensional Scoring**: Rate responses on Helpfulness (1-5), Truthfulness (1-5), and Harmlessness (1-5)
- **Descriptive Labels**: Clear rating scale from Poor to Excellent
- **Detailed Comments**: Add comprehensive feedback and observations
- **Export Reports**: Generate professional analysis reports

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS styling
- **Data Visualization**: Plotly for interactive charts
- **Data Storage**: JSON-based persistence with PostgreSQL support
- **Analytics**: Pandas for data processing and analysis
- **Backend**: Python 3.11+ with modern libraries

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/gpt-feedback-engine.git
cd gpt-feedback-engine
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run main.py
```

4. **Open your browser**
Navigate to `http://localhost:8501` to start using the GPT Feedback Engine!

## 📋 Dependencies

```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
psycopg2-binary>=2.9.0
sqlalchemy>=2.0.0
requests>=2.31.0
```

## 🎯 How to Use

### 1. Analyze Custom Prompts
- Choose from professional templates or write your own
- Get instant quality analysis and suggestions
- Add responses manually or use sample responses
- Rate responses across three key dimensions

### 2. Review Existing Prompts
- Browse through your evaluation history
- View comprehensive analytics and trends
- Filter by evaluation status
- Navigate with smart controls

### 3. Compare Prompts
- Test different prompt approaches side by side
- Compare effectiveness metrics
- Optimize your prompt strategies

## 📊 Project Structure

```
gpt-feedback-engine/
├── main.py                 # Main Streamlit application
├── utils.py               # Utility functions for data handling
├── database.py            # Database operations (optional)
├── data/
│   ├── prompts.json       # Sample prompts and responses
│   └── evaluations.json   # Stored evaluations
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
```

## 🔧 Configuration

### Streamlit Configuration
The app comes with optimized Streamlit settings in `.streamlit/config.toml`:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

### Database Setup (Optional)
For production use, you can enable PostgreSQL support:
1. Set up a PostgreSQL database
2. Configure the `DATABASE_URL` environment variable
3. The app will automatically migrate existing JSON data

## 📈 Key Metrics and Analytics

The GPT Feedback Engine provides comprehensive analytics including:

- **Response Quality Scores**: Average ratings across all three dimensions
- **Prompt Effectiveness**: Analysis of prompt characteristics that lead to better responses
- **Evaluation Trends**: Historical performance tracking
- **Content Analysis**: Word count, complexity, and structure analysis

## 🎨 Customization

### Adding New Prompt Templates
Edit the `prompt_templates` dictionary in `main.py`:
```python
prompt_templates = {
    "Your Template": "Your template text with [PLACEHOLDERS]",
    # ... existing templates
}
```

### Custom Scoring Criteria
Modify the evaluation criteria in the rating sections to match your specific needs.

### Styling
Custom CSS is included for professional appearance. Modify the styling in the `st.markdown()` sections.

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Contribution Areas
- New prompt templates
- Additional analytics features
- UI/UX improvements
- Performance optimizations
- Documentation enhancements

## 📝 Use Cases

### For Researchers
- Systematic evaluation of AI model outputs
- Comparative analysis of different prompting strategies
- Data collection for AI safety research

### For Developers
- Testing and optimizing chatbot responses
- Quality assurance for AI-powered applications
- Prompt engineering and optimization

### For Educators
- Teaching prompt engineering techniques
- Demonstrating AI evaluation methodologies
- Student assessment tools

### For Content Creators
- Improving AI-generated content quality
- Developing effective prompting strategies
- Content evaluation and optimization

## 🔐 Privacy and Security

- All data is stored locally by default
- No external API calls required for core functionality
- Optional database encryption support
- User data remains private and secure

## 📊 Sample Analysis Report

The engine generates detailed reports including:
- Prompt and response analysis
- Quality metrics and scores
- Improvement recommendations
- Trend analysis

## 🚀 Deployment

### Local Development
```bash
streamlit run main.py
```

### Production Deployment
The app is ready for deployment on platforms like:
- Streamlit Cloud
- Heroku
- AWS
- Google Cloud Platform

## 🐛 Troubleshooting

### Common Issues

**App won't start**
- Ensure Python 3.11+ is installed
- Check all dependencies are installed
- Verify port 8501 is available

**Data not saving**
- Check file permissions in the `data/` directory
- Ensure the application has write access

**Charts not displaying**
- Verify Plotly is installed correctly
- Check browser compatibility

## 🔮 Future Enhancements

- [ ] Multi-language support
- [ ] Advanced AI model integrations
- [ ] Collaborative evaluation features
- [ ] API endpoint for programmatic access
- [ ] Mobile-responsive design
- [ ] Export to multiple formats (PDF, CSV, Excel)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Visualizations powered by [Plotly](https://plotly.com/)
- Inspired by AI safety and evaluation research

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review existing issues for solutions

---

**Made with ❤️ for the AI research and development community**

*Star this repository if you find it useful! ⭐*
