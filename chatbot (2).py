import tkinter as tk
from tkinter import scrolledtext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk, string
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

FAQS = {
    "What is CodeAlpha?": "CodeAlpha is a leading software development company focused on innovation and emerging technologies.",
    "How do I apply for an internship?": "Visit www.codealpha.tech and fill out the internship application form.",
    "What are the internship perks?": "Interns receive an offer letter, completion certificate, recommendation letter, and placement support.",
    "How long is the internship?": "The internship duration is typically 1 month.",
    "What tasks do I need to complete?": "You must complete at least 2 out of the 4 assigned tasks in your domain.",
    "How do I submit my tasks?": "Upload your code to GitHub and submit via the form shared in your WhatsApp group.",
    "Will I get a certificate?": "Yes, you receive a QR-verified completion certificate after finishing at least 2 tasks.",
    "What is the GitHub naming convention?": "Name your repository as CodeAlpha_ProjectName.",
    "How do I contact CodeAlpha?": "Email: services@codealpha.tech or WhatsApp: +91 9336576683.",
    "Do I need to post on LinkedIn?": "Yes, share your internship status and a video of your project on LinkedIn, tagging @CodeAlpha.",
}

questions = list(FAQS.keys())
answers = list(FAQS.values())
stop_words = set(stopwords.words('english'))

def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    return " ".join([t for t in tokens if t not in stop_words and t not in string.punctuation])

processed_qs = [preprocess(q) for q in questions]

def get_answer(user_input):
    processed_input = preprocess(user_input)
    vectorizer = TfidfVectorizer()
    all_texts = processed_qs + [processed_input]
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    best_idx = similarities.argmax()
    best_score = similarities[0][best_idx]
    if best_score < 0.1:
        return "Sorry, I don't have an answer to that. Please contact services@codealpha.tech"
    return answers[best_idx]

def send_message(event=None):
    user_msg = entry.get().strip()
    if not user_msg:
        return
    chat_area.config(state="normal")
    chat_area.insert(tk.END, f"You: {user_msg}\n", "user")
    response = get_answer(user_msg)
    chat_area.insert(tk.END, f"Bot: {response}\n\n", "bot")
    chat_area.config(state="disabled")
    chat_area.see(tk.END)
    entry.delete(0, tk.END)

root = tk.Tk()
root.title("CodeAlpha FAQ Chatbot")
root.geometry("600x500")
root.resizable(False, False)

tk.Label(root, text="CodeAlpha FAQ Chatbot", font=("Arial", 15, "bold")).pack(pady=10)

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="disabled",
                                       font=("Arial", 11), height=20, width=68)
chat_area.pack(padx=15, pady=5)
chat_area.tag_config("user", foreground="#2563eb", font=("Arial", 11, "bold"))
chat_area.tag_config("bot", foreground="#16a34a")

frame = tk.Frame(root)
frame.pack(fill="x", padx=15, pady=8)
entry = tk.Entry(frame, font=("Arial", 11))
entry.pack(side="left", fill="x", expand=True, ipady=6)
entry.bind("<Return>", send_message)
tk.Button(frame, text="Send", command=send_message,
          bg="#2563eb", fg="white", font=("Arial", 11), padx=14).pack(side="right", padx=(8,0))

chat_area.config(state="normal")
chat_area.insert(tk.END, "Bot: Hello! Ask me anything about CodeAlpha internship.\n\n", "bot")
chat_area.config(state="disabled")

root.mainloop()
