import streamlit as st
import webbrowser

def show_home():
    """Display the home page content"""
    st.title("Welcome to RMC Data")
    st.write("""
    This is the home page of RMC Data application.
    Navigate through different sections using the menu above.
    """)
    
    st.image("https://placehold.co/800x400?text=RMC+Data+Dashboard",
             caption="Data Analysis Dashboard")
    
    st.markdown("""
    ## Key Features:
    - Real-time data processing
    - Economic indicators
    - Financial analysis tools
    - Security metrics
    """)

def show_about():
    """Display the about page content"""
    st.title("About RMC Data")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image("https://placehold.co/300x300?text=RMC+Team",
                 width=250)
    
    with col2:
        st.write("""
        ### Our Mission
        We provide comprehensive data analysis solutions for financial and economic metrics.
        
        ## Team Members
        - Breno Holiveira (Founder)
        - Data Science Team
        - Financial Analysts
        """)
    
    st.markdown("---")
    st.write("""
    ### Contact Information
    Email: contact@rmcdata.com
    Phone: +55 11 98765-4321
    """)

def show_economy():
    """Display economy page content"""
    st.title("Economic Indicators")
    
    st.write("""
    ### Key Economic Metrics
    Explore various economic indicators and trends.
    """)
    
    tab1, tab2, tab3 = st.tabs(["GDP", "Unemployment", "CPI"])
    
    with tab1:
        st.subheader("Gross Domestic Product")
        st.line_chart([0.5, 0.7, 0.6, 0.9, 1.2, 1.0, 1.4])
    
    with tab2:
        st.subheader("Unemployment Rate")
        st.bar_chart([8.5, 7.8, 7.2, 6.9, 6.5, 6.2])
    
    with tab3:
        st.subheader("Consumer Price Index")
        st.line_chart([100, 102, 104, 106, 108, 110])

def show_finance():
    """Display finance page content"""
    st.title("Financial Analysis")
    
    st.write("""
    ### Market Trends and Financial Data
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Stock Market")
        st.line_chart([15300, 15450, 15600, 15500, 15700, 15900])
    
    with col2:
        st.subheader("Currency Exchange")
        st.line_chart([4.85, 4.82, 4.79, 4.81, 4.83, 4.80])

def show_security():
    """Display security page content"""
    st.title("Security Metrics")
    
    st.write("""
    ### System Security and Performance
    """)
    
    with st.expander("Security Alerts"):
        st.warning("2 active security alerts")
        st.info("System performance is optimal")
        
    st.metric("Incidents this month", "4", delta="-2", delta_color="inverse")
    
    st.progress(85, text="System Security Score")

def redirect_to_github():
    """Redirect to GitHub repository"""
    st.write("Redirecting to GitHub...")
    webbrowser.open_new_tab("https://github.com/breno-holiveira/rmc")
