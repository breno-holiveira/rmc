import streamlit as st

def academic_navigation_bar():
    st.markdown("""
    <style>
    /* Reset Streamlit defaults */
    #MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Main container padding adjustment */
    .block-container {
        padding-top: 70px !important;
    }
    
    /* Navigation bar */
    .academic-navbar {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 70px;
        background-color: #fff;
        border-bottom: 1px solid #e0e0e0;
        z-index: 1000;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 2rem;
        font-family: 'Georgia', 'Times New Roman', serif;
    }
    
    /* Logo section */
    .nav-logo {
        display: flex;
        align-items: baseline;
        cursor: default;
    }
    .nav-logo-main {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2c3e50;
    }
    .nav-logo-sub {
        font-size: 1.1rem;
        font-weight: 400;
        color: #7f8c8d;
        margin-left: 0.3rem;
    }
    
    /* Navigation links container */
    .nav-links {
        display: flex;
        height: 100%;
    }
    
    /* Navigation items */
    .nav-item {
        position: relative;
        height: 100%;
        display: flex;
        align-items: center;
    }
    
    /* Links styling */
    .nav-link {
        color: #34495e;
        font-size: 0.95rem;
        padding: 0 1.2rem;
        height: 100%;
        display: flex;
        align-items: center;
        text-decoration: none;
        transition: color 0.2s;
    }
    .nav-link:hover {
        color: #2980b9;
    }
    
    /* Dropdown arrow */
    .dropdown-arrow {
        margin-left: 0.4rem;
        transition: transform 0.2s;
    }
    
    /* Dropdown menu */
    .dropdown-menu {
        position: absolute;
        top: 100%;
        left: 0;
        background: #fff;
        min-width: 200px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        border-top: none;
        opacity: 0;
        visibility: hidden;
        transition: all 0.2s;
        z-index: 1001;
    }
    
    /* Dropdown items */
    .dropdown-item {
        padding: 0.7rem 1.2rem;
        color: #34495e;
        text-decoration: none;
        display: block;
        font-size: 0.9rem;
        transition: all 0.2s;
    }
    .dropdown-item:hover {
        background: #f8f9fa;
        color: #2980b9;
    }
    
    /* Hover states */
    .nav-item:hover .nav-link {
        color: #2980b9;
    }
    .nav-item:hover .dropdown-arrow {
        transform: rotate(180deg);
    }
    .nav-item:hover .dropdown-menu {
        opacity: 1;
        visibility: visible;
    }
    
    /* Vertical divider */
    .nav-divider {
        width: 1px;
        height: 30px;
        background: #e0e0e0;
        margin: 0 0.5rem;
    }
    </style>
    
    <!-- Navigation Bar HTML -->
    <nav class="academic-navbar">
        <div class="nav-logo">
            <span class="nav-logo-main">RMC</span>
            <span class="nav-logo-sub">Data</span>
        </div>
        
        <div class="nav-links">
            <div class="nav-item">
                <a href="#" class="nav-link">Home</a>
            </div>
            
            <div class="nav-divider"></div>
            
            <div class="nav-item">
                <a href="#" class="nav-link">
                    Economy 
                    <svg class="dropdown-arrow" width="10" height="6" viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M1 1L5 5L9 1" stroke="#34495e" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                </a>
                <div class="dropdown-menu">
                    <a href="#" class="dropdown-item">GDP Analysis</a>
                    <a href="#" class="dropdown-item">Regional Economies</a>
                    <a href="#" class="dropdown-item">Sectorial Data</a>
                </div>
            </div>
            
            <div class="nav-item">
                <a href="#" class="nav-link">
                    Finance 
                    <svg class="dropdown-arrow" width="10" height="6" viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M1 1L5 5L9 1" stroke="#34495e" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                </a>
                <div class="dropdown-menu">
                    <a href="#" class="dropdown-item">Public Budget</a>
                    <a href="#" class="dropdown-item">Tax Revenue</a>
                    <a href="#" class="dropdown-item">Fiscal Reports</a>
                </div>
            </div>
            
            <div class="nav-item">
                <a href="#" class="nav-link">
                    Security 
                    <svg class="dropdown-arrow" width="10" height="6" viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M1 1L5 5L9 1" stroke="#34495e" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                </a>
                <div class="dropdown-menu">
                    <a href="#" class="dropdown-item">Crime Statistics</a>
                    <a href="#" class="dropdown-item">Public Safety</a>
                    <a href="#" class="dropdown-item">Surveillance</a>
                </div>
            </div>
            
            <div class="nav-divider"></div>
            
            <div class="nav-item">
                <a href="#" class="nav-link">Contact</a>
            </div>
        </div>
    </nav>
    """, unsafe_allow_html=True)

# Initialize the app
def main():
    st.set_page_config(
        page_title="Academic Data Portal",
        page_icon="📊",
        layout="wide"
    )
    
    academic_navigation_bar()
    
    # Main content
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    st.title("Academic Data Portal")
    st.write("Welcome to the regional metropolitan data analysis platform.")
    
if __name__ == "__main__":
    main()
