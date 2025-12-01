"""Main Streamlit application entry point for unified MysterySeek platform."""

import sys
from pathlib import Path

root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))
sys.path.insert(0, str(root_path / "AutoWerewolf"))
sys.path.insert(0, str(root_path / "Echoes-of-Deceit-v2" / "src"))

import streamlit as st

from unified_webui.config import PAGE_CONFIG, APP_NAME, APP_ICON
from unified_webui.i18n import set_language, get_available_languages
from unified_webui.components import render_css
from unified_webui import session_state as state
from unified_webui.pages.home import render_home_page
from unified_webui.pages.werewolf import render_werewolf_page
from unified_webui.pages.turtle_soup import render_turtle_soup_page


def render_global_sidebar():
    """Render the global sidebar with language selection."""
    with st.sidebar:
        # App title with styling
        st.markdown(
            f"""
            <div style="text-align: center; padding: 1rem 0; margin-bottom: 1rem;">
                <h1 style="font-size: 1.8rem; margin: 0; color: #ffffff;">
                    {APP_ICON} {APP_NAME}
                </h1>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        i18n = state.get_i18n()
        
        # Language selection
        languages = get_available_languages()
        lang_options = list(languages.keys())
        lang_labels = list(languages.values())
        current_lang = state.get_language()
        current_index = lang_options.index(current_lang) if current_lang in lang_options else 0
        
        new_lang_label = st.selectbox(
            f"🌐 {i18n('sidebar_language')}",
            options=lang_labels,
            index=current_index,
            key="global_lang_select",
        )
        new_lang = lang_options[lang_labels.index(new_lang_label)]
        
        if new_lang != current_lang:
            state.set_language(new_lang)
            st.rerun()
        
        st.divider()


def main():
    """Main application entry point."""
    st.set_page_config(**PAGE_CONFIG)
    
    # Apply global CSS styles (including hiding default navigation)
    render_css()
    
    # Initialize session state
    state.init_session_state()
    
    # Get current game and render appropriate page
    current_game = state.get_current_game()
    
    if current_game == "werewolf":
        render_werewolf_page()
    elif current_game == "turtle_soup":
        render_turtle_soup_page()
    else:
        render_global_sidebar()
        render_home_page()


if __name__ == "__main__":
    main()
