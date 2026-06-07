"""Customer segmentation using KMeans clustering.

This is UNSUPERVISED learning: there is no training step and no saved model.
Every time you press "Run Segmentation" it reads the current customers and
their bookings, then groups them automatically into:

    * Premium  - high spenders
    * Frequent - many stays
    * Budget   - low spend / few stays

Just keep adding customers and bookings, then run it again to re-group.
"""

from tkinter import *
from tkinter import ttk, messagebox

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from db import get_connection


# Same pricing used elsewhere in the app, for estimating each customer's spend.
ROOM_PRICE = {"Single": 1500, "Double": 1000, "Luxury": 3000}
MEAL_PRICE = {"Breakfast": 150, "Lunch": 500, "Dinner": 800}

SEGMENT_COLORS = {
    "Premium": "#15803d",
    "Frequent": "#2563eb",
    "Budget": "#ca8a04",
    "Unclassified": "#6b7280",
}


class Customer_Segmentation:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Segmentation")
        self.root.geometry("1100x560+200+120")

        lbl_title = Label(self.root, text="CUSTOMER SEGMENTATION (AUTO GROUPING)",
                          font=("times new roman", 18, "bold"),
                          bg="black", fg="gold", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1100, height=50)

        top = Frame(self.root, bd=2, relief=RIDGE)
        top.place(x=5, y=55, width=1090, height=50)

        Label(top, text="Number of groups (k):", font=("arial", 12, "bold")).pack(side=LEFT, padx=8)
        self.var_k = StringVar(value="3")
        ttk.Combobox(top, textvariable=self.var_k, values=("2", "3", "4", "5"),
                     width=5, state="readonly", font=("arial", 12, "bold")).pack(side=LEFT)

        Button(top, text="Run Segmentation", font=("arial", 12, "bold"), bg="black", fg="gold",
               command=self.run_segmentation).pack(side=LEFT, padx=12)
        self.lbl_status = Label(top, text="", font=("arial", 11, "bold"), fg="darkgreen")
        self.lbl_status.pack(side=LEFT, padx=10)

        # ---------------- results table ----------------
        table_frame = Frame(self.root, bd=2, relief=RIDGE)
        table_frame.place(x=5, y=110, width=1090, height=440)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.table = ttk.Treeview(
            table_frame,
            column=("name", "contact", "nationality", "bookings", "days", "spend", "favtype", "segment"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.table.xview)
        scroll_y.config(command=self.table.yview)

        headings = {
            "name": ("Customer", 150),
            "contact": ("Contact", 110),
            "nationality": ("Nationality", 100),
            "bookings": ("Bookings", 80),
            "days": ("Total Days", 90),
            "spend": ("Total Spend", 110),
            "favtype": ("Favourite Room", 120),
            "segment": ("Segment", 120),
        }
        for col, (text, width) in headings.items():
            self.table.heading(col, text=text)
            self.table.column(col, width=width)
        self.table["show"] = "headings"
        self.table.pack(fill=BOTH, expand=1)

        # colour rows by segment
        for seg, colour in SEGMENT_COLORS.items():
            self.table.tag_configure(seg, foreground=colour)

    # ------------------------------------------------------------------
    def _load_customer_features(self):
        """Return a list of dicts, one per customer, with aggregated features."""
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT Name, Mobile, Nationality FROM customer")
        customers = cursor.fetchall()

        cursor.execute(
            "SELECT `Customer Contact`, `Room Type`, Meal, `No Of Days` FROM room")
        bookings = cursor.fetchall()
        connection.close()

        # Aggregate bookings per contact.
        agg = {}
        for contact, room_type, meal, days in bookings:
            try:
                days = int(days)
            except (TypeError, ValueError):
                days = 0
            per_day = ROOM_PRICE.get(room_type, 0) + MEAL_PRICE.get(meal, 0)
            net = per_day * days
            spend = net + 0.04 * net

            entry = agg.setdefault(str(contact), {"bookings": 0, "days": 0, "spend": 0.0, "types": {}})
            entry["bookings"] += 1
            entry["days"] += days
            entry["spend"] += spend
            if room_type:
                entry["types"][room_type] = entry["types"].get(room_type, 0) + 1

        result = []
        for name, mobile, nationality in customers:
            stats = agg.get(str(mobile), {"bookings": 0, "days": 0, "spend": 0.0, "types": {}})
            fav_type = max(stats["types"], key=stats["types"].get) if stats["types"] else "-"
            result.append({
                "name": name,
                "contact": mobile,
                "nationality": nationality,
                "bookings": stats["bookings"],
                "days": stats["days"],
                "spend": round(stats["spend"], 2),
                "favtype": fav_type,
            })
        return result

    def _label_clusters(self, model, k):
        """Map raw cluster numbers to Premium / Frequent / Budget labels.

        Uses the cluster centres (un-scaled) so the naming reflects real
        spend and booking behaviour rather than arbitrary cluster ids.
        """
        # centres back in original units: [bookings, days, spend]
        centres = self.scaler.inverse_transform(model.cluster_centers_)
        order = list(range(k))

        labels = {}
        remaining = set(order)

        # Highest average spend -> Premium
        premium = max(remaining, key=lambda c: centres[c][2])
        labels[premium] = "Premium"
        remaining.discard(premium)

        # Of the rest, most bookings -> Frequent
        if remaining:
            frequent = max(remaining, key=lambda c: centres[c][0])
            labels[frequent] = "Frequent"
            remaining.discard(frequent)

        # Everyone else -> Budget
        for c in remaining:
            labels[c] = "Budget"
        return labels

    def run_segmentation(self):
        try:
            data = self._load_customer_features()
        except Exception as es:
            messagebox.showerror("Error", f"Could not load data:\n{es}", parent=self.root)
            return

        self.table.delete(*self.table.get_children())

        if len(data) == 0:
            self.lbl_status.config(text="No customers found.", fg="red")
            return

        k = int(self.var_k.get())
        # KMeans needs at least k customers; shrink k if there are fewer.
        k = min(k, len(data))

        if k < 2:
            # Not enough customers to form groups - show them as Unclassified.
            for d in data:
                self.table.insert("", END, tags=("Unclassified",), values=(
                    d["name"], d["contact"], d["nationality"], d["bookings"],
                    d["days"], d["spend"], d["favtype"], "Unclassified"))
            self.lbl_status.config(text="Add at least 2 customers to form groups.", fg="orange")
            return

        # Feature matrix: [bookings, total days, total spend]
        X = [[d["bookings"], d["days"], d["spend"]] for d in data]
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        cluster_ids = model.fit_predict(X_scaled)

        label_map = self._label_clusters(model, k)

        counts = {}
        for d, cid in zip(data, cluster_ids):
            segment = label_map.get(cid, "Budget")
            counts[segment] = counts.get(segment, 0) + 1
            self.table.insert("", END, tags=(segment,), values=(
                d["name"], d["contact"], d["nationality"], d["bookings"],
                d["days"], d["spend"], d["favtype"], segment))

        summary = "   ".join(f"{seg}: {n}" for seg, n in counts.items())
        self.lbl_status.config(text=f"{len(data)} customers grouped  |  {summary}", fg="darkgreen")


if __name__ == "__main__":
    root = Tk()
    obj = Customer_Segmentation(root)
    root.mainloop()
