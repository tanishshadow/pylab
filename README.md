# Coding Profile Analytics

Streamlit apps for checking competitive programming profile stats from LeetCode and Codeforces.

## Features

- LeetCode profile lookup by username
- LeetCode solved problem count by difficulty
- Codeforces profile lookup by handle
- Codeforces rating history graph
- Codeforces solved problem difficulty distribution
- Basic Codeforces topic strength and weak area detection

## Project Files

```text
pylab/
+-- lc.py        # LeetCode analytics app
+-- cf.py        # Codeforces analytics app
+-- README.md    # Setup and usage guide
```

## Requirements

- Python 3.9 or newer
- Internet connection
- A valid LeetCode username or Codeforces handle

## Installation

1. Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY/pylab
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment.

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install streamlit requests matplotlib
```

## Running The Apps

### LeetCode Analytics

```bash
streamlit run lc.py
```

Enter a LeetCode username and click **Analyze**.

### Codeforces Analytics

```bash
streamlit run cf.py
```

Enter a Codeforces handle and click **Analyze**.

## Dependencies

This project uses:

- `streamlit` for the web interface
- `requests` for API calls
- `matplotlib` for graphs

Optional `requirements.txt` content:

```text
streamlit
requests
matplotlib
```

## API Notes

- LeetCode data is fetched from the LeetCode GraphQL endpoint.
- Codeforces data is fetched from the public Codeforces API.
- The apps require internet access while running.
- If an API is temporarily down or rate-limited, the app may show an error message.

## GitHub Upload Guide

From the main repository folder:

```bash
git add pylab/lc.py pylab/cf.py pylab/README.md
git commit -m "Add coding profile analytics apps"
git push origin main
```

If your default branch is named `master`, use:

```bash
git push origin master
```

## License

Add a license file if you want others to reuse or modify this project.
