import tkinter as tk
from tkinter import filedialog, messagebox
import nltk
import string
import matplotlib.pyplot as plt
from collections import Counter

try:
    nltk.data.find('tokenizers/punkt')
except:
    nltk.download('punkt')

from nltk.tokenize import word_tokenize

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    return [w for w in tokens if w.isalpha()]

def choose_file():
    path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if path:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, content)

def analyze():
    content = text_area.get(1.0, tk.END)

    if not content.strip():
        messagebox.showwarning("Thông báo", "Vui lòng chọn file trước!")
        return

    words = preprocess_text(content)
    word_freq = Counter(words)
    top_words = word_freq.most_common(10)

    bigrams = []
    for i in range(len(words) - 1):
        bigrams.append(words[i] + " " + words[i+1])

    bigram_counts = Counter(bigrams)
    top_phrases = bigram_counts.most_common(10)

    result_area.delete(1.0, tk.END)

    result_area.insert(tk.END, "===== TOP 10 TỪ KHÓA ĐƠN =====\n\n")
    for w, c in top_words:
        result_area.insert(tk.END, f"{w} ({c})\n")

    result_area.insert(tk.END, "\n===== TOP 10 CỤM TỪ KHÓA =====\n\n")
    for p, c in top_phrases:
        result_area.insert(tk.END, f"{p} ({c})\n")


    text_area.tag_delete("word_tag")
    text_area.tag_delete("phrase_tag")

    text_area.tag_config("word_tag", underline=True, foreground="blue")
    text_area.tag_config("phrase_tag", underline=True, foreground="red")

    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, content)

    
    for word, _ in top_words:
        start = "1.0"
        while True:
            pos = text_area.search(r'\m' + word + r'\M',
                                   start,
                                   stopindex=tk.END,
                                   regexp=True,
                                   nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(word)}c"
            text_area.tag_add("word_tag", pos, end)
            start = end


    for phrase, _ in top_phrases:
        start = "1.0"
        while True:
            pos = text_area.search(phrase,
                                   start,
                                   stopindex=tk.END,
                                   nocase=True)
            if not pos:
                break
            end = f"{pos}+{len(phrase)}c"
            text_area.tag_add("phrase_tag", pos, end)
            start = end

    text_area.tag_raise("phrase_tag")

    plot_pie_charts(top_words, top_phrases)

def plot_pie_charts(top_words, top_phrases):

    words = [w for w, _ in top_words]
    word_counts = [c for _, c in top_words]

    phrases = [p for p, _ in top_phrases]
    phrase_counts = [c for _, c in top_phrases]

    plt.figure(figsize=(14, 7))

    plt.subplot(1, 2, 1)
    plt.pie(word_counts,
            labels=words,
            autopct='%1.1f%%',
            startangle=90)
    plt.title("Top 10 từ đơn", fontsize=14, fontweight="bold")

    plt.subplot(1, 2, 2)
    plt.pie(phrase_counts,
            labels=phrases,
            autopct='%1.1f%%',
            startangle=90)
    plt.title("Top 10 cụm từ", fontsize=14, fontweight="bold")

    plt.tight_layout()
    plt.show()


root = tk.Tk()
root.title("Phân tích văn bản")
root.geometry("1000x600")
root.configure(bg="#e6e6e6")

header = tk.Label(root,
                  text="CHƯƠNG TRÌNH PHÂN TÍCH VÀ THỐNG KÊ TỪ KHÓA",
                  bg="#2c3e50", fg="white",
                  font=("Arial", 16, "bold"),
                  pady=10)
header.pack(fill=tk.X)

main_frame = tk.Frame(root, bg="#e6e6e6")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

left_frame = tk.LabelFrame(main_frame,
                           text="NỘI DUNG VĂN BẢN",
                           font=("Arial", 11, "bold"),
                           padx=10, pady=10)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

btn_choose = tk.Button(left_frame,
                       text="Chọn file văn bản (.txt)",
                       bg="#3498db", fg="white",
                       command=choose_file)
btn_choose.pack(pady=5)

text_area = tk.Text(left_frame, wrap=tk.WORD)
text_area.pack(fill=tk.BOTH, expand=True)

right_frame = tk.LabelFrame(main_frame,
                            text="KẾT QUẢ PHÂN TÍCH",
                            font=("Arial", 11, "bold"),
                            padx=10, pady=10)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

btn_analyze = tk.Button(right_frame,
                        text="Phân tích văn bản",
                        bg="#27ae60", fg="white",
                        command=analyze)
btn_analyze.pack(pady=5)

result_area = tk.Text(right_frame, wrap=tk.WORD)
result_area.pack(fill=tk.BOTH, expand=True)

root.mainloop()