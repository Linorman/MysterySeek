"""Reusable UI components for unified MysterySeek platform."""

from typing import Optional, List
import streamlit as st

from unified_webui.config import EMOJI_MAP, CSS_STYLES, HIDE_STREAMLIT_STYLE
from unified_webui.i18n import I18n


def render_css() -> None:
    """Render global CSS styles and hide default Streamlit navigation."""
    st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)
    st.markdown(CSS_STYLES, unsafe_allow_html=True)


def render_platform_header(i18n: I18n) -> None:
    st.markdown(
        f"""
        <div class="main-header">
            <h1>{EMOJI_MAP['puzzle']} {i18n('platform_title')}</h1>
            <p>{i18n('platform_subtitle')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_error(message: str) -> None:
    if message:
        st.error(f"{EMOJI_MAP['error']} {message}")


def render_success(message: str) -> None:
    if message:
        st.success(f"{EMOJI_MAP['success']} {message}")


def render_info(message: str) -> None:
    if message:
        st.info(f"{EMOJI_MAP['info']} {message}")


def render_warning(message: str) -> None:
    if message:
        st.warning(f"{EMOJI_MAP['warning']} {message}")


def render_game_card(
    game_id: str,
    icon: str,
    title: str,
    subtitle: str,
    description: str,
    css_class: str = "",
) -> None:
    st.markdown(
        f"""
        <div class="game-card {css_class}">
            <h2>{icon} {title}</h2>
            <h3>{subtitle}</h3>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_box(icon: str, title: str) -> None:
    """Render a feature highlight box with icon and title."""
    st.markdown(
        f"""
        <div class="feature-box">
            <span class="icon">{icon}</span>
            <span class="title">{title}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_puzzle_card(
    puzzle_id: str,
    title: str,
    description: str = "",
    difficulty: Optional[str] = None,
    tags: Optional[List[str]] = None,
    language: str = "en",
) -> None:
    tags = tags or []
    
    with st.container():
        st.markdown(
            f"""
            <div class="puzzle-card">
                <h3>{EMOJI_MAP['puzzle']} {title}</h3>
                <p>{description if description else puzzle_id}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        cols = st.columns(3)
        if difficulty:
            cols[0].markdown(f"**Difficulty:** {difficulty}")
        cols[1].markdown(f"**Language:** {language.upper()}")
        if tags:
            cols[2].markdown(f"**Tags:** {', '.join(tags)}")


def render_game_stats(
    turn_count: int,
    hints_used: int,
    hints_total: int,
    state: str,
    i18n: I18n,
) -> None:
    cols = st.columns(4)
    
    with cols[0]:
        st.metric(i18n("turtle_turn"), turn_count)
    
    with cols[1]:
        st.metric(i18n("turtle_hints_used"), f"{hints_used}/{hints_total}")
    
    with cols[2]:
        state_key = f"turtle_state_{state.lower().replace(' ', '_')}"
        state_display = i18n(state_key)
        st.metric(i18n("turtle_game_state"), state_display)
    
    with cols[3]:
        hints_remaining = hints_total - hints_used
        st.metric(i18n("turtle_hints_remaining"), hints_remaining)


def render_status_badge(state: str, i18n: I18n) -> str:
    state_lower = state.lower().replace(" ", "_")
    state_key = f"turtle_state_{state_lower}"
    state_display = i18n(state_key)
    
    css_class = f"status-{state_lower.replace('_', '-')}"
    
    return f'<span class="status-badge {css_class}">{state_display}</span>'


def render_chat_message(
    role: str,
    content: str,
    verdict: Optional[str] = None,
    i18n: Optional[I18n] = None,
) -> None:
    if role.lower() in ["player", "user", "you"]:
        avatar = EMOJI_MAP["player"]
        name = i18n("turtle_you") if i18n else "You"
    else:
        avatar = EMOJI_MAP["dm"]
        name = i18n("turtle_dm") if i18n else "DM"
    
    msg_role = "user" if role.lower() in ["player", "user", "you"] else "assistant"
    
    with st.chat_message(msg_role, avatar=avatar):
        if verdict:
            verdict_emoji = EMOJI_MAP.get(verdict.lower(), "")
            st.markdown(f"**{name}:** {content} {verdict_emoji}")
        else:
            st.markdown(f"**{name}:** {content}")


def render_verdict_badge(verdict: str) -> str:
    verdict_lower = verdict.lower()
    emoji = EMOJI_MAP.get(verdict_lower, "")
    css_class = f"verdict-{verdict_lower.replace('_', '-')}"
    
    return f'<span class="verdict-badge {css_class}">{emoji} {verdict.upper()}</span>'


def render_commands_panel(i18n: I18n) -> None:
    with st.expander(f"{EMOJI_MAP['info']} {i18n('turtle_commands_title')}", expanded=False):
        st.markdown(
            f"""
            <div class="command-list">
                <p><code>/hint</code> - {i18n('turtle_commands_hint').split(' - ')[1] if ' - ' in i18n('turtle_commands_hint') else 'Get a hint'}</p>
                <p><code>/status</code> - {i18n('turtle_commands_status').split(' - ')[1] if ' - ' in i18n('turtle_commands_status') else 'View game status'}</p>
                <p><code>/history</code> - {i18n('turtle_commands_history').split(' - ')[1] if ' - ' in i18n('turtle_commands_history') else 'View recent Q&A'}</p>
                <p><code>/quit</code> - {i18n('turtle_commands_quit').split(' - ')[1] if ' - ' in i18n('turtle_commands_quit') else 'End the game'}</p>
                <p><code>/help</code> - {i18n('turtle_commands_help').split(' - ')[1] if ' - ' in i18n('turtle_commands_help') else 'Show help'}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_how_to_play(i18n: I18n) -> None:
    with st.expander(f"{EMOJI_MAP['question']} {i18n('turtle_how_to_play')}", expanded=False):
        st.markdown(i18n("turtle_instructions"))


def render_empty_state(message: str, icon: str = "info") -> None:
    emoji = EMOJI_MAP.get(icon, EMOJI_MAP["info"])
    st.markdown(
        f"""
        <div style="text-align: center; padding: 2rem; color: #666;">
            <div style="font-size: 3rem;">{emoji}</div>
            <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
