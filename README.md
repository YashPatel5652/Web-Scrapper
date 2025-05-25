# 🌐 Interactive Web Scraper CLI

A Python command-line tool that scrapes web content like headings, paragraphs, links, and images from any URL. It offers interactive saving, link browsing, and image previews in the browser. All data can be saved to uniquely named text files based on the URL.

---

## ✨ Features

- 📚 Extract **headings** (`<h1>` to `<h6>`)
- 📝 Extract **paragraphs**
- 🔗 Extract and optionally open **links**
- 🖼️ Extract **images** and open selected ones in browser
- 💾 Save data into structured `.txt` files with domain-based filenames
- 📦 Scrape and save **everything** in one go
- ✅ Automatically appends to file if it already exists

---
# 🌐 Interactive Web Scraper CLI

A Python command-line tool that scrapes web content like headings, paragraphs, links, and images from any URL. It offers interactive saving, link browsing, and image previews in the browser. All data can be saved to uniquely named text files based on the URL.

---

## ✨ Features

- 📚 Extract **headings** (`<h1>` to `<h6>`)
- 📝 Extract **paragraphs**
- 🔗 Extract and optionally open **links**
- 🖼️ Extract **images** and open selected ones in browser
- 💾 Save data into structured `.txt` files with domain-based filenames
- 📦 Scrape and save **everything** in one go
- ✅ Automatically appends to file if it already exists

---

## 📂 Folder Structure

```
.
├── scraper.py          # Main script file
├── scraped_*.txt       # Output files (generated dynamically)
```

---

## 🧰 Requirements

Install the dependencies using `pip`:

```bash
pip install requests beautifulsoup4
```

You may also need:

```bash
pip install Pillow  # Only required if you modify for image processing
```

---

## 🚀 How to Run

```bash
python -m streamlit run Web_scrapper.py
```

You will be prompted to enter a URL and interact with a menu-driven interface to scrape and save different components of the page.

---

## 📋 Menu Options

1. **Scrape Headings** – Displays and optionally saves all headings  
2. **Scrape Links** – Lists all links and allows opening one in browser  
3. **Scrape Paragraphs** – Displays and optionally saves text content  
4. **Scrape Images** – Lists image URLs and opens selected images in a browser tab  
5. **Scrape & Save All Data** – Saves everything (headings, links, paragraphs, and images) into one `.txt` file  
6. **Exit** – Go back or quit scraping  

---

## 📁 Output File Format

Saved `.txt` files follow this format:

```
===== Scraped from: https://example.com =====

--- Headings ---
H1: Example Heading

--- Paragraphs ---
This is a sample paragraph.

--- Links ---
1. Link text → https://example.com/page

--- Image URLs ---
https://example.com/image.jpg
```

Filenames are generated like:  
`scraped_example_com_<hash>.txt`

---

## 💡 Notes

- Invalid or very long image URLs are skipped
- Safe browsing is ensured using `requests.compat.urljoin` for resolving relative links
- The script uses `tempfile` to open selected images in a temporary HTML page

---

## 📃 License

This project is released under the **MIT License**. Feel free to modify and use it as needed.

---

## 🙋‍♂️ Author

**[Your Name]**  
Connect on [GitHub](https://github.com/YashPatel5652) | [LinkedIn](www.linkedin.com/in/yash-patel-bb2984303)

---

## 📌 TODO / Ideas for Extension

- Add image downloading support
- Export data in JSON or CSV format
- Add GUI using Tkinter or PyQt
- Add CLI argument support for automation
