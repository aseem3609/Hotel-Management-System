"""Dashboard window: key totals and charts for the Hotel Management System."""

from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from db import get_connection, ensure_schema, ensure_reviews_table


# Same pricing used in the booking screen, kept here for revenue estimates.
ROOM_PRICE = {"Single": 1500, "Double": 1000, "Luxury": 3000}
MEAL_PRICE = {"Breakfast": 150, "Lunch": 500, "Dinner": 800}


class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1295x650+150+80")
        self.root.configure(bg="#0f1b2d")

        ensure_schema()
        ensure_reviews_table()

        lbl_title = Label(self.root, text="HOTEL DASHBOARD",
                          font=("times new roman", 28, "bold"),
                          bg="black", fg="gold", bd=4, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X)

        # Top row of summary cards.
        self.cards_frame = Frame(self.root, bg="#0f1b2d")
        self.cards_frame.pack(side=TOP, fill=X, padx=10, pady=12)

        # Charts area.
        self.charts_frame = Frame(self.root, bg="#0f1b2d")
        self.charts_frame.pack(side=TOP, fill=BOTH, expand=1, padx=10, pady=5)

        refresh_btn = Button(self.root, text="Refresh", font=("arial", 12, "bold"),
                             bg="black", fg="gold", width=12, command=self.load)
        refresh_btn.pack(side=BOTTOM, pady=8)

        self.load()

    # ------------------------------------------------------------------
    def _query(self, sql, params=()):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        connection.close()
        return rows

    def load(self):
        try:
            stats = self._gather_stats()
        except Exception as es:
            messagebox.showerror("Error", f"Could not load dashboard data:\n{es}", parent=self.root)
            return
        self._render_cards(stats)
        self._render_charts(stats)

    def _gather_stats(self):
        today = datetime.now().strftime("%Y/%m/%d")

        total_rooms = self._query("SELECT COUNT(*) FROM details")[0][0]
        occupied = self._query(
            "SELECT COUNT(DISTINCT `Room No`) FROM room "
            "WHERE Status='Checked-in' AND `Checkin date` <= %s AND `Checkout date` > %s",
            (today, today),
        )[0][0]
        available = max(total_rooms - occupied, 0)

        checkins_today = self._query(
            "SELECT COUNT(*) FROM room WHERE `Checkin date`=%s", (today,))[0][0]
        checkouts_today = self._query(
            "SELECT COUNT(*) FROM room WHERE `Checkout date`=%s", (today,))[0][0]

        total_customers = self._query("SELECT COUNT(*) FROM customer")[0][0]

        # Revenue estimate from active bookings.
        bookings = self._query(
            "SELECT `Room Type`, Meal, `No Of Days` FROM room WHERE Status='Checked-in'")
        revenue = 0
        for room_type, meal, days in bookings:
            try:
                days = int(days)
            except (TypeError, ValueError):
                days = 0
            per_day = ROOM_PRICE.get(room_type, 0) + MEAL_PRICE.get(meal, 0)
            net = per_day * days
            revenue += net + 0.04 * net

        # Occupancy by room type for a chart.
        type_rows = self._query("SELECT `Room Type`, COUNT(*) FROM details GROUP BY `Room Type`")
        rooms_by_type = {t: c for t, c in type_rows}

        booked_rows = self._query(
            "SELECT `Room Type`, COUNT(*) FROM room WHERE Status='Checked-in' GROUP BY `Room Type`")
        booked_by_type = {t: c for t, c in booked_rows}

        # Status distribution.
        status_rows = self._query("SELECT Status, COUNT(*) FROM room GROUP BY Status")
        status_dist = {s: c for s, c in status_rows}

        # Review sentiment breakdown.
        sentiment_rows = self._query("SELECT sentiment, COUNT(*) FROM reviews GROUP BY sentiment")
        sentiment_dist = {s: c for s, c in sentiment_rows}
        total_reviews = sum(sentiment_dist.values())
        positive_pct = round(sentiment_dist.get("Positive", 0) * 100 / total_reviews) if total_reviews else 0

        return {
            "total_rooms": total_rooms,
            "occupied": occupied,
            "available": available,
            "checkins_today": checkins_today,
            "checkouts_today": checkouts_today,
            "total_customers": total_customers,
            "revenue": round(revenue, 2),
            "rooms_by_type": rooms_by_type,
            "booked_by_type": booked_by_type,
            "status_dist": status_dist,
            "sentiment_dist": sentiment_dist,
            "total_reviews": total_reviews,
            "positive_pct": positive_pct,
        }

    def _render_cards(self, stats):
        for w in self.cards_frame.winfo_children():
            w.destroy()

        cards = [
            ("Total Rooms", stats["total_rooms"], "#2563eb"),
            ("Occupied", stats["occupied"], "#dc2626"),
            ("Available", stats["available"], "#16a34a"),
            ("Check-ins Today", stats["checkins_today"], "#9333ea"),
            ("Check-outs Today", stats["checkouts_today"], "#ea580c"),
            ("Customers", stats["total_customers"], "#0891b2"),
            ("Revenue (active)", stats["revenue"], "#ca8a04"),
            ("Positive Reviews", f"{stats['positive_pct']}%", "#15803d"),
        ]
        for i, (title, value, color) in enumerate(cards):
            card = Frame(self.cards_frame, bg=color, bd=2, relief=RIDGE)
            card.grid(row=0, column=i, padx=6, ipadx=6, ipady=6, sticky="nsew")
            self.cards_frame.grid_columnconfigure(i, weight=1)
            Label(card, text=str(value), font=("arial", 20, "bold"),
                  bg=color, fg="white").pack(pady=(8, 0))
            Label(card, text=title, font=("arial", 11, "bold"),
                  bg=color, fg="white").pack(pady=(0, 8))

    def _render_charts(self, stats):
        for w in self.charts_frame.winfo_children():
            w.destroy()

        fig = Figure(figsize=(12, 4.2), dpi=100)
        fig.patch.set_facecolor("#0f1b2d")

        # Chart 1: occupancy (occupied vs available).
        ax1 = fig.add_subplot(1, 4, 1)
        occ = [stats["occupied"], stats["available"]]
        if sum(occ) == 0:
            occ = [0, 1]
        ax1.pie(occ, labels=["Occupied", "Available"], autopct="%1.0f%%",
                colors=["#dc2626", "#16a34a"], textprops={"color": "white"})
        ax1.set_title("Room Occupancy", color="white")

        # Chart 2: rooms booked by type.
        ax2 = fig.add_subplot(1, 4, 2)
        types = list(stats["rooms_by_type"].keys()) or ["None"]
        booked = [stats["booked_by_type"].get(t, 0) for t in types]
        ax2.bar(types, booked, color="#2563eb")
        ax2.set_title("Active Bookings by Room Type", color="white")
        ax2.set_facecolor("#16243a")
        ax2.tick_params(colors="white")
        for spine in ax2.spines.values():
            spine.set_color("white")

        # Chart 3: booking status distribution.
        ax3 = fig.add_subplot(1, 4, 3)
        status = stats["status_dist"]
        if status:
            ax3.bar(list(status.keys()), list(status.values()), color="#ca8a04")
        else:
            ax3.bar(["No data"], [0], color="#ca8a04")
        ax3.set_title("Bookings by Status", color="white")
        ax3.set_facecolor("#16243a")
        ax3.tick_params(colors="white")
        for spine in ax3.spines.values():
            spine.set_color("white")

        # Chart 4: review sentiment breakdown.
        ax4 = fig.add_subplot(1, 4, 4)
        sentiment = stats["sentiment_dist"]
        if stats["total_reviews"]:
            order = ["Positive", "Neutral", "Negative"]
            values = [sentiment.get(s, 0) for s in order]
            ax4.pie(values, labels=order, autopct="%1.0f%%",
                    colors=["#16a34a", "#f59e0b", "#dc2626"], textprops={"color": "white"})
        else:
            ax4.pie([1], labels=["No reviews"], colors=["#6b7280"], textprops={"color": "white"})
        ax4.set_title("Review Sentiment", color="white")

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.charts_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)


if __name__ == "__main__":
    root = Tk()
    obj = Dashboard(root)
    root.mainloop()
