"""Echoes of Deceit (Turtle Soup) game page for unified MysterySeek platform."""

import logging
import sys
import asyncio
from pathlib import Path
from typing import Optional

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "Echoes-of-Deceit-v2" / "src"))

from unified_webui.i18n import I18n
from unified_webui.config import EMOJI_MAP, TURTLE_SOUP_ICON
from unified_webui.components import (
    render_css,
    render_error,
    render_success,
    render_game_stats,
    render_chat_message,
    render_commands_panel,
    render_how_to_play,
    render_status_badge,
    render_empty_state,
)
from unified_webui import session_state as state

logger = logging.getLogger(__name__)

_turtle_soup_initialized = False
_turtle_engine_ready_printed = False

# Global event loop management for safe async execution
_loop = None
_loop_lock = None

try:
    import threading
    _loop_lock = threading.Lock()
except ImportError:
    pass

try:
    import nest_asyncio
    _nest_asyncio_available = True
except ImportError:
    _nest_asyncio_available = False
    logger.warning("nest_asyncio not available, async operations may fail in some contexts")


def _get_event_loop():
    """Get or create a shared event loop for async operations."""
    global _loop
    
    if _loop_lock is not None:
        with _loop_lock:
            if _loop is None or _loop.is_closed():
                _loop = asyncio.new_event_loop()
            return _loop
    else:
        if _loop is None or _loop.is_closed():
            _loop = asyncio.new_event_loop()
        return _loop


def run_async(coro):
    """Safely run an async coroutine from synchronous code.
    
    This function uses a shared event loop instead of creating new ones,
    preventing 'Event loop is closed' errors from libraries that
    maintain async state.
    """
    loop = _get_event_loop()
    
    # Check if we're already in an async context
    try:
        running_loop = asyncio.get_running_loop()
        if running_loop is loop and _nest_asyncio_available:
            # We're inside the same loop - use nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(coro)
    except RuntimeError:
        # No running loop - this is the normal case
        pass
    
    # Set the loop and run
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


def _init_turtle_soup_imports():
    global _turtle_soup_initialized
    if _turtle_soup_initialized:
        return True
    
    try:
        from game.engine import GameEngine
        from game.domain.entities import GameState as TurtleGameState
        from game.session_runner import GameSessionRunner
        
        _turtle_soup_initialized = True
        return True
    except ImportError as e:
        logger.error(f"Failed to import Echoes of Deceit modules: {e}")
        return False


def _init_game_engine():
    global _turtle_engine_ready_printed
    
    if state.get_turtle_game_engine() is None:
        try:
            from game.engine import GameEngine
            engine = GameEngine()
            state.set_turtle_game_engine(engine)
            
            if not _turtle_engine_ready_printed:
                print("\n" + "=" * 50)
                print("🎭 Turtle Soup game engine initialized!")
                print("=" * 50 + "\n")
                _turtle_engine_ready_printed = True
            
            return True
        except Exception as e:
            state.set_turtle_error_message(f"Failed to initialize game engine: {str(e)}")
            return False
    return True


def _on_start_puzzle(puzzle_id: str):
    state.reset_turtle_game_state()
    state.set_turtle_puzzle_id(puzzle_id)
    st.session_state.turtle_home_action = "start_game"


def _on_continue_session(session_id: str, puzzle_id: str):
    state.set_turtle_session_id(session_id)
    state.set_turtle_puzzle_id(puzzle_id)
    st.session_state.turtle_home_action = "continue_game"


def render_turtle_sidebar(i18n: I18n):
    st.markdown(f"*{i18n('turtle_app_subtitle')}*")
    
    st.markdown("---")
    
    player_id = st.text_input(
        i18n("turtle_player_id"),
        value=state.get_turtle_player_id(),
        key="turtle_sidebar_player_input",
        help=i18n("turtle_player_id_help"),
    )
    
    if player_id != state.get_turtle_player_id():
        state.set_turtle_player_id(player_id)
    
    turtle_settings = state.get_turtle_settings()
    player_agent_mode = st.checkbox(
        i18n("turtle_player_agent_mode"),
        value=turtle_settings.player_agent_mode,
        key="turtle_sidebar_agent_mode",
        help=i18n("turtle_player_agent_mode_help"),
    )
    if player_agent_mode != turtle_settings.player_agent_mode:
        turtle_settings.player_agent_mode = player_agent_mode
        state.set_turtle_settings(turtle_settings)
        # Reset runner so it will be recreated with the new player_agent_mode setting
        state.set_turtle_session_runner(None)
    
    st.markdown("---")
    
    session_id = state.get_turtle_session_id()
    if session_id:
        st.caption(f"Session: {session_id[:8]}...")
    
    if turtle_settings.player_agent_mode:
        st.info(f"🤖 {i18n('turtle_player_agent_mode')}")


def render_puzzle_selection(i18n: I18n) -> Optional[str]:
    st.markdown(f"#### {EMOJI_MAP['puzzle']} {i18n('turtle_select_puzzle')}")
    
    engine = state.get_turtle_game_engine()
    if engine is None:
        render_error(i18n("turtle_error_init_required"))
        return None
    
    try:
        puzzles = engine.list_puzzles()
    except Exception as e:
        render_error(f"{i18n('error_generic')}: {str(e)}")
        return None
    
    if not puzzles:
        render_empty_state(i18n("turtle_no_puzzles"), icon="puzzle")
        return None
    
    for puzzle in puzzles:
        with st.container():
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"**{puzzle.title if puzzle.title else puzzle.id}**")
                if puzzle.description:
                    st.caption(puzzle.description[:100] + "..." if len(puzzle.description) > 100 else puzzle.description)
                
                meta_cols = st.columns(3)
                if puzzle.difficulty:
                    meta_cols[0].caption(f"{i18n('turtle_puzzle_difficulty')}: {puzzle.difficulty}")
                meta_cols[1].caption(f"{i18n('turtle_puzzle_language')}: {puzzle.language.upper()}")
                if puzzle.tags:
                    meta_cols[2].caption(f"{i18n('turtle_puzzle_tags')}: {', '.join(puzzle.tags[:3])}")
            
            with col2:
                st.button(
                    f"{EMOJI_MAP['game']} {i18n('turtle_start_game')}",
                    key=f"turtle_start_puzzle_{puzzle.id}",
                    use_container_width=True,
                    on_click=_on_start_puzzle,
                    args=[puzzle.id],
                )
            
            st.markdown("<hr style='margin: 0.75rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
    
    return None


def render_active_sessions(i18n: I18n) -> Optional[str]:
    st.markdown(f"#### {EMOJI_MAP['game']} {i18n('turtle_active_sessions')}")
    
    engine = state.get_turtle_game_engine()
    if engine is None:
        return None
    
    try:
        from game.domain.entities import GameState as TurtleGameState
        all_sessions = engine.list_sessions(player_id=state.get_turtle_player_id())
        sessions = [s for s in all_sessions if s.state == TurtleGameState.IN_PROGRESS]
    except Exception as e:
        render_error(str(e))
        return None
    
    if not sessions:
        render_empty_state(i18n("turtle_no_active_sessions"), icon="game")
        return None
    
    for session in sessions[:5]:
        with st.container():
            try:
                puzzle = engine.get_puzzle(session.puzzle_id)
                puzzle_title = puzzle.title if puzzle.title else session.puzzle_id
            except:
                puzzle_title = session.puzzle_id
            
            st.markdown(f"**{puzzle_title}**")
            
            status_html = render_status_badge(session.state.value, i18n)
            st.markdown(
                f"{status_html} | {i18n('turtle_turn')}: {session.question_count}",
                unsafe_allow_html=True,
            )
            
            st.button(
                f"{EMOJI_MAP['game']} {i18n('turtle_continue_game')}",
                key=f"turtle_continue_session_{session.session_id}",
                use_container_width=True,
                on_click=_on_continue_session,
                args=[session.session_id, session.puzzle_id],
            )
            
            st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
    
    return None


def render_turtle_home_page(i18n: I18n) -> Optional[str]:
    st.title(f"{TURTLE_SOUP_ICON} {i18n('turtle_app_title')}")
    
    st.markdown(f"### {i18n('turtle_welcome_title')}")
    st.markdown(i18n("turtle_welcome_description"))
    
    turtle_settings = state.get_turtle_settings()
    if turtle_settings.player_agent_mode:
        st.info(f"🤖 {i18n('turtle_player_agent_mode')} - AI will play automatically")
    
    st.markdown("---")
    
    if "turtle_home_action" not in st.session_state:
        st.session_state.turtle_home_action = None
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        action = render_puzzle_selection(i18n)
        if action:
            return action
    
    with col2:
        action = render_active_sessions(i18n)
        if action:
            return action
    
    action = st.session_state.get("turtle_home_action")
    if action:
        st.session_state.turtle_home_action = None
        return action
    
    return None


def _process_player_input(runner, user_input: str, i18n: I18n) -> None:
    state.add_turtle_message("user", user_input, turn_index=runner.session.turn_count + 1)
    
    try:
        response = run_async(runner.process_player_input(user_input))
        
        state.add_turtle_message(
            "assistant",
            response.message,
            verdict=response.verdict or "",
            turn_index=runner.session.turn_count,
        )
        
        if response.game_over:
            state.set_turtle_success_message(i18n("turtle_game_over_message"))
        
        st.rerun()
    except Exception as e:
        state.set_turtle_error_message(f"{i18n('error_generic')}: {str(e)}")
        st.rerun()


def _run_agent_turn(runner, i18n: I18n) -> None:
    try:
        with st.spinner(i18n("turtle_agent_thinking")):
            response = run_async(runner.run_player_agent_turn())
        
        player_msg = response.metadata.get('player_message', '')
        if player_msg:
            state.add_turtle_message(
                "user",
                player_msg,
                turn_index=runner.session.turn_count,
                is_agent=True,
            )
        
        state.add_turtle_message(
            "assistant",
            response.message,
            verdict=response.verdict or "",
            turn_index=runner.session.turn_count,
        )
        
        if response.game_over:
            state.set_turtle_success_message(i18n("turtle_game_over_message"))
        
        st.rerun()
    except Exception as e:
        state.set_turtle_error_message(f"{i18n('error_generic')}: {str(e)}")
        st.rerun()


def render_turtle_game_page(i18n: I18n) -> Optional[str]:
    session_id = state.get_turtle_session_id()
    puzzle_id = state.get_turtle_puzzle_id()
    
    if not session_id or not puzzle_id:
        render_error(i18n("turtle_error_no_active_session"))
        if st.button(f"{EMOJI_MAP['puzzle']} {i18n('nav_home')}", key="turtle_back_to_home"):
            return "back_home"
        return None
    
    engine = state.get_turtle_game_engine()
    if engine is None:
        render_error(i18n("turtle_error_init_required"))
        return None
    
    runner = state.get_turtle_session_runner()
    if runner is None:
        try:
            session = engine.get_session(session_id)
            puzzle = engine.get_puzzle(puzzle_id)
            
            turtle_settings = state.get_turtle_settings()
            player_agent_mode = turtle_settings.player_agent_mode
            
            from game.session_runner import GameSessionRunner
            runner = GameSessionRunner(
                session=session,
                puzzle=puzzle,
                kb_manager=engine.kb_manager,
                memory_manager=engine.memory_manager,
                session_store=engine.session_store,
                llm_client=engine.model_registry.get_llm_client(),
                agents_config=engine.agents_config,
                player_agent_mode=player_agent_mode,
                dm_agent_mode=True,
            )
            state.set_turtle_session_runner(runner)
            
            if session.turn_count == 0:
                response = runner.start_game()
                state.add_turtle_message("assistant", response.message, turn_index=0)
        except Exception as e:
            render_error(f"{i18n('error_generic')}: {str(e)}")
            if st.button(f"{EMOJI_MAP['puzzle']} {i18n('nav_home')}", key="turtle_back_to_home_error"):
                state.reset_turtle_game_state()
                return "back_home"
            return None
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        puzzle = engine.get_puzzle(puzzle_id)
        st.markdown(f"### {EMOJI_MAP['puzzle']} {puzzle.title if puzzle.title else puzzle_id}")
        if puzzle.puzzle_statement:
            with st.expander(i18n("turtle_puzzle_story"), expanded=False):
                st.markdown(puzzle.puzzle_statement)
    
    with col2:
        if st.button(f"🏠 {i18n('nav_home')}", key="turtle_nav_home_btn", use_container_width=True):
            return "back_home"
    
    st.markdown("---")
    
    session = runner.session
    render_game_stats(
        turn_count=session.turn_count,
        hints_used=session.hint_count,
        hints_total=runner.puzzle.constraints.max_hints,
        state=session.state.value,
        i18n=i18n,
    )
    
    st.markdown("---")
    
    render_commands_panel(i18n)
    render_how_to_play(i18n)
    
    st.markdown("---")
    st.markdown(f"#### {EMOJI_MAP['game']} {i18n('turtle_chat_history')}")
    
    messages = state.get_turtle_messages()
    chat_container = st.container()
    with chat_container:
        for msg in messages:
            render_chat_message(
                role=msg["role"],
                content=msg["content"],
                verdict=msg.get("verdict"),
                i18n=i18n,
            )
    
    from game.domain.entities import GameState as TurtleGameState
    if session.state == TurtleGameState.IN_PROGRESS:
        turtle_settings = state.get_turtle_settings()
        
        if turtle_settings.player_agent_mode:
            st.info(f"🤖 {i18n('turtle_player_agent_mode')} - AI will ask questions automatically")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(f"▶️ {i18n('turtle_agent_next_turn')}", key="turtle_agent_next_turn", use_container_width=True):
                    _run_agent_turn(runner, i18n)
            
            with col2:
                auto_play = st.checkbox(i18n("turtle_agent_auto_play"), key="turtle_auto_play_checkbox")
            
            with col3:
                if st.button(f"⏹️ {i18n('turtle_agent_stop')}", key="turtle_agent_stop", use_container_width=True):
                    st.session_state.turtle_auto_play_checkbox = False
                    st.rerun()
            
            if auto_play and runner.is_active:
                _run_agent_turn(runner, i18n)
        else:
            with st.form(key="turtle_player_input_form", clear_on_submit=True):
                user_input = st.text_input(
                    i18n("turtle_your_question"),
                    key="turtle_player_question_input",
                    placeholder=i18n("turtle_input_placeholder"),
                )
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    submit = st.form_submit_button(
                        f"{EMOJI_MAP['question']} {i18n('turtle_send')}",
                        use_container_width=True,
                    )
                with col2:
                    hint_btn = st.form_submit_button(
                        f"{EMOJI_MAP['info']} {i18n('turtle_hint')}",
                        use_container_width=True,
                    )
                
                if submit and user_input.strip():
                    _process_player_input(runner, user_input.strip(), i18n)
                elif hint_btn:
                    _process_player_input(runner, "/hint", i18n)
    else:
        _render_turtle_game_over(session, i18n)
        
        if st.button(f"🏠 {i18n('turtle_back_home')}", key="turtle_game_over_back"):
            return "back_home"
    
    return None


def _render_turtle_game_over(session, i18n: I18n) -> None:
    """Render the game over section with proper state handling and score display."""
    from game.domain.entities import GameState as TurtleGameState
    
    if session.state == TurtleGameState.COMPLETED:
        st.success(f"🎉 {i18n('turtle_congratulations')}")
    elif session.state == TurtleGameState.ABORTED:
        st.warning(f"⚠️ {i18n('turtle_ended')}: {i18n('turtle_state_aborted')}")
    else:
        st.info(f"📋 {i18n('turtle_ended')}: {session.state.value}")
    
    st.markdown(f"**{i18n('turtle_final_score')}:** {session.score or 'N/A'}")
    st.markdown(f"**{i18n('turtle_total_turns')}:** {session.turn_count}")


def render_turtle_soup_page():
    render_css()
    
    i18n = state.get_i18n()
    
    if not _init_turtle_soup_imports():
        st.error("Failed to initialize Echoes of Deceit. Please check if the module is properly installed.")
        if st.button(f"🏠 {i18n('btn_home')}", key="turtle_init_error_home"):
            state.set_current_game("home")
            st.rerun()
        return
    
    if not _init_game_engine():
        error_msg = state.get_turtle_error_message()
        if error_msg:
            render_error(error_msg)
        if st.button(f"🏠 {i18n('btn_home')}", key="turtle_engine_error_home"):
            state.set_current_game("home")
            st.rerun()
        return
    
    with st.sidebar:
        if st.button(f"🏠 {i18n('btn_home')}", key="turtle_back_home_btn", use_container_width=True):
            state.set_current_game("home")
            st.rerun()
        
        st.divider()
        
        render_turtle_sidebar(i18n)
    
    current_turtle_page = state.get_turtle_current_page()
    
    if current_turtle_page == "game" or state.get_turtle_session_id():
        action = render_turtle_game_page(i18n)
        if action == "back_home":
            state.reset_turtle_game_state()
            state.set_turtle_current_page("home")
            st.rerun()
    else:
        action = render_turtle_home_page(i18n)
        if action == "start_game":
            _start_new_turtle_game(i18n)
        elif action == "continue_game":
            state.set_turtle_current_page("game")
            st.rerun()


def _start_new_turtle_game(i18n: I18n) -> None:
    engine = state.get_turtle_game_engine()
    puzzle_id = state.get_turtle_puzzle_id()
    player_id = state.get_turtle_player_id()
    
    if not engine or not puzzle_id:
        state.set_turtle_error_message(i18n("turtle_error_missing_puzzle"))
        return
    
    try:
        session = run_async(engine.create_session(puzzle_id, player_id))
        state.set_turtle_session_id(session.session_id)
        state.set_turtle_current_page("game")
        st.rerun()
    except Exception as e:
        state.set_turtle_error_message(f"{i18n('error_generic')}: {str(e)}")
        st.rerun()
