import streamlit as st
from library import Library
from books import Book
from member_basic import Member
from exceptions import (
    LibraryError,
    MemberNotFoundError,
    BookNotFoundError,
    BookNotAvailableError,
    BorrowLimitExceededError,
)

from pathlib import Path
import csv
import io


# ---------- PAGE CONFIG ----------
# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="🏰 Maygal Books Vault",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="expanded",
)



# ---------- CUSTOM STYLING ----------
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <style>
    /* ===== GLOBAL THEME ===== */
    :root {
        --gold: #D4AF37;
        --dark-blue: #1A2A3A;
        --accent-blue: #2D5F8D;
        --bg-dark: #0F1419;
        --surface: #1a1f2e;
        --surface-light: #232A3E;
        --text-primary: #F5F1E8;
        --text-secondary: #B8B5A8;
        --border-color: rgba(212, 175, 55, 0.15);
    }

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0F1419 0%, #1A1F2E 50%, #0F1419 100%);
        color: var(--text-primary);
    }

    /* Remove Streamlit defaults */
    header {
        background: transparent !important;
        border: none !important;
    }

    /* ===== TYPOGRAPHY ===== */
    * {
        font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }

    h1, h2, h3 {
        font-family: "Playfair Display", serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.8px;
        color: var(--gold) !important;
        text-shadow: 0 2px 8px rgba(212, 175, 55, 0.2);
    }

    h1 {
        font-size: 2.8rem !important;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        font-size: 2rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }

    h3 {
        font-size: 1.4rem !important;
        color: var(--text-primary) !important;
        text-shadow: none;
    }

    p, span, label {
        color: var(--text-primary);
        font-weight: 400;
        line-height: 1.6;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F1419 0%, #1A2A3A 100%);
        border-right: 1px solid var(--border-color);
    }

    section[data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 1.8rem;
        color: var(--gold) !important;
        margin-bottom: 0.3rem;
    }

    /* ===== CARDS & CONTAINERS ===== */
    .vault-card {
        background: rgba(26, 47, 62, 0.4);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(12px);
        box-shadow:
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(212, 175, 55, 0.1);
        transition: transform 0.3s cubic-bezier(0.23, 1, 0.320, 1),
                    box-shadow 0.3s ease-out,
                    border-color 0.3s ease-out;
        animation: slideUp 0.6s ease-out;
    }

    .vault-card:hover {
        transform: translateY(-6px);
        border-color: rgba(212, 175, 55, 0.35);
        box-shadow:
            0 12px 48px rgba(212, 175, 55, 0.2),
            inset 0 1px 0 rgba(212, 175, 55, 0.15);
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* ===== METRICS ===== */
    .metric-box {
        background: linear-gradient(135deg, rgba(45, 95, 141, 0.2) 0%, rgba(26, 42, 58, 0.3) 100%);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(8px);
        transition: transform 0.25s ease-out, box-shadow 0.25s ease-out;
    }

    .metric-box:hover {
        transform: scale(1.03);
        box-shadow: 0 8px 24px rgba(212, 175, 55, 0.15);
    }

    .metric-value {
        font-family: "Playfair Display", serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--gold);
        text-shadow: 0 2px 4px rgba(212, 175, 55, 0.3);
    }

    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }

    /* ===== INPUT FIELDS ===== */
    .stTextInput > div > div > input,
    .stTextArea textarea,
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] > div {
        background: rgba(15, 20, 25, 0.8) !important;
        color: var(--text-primary) !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        border-radius: 12px !important;
        font-family: "Inter", sans-serif !important;
        font-size: 0.95rem;
        padding: 12px 16px !important;
        transition: all 0.3s ease-out;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea textarea::placeholder {
        color: rgba(212, 175, 55, 0.4) !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus,
    .stSelectbox div[data-baseweb="select"]:focus-within > div {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1) !important;
        background: rgba(15, 20, 25, 0.95) !important;
    }

    /* ===== BUTTONS ===== */
    .stButton > button,
    button[kind="primary"] {
        background: linear-gradient(135deg, #D4AF37 0%, #C9A727 100%);
        color: #0F1419 !important;
        font-family: "Inter", sans-serif !important;
        font-weight: 600;
        font-size: 0.95rem;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 24px !important;
        letter-spacing: 0.5px;
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.35);
        transition: all 0.25s cubic-bezier(0.23, 1, 0.320, 1);
        cursor: pointer;
    }

    .stButton > button:hover,
    button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.5);
        background: linear-gradient(135deg, #E5C158 0%, #D4AF37 100%);
    }

    .stButton > button:active,
    button[kind="primary"]:active {
        transform: translateY(0);
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
    }

    /* Secondary button style */
    button[kind="secondary"],
    .btn-secondary {
        background: rgba(45, 95, 141, 0.3) !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        color: var(--gold) !important;
        box-shadow: none !important;
    }

    button[kind="secondary"]:hover,
    .btn-secondary:hover {
        background: rgba(45, 95, 141, 0.5) !important;
        border-color: var(--gold) !important;
    }

    /* ===== SELECTBOX ===== */
    .stSelectbox div[data-baseweb="select"] > div {
        padding: 12px 16px;
    }

    /* ===== TABLES ===== */
    .stTable {
        font-family: "Inter", sans-serif;
    }

    .stTable table {
        background: rgba(26, 47, 62, 0.4);
        border-collapse: collapse;
    }

    .stTable thead {
        background: linear-gradient(90deg, rgba(212, 175, 55, 0.15) 0%, transparent 100%);
    }

    .stTable th {
        color: var(--gold);
        font-weight: 600;
        letter-spacing: 0.5px;
        border-bottom: 2px solid rgba(212, 175, 55, 0.2);
        padding: 12px 16px;
        text-transform: uppercase;
        font-size: 0.85rem;
    }

    .stTable td {
        color: var(--text-primary);
        border-bottom: 1px solid rgba(212, 175, 55, 0.1);
        padding: 12px 16px;
    }

    .stTable tr:hover {
        background: rgba(212, 175, 55, 0.08);
    }

    /* ===== ALERTS & MESSAGES ===== */
    .stSuccess {
        background: rgba(34, 197, 94, 0.15) !important;
        color: #86EFAC !important;
        border: 1px solid rgba(34, 197, 94, 0.3) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }

    .stError {
        background: rgba(239, 68, 68, 0.15) !important;
        color: #FCA5A5 !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }

    .stWarning {
        background: rgba(245, 158, 11, 0.15) !important;
        color: #FCD34D !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }

    .stInfo {
        background: rgba(59, 130, 246, 0.15) !important;
        color: #93C5FD !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }

    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [role="tablist"] {
        border-bottom: 1px solid rgba(212, 175, 55, 0.1);
    }

    .stTabs [role="tab"] {
        color: var(--text-secondary) !important;
        border-radius: 8px 8px 0 0;
        border-bottom: 3px solid transparent;
    }

    .stTabs [role="tab"][aria-selected="true"] {
        color: var(--gold) !important;
        border-bottom-color: var(--gold) !important;
    }

    /* ===== SPACING & DIVIDERS ===== */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.2), transparent);
        margin: 2rem 0;
    }

    .vault-divider {
        height: 2px;
        background: linear-gradient(90deg, rgba(212, 175, 55, 0.15), rgba(212, 175, 55, 0.3), rgba(212, 175, 55, 0.15));
        margin: 2rem 0;
        border-radius: 1px;
    }

    /* ===== UTILITY ===== */
    .text-gold {
        color: var(--gold);
    }

    .text-secondary {
        color: var(--text-secondary);
    }

    .text-center {
        text-align: center;
    }

    .opacity-75 {
        opacity: 0.75;
    }

    /* Smooth scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(212, 175, 55, 0.05);
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(212, 175, 55, 0.3);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(212, 175, 55, 0.5);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- SESSION LIBRARY ----------
# ---------- SESSION LIBRARY ----------
def get_library():
    if "library" not in st.session_state:
        # ✅ Renamed to your custom brand
        st.session_state.library = Library("Maygal Books Vault")
    return st.session_state.library



# ---------- HELPER COMPONENTS ----------

# ---------- HELPER COMPONENTS ----------

def render_metric(value, label, icon=""):
    """Render a single metric box"""
    st.markdown(
        f"""
<div class="metric-box">
    <div class="metric-value">{value}</div>
    <div class="metric-label">{icon} {label}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_card_header(title, icon=""):
    """Render a card with header styling"""
    st.markdown(
        f"""
<div style="margin-bottom: 1.5rem;">
    <h2 style="margin: 0; color: var(--gold);">{icon} {title}</h2>
    <div class="vault-divider"></div>
</div>
""",
        unsafe_allow_html=True,
    )


# ---------- PAGES ----------

def page_dashboard(library: Library):
    render_card_header("Dashboard", "📊")

    stats = library.stats()

    # Metrics Grid
    cols = st.columns(4)
    with cols[0]:
        render_metric(stats["total_books"], "Total Books", "📖")
    with cols[1]:
        render_metric(stats["total_members"], "Members", "👥")
    with cols[2]:
        render_metric(stats["total_copies"], "Total Copies", "📚")
    with cols[3]:
        render_metric(stats["available_copies"], "Available", "✅")

    st.markdown("<div class='vault-divider'></div>", unsafe_allow_html=True)

    # Additional Stats
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 📈 Library Status")
        try:
            borrowed = stats["total_copies"] - stats["available_copies"]
            borrow_rate = (borrowed / stats["total_copies"] * 100) if stats["total_copies"] > 0 else 0
            st.markdown(
                f"""
<div class="vault-card">
    <p style="margin: 0 0 10px 0;">📤 Borrowed Books: <span class="text-gold"><strong>{borrowed}</strong></span></p>
    <p style="margin: 0;">📊 Borrow Rate: <span class="text-gold"><strong>{borrow_rate:.1f}%</strong></span></p>
</div>
""",
                unsafe_allow_html=True,
            )
        except:
            pass

    with col_right:
        st.markdown("### 💡 Quick Stats")
        st.markdown(
            f"""
<div class="vault-card">
    <p style="margin: 0 0 10px 0;">🎯 Unique Titles: <span class="text-gold"><strong>{len(library._books)}</strong></span></p>
    <p style="margin: 0;">👥 Active Members: <span class="text-gold"><strong>{len(library._members)}</strong></span></p>
</div>
""",
            unsafe_allow_html=True,
        )



def page_add_book(library: Library):
    render_card_header("Add New Book", "➕")

    with st.container():
        st.markdown('<div class="vault-card">', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            book_id = st.text_input("📖 Book ID", key="add_book_id", placeholder="e.g., B001")
            genre = st.text_input("🏷️ Genre", key="add_book_genre", placeholder="e.g., Fiction")

        with col2:
            title = st.text_input("📚 Title", key="add_book_title", placeholder="e.g., The Great Gatsby")
            author = st.text_input("✍️ Author", key="add_book_author", placeholder="e.g., F. Scott Fitzgerald")

        copies = st.number_input("📦 Total Copies", key="add_book_copies", min_value=1, value=1, step=1)

        col_btn, col_empty = st.columns([1, 4])
        with col_btn:
            if st.button("🔥 Add Book", key="add_book_button"):
                if not book_id or not title or not author:
                    st.error("❌ Please fill all required fields.")
                elif library.get_book(book_id):
                    st.warning("⚠️ A book with this ID already exists.")
                else:
                    book = Book(book_id, title, author, genre, copies)
                    library.add_book(book)
                    st.success("✅ Book added successfully to the vault!")

        st.markdown('</div>', unsafe_allow_html=True)


def page_register_member(library: Library):
    render_card_header("Register New Member", "🧑‍🤝‍🧑")

    with st.container():
        st.markdown('<div class="vault-card">', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            member_id = st.text_input("🆔 Member ID", key="reg_member_id", placeholder="e.g., M001")
            email = st.text_input("📧 Email", key="reg_member_email", placeholder="e.g., user@example.com")

        with col2:
            name = st.text_input("👤 Full Name", key="reg_member_name", placeholder="e.g., John Doe")
            max_books = st.number_input(
                "📚 Max Books to Borrow",
                key="reg_member_max",
                min_value=1,
                value=5,
                step=1,
            )

        col_btn, col_empty = st.columns([1, 4])
        with col_btn:
            if st.button("✍️ Register Member", key="reg_member_button"):
                if not member_id or not name:
                    st.error("❌ Please fill all required fields.")
                elif library.get_member(member_id):
                    st.warning("⚠️ A member with this ID already exists.")
                else:
                    member = Member(member_id, name, email, max_books)
                    library.register_member(member)
                    st.success("✅ Member registered successfully!")

        st.markdown('</div>', unsafe_allow_html=True)


def page_issue_book(library: Library):
    render_card_header("Issue Book", "📤")

    members = list(library._members.values())
    books = list(library._books.values())

    if not members or not books:
        st.markdown(
            """
            <div class="vault-card">
                <p style="text-align: center; color: var(--text-secondary);">⚠️ Need at least one member and one book to proceed.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    with st.container():
        st.markdown('<div class="vault-card">', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        member_options = {f"👤 {m._name} (ID: {m._member_id})" : m._member_id for m in members}
        book_options = {
            f"📖 {b.title} by {b.author} ({b.available_copies} available)": b.book_id
            for b in books
        }

        with col1:
            member_label = st.selectbox("Select Member", list(member_options.keys()), key="issue_member")

        with col2:
            book_label = st.selectbox("Select Book", list(book_options.keys()), key="issue_book")

        member_id = member_options[member_label]
        book_id = book_options[book_label]

        col_btn, col_empty = st.columns([1, 4])
        with col_btn:
            if st.button("✅ Issue Book", key="issue_button"):
                try:
                    library.issue_book(member_id, book_id)
                    st.success("✅ Book issued successfully!")
                except (
                    BookNotAvailableError,
                    BorrowLimitExceededError,
                    MemberNotFoundError,
                    BookNotFoundError,
                    LibraryError,
                ) as e:
                    st.error(f"❌ {str(e)}")

        st.markdown('</div>', unsafe_allow_html=True)


def page_return_book(library: Library):
    render_card_header("Return Book", "📥")

    members = list(library._members.values())

    if not members:
        st.info("👥 No members registered yet.")
        return

    with st.container():
        st.markdown('<div class="vault-card">', unsafe_allow_html=True)

        # 1. Select Member First
        member_options = {f"👤 {m._name} (ID: {m._member_id})": m._member_id for m in members}
        member_label = st.selectbox("Select Member", list(member_options.keys()), key="ret_member")
        
        # Get the actual member object using the selected ID
        member_id = member_options[member_label]
        member = library.get_member(member_id)

        # 2. Filter Books: Only show books this member has borrowed!
        if not member._borrowed_books:
            st.info(f"🤷‍♂️ {member._name} has no books to return right now.")
        else:
            # Create a list of only the borrowed books
            borrowed_book_options = {}
            for book_id in member._borrowed_books:
                book = library.get_book(book_id)
                if book:
                    borrowed_book_options[f"📖 {book.title} (ID: {book.book_id})"] = book.book_id
                else:
                    # Fallback if book data is missing for some reason
                    borrowed_book_options[f"ID: {book_id} (Unknown Title)"] = book_id

            # 3. Show the filtered Book dropdown
            book_label = st.selectbox("Select Book to Return", list(borrowed_book_options.keys()), key="ret_book")
            book_id = borrowed_book_options[book_label]

            # Return Button
            col_btn, col_empty = st.columns([1, 4])
            with col_btn:
                if st.button("✅ Return Book", key="ret_button"):
                    try:
                        library.return_book(member_id, book_id)
                        st.success(f"✅ Successfully returned '{book_label.split(' (')[0][2:]}'!")
                        # Rerun to refresh the list immediately
                        st.rerun()
                    except (MemberNotFoundError, BookNotFoundError, LibraryError) as e:
                        st.error(f"❌ {str(e)}")

        st.markdown('</div>', unsafe_allow_html=True)



def page_view_books(library: Library):
    render_card_header("All Books in Vault", "📚")

    with st.container():
        st.markdown('<div class="vault-card">', unsafe_allow_html=True)

        query = st.text_input(
            "🔍 Search by title or author",
            key="view_books_query",
            placeholder="Search...",
        )

        if query:
            books = library.search_books(query)
            st.caption(f"📌 Showing results for: '{query}'")
        else:
            books = list(library._books.values())

        if not books:
            st.info("📭 No books found.")
            return

        rows = [
            {
                "ID": b.book_id,
                "Title": b.title,
                "Author": b.author,
                "Genre": b.genre,
                "Available": b.available_copies,
                "Total": b.total_copies,
            }
            for b in books
        ]

        st.table(rows)

        # Download button
        books_file = Path("data") / "books.csv"
        if books_file.exists():
            csv_content = books_file.read_text(encoding="utf-8")
            st.download_button(
                "📥 Download Books CSV",
                csv_content,
                "books.csv",
                "text/csv",
            )

        st.markdown('</div>', unsafe_allow_html=True)


def page_view_members(library: Library):
    render_card_header("All Registered Members", "👥")

    with st.container():
        st.markdown('<div class="vault-card">', unsafe_allow_html=True)

        members = list(library._members.values())

        if not members:
            st.info("👥 No members registered yet.")
            return

        # Build the rows with book titles
        rows = []
        for m in members:
            # 🔍 LOOKUP LOGIC: Convert Book IDs -> Book Titles
            borrowed_titles = []
            for book_id in m._borrowed_books:
                book = library.get_book(book_id)
                if book:
                    borrowed_titles.append(f"{book.title}")  # Just the title
                else:
                    borrowed_titles.append(f"{book_id} (Unknown)") # Fallback
            
            # Join them into a nice string, e.g., "The Great Gatsby, 1984"
            issued_display = ", ".join(borrowed_titles) if borrowed_titles else "—"

            rows.append({
                "ID": m._member_id,
                "Name": m._name,
                "Email": m._email,
                "Max Books": m._max_books,
                "Issued Books": issued_display  # ✅ NEW COLUMN
            })

        st.table(rows)

        # Download button
        members_file = Path("data") / "members.csv"
        if members_file.exists():
            csv_content = members_file.read_text(encoding="utf-8")
            st.download_button(
                "📥 Download Members CSV",
                csv_content,
                "members.csv",
                "text/csv",
            )

        st.markdown('</div>', unsafe_allow_html=True)




# ---------- MAIN APP ----------

# ---------- MAIN APP ----------

def main():
    # Header with NEW Name
    # 👇 LOOK HERE: No spaces at the start of lines inside """ ... """
    st.markdown(
        """
<div style="margin-bottom: 2rem; animation: fadeIn 0.8s ease-out;">
    <h1 style="margin: 0; font-size: 3.2rem; letter-spacing: 1px;">🏰 Maygal Books Vault</h1>
    <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary); font-size: 1rem; letter-spacing: 0.5px;">
        The Premium Archive for Knowledge
    </p>
</div>
""",
        unsafe_allow_html=True,
    )

    library = get_library()

    # Sidebar Navigation
    st.sidebar.markdown(
        """
<div style="margin-bottom: 1.5rem;">
    <h2 style="margin: 0; font-size: 1.6rem;">⚙️ Navigation</h2>
</div>
""",
        unsafe_allow_html=True,
    )

    menu = st.sidebar.radio(
        "Go to",
        [
            "📊 Dashboard",
            "📖 Add Book",
            "👤 Register Member",
            "📤 Issue Book",
            "📥 Return Book",
            "📚 View Books",
            "👥 View Members",
        ],
        label_visibility="collapsed",
    )

    # Page routing
    if menu == "📊 Dashboard":
        page_dashboard(library)
    elif menu == "📖 Add Book":
        page_add_book(library)
    elif menu == "👤 Register Member":
        page_register_member(library)
    elif menu == "📤 Issue Book":
        page_issue_book(library)
    elif menu == "📥 Return Book":
        page_return_book(library)
    elif menu == "📚 View Books":
        page_view_books(library)
    elif menu == "👥 View Members":
        page_view_members(library)

    # Footer Buttons
    st.markdown("<div class='vault-divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("💾 Save All Data", use_container_width=True):
            library.save_all()
            st.success("✅ All data saved to CSV!")

    with col2:
        if st.button("🔄 Refresh App", use_container_width=True):
            st.rerun()

    # ---------------- FINAL FOOTER ----------------
    # 👇 LOOK HERE: Absolutely NO indentation inside the quotes!
        # ---------------- FINAL FOOTER ----------------
    st.markdown(
        """
<div style="text-align: center; margin-top: 3rem; padding-bottom: 2rem;">
<p style="font-size: 1rem; margin-bottom: 15px; color: var(--text-secondary);">
Made with ❤️ by <span style="color: var(--gold); font-weight: 600;">Mayank</span>
</p>
<div style="display: flex; justify-content: center; gap: 25px;">
<a href="https://github.com/mayank-goyal09" target="_blank" style="text-decoration: none; transition: transform 0.2s;">
<div style="font-size: 1.8rem; filter: grayscale(100%); transition: filter 0.3s;">
🐙 <span style="font-size: 0.9rem; color: var(--text-secondary); display: block;">GitHub</span>
</div>
</a>
<a href="https://www.linkedin.com/in/mayank-goyal-4b8756363/" target="_blank" style="text-decoration: none; transition: transform 0.2s;">
<div style="font-size: 1.8rem; filter: grayscale(100%); transition: filter 0.3s;">
💼 <span style="font-size: 0.9rem; color: var(--text-secondary); display: block;">LinkedIn</span>
</div>
</a>
</div>
<p style="font-size: 0.75rem; margin-top: 20px; opacity: 0.4;">
Maygal Books Vault © 2025
</p>
</div>
""",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()


