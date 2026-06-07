"""Customer reviews with automatic sentiment analysis.

Uses VADER (vaderSentiment) to classify each review as Positive, Negative
or Neutral. VADER is lightweight, needs no model download, and works well
on short, informal feedback text.
"""

from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from db import get_connection, ensure_reviews_table


# One shared analyzer instance for the whole window.
_analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    """Return (label, compound_score) for a piece of review text."""
    score = _analyzer.polarity_scores(text or "")["compound"]
    if score >= 0.05:
        label = "Positive"
    elif score <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
    return label, score


class Reviews:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Reviews & Sentiment")
        self.root.geometry("1295x550+230+220")

        ensure_reviews_table()

        # ---------------- variables ----------------
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_rating = StringVar()
        self.var_search = StringVar()
        self.var_filter = StringVar()

        # ---------------- title ----------------
        lbl_title = Label(self.root, text="CUSTOMER REVIEWS & SENTIMENT ANALYSIS",
                          font=("times new roman", 18, "bold"),
                          bg="black", fg="gold", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1295, height=50)

        # ---------------- left form ----------------
        form = LabelFrame(self.root, bd=2, relief=RIDGE, text="Add Review",
                          padx=2, font=("times new roman", 12, "bold"))
        form.place(x=5, y=60, width=420, height=470)

        Label(form, text="Customer Contact", font=("arial", 12, "bold"), padx=2, pady=6).grid(row=0, column=0, sticky=W)
        ttk.Entry(form, width=22, textvariable=self.var_contact, font=("arial", 12, "bold")).grid(row=0, column=1)

        btn_fetch = Button(form, text="Fetch", font=("arial", 8, "bold"), bg="black", fg="gold",
                           width=6, command=self.fetch_customer)
        btn_fetch.grid(row=0, column=2, padx=2)

        Label(form, text="Customer Name", font=("arial", 12, "bold"), padx=2, pady=6).grid(row=1, column=0, sticky=W)
        ttk.Entry(form, width=22, textvariable=self.var_name, font=("arial", 12, "bold")).grid(row=1, column=1)

        Label(form, text="Rating (1-5)", font=("arial", 12, "bold"), padx=2, pady=6).grid(row=2, column=0, sticky=W)
        combo_rating = ttk.Combobox(form, textvariable=self.var_rating, font=("arial", 12, "bold"),
                                    width=20, state="readonly")
        combo_rating["value"] = ("5", "4", "3", "2", "1")
        combo_rating.current(0)
        combo_rating.grid(row=2, column=1)

        Label(form, text="Review", font=("arial", 12, "bold"), padx=2, pady=6).grid(row=3, column=0, sticky=NW)
        self.txt_review = Text(form, width=30, height=8, font=("arial", 11))
        self.txt_review.grid(row=3, column=1, columnspan=2, pady=4)

        # live sentiment preview
        self.lbl_preview = Label(form, text="Sentiment: -", font=("arial", 12, "bold"), fg="gray")
        self.lbl_preview.grid(row=4, column=0, columnspan=3, pady=4)

        btns = Frame(form)
        btns.grid(row=5, column=0, columnspan=3, pady=6)
        Button(btns, text="Analyze", font=("arial", 11, "bold"), bg="black", fg="gold",
               width=9, command=self.preview_sentiment).grid(row=0, column=0, padx=2)
        Button(btns, text="Submit", font=("arial", 11, "bold"), bg="black", fg="gold",
               width=9, command=self.add_review).grid(row=0, column=1, padx=2)
        Button(btns, text="Delete", font=("arial", 11, "bold"), bg="black", fg="gold",
               width=9, command=self.delete_review).grid(row=0, column=2, padx=2)
        Button(btns, text="Reset", font=("arial", 11, "bold"), bg="black", fg="gold",
               width=9, command=self.reset).grid(row=0, column=3, padx=2)

        # summary line
        self.lbl_summary = Label(form, text="", font=("arial", 11, "bold"), fg="darkgreen")
        self.lbl_summary.grid(row=6, column=0, columnspan=3, pady=6)

        # ---------------- right table ----------------
        table_frame = LabelFrame(self.root, bd=2, relief=RIDGE, text="All Reviews",
                                 padx=2, font=("times new roman", 12, "bold"))
        table_frame.place(x=435, y=60, width=855, height=470)

        Label(table_frame, text="Filter:", font=("arial", 11, "bold")).grid(row=0, column=0, padx=2, pady=4)
        combo_filter = ttk.Combobox(table_frame, textvariable=self.var_filter, font=("arial", 11, "bold"),
                                    width=14, state="readonly")
        combo_filter["value"] = ("All", "Positive", "Negative", "Neutral")
        combo_filter.current(0)
        combo_filter.grid(row=0, column=1, padx=2)
        combo_filter.bind("<<ComboboxSelected>>", lambda e: self.fetch_data())

        Label(table_frame, text="Search contact:", font=("arial", 11, "bold")).grid(row=0, column=2, padx=2)
        ttk.Entry(table_frame, width=18, textvariable=self.var_search, font=("arial", 11, "bold")).grid(row=0, column=3, padx=2)
        Button(table_frame, text="Search", font=("arial", 10, "bold"), bg="black", fg="gold",
               command=self.fetch_data).grid(row=0, column=4, padx=2)
        Button(table_frame, text="Show All", font=("arial", 10, "bold"), bg="black", fg="gold",
               command=self.show_all).grid(row=0, column=5, padx=2)

        tbl = Frame(table_frame, bd=2, relief=RIDGE)
        tbl.place(x=0, y=45, width=840, height=390)

        scroll_x = ttk.Scrollbar(tbl, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tbl, orient=VERTICAL)

        self.review_table = ttk.Treeview(
            tbl,
            column=("id", "contact", "name", "rating", "review", "sentiment", "score", "date"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.review_table.xview)
        scroll_y.config(command=self.review_table.yview)

        headings = {
            "id": ("ID", 40),
            "contact": ("Contact", 90),
            "name": ("Name", 110),
            "rating": ("Rating", 55),
            "review": ("Review", 250),
            "sentiment": ("Sentiment", 80),
            "score": ("Score", 60),
            "date": ("Date", 130),
        }
        for col, (text, width) in headings.items():
            self.review_table.heading(col, text=text)
            self.review_table.column(col, width=width)
        self.review_table["show"] = "headings"
        self.review_table.pack(fill=BOTH, expand=1)
        self.review_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()

    # ------------------------------------------------------------------
    def fetch_customer(self):
        if self.var_contact.get() == "":
            messagebox.showerror("Error", "Please enter the customer contact.", parent=self.root)
            return
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT Name FROM customer WHERE Mobile=%s", (self.var_contact.get(),))
        row = cursor.fetchone()
        connection.close()
        if row:
            self.var_name.set(row[0])
        else:
            messagebox.showinfo("Info", "No customer found for that contact.", parent=self.root)

    def preview_sentiment(self):
        text = self.txt_review.get("1.0", END).strip()
        if not text:
            self.lbl_preview.config(text="Sentiment: -", fg="gray")
            return None, None
        label, score = analyze_sentiment(text)
        colors = {"Positive": "green", "Negative": "red", "Neutral": "orange"}
        self.lbl_preview.config(text=f"Sentiment: {label}  ({score:+.2f})", fg=colors[label])
        return label, score

    def add_review(self):
        text = self.txt_review.get("1.0", END).strip()
        if self.var_contact.get() == "" or text == "":
            messagebox.showerror("Error", "Customer contact and review text are required.", parent=self.root)
            return
        label, score = analyze_sentiment(text)
        try:
            rating = int(self.var_rating.get())
        except (TypeError, ValueError):
            rating = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO reviews "
                "(customer_contact, customer_name, rating, review_text, sentiment, sentiment_score, created_at) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (self.var_contact.get(), self.var_name.get(), rating, text, label, score,
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            connection.commit()
            connection.close()
            self.preview_sentiment()
            self.fetch_data()
            messagebox.showinfo("Success", f"Review saved. Sentiment: {label}", parent=self.root)
        except Exception as es:
            messagebox.showwarning("Warning", f"Something went wrong: {es}", parent=self.root)

    def get_cursor(self, event=""):
        cursor_row = self.review_table.focus()
        content = self.review_table.item(cursor_row)
        row = content["values"]
        if not row:
            return
        self._selected_id = row[0]
        self.var_contact.set(row[1])
        self.var_name.set(row[2])
        self.var_rating.set(str(row[3]))
        self.txt_review.delete("1.0", END)
        self.txt_review.insert(END, row[4])
        self.preview_sentiment()

    def delete_review(self):
        selected = getattr(self, "_selected_id", None)
        if not selected:
            messagebox.showerror("Error", "Please select a review from the table.", parent=self.root)
            return
        if not messagebox.askyesno("Confirm", "Delete this review?", parent=self.root):
            return
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM reviews WHERE id=%s", (selected,))
        connection.commit()
        connection.close()
        self.reset()
        self.fetch_data()

    def reset(self):
        self.var_contact.set("")
        self.var_name.set("")
        self.txt_review.delete("1.0", END)
        self.lbl_preview.config(text="Sentiment: -", fg="gray")
        self._selected_id = None

    def show_all(self):
        self.var_search.set("")
        self.var_filter.set("All")
        self.fetch_data()

    def fetch_data(self):
        query = ("SELECT id, customer_contact, customer_name, rating, review_text, "
                 "sentiment, sentiment_score, created_at FROM reviews")
        conditions = []
        params = []
        if self.var_filter.get() and self.var_filter.get() != "All":
            conditions.append("sentiment=%s")
            params.append(self.var_filter.get())
        if self.var_search.get().strip():
            conditions.append("customer_contact LIKE %s")
            params.append("%" + self.var_search.get().strip() + "%")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY id DESC"

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        connection.close()

        self.review_table.delete(*self.review_table.get_children())
        pos = neg = neu = 0
        for r in rows:
            r = list(r)
            if r[6] is not None:
                r[6] = round(r[6], 2)
            self.review_table.insert("", END, values=r)
            if r[5] == "Positive":
                pos += 1
            elif r[5] == "Negative":
                neg += 1
            else:
                neu += 1

        total = pos + neg + neu
        if total:
            self.lbl_summary.config(
                text=f"Total: {total}   |   Positive: {pos} ({pos*100//total}%)   "
                     f"Negative: {neg}   Neutral: {neu}")
        else:
            self.lbl_summary.config(text="No reviews yet.")


if __name__ == "__main__":
    root = Tk()
    obj = Reviews(root)
    root.mainloop()
