def set_dark_theme(widget):
    # Apply dark theme styles
    neon_blue = "#00f3ff"
    dark_bg = "#1a1a2e"
    darker_bg = "#16213e"
    
    style = f"""
        QWidget {{
            background-color: {dark_bg};
            color: {neon_blue};
            font-family: 'Roboto';
            font-size: 12pt;
        }}
        QGroupBox {{
            border: 2px solid {neon_blue};
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }}
        QPushButton {{
            background-color: {darker_bg};
            border: 2px solid {neon_blue};
            border-radius: 5px;
            padding: 8px;
            min-width: 100px;
        }}
        QPushButton:hover {{
            background-color: #0f3460;
            border-color: #e94560;
        }}
        QTextEdit, QLineEdit {{
            background-color: {darker_bg};
            border: 1px solid {neon_blue};
            border-radius: 3px;
            padding: 5px;
        }}
        QComboBox {{
            background-color: {darker_bg};
            border: 1px solid {neon_blue};
            padding: 5px;
        }}
        QProgressBar {{
            border: 2px solid {neon_blue};
            border-radius: 5px;
            text-align: center;
            background: {darker_bg};
        }}
        QProgressBar::chunk {{
            background-color: {neon_blue};
        }}
    """
    widget.setStyleSheet(style)
