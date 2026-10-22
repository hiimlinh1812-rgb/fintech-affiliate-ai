"""
Interactive Plotly Charts Module
Implements Bar, Pie, Line, and Combo charts as specified in report CNDVTC.docx (Section 9, 3.1.4).
Clean modern Fintech styling with Vietnamese number/currency formatting.
"""

from typing import Optional
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


FINTECH_COLORS = {
    "Shopee": "#EE4D2D",
    "Lazada": "#000080",
    "TikTok Shop": "#000000",
    "Primary": "#1E3A8A",
    "Accent": "#10B981",
    "Warning": "#F59E0B",
    "Danger": "#EF4444",
    "Palette": ["#3B82F6", "#10B981", "#8B5CF6", "#F59E0B", "#EC4899", "#06B6D4"]
}


def format_currency_vnd(val: float) -> str:
    """Formats numeric value to VND currency string."""
    return f"{int(val):,} ₫"


def create_platform_bar_chart(platform_df: pd.DataFrame, metric: str = "revenue", title: Optional[str] = None) -> go.Figure:
    """
    Bar Chart: Doanh thu hoặc Hoa hồng theo từng sàn thương mại điện tử.
    """
    if platform_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Không có dữ liệu", showarrow=False, font=dict(size=14))
        return fig

    metric_label = {
        "revenue": "Tổng Doanh Thu (GMV)",
        "commission": "Tổng Hoa Hồng",
        "profit": "Lợi Nhuận Ròng",
        "ad_cost": "Chi Phí Quảng Cáo"
    }.get(metric, "Giá trị")

    color_seq = [FINTECH_COLORS.get(p, FINTECH_COLORS["Primary"]) for p in platform_df["platform"]]

    fig = go.Figure(
        data=[
            go.Bar(
                x=platform_df["platform"],
                y=platform_df[metric],
                text=[format_currency_vnd(v) for v in platform_df[metric]],
                textposition="auto",
                marker=dict(color=color_seq, line=dict(color="#FFFFFF", width=1.5)),
                hovertemplate="<b>%{x}</b><br>" + f"{metric_label}: " + "%{y:,.0f} ₫<extra></extra>"
            )
        ]
    )

    fig.update_layout(
        title=title or f"So sánh {metric_label} theo Nền Tảng",
        xaxis_title="Nền tảng",
        yaxis_title="Số tiền (VND)",
        template="plotly_white",
        height=380,
        margin=dict(l=40, r=30, t=50, b=40)
    )
    return fig


def create_top_products_bar_chart(products_df: pd.DataFrame, metric: str = "revenue", top_n: int = 8) -> go.Figure:
    """
    Bar Chart: Top sản phẩm theo Doanh thu / Hoa hồng / ROI.
    """
    if products_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Không có dữ liệu", showarrow=False)
        return fig

    df_plot = products_df.head(top_n).sort_values(by=metric, ascending=True)

    metric_name = "Doanh Thu" if metric == "revenue" else ("Hoa Hồng" if metric == "commission" else "ROI")
    text_values = [f"{v:.2f}x" if metric == "roi" else format_currency_vnd(v) for v in df_plot[metric]]

    fig = go.Figure(
        go.Bar(
            x=df_plot[metric],
            y=df_plot["product_name"].apply(lambda n: n[:28] + "..." if len(n) > 28 else n),
            orientation="h",
            text=text_values,
            textposition="auto",
            marker=dict(color="#2563EB", line=dict(color="#1D4ED8", width=1)),
            hovertemplate="<b>%{y}</b><br>" + f"{metric_name}: " + "%{x}<extra></extra>"
        )
    )

    fig.update_layout(
        title=f"Top {top_n} Sản Phẩm Có {metric_name} Cao Nhất",
        xaxis_title=metric_name,
        yaxis_title="",
        template="plotly_white",
        height=400,
        margin=dict(l=40, r=40, t=50, b=40)
    )
    return fig


def create_platform_pie_chart(platform_df: pd.DataFrame, metric: str = "revenue", title: Optional[str] = None) -> go.Figure:
    """
    Pie Chart: Phân bổ tỷ trọng Doanh thu hoặc Hoa hồng giữa các sàn (Shopee, Lazada, TikTok Shop).
    """
    if platform_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Không có dữ liệu", showarrow=False)
        return fig

    metric_label = "Doanh thu" if metric == "revenue" else "Hoa hồng"
    colors = [FINTECH_COLORS.get(p, FINTECH_COLORS["Palette"][i % len(FINTECH_COLORS["Palette"])]) 
              for i, p in enumerate(platform_df["platform"])]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=platform_df["platform"],
                values=platform_df[metric],
                hole=0.45,  # Donut style for modern fintech UI
                marker=dict(colors=colors),
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>" + f"{metric_label}: " + "%{value:,.0f} ₫ (%{percent})<extra></extra>"
            )
        ]
    )

    fig.update_layout(
        title=title or f"Phân Bổ Tỷ Trọng {metric_label} Theo Sàn",
        template="plotly_white",
        height=380,
        margin=dict(l=30, r=30, t=50, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
    )
    return fig


def create_revenue_trend_line_chart(month_df: pd.DataFrame) -> go.Figure:
    """
    Line Chart: Xu hướng Doanh thu và Hoa hồng theo thời gian (Hình 1 & 5 trong CNDVTC.docx).
    """
    if month_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Không có dữ liệu", showarrow=False)
        return fig

    fig = go.Figure()

    # Revenue Line
    fig.add_trace(
        go.Scatter(
            x=month_df["month"],
            y=month_df["revenue"],
            mode="lines+markers",
            name="Doanh thu (GMV)",
            line=dict(color="#2563EB", width=3),
            marker=dict(size=8, symbol="circle"),
            hovertemplate="<b>Tháng %{x}</b><br>Doanh thu: %{y:,.0f} ₫<extra></extra>"
        )
    )

    # Commission Line
    if "commission" in month_df.columns:
        fig.add_trace(
            go.Scatter(
                x=month_df["month"],
                y=month_df["commission"],
                mode="lines+markers",
                name="Hoa hồng",
                line=dict(color="#10B981", width=2.5, dash="dot"),
                marker=dict(size=7, symbol="diamond"),
                hovertemplate="<b>Tháng %{x}</b><br>Hoa hồng: %{y:,.0f} ₫<extra></extra>"
            )
        )

    # Ad cost
    if "ad_cost" in month_df.columns:
        fig.add_trace(
            go.Scatter(
                x=month_df["month"],
                y=month_df["ad_cost"],
                mode="lines+markers",
                name="Chi phí Ads",
                line=dict(color="#EF4444", width=2, dash="dash"),
                marker=dict(size=6, symbol="x"),
                hovertemplate="<b>Tháng %{x}</b><br>Chi phí Ads: %{y:,.0f} ₫<extra></extra>"
            )
        )

    fig.update_layout(
        title="Xu Hướng Doanh Số và Hoa Hồng Theo Thời Gian",
        xaxis_title="Tháng",
        yaxis_title="Số tiền (VND)",
        template="plotly_white",
        height=380,
        hovermode="x unified",
        margin=dict(l=40, r=30, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
    )
    return fig


def create_combo_revenue_profit_chart(month_df: pd.DataFrame) -> go.Figure:
    """
    Combo Bar & Line Chart: Doanh thu (Bar) và Lợi nhuận gộp/ROI (Line) theo thời gian.
    Matches Hình 5 trong CNDVTC.docx.
    """
    if month_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Không có dữ liệu", showarrow=False)
        return fig

    fig = go.Figure()

    # Bar: Doanh thu
    fig.add_trace(
        go.Bar(
            x=month_df["month"],
            y=month_df["revenue"],
            name="Doanh thu (GMV)",
            marker_color="#93C5FD",
            hovertemplate="Doanh thu: %{y:,.0f} ₫<extra></extra>"
        )
    )

    # Bar: Lợi nhuận
    fig.add_trace(
        go.Bar(
            x=month_df["month"],
            y=month_df["profit"],
            name="Lợi nhuận ròng",
            marker_color="#10B981",
            hovertemplate="Lợi nhuận: %{y:,.0f} ₫<extra></extra>"
        )
    )

    # Line: ROI on secondary axis
    if "roi" in month_df.columns:
        fig.add_trace(
            go.Scatter(
                x=month_df["month"],
                y=month_df["roi"],
                name="ROI",
                yaxis="y2",
                mode="lines+markers",
                line=dict(color="#F59E0B", width=3),
                marker=dict(size=8),
                hovertemplate="ROI: %{y:.2f}x<extra></extra>"
            )
        )

    fig.update_layout(
        title="Doanh Số và Lợi Nhuận Theo Thời Gian (Line & Bar)",
        xaxis_title="Tháng",
        yaxis=dict(title="Số tiền (VND)"),
        yaxis2=dict(
            title="ROI (Hệ số)",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        barmode="group",
        template="plotly_white",
        height=400,
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
    )
    return fig
