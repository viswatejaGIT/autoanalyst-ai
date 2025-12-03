# AutoAnalyst AI

Tired of staring at spreadsheets trying to figure out what your data is telling you? This tool does the heavy lifting for you.

Just upload your CSV or Excel file, and get executive-level insights in plain English - no data science degree required.

## What it does

Upload a file → Get business insights that actually make sense

- **Executive Summary**: What's in your data, explained like you're talking to your boss
- **Key Numbers**: The important stuff with actual figures
- **What to do next**: Actionable recommendations you can implement
- **Red flags**: Problems in your data you should know about

## Why I built this

I got tired of:
- Spending hours trying to understand what datasets mean
- Writing the same analysis code over and over
- Explaining data in technical jargon that nobody understands

So I made this. It takes any spreadsheet and tells you what matters in business terms.

## How to use it

1. Get an OpenAI API key (costs like $5 for hundreds of analyses)
2. Clone this repo
3. Install stuff: `pip install -r requirements.txt`
4. Create a `.env` file with your API key:
   ```
   OPENAI_API_KEY=your_key_here
   ```
5. Run it: `streamlit run app.py`
6. Upload your file and click the button

## What it works with

- CSV files
- Excel files (.xlsx)
- Pretty much any tabular data

## Built with

- Streamlit (for the web interface)
- Pandas (for data handling)
- OpenAI GPT-4 (for the smart analysis)
- A bunch of Python libraries

## Examples of what you'll get

Instead of "The mean of column A is 47.3 with a standard deviation of 12.8", you get:

"Your sales data shows an average deal size of $47K, but there's significant variation. Three deals over $100K are skewing your numbers upward - investigate these outliers."

## Contributing

Found a bug? Have an idea? Open an issue or send a PR. I'm always looking to make this better.

## License

MIT - do whatever you want with it.

---

*Stop wrestling with spreadsheets. Let AI do the analysis.*