import requests
from bs4 import BeautifulSoup
import webbrowser
import hashlib
import os
import tempfile

def fetch_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching the URL: {e}")
        return None

def generate_filename_from_url(url):
    domain = url.split("//")[-1].split("/")[0]
    hashed = hashlib.md5(url.encode()).hexdigest()[:6]
    return f"scraped_{domain}_{hashed}.txt"

def save_to_file(data_list, section_name, filename):
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"\n--- {section_name} ---\n")
            for item in data_list:
                f.write(item + '\n')
        print(f"✅ {section_name} saved to '{filename}'")
    except Exception as e:
        print(f"⚠️ Failed to save {section_name}: {e}")

def scrape_headings(soup, filename=None):
    print("\n📚 Headings found on the page:")
    headings = []
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        for heading in soup.find_all(tag):
            text = f"{tag.upper()}: {heading.get_text(strip=True)}"
            print(text)
            headings.append(text)

    if filename and input("💾 Save headings to file? (yes/no): ").strip().lower() == 'yes':
        save_to_file(headings, "Headings", filename)

def scrape_paragraphs(soup, filename=None):
    print("\n📝 Paragraphs found on the page:")
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]
    for para in paragraphs:
        print(para)

    if filename and input("💾 Save paragraphs to file? (yes/no): ").strip().lower() == 'yes':
        save_to_file(paragraphs, "Paragraphs", filename)

def scrape_links(soup, base_url, filename=None):
    print("\n🔗 Links found on the page:")
    links = soup.find_all('a', href=True)
    if not links:
        print("No links found.")
        return

    formatted_links = []
    for i, link in enumerate(links):
        text = link.get_text(strip=True) or "No text"
        href = link['href']
        full_url = requests.compat.urljoin(base_url, href)
        entry = f"{i + 1}. {text} → {full_url}"
        print(entry)
        formatted_links.append(entry)

    if filename and input("💾 Save links to file? (yes/no): ").strip().lower() == 'yes':
        save_to_file(formatted_links, "Links", filename)

    try:
        choice = int(input("\nEnter the number of the link to open (0 to skip): "))
        if 1 <= choice <= len(links):
            href = links[choice - 1]['href']
            full_url = requests.compat.urljoin(base_url, href)
            webbrowser.open_new(full_url)
            print(f"🌐 Opened: {full_url}")
        elif choice == 0:
            print("🔕 No link opened.")
        else:
            print("❌ Invalid choice.")
    except ValueError:
        print("⚠️ Invalid input. Please enter a number.")

def open_images_in_browser(image_urls, num):
    html_content = "<html><head><title>Image Viewer</title></head><body style='text-align:center;'>"
    html_content += "".join(
        f'<img src="{url}" style="max-width:90%; margin:10px;"><br>' for url in image_urls[:num]
    )
    html_content += "</body></html>"

    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as f:
        f.write(html_content)
        webbrowser.open_new_tab(f.name)
    print(f"✅ Opened {num} image(s) in browser via a single HTML page.")

def scrape_images(soup, base_url, filename=None):
    print("\n🖼️ Found images on the page:")
    image_urls = []
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            full_src = requests.compat.urljoin(base_url, src)
            if full_src.startswith("http") and len(full_src) < 2000:
                image_urls.append(full_src)
            else:
                print(f"⚠️ Skipped: {full_src[:60]}...")

    total = len(image_urls)
    print(f"🔍 {total} valid image(s) found.")

    if filename and input("💾 Save image URLs to file? (yes/no): ").strip().lower() == 'yes':
        save_to_file(image_urls, "Image URLs", filename)

    if total == 0:
        return

    while True:
        try:
            num = int(input(f"How many images to open? (0–{total}): "))
            if 0 <= num <= total:
                break
            print("❌ Invalid number.")
        except ValueError:
            print("⚠️ Please enter a number.")

    if num > 0:
        open_images_in_browser(image_urls, num)

def scrape_all(soup, url):
    filename = generate_filename_from_url(url)
    mode = 'a' if os.path.exists(filename) else 'w'
    print(f"📦 Saving scraped data to '{filename}' ({'appending' if mode == 'a' else 'creating new'})...")

    headings = [f"{tag.upper()}: {h.get_text(strip=True)}"
                for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
                for h in soup.find_all(tag)]

    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]

    links = [f"{i+1}. {link.get_text(strip=True) or 'No text'} → {requests.compat.urljoin(url, link['href'])}"
             for i, link in enumerate(soup.find_all('a', href=True))]

    images = [requests.compat.urljoin(url, img['src'])
              for img in soup.find_all('img') if img.get('src') and len(img.get('src')) < 2000]

    try:
        with open(filename, mode, encoding='utf-8') as f:
            f.write(f"\n\n===== Scraped from: {url} =====\n\n")
            f.write("--- Headings ---\n" + "\n".join(headings) + "\n\n")
            f.write("--- Paragraphs ---\n" + "\n".join(paragraphs) + "\n\n")
            f.write("--- Links ---\n" + "\n".join(links) + "\n\n")
            f.write("--- Image URLs ---\n" + "\n".join(images) + "\n")
        print(f"✅ All data saved to '{filename}'.")
    except Exception as e:
        print(f"⚠️ Error saving data: {e}")

def scraper_menu():
    print("\n📋 --- Web Scraper Menu ---")
    print("1. Scrape Headings")
    print("2. Scrape Links & Open Option")
    print("3. Scrape Paragraphs")
    print("4. Scrape Images")
    print("5. Scrape & Save All Data")
    print("6. Exit Current URL")

def main():
    while True:
        url = input("\n🔗 Enter the URL of the website: ").strip()
        soup = fetch_html(url)
        if not soup:
            continue

        filename = generate_filename_from_url(url)

        while True:
            scraper_menu()
            choice = input("Enter your choice (1-6): ").strip()
            if choice == '1':
                scrape_headings(soup, filename)
            elif choice == '2':
                scrape_links(soup, url, filename)
            elif choice == '3':
                scrape_paragraphs(soup, filename)
            elif choice == '4':
                scrape_images(soup, url, filename)
            elif choice == '5':
                scrape_all(soup, url)
            elif choice == '6':
                break
            else:
                print("⚠️ Invalid option. Please choose 1–6.")

        again = input("\n🔁 Do you want to scrape another website? (yes/no): ").strip().lower()
        if again != 'yes':
            print("👋 Exiting Web Scraper. Happy Scraping!")
            break

if __name__ == "__main__":
    main()
