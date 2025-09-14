import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

def load_feedback_data():
    """Load user feedback data for analytics"""
    feedback_file = 'user_feedback.csv'
    if os.path.exists(feedback_file):
        return pd.read_csv(feedback_file)
    else:
        return pd.DataFrame()

def analytics_dashboard():
    """Create analytics dashboard for Gift Guru"""
    st.set_page_config(
        page_title="📊 Gift Guru Analytics",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Gift Guru Analytics Dashboard")
    st.markdown("Track user engagement, satisfaction, and recommendation performance.")
    
    # Load data
    df = load_feedback_data()
    
    if df.empty:
        st.warning("📈 No user feedback data available yet. Start getting users to rate recommendations!")
        st.info("💡 **Pro Tip**: Share your Gift Guru app with friends and collect feedback to see analytics here.")
        return
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_users = len(df)
        st.metric("👥 Total Users", total_users)
    
    with col2:
        avg_rating = df['average_rating'].mean()
        st.metric("⭐ Avg Rating", f"{avg_rating:.2f}/5")
    
    with col3:
        satisfaction_rate = len(df[df['average_rating'] >= 4]) / len(df) * 100
        st.metric("🎯 Satisfaction Rate", f"{satisfaction_rate:.1f}%")
    
    with col4:
        recent_users = len(df[pd.to_datetime(df['timestamp']) > datetime.now() - timedelta(days=7)])
        st.metric("📅 Weekly Users", recent_users)
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Rating Distribution")
        rating_dist = df['average_rating'].value_counts().sort_index()
        fig_ratings = px.bar(
            x=rating_dist.index,
            y=rating_dist.values,
            labels={'x': 'Rating', 'y': 'Number of Users'},
            color=rating_dist.values,
            color_continuous_scale='viridis'
        )
        st.plotly_chart(fig_ratings, use_container_width=True)
    
    with col2:
        st.subheader("🎉 Popular Occasions")
        occasion_counts = df['occasion'].value_counts() if 'occasion' in df.columns else pd.Series()
        if not occasion_counts.empty:
            fig_occasions = px.pie(
                values=occasion_counts.values,
                names=occasion_counts.index,
                title="Gift Occasions"
            )
            st.plotly_chart(fig_occasions, use_container_width=True)
    
    # Age Demographics
    st.subheader("📅 Age Demographics")
    if 'age_range' in df.columns:
        age_dist = df['age_range'].value_counts()
        fig_age = px.histogram(
            df, 
            x='age_range',
            title="User Age Distribution",
            color_discrete_sequence=['#FF6B6B']
        )
        st.plotly_chart(fig_age, use_container_width=True)
    
    # Time Series
    st.subheader("📈 User Activity Over Time")
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    daily_users = df.groupby('date').size().reset_index(name='users')
    
    fig_timeline = px.line(
        daily_users,
        x='date',
        y='users',
        title="Daily User Activity",
        markers=True
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Detailed Feedback Table
    st.subheader("📝 Recent Feedback")
    if not df.empty:
        recent_feedback = df.sort_values('timestamp', ascending=False).head(10)
        st.dataframe(
            recent_feedback[['timestamp', 'age_range', 'interests', 'average_rating']],
            use_container_width=True
        )
    
    # Export Options
    st.subheader("💾 Export Data")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Download Analytics Report"):
            # Generate summary report
            report = f"""
            Gift Guru Analytics Report
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            Key Metrics:
            - Total Users: {total_users}
            - Average Rating: {avg_rating:.2f}/5
            - Satisfaction Rate: {satisfaction_rate:.1f}%
            - Weekly Active Users: {recent_users}
            
            Top Insights:
            - Most Popular Occasion: {occasion_counts.index[0] if not occasion_counts.empty else 'N/A'}
            - Highest Rating: {df['average_rating'].max():.1f}
            - Lowest Rating: {df['average_rating'].min():.1f}
            """
            
            st.download_button(
                label="Download Report",
                data=report,
                file_name=f"gift_guru_analytics_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    with col2:
        if st.button("📁 Download Raw Data"):
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"gift_guru_feedback_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    analytics_dashboard()
