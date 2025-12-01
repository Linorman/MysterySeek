"""Home page for MysterySeek platform."""

import streamlit as st
from unified_webui.config import WEREWOLF_ICON, TURTLE_SOUP_ICON
from unified_webui.components import render_css, render_feature_box
from unified_webui import session_state as state


def render_home_page():
    render_css()
    
    i18n = state.get_i18n()
    
    # Hero Section
    st.markdown(
        f"""
        <div class="main-header">
            <h1>🔍 {i18n('platform_title')}</h1>
            <p style="font-size: 1.3em; color: #666; margin-top: 0.5rem;">{i18n('platform_subtitle')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Welcome Section
    col_welcome, col_spacer = st.columns([3, 1])
    with col_welcome:
        st.markdown(f"### {i18n('platform_welcome')}")
        st.markdown(i18n("platform_description"))
    
    st.markdown("---")
    
    # Game Selection Section
    st.markdown(f"## 🎮 {i18n('home_choose_game')}")
    
    col1, col_space, col2 = st.columns([5, 1, 5])
    
    with col1:
        st.markdown(
            f"""
            <div class="game-card werewolf">
                <h2>{WEREWOLF_ICON} {i18n('game_werewolf_title')}</h2>
                <h3>{i18n('game_werewolf_subtitle')}</h3>
                <p>{i18n('game_werewolf_description')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            f"{WEREWOLF_ICON} {i18n('home_play_now')}",
            key="play_werewolf_btn",
            use_container_width=True,
            type="primary",
        ):
            state.set_current_game("werewolf")
            st.rerun()
    
    with col2:
        st.markdown(
            f"""
            <div class="game-card turtle-soup">
                <h2>{TURTLE_SOUP_ICON} {i18n('game_turtle_soup_title')}</h2>
                <h3>{i18n('game_turtle_soup_subtitle')}</h3>
                <p>{i18n('game_turtle_soup_description')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            f"{TURTLE_SOUP_ICON} {i18n('home_play_now')}",
            key="play_turtle_soup_btn",
            use_container_width=True,
            type="primary",
        ):
            state.set_current_game("turtle_soup")
            st.rerun()
    
    st.markdown("---")
    
    # Features Section
    st.markdown(f"## ✨ {i18n('home_features')}")
    
    feat_cols = st.columns(4)
    
    with feat_cols[0]:
        render_feature_box("🤖", i18n("home_ai_agents"))
    
    with feat_cols[1]:
        render_feature_box("👥", i18n("home_multiplayer"))
    
    with feat_cols[2]:
        render_feature_box("🧩", i18n("home_puzzles"))
    
    with feat_cols[3]:
        render_feature_box("🌍", i18n("home_languages"))
