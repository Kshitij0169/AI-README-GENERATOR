# 🎉 GitHub Repository Analyzer with Streamlit

Welcome to the **GitHub Repository Analyzer**! This project provides a user-friendly interface to analyze codebases hosted on GitHub using **Streamlit** and **OpenAI**'s API. With this application, you can extract and visualize codebase details in a few simple steps.

## 🚀 Features
- **Streamlit Interface**: A clean and interactive web application built with Streamlit.
- **OpenAI Integration**: Utilize OpenAI's powerful models to analyze code and generate insights.
- **Environment Variables**: Securely manage API keys using a `.env` file.

## 📁 Project Structure
```
.
├── .env
├── app.py
└── myapp-env
```

- **`.env`**: Contains environment variables, including the OpenAI API key.
- **`app.py`**: The main application file where the Streamlit app is defined.
- **`myapp-env`**: A virtual environment for managing project dependencies (not included in the repository).

## ⚙️ Installation

To get started with this project, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/repo-name.git
   cd repo-name
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv myapp-env
   source myapp-env/bin/activate  # On Windows use `myapp-env\Scripts\activate`
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**: Add your OpenAI API key to this file.
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🛠️ Usage

1. **Run the application**:
   ```bash
   streamlit run app.py
   ```

2. **Navigate to the local server**: Open your web browser and go to `http://localhost:8501`.

3. **Input a GitHub repository URL**: Paste the URL of the GitHub repository you want to analyze.

4. **Explore the results**: The app will display the codebase details and insights generated using OpenAI.

## 📄 Example Usage

```python
# Example function to extract codebase details from a GitHub repository
def get_repo_files_and_contents(github_url):
    github_url = github_url.rstrip('.git')
    # ... (function implementation)
```

## 📝 Additional Information
- Make sure to keep your API keys secure and not share your `.env` file.
- Contributions to improve the app or add new features are welcome! Please create a pull request or open an issue.

## 🤝 Contributing
If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

## 📞 Contact
For any questions or feedback, feel free to reach out:

- **Email**: your-email@example.com
- **GitHub**: [yourusername](https://github.com/yourusername)

---

Thank you for checking out the GitHub Repository Analyzer! Enjoy analyzing your favorite repositories! 🚀
