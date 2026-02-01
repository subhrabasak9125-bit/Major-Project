import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import time

# Page configuration
st.set_page_config(
    page_title="Face Recognition Attendance System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for futuristic design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&display=swap');
    
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(90deg, #00d4ff, #7b2ff7, #f107a3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 30, 60, 0.9), rgba(20, 20, 40, 0.9));
        border: 2px solid rgba(123, 47, 247, 0.3);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(123, 47, 247, 0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(123, 47, 247, 0.8);
        box-shadow: 0 12px 40px 0 rgba(123, 47, 247, 0.4);
    }
    
    .stMetric {
        background: linear-gradient(135deg, rgba(30, 30, 60, 0.8), rgba(20, 20, 40, 0.8));
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(123, 47, 247, 0.3);
    }
    
    .stMetric label {
        color: #00d4ff !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 32px !important;
        font-weight: 900 !important;
        font-family: 'Orbitron', sans-serif;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    div[data-testid="stSidebarNav"] {
        background: rgba(30, 30, 60, 0.5);
        border-radius: 10px;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #7b2ff7, #f107a3);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 30px;
        font-weight: 700;
        font-family: 'Orbitron', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(123, 47, 247, 0.8);
    }
    
    .highlight-box {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(123, 47, 247, 0.1));
        border-left: 4px solid #7b2ff7;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'attendance_data' not in st.session_state:
    st.session_state.attendance_data = {
        'total_students': 250,
        'present_today': 187,
        'absent_today': 63,
        'photos_collected': 12500,
        'model_accuracy': 98.5,
        'last_trained_date': '2025-11-25'
    }

# Sample data generation
def generate_weekly_data():
    return pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
        'Present': [235, 228, 242, 238, 220, 187],
        'Absent': [15, 22, 8, 12, 30, 63],
        'Rate': [94, 91, 97, 95, 88, 75]
    })

def generate_hourly_data():
    return pd.DataFrame({
        'Time': ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00'],
        'Count': [45, 82, 128, 165, 187, 187, 187]
    })

def generate_department_data():
    return pd.DataFrame({
        'Department': ['Computer Science', 'Electronics', 'Mechanical', 'Civil', 'Others'],
        'Students': [85, 62, 48, 35, 20],
        'Color': ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981']
    })

def generate_training_history():
    return pd.DataFrame({
        'Epoch': [1, 5, 10, 15, 20],
        'Accuracy': [75.2, 88.5, 94.2, 97.1, 98.5],
        'Loss': [0.85, 0.45, 0.28, 0.15, 0.08]
    })

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Navigation")
    page = st.radio(
        "Select Page",
        ["📊 Overview", "📈 Analytics", "🧠 Model Training"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    auto_refresh = st.checkbox("Auto Refresh", value=True)
    refresh_interval = st.slider("Refresh Interval (seconds)", 5, 60, 10)
    
    st.markdown("---")
    st.markdown("### 📅 Date Range")
    date_range = st.date_input(
        "Select Date Range",
        value=(datetime.now() - timedelta(days=7), datetime.now()),
        max_value=datetime.now()
    )
    
    st.markdown("---")
    st.markdown("### 🔔 Quick Actions")
    if st.button("🔄 Refresh Data"):
        st.rerun()
    if st.button("📸 Capture Photos"):
        st.success("Photo capture initiated!")
    if st.button("🧠 Train Model"):
        st.success("Model training started!")

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# 🎯 Face Recognition Attendance System")
    st.markdown("### AI-Powered Real-Time Monitoring Dashboard")
with col2:
    current_time = datetime.now()
    st.markdown(f"### ⏰ {current_time.strftime('%H:%M:%S')}")
    st.markdown(f"📅 {current_time.strftime('%B %d, %Y')}")

st.markdown("---")

# Main Content based on selected page
if page == "📊 Overview":
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Total Students",
            value=st.session_state.attendance_data['total_students'],
            delta="Enrolled"
        )
    
    with col2:
        present = st.session_state.attendance_data['present_today']
        total = st.session_state.attendance_data['total_students']
        attendance_rate = (present / total) * 100
        st.metric(
            label="✅ Present Today",
            value=present,
            delta=f"{attendance_rate:.1f}% attendance"
        )
    
    with col3:
        st.metric(
            label="📸 Photos Collected",
            value=f"{st.session_state.attendance_data['photos_collected']:,}",
            delta="+12.3%"
        )
    
    with col4:
        st.metric(
            label="🧠 Model Accuracy",
            value=f"{st.session_state.attendance_data['model_accuracy']}%",
            delta="Optimal"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Today's Attendance Flow")
        hourly_data = generate_hourly_data()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hourly_data['Time'],
            y=hourly_data['Count'],
            mode='lines+markers',
            name='Students',
            line=dict(color='#3b82f6', width=3),
            fill='tonexty',
            fillcolor='rgba(59, 130, 246, 0.3)',
            marker=dict(size=10, color='#3b82f6')
        ))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(30,30,60,0.5)',
            font=dict(color='white'),
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Weekly Attendance")
        weekly_data = generate_weekly_data()
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=weekly_data['Day'],
            y=weekly_data['Present'],
            name='Present',
            marker_color='#10b981',
            text=weekly_data['Present'],
            textposition='auto'
        ))
        fig.add_trace(go.Bar(
            x=weekly_data['Day'],
            y=weekly_data['Absent'],
            name='Absent',
            marker_color='#ef4444',
            text=weekly_data['Absent'],
            textposition='auto'
        ))
        fig.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(30,30,60,0.5)',
            font=dict(color='white'),
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎓 Department Distribution")
        dept_data = generate_department_data()
        fig = go.Figure(data=[go.Pie(
            labels=dept_data['Department'],
            values=dept_data['Students'],
            marker=dict(colors=dept_data['Color']),
            hole=0.4,
            textposition='auto',
            textinfo='label+percent'
        )])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(30,30,60,0.5)',
            font=dict(color='white', size=12),
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.1)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📉 Attendance Rate Trend")
        weekly_data = generate_weekly_data()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=weekly_data['Day'],
            y=weekly_data['Rate'],
            mode='lines+markers',
            name='Attendance Rate',
            line=dict(color='#f59e0b', width=3),
            marker=dict(size=12, color='#f59e0b')
        ))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(30,30,60,0.5)',
            font=dict(color='white'),
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', range=[0, 100])
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "📈 Analytics":
    st.markdown("## 📊 Advanced Analytics")
    
    # Analytics Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### ⏰ Avg Check-in Time")
        st.markdown("<h1 style='text-align: center; color: #3b82f6;'>9:24 AM</h1>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ✅ On-Time Rate")
        st.markdown("<h1 style='text-align: center; color: #10b981;'>92.3%</h1>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("### ⚠️ Late Arrivals")
        st.markdown("<h1 style='text-align: center; color: #ef4444;'>14</h1>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Detailed Chart
    st.markdown("### 📈 Weekly Attendance Comparison")
    weekly_data = generate_weekly_data()
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=weekly_data['Day'],
        y=weekly_data['Present'],
        name='Present',
        mode='lines+markers',
        line=dict(color='#10b981', width=3),
        fill='tonexty',
        fillcolor='rgba(16, 185, 129, 0.3)',
        marker=dict(size=10)
    ))
    
    fig.add_trace(go.Scatter(
        x=weekly_data['Day'],
        y=weekly_data['Absent'],
        name='Absent',
        mode='lines+markers',
        line=dict(color='#ef4444', width=3),
        fill='tonexty',
        fillcolor='rgba(239, 68, 68, 0.3)',
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(30,30,60,0.5)',
        font=dict(color='white'),
        height=500,
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Additional Stats
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Monthly Statistics")
        monthly_stats = pd.DataFrame({
            'Metric': ['Total Classes', 'Avg Attendance', 'Peak Day', 'Lowest Day'],
            'Value': ['120', '89.2%', 'Wednesday', 'Saturday']
        })
        st.dataframe(monthly_stats, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### 🏆 Top Performers")
        top_performers = pd.DataFrame({
            'Department': ['Computer Science', 'Electronics', 'Mechanical', 'Civil'],
            'Attendance': ['94.5%', '92.1%', '88.7%', '85.3%']
        })
        st.dataframe(top_performers, use_container_width=True, hide_index=True)

elif page == "🧠 Model Training":
    st.markdown("## 🤖 Model Training & Performance")
    
    # Training Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔄 Training Epochs", "20", "+5")
    with col2:
        st.metric("📷 Images/Student", "50", "+10")
    with col3:
        st.metric("⚡ Recognition Speed", "0.3s", "-0.1s")
    with col4:
        st.metric("✅ Success Rate", "98.5%", "+2.3%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Training History Chart
    st.markdown("### 📈 Training Progress")
    training_data = generate_training_history()
    
    fig = go.Figure()
    
    # Accuracy line
    fig.add_trace(go.Scatter(
        x=training_data['Epoch'],
        y=training_data['Accuracy'],
        name='Accuracy (%)',
        mode='lines+markers',
        line=dict(color='#10b981', width=3),
        marker=dict(size=10),
        yaxis='y'
    ))
    
    # Loss line
    fig.add_trace(go.Scatter(
        x=training_data['Epoch'],
        y=training_data['Loss'],
        name='Loss',
        mode='lines+markers',
        line=dict(color='#ef4444', width=3),
        marker=dict(size=10),
        yaxis='y2'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(30,30,60,0.5)',
        font=dict(color='white'),
        height=500,
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(
            title='Training Epochs',
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis=dict(
            title='Accuracy (%)',
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            side='left'
        ),
        yaxis2=dict(
            title='Loss',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Model Details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔧 Model Configuration")
        config_data = pd.DataFrame({
            'Parameter': ['Architecture', 'Framework', 'Optimizer', 'Learning Rate', 'Batch Size', 'Input Size'],
            'Value': ['ResNet50', 'TensorFlow', 'Adam', '0.001', '32', '224x224']
        })
        st.dataframe(config_data, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### 📊 Performance Metrics")
        perf_data = pd.DataFrame({
            'Metric': ['Precision', 'Recall', 'F1-Score', 'False Positive Rate', 'False Negative Rate', 'Inference Time'],
            'Score': ['98.2%', '98.8%', '98.5%', '1.3%', '1.5%', '0.3s']
        })
        st.dataframe(perf_data, use_container_width=True, hide_index=True)
    
    # Training Controls
    st.markdown("### 🎮 Training Controls")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Start Training", use_container_width=True):
            with st.spinner("Training in progress..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)
                st.success("✅ Training completed successfully!")
    
    with col2:
        if st.button("💾 Save Model", use_container_width=True):
            st.success("✅ Model saved successfully!")
    
    with col3:
        if st.button("🔄 Reset Training", use_container_width=True):
            st.warning("⚠️ Training data has been reset!")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #7b2ff7; font-family: Orbitron;'>"
    "🎯 Face Recognition Attendance System v2.0 | Powered by AI & Machine Learning"
    "</div>",
    unsafe_allow_html=True
)

# Auto-refresh functionality
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()