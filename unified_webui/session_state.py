"""Unified session state management for MysterySeek platform."""

from typing import Optional, List, Dict, Any
import streamlit as st

from unified_webui.config import (
    UISettings,
    WerewolfSettings,
    TurtleSoupSettings,
    PlatformSettings,
    DEFAULT_LANGUAGE,
    DEFAULT_PLAYER_ID,
)
from unified_webui.i18n import I18n, set_language as i18n_set_language


def init_session_state() -> None:
    if "unified_initialized" not in st.session_state:
        st.session_state.unified_initialized = True
        st.session_state.language = DEFAULT_LANGUAGE
        st.session_state.i18n = I18n(DEFAULT_LANGUAGE)
        st.session_state.current_game = "home"
        st.session_state.ui_settings = UISettings()
        
        st.session_state.werewolf_session = None
        st.session_state.werewolf_settings = WerewolfSettings()
        st.session_state.werewolf_last_event_count = 0
        st.session_state.werewolf_pending_action = None
        st.session_state.werewolf_action_submitted = False
        st.session_state.werewolf_event_filters = {"all"}
        st.session_state.werewolf_show_winner_modal = False
        st.session_state.werewolf_winner_team = None
        st.session_state.werewolf_winner_shown_for_game = None
        st.session_state.werewolf_config_loaded = False
        
        st.session_state.turtle_player_id = DEFAULT_PLAYER_ID
        st.session_state.turtle_display_name = ""
        st.session_state.turtle_current_page = "home"
        st.session_state.turtle_current_session_id = ""
        st.session_state.turtle_current_puzzle_id = ""
        st.session_state.turtle_messages = []
        st.session_state.turtle_game_engine = None
        st.session_state.turtle_session_runner = None
        st.session_state.turtle_settings = TurtleSoupSettings()
        st.session_state.turtle_error_message = ""
        st.session_state.turtle_success_message = ""


def get_i18n() -> I18n:
    if "i18n" not in st.session_state:
        st.session_state.i18n = I18n(get_language())
    return st.session_state.i18n


def get_language() -> str:
    return st.session_state.get("language", DEFAULT_LANGUAGE)


def set_language(language: str) -> None:
    st.session_state.language = language
    st.session_state.i18n = I18n(language)
    i18n_set_language(language)


def get_current_game() -> str:
    return st.session_state.get("current_game", "home")


def set_current_game(game: str) -> None:
    st.session_state.current_game = game


def get_ui_settings() -> UISettings:
    if "ui_settings" not in st.session_state:
        st.session_state.ui_settings = UISettings()
    return st.session_state.ui_settings


def set_ui_settings(settings: UISettings) -> None:
    st.session_state.ui_settings = settings


def get_werewolf_session():
    return st.session_state.get("werewolf_session")


def set_werewolf_session(session) -> None:
    st.session_state.werewolf_session = session


def get_werewolf_settings() -> WerewolfSettings:
    if "werewolf_settings" not in st.session_state:
        st.session_state.werewolf_settings = WerewolfSettings()
    return st.session_state.werewolf_settings


def set_werewolf_settings(settings: WerewolfSettings) -> None:
    st.session_state.werewolf_settings = settings


def reset_werewolf_state() -> None:
    st.session_state.werewolf_session = None
    st.session_state.werewolf_last_event_count = 0
    st.session_state.werewolf_pending_action = None
    st.session_state.werewolf_action_submitted = False
    st.session_state.werewolf_show_winner_modal = False
    st.session_state.werewolf_winner_team = None
    st.session_state.werewolf_winner_shown_for_game = None


def get_turtle_player_id() -> str:
    return st.session_state.get("turtle_player_id", DEFAULT_PLAYER_ID)


def set_turtle_player_id(player_id: str) -> None:
    st.session_state.turtle_player_id = player_id


def get_turtle_display_name() -> str:
    return st.session_state.get("turtle_display_name", "")


def set_turtle_display_name(name: str) -> None:
    st.session_state.turtle_display_name = name


def get_turtle_current_page() -> str:
    return st.session_state.get("turtle_current_page", "home")


def set_turtle_current_page(page: str) -> None:
    st.session_state.turtle_current_page = page


def get_turtle_session_id() -> str:
    return st.session_state.get("turtle_current_session_id", "")


def set_turtle_session_id(session_id: str) -> None:
    st.session_state.turtle_current_session_id = session_id


def get_turtle_puzzle_id() -> str:
    return st.session_state.get("turtle_current_puzzle_id", "")


def set_turtle_puzzle_id(puzzle_id: str) -> None:
    st.session_state.turtle_current_puzzle_id = puzzle_id


def get_turtle_messages() -> List[Dict[str, Any]]:
    return st.session_state.get("turtle_messages", [])


def add_turtle_message(role: str, content: str, verdict: str = "", turn_index: int = 0, is_agent: bool = False) -> None:
    if "turtle_messages" not in st.session_state:
        st.session_state.turtle_messages = []
    
    message = {
        "role": role,
        "content": content,
        "verdict": verdict,
        "turn_index": turn_index,
        "is_agent": is_agent,
    }
    st.session_state.turtle_messages.append(message)


def clear_turtle_messages() -> None:
    st.session_state.turtle_messages = []


def get_turtle_game_engine():
    return st.session_state.get("turtle_game_engine")


def set_turtle_game_engine(engine) -> None:
    st.session_state.turtle_game_engine = engine


def get_turtle_session_runner():
    return st.session_state.get("turtle_session_runner")


def set_turtle_session_runner(runner) -> None:
    st.session_state.turtle_session_runner = runner


def get_turtle_settings() -> TurtleSoupSettings:
    if "turtle_settings" not in st.session_state:
        st.session_state.turtle_settings = TurtleSoupSettings()
    return st.session_state.turtle_settings


def set_turtle_settings(settings: TurtleSoupSettings) -> None:
    st.session_state.turtle_settings = settings


def get_turtle_error_message() -> str:
    return st.session_state.get("turtle_error_message", "")


def set_turtle_error_message(message: str) -> None:
    st.session_state.turtle_error_message = message


def clear_turtle_error_message() -> None:
    st.session_state.turtle_error_message = ""


def get_turtle_success_message() -> str:
    return st.session_state.get("turtle_success_message", "")


def set_turtle_success_message(message: str) -> None:
    st.session_state.turtle_success_message = message


def clear_turtle_success_message() -> None:
    st.session_state.turtle_success_message = ""


def reset_turtle_game_state() -> None:
    st.session_state.turtle_current_session_id = ""
    st.session_state.turtle_session_runner = None
    st.session_state.turtle_messages = []
    clear_turtle_error_message()
    clear_turtle_success_message()
