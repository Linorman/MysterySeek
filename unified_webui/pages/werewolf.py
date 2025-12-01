"""AutoWerewolf game page for unified MysterySeek platform."""

import logging
import sys
import time
from pathlib import Path
from typing import Optional, List

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "AutoWerewolf"))

from unified_webui.i18n import I18n
from unified_webui.config import WEREWOLF_ROLE_ICONS, WEREWOLF_ICON, WerewolfSettings
from unified_webui.components import render_css
from unified_webui import session_state as state

logger = logging.getLogger(__name__)

_werewolf_initialized = False
_werewolf_config_loaded = False


def _init_werewolf_imports():
    global _werewolf_initialized
    if _werewolf_initialized:
        return True
    
    try:
        from autowerewolf.streamlit_web.session import (
            StreamlitGameSession,
            StreamlitModelConfig,
            StreamlitGameConfig,
            StreamlitCorrectorConfig,
            session_manager,
            PlayerData,
            EventData,
        )
        from autowerewolf.streamlit_web.config_loader import streamlit_config_loader
        
        _werewolf_initialized = True
        return True
    except ImportError as e:
        logger.error(f"Failed to import AutoWerewolf modules: {e}")
        return False


def _load_werewolf_config():
    global _werewolf_config_loaded
    if _werewolf_config_loaded:
        return
    
    if not st.session_state.get("werewolf_config_loaded", False):
        try:
            from autowerewolf.streamlit_web.config_loader import streamlit_config_loader
            
            streamlit_config_loader.load_from_file()
            streamlit_config_loader.load_game_config()
            
            mc = streamlit_config_loader.model_config
            gc = streamlit_config_loader.game_config
            
            if mc and gc:
                werewolf_settings = WerewolfSettings(
                    backend=mc.backend,
                    model_name=mc.model_name,
                    api_base=mc.api_base,
                    api_key=mc.api_key,
                    ollama_base_url=mc.ollama_base_url,
                    temperature=mc.temperature,
                    max_tokens=mc.max_tokens,
                    enable_corrector=mc.enable_corrector,
                    corrector_max_retries=mc.corrector_max_retries,
                    role_set=gc.role_set,
                    game_language=gc.language,
                    random_seed=gc.random_seed,
                )
                state.set_werewolf_settings(werewolf_settings)
                logger.info("Loaded werewolf settings from config files")
            
            st.session_state.werewolf_config_loaded = True
        except Exception as e:
            logger.warning(f"Could not load werewolf config: {e}")
            st.session_state.werewolf_config_loaded = True
    
    _werewolf_config_loaded = True


def _get_werewolf_session():
    return st.session_state.get("werewolf_session")


def render_werewolf_sidebar(i18n: I18n):
    session = _get_werewolf_session()
    game_running = session is not None and session.status == "running"
    
    status_color = "🟢" if game_running else "🔴"
    status_text = i18n("werewolf_connected") if game_running else i18n("werewolf_disconnected")
    st.caption(f"{status_color} {status_text}")
    
    mode = st.radio(
        i18n("werewolf_mode"),
        options=["watch", "play"],
        format_func=lambda x: i18n("werewolf_watch_mode") if x == "watch" else i18n("werewolf_play_mode"),
        horizontal=True,
        disabled=game_running,
        key="werewolf_mode_radio",
    )
    
    st.subheader(i18n("werewolf_model_config"))
    
    werewolf_settings = state.get_werewolf_settings()
    
    backend = st.selectbox(
        i18n("werewolf_backend"),
        options=["ollama", "api"],
        format_func=lambda x: "Ollama" if x == "ollama" else "API",
        index=0 if werewolf_settings.backend == "ollama" else 1,
        disabled=game_running,
        key="werewolf_backend_select",
    )
    
    model_name = st.text_input(
        i18n("werewolf_model_name"),
        value=werewolf_settings.model_name,
        disabled=game_running,
        key="werewolf_model_name_input",
    )
    
    if backend == "ollama":
        ollama_url = st.text_input(
            i18n("werewolf_ollama_url"),
            value=werewolf_settings.ollama_base_url or "",
            placeholder="http://localhost:11434",
            disabled=game_running,
            key="werewolf_ollama_url_input",
        )
        api_base = None
        api_key = None
    else:
        api_base = st.text_input(
            i18n("werewolf_api_base"),
            value=werewolf_settings.api_base or "",
            placeholder="https://api.openai.com/v1",
            disabled=game_running,
            key="werewolf_api_base_input",
        )
        api_key = st.text_input(
            i18n("werewolf_api_key"),
            value=werewolf_settings.api_key or "",
            type="password",
            disabled=game_running,
            key="werewolf_api_key_input",
        )
        ollama_url = None
    
    col1, col2 = st.columns(2)
    with col1:
        temperature = st.number_input(
            i18n("werewolf_temperature"),
            min_value=0.0,
            max_value=2.0,
            value=werewolf_settings.temperature,
            step=0.1,
            disabled=game_running,
            key="werewolf_temp_input",
        )
    with col2:
        max_tokens = st.number_input(
            i18n("werewolf_max_tokens"),
            min_value=100,
            value=werewolf_settings.max_tokens,
            step=100,
            disabled=game_running,
            key="werewolf_tokens_input",
        )
    
    with st.expander(i18n("werewolf_output_corrector")):
        enable_corrector = st.checkbox(
            i18n("werewolf_enable_corrector"),
            value=werewolf_settings.enable_corrector,
            disabled=game_running,
            key="werewolf_corrector_check",
        )
        
        if enable_corrector:
            corrector_retries = st.number_input(
                i18n("werewolf_corrector_retries"),
                min_value=1,
                max_value=5,
                value=werewolf_settings.corrector_max_retries,
                disabled=game_running,
                key="werewolf_corrector_retries_input",
            )
        else:
            corrector_retries = 2
    
    st.subheader(i18n("werewolf_game_rules"))
    
    role_set = st.selectbox(
        i18n("werewolf_role_set"),
        options=["A", "B"],
        format_func=lambda x: i18n("werewolf_role_set_a") if x == "A" else i18n("werewolf_role_set_b"),
        index=0 if werewolf_settings.role_set == "A" else 1,
        disabled=game_running,
        key="werewolf_role_set_select",
    )
    
    game_language = st.selectbox(
        i18n("werewolf_game_language"),
        options=["en", "zh"],
        format_func=lambda x: "English" if x == "en" else "中文",
        index=0 if werewolf_settings.game_language == "en" else 1,
        disabled=game_running,
        key="werewolf_game_lang_select",
        help=i18n("werewolf_game_language_hint"),
    )
    
    random_seed = st.text_input(
        i18n("werewolf_random_seed"),
        value=str(werewolf_settings.random_seed) if werewolf_settings.random_seed else "",
        disabled=game_running,
        key="werewolf_seed_input",
    )
    seed_value = int(random_seed) if random_seed.isdigit() else None
    
    if mode == "play":
        st.subheader(i18n("werewolf_player_settings"))
        col1, col2 = st.columns(2)
        with col1:
            player_seat = st.selectbox(
                i18n("werewolf_your_seat"),
                options=list(range(1, 13)),
                disabled=game_running,
                key="werewolf_seat_select",
            )
        with col2:
            player_name = st.text_input(
                i18n("werewolf_your_name"),
                value="Human Player",
                disabled=game_running,
                key="werewolf_name_input",
            )
    else:
        player_seat = None
        player_name = None
    
    if not game_running:
        needs_update = (
            werewolf_settings.backend != backend or
            werewolf_settings.model_name != model_name or
            werewolf_settings.temperature != temperature or
            werewolf_settings.max_tokens != int(max_tokens) or
            werewolf_settings.enable_corrector != enable_corrector or
            werewolf_settings.corrector_max_retries != int(corrector_retries) or
            werewolf_settings.role_set != role_set or
            werewolf_settings.game_language != game_language or
            werewolf_settings.random_seed != seed_value or
            (backend == "ollama" and werewolf_settings.ollama_base_url != (ollama_url or None)) or
            (backend == "api" and (werewolf_settings.api_base != (api_base or None) or 
                                   werewolf_settings.api_key != (api_key or None)))
        )
        
        if needs_update:
            werewolf_settings.backend = backend
            werewolf_settings.model_name = model_name
            werewolf_settings.temperature = temperature
            werewolf_settings.max_tokens = int(max_tokens)
            werewolf_settings.enable_corrector = enable_corrector
            werewolf_settings.corrector_max_retries = int(corrector_retries)
            werewolf_settings.role_set = role_set
            werewolf_settings.game_language = game_language
            werewolf_settings.random_seed = seed_value
            if backend == "ollama":
                werewolf_settings.ollama_base_url = ollama_url or None
                werewolf_settings.api_base = None
                werewolf_settings.api_key = None
            else:
                werewolf_settings.api_base = api_base or None
                werewolf_settings.api_key = api_key or None
                werewolf_settings.ollama_base_url = None
            state.set_werewolf_settings(werewolf_settings)
    
    st.divider()
    
    if not game_running:
        if st.button(i18n("werewolf_start_game"), type="primary", use_container_width=True, key="werewolf_start_btn"):
            _start_werewolf_game(
                mode=mode,
                backend=backend,
                model_name=model_name,
                api_base=api_base,
                api_key=api_key,
                ollama_url=ollama_url,
                temperature=temperature,
                max_tokens=int(max_tokens),
                enable_corrector=enable_corrector,
                corrector_retries=int(corrector_retries),
                role_set=role_set,
                game_language=game_language,
                seed_value=seed_value,
                player_seat=player_seat,
                player_name=player_name,
            )
    else:
        if st.button(i18n("werewolf_stop_game"), type="secondary", use_container_width=True, key="werewolf_stop_btn"):
            if session:
                session.stop()
                st.session_state.werewolf_session = None
                st.rerun()


def _start_werewolf_game(
    mode: str,
    backend: str,
    model_name: str,
    api_base: Optional[str],
    api_key: Optional[str],
    ollama_url: Optional[str],
    temperature: float,
    max_tokens: int,
    enable_corrector: bool,
    corrector_retries: int,
    role_set: str,
    game_language: str,
    seed_value: Optional[int],
    player_seat: Optional[int],
    player_name: Optional[str],
):
    if not _init_werewolf_imports():
        st.error("Failed to initialize AutoWerewolf. Please check if the module is properly installed.")
        return
    
    from autowerewolf.streamlit_web.session import (
        StreamlitModelConfig,
        StreamlitGameConfig,
        StreamlitCorrectorConfig,
        session_manager,
    )
    
    model_config = StreamlitModelConfig(
        backend=backend,
        model_name=model_name,
        api_base=api_base or None,
        api_key=api_key or None,
        ollama_base_url=ollama_url or None,
        temperature=temperature,
        max_tokens=max_tokens,
        enable_corrector=enable_corrector,
        corrector_max_retries=corrector_retries,
    )
    
    game_config = StreamlitGameConfig(
        role_set=role_set,
        random_seed=seed_value,
        language=game_language,
    )
    
    corrector_config = StreamlitCorrectorConfig(
        enabled=enable_corrector,
        max_retries=corrector_retries,
        use_separate_model=False,
    )
    
    session = session_manager.create_session(
        mode=mode,
        model_config=model_config,
        game_config=game_config,
        corrector_config=corrector_config,
        player_seat=player_seat,
        player_name=player_name,
    )
    session.start()
    st.session_state.werewolf_session = session
    st.session_state.werewolf_last_event_count = 0
    st.session_state.werewolf_winner_shown_for_game = None
    st.session_state.werewolf_show_winner_modal = False
    st.session_state.werewolf_winner_team = None
    st.rerun()


def render_player_card(player, sheriff_id: Optional[str], i18n: I18n):
    role_icon = WEREWOLF_ROLE_ICONS.get(player.role, "❓")
    
    border_color = '#22c55e' if player.is_alive else '#6b7280'
    bg_color = '#1a1a2e' if player.is_alive else '#2d2d3d'
    opacity = '1' if player.is_alive else '0.6'
    sheriff_badge = '👑' if player.id == sheriff_id else ''
    role_text = i18n(f"werewolf_{player.role}") if player.role != 'hidden' else i18n('werewolf_hidden')
    teammate_icon = ' 🐺' if player.is_teammate else ''
    human_icon = ' ⭐' if player.is_human else ''
    status_color = '#22c55e' if player.is_alive else '#ef4444'
    status_text = i18n('werewolf_alive') if player.is_alive else i18n('werewolf_dead')
    
    card_html = f'''<div style="padding: 10px; border-radius: 8px; border: 2px solid {border_color}; background: {bg_color}; opacity: {opacity}; margin: 5px 0;">
<div style="display: flex; justify-content: space-between; align-items: center;">
<span style="font-weight: bold;">#{player.seat_number} {player.name}</span>
<span>{sheriff_badge}</span>
</div>
<div style="margin-top: 5px;">
<span>{role_icon} {role_text}</span>{teammate_icon}{human_icon}
</div>
<div style="font-size: 0.8em; color: {status_color};">
{status_text}
</div>
</div>'''
    
    st.markdown(card_html, unsafe_allow_html=True)


def render_game_arena(session, i18n: I18n):
    game_state = session.get_state()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(i18n("werewolf_day_number"), game_state["day_number"])
    with col2:
        phase = game_state["phase"]
        phase_icon = "🌙" if phase == "night" else "☀️"
        phase_text = i18n("werewolf_night") if phase == "night" else i18n("werewolf_day")
        st.metric(i18n("werewolf_current_phase"), f"{phase_icon} {phase_text}")
    with col3:
        alive_count = sum(1 for p in game_state["players"] if p.is_alive)
        st.metric(i18n("werewolf_players_alive"), f"{alive_count}/12")
    
    status = session.status
    if status == "running":
        st.info(f"🎮 {i18n('werewolf_game_running')}")
    elif status == "completed":
        winning = game_state.get("winning_team")
        if winning == "village":
            st.success(i18n("werewolf_village_wins"))
        else:
            st.error(i18n("werewolf_werewolf_wins"))
    elif status == "error":
        st.error(f"❌ {i18n('werewolf_game_error')}: {session.error_message}")
    elif status == "stopped":
        st.warning(f"⏹️ {i18n('werewolf_game_stopped')}")
    
    st.subheader(i18n("werewolf_players"))
    
    players = game_state.get("players", [])
    if players:
        cols = st.columns(4)
        for i, player in enumerate(players):
            with cols[i % 4]:
                render_player_card(player, game_state.get("sheriff_id"), i18n)


def render_human_panel(session, i18n: I18n):
    game_state = session.get_state()
    human_view = game_state.get("human_player_view")
    
    if not human_view:
        return
    
    st.subheader(f"🎯 {i18n('werewolf_your_status')}")
    
    role = human_view.get("role", "hidden")
    role_icon = WEREWOLF_ROLE_ICONS.get(role, "❓")
    alignment = human_view.get("alignment", "hidden")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        role_text = i18n(f"werewolf_{role}")
        st.metric(i18n("werewolf_role"), f"{role_icon} {role_text}")
    with col2:
        alignment_text = i18n(f"werewolf_{alignment}") if alignment != "hidden" else "???"
        st.metric(i18n("werewolf_alignment"), alignment_text)
    with col3:
        status_text = i18n("werewolf_alive") if human_view.get("is_alive") else i18n("werewolf_dead")
        if human_view.get("is_sheriff"):
            status_text = f"👑 {status_text}"
        st.metric(i18n("werewolf_status"), status_text)
    
    private_info = human_view.get("private_info", {})
    
    if private_info:
        with st.expander(i18n("werewolf_player_info"), expanded=True):
            if "teammates" in private_info:
                st.write(f"🐺 **{i18n('werewolf_teammates')}:**")
                for tm in private_info["teammates"]:
                    status_icon = "✅" if tm["is_alive"] else "💀"
                    st.write(f"  {status_icon} {tm['name']}")
            
            if "check_results" in private_info:
                st.write(f"🔮 **{i18n('werewolf_seer_checks')}:**")
                for check in private_info["check_results"]:
                    result_icon = "👤" if check["result"] == "village" else "🐺"
                    result_key = "werewolf_" + check["result"]
                    st.write(f"  {result_icon} {check['player_name']}: {i18n(result_key)}")
            
            if "has_cure" in private_info:
                st.write(f"💊 **{i18n('werewolf_cure')}:** {'✅' if private_info['has_cure'] else '❌'}")
                st.write(f"☠️ **{i18n('werewolf_poison')}:** {'✅' if private_info.get('has_poison') else '❌'}")
                if "attack_target" in private_info:
                    st.write(f"⚠️ **{i18n('werewolf_attack_target')}:** {private_info['attack_target']['name']}")
            
            if "can_shoot" in private_info:
                st.write(f"🔫 **{i18n('werewolf_can_shoot')}:** {'✅' if private_info['can_shoot'] else '❌'}")
            
            if "last_protected" in private_info and private_info["last_protected"]:
                st.write(f"🛡️ **{i18n('werewolf_last_protected')}:** {private_info['last_protected']['name']}")
            
            if "revealed" in private_info:
                st.write(f"🃏 **{i18n('werewolf_revealed')}:** {'✅' if private_info['revealed'] else '❌'}")


def render_action_panel(session, i18n: I18n):
    action = session.get_action_request(timeout=0.05)
    
    if action:
        st.session_state.werewolf_pending_action = action
        st.session_state.werewolf_action_submitted = False
    
    pending = st.session_state.get("werewolf_pending_action")
    if not pending or st.session_state.get("werewolf_action_submitted"):
        return
    
    st.subheader(f"⚡ {i18n('werewolf_your_turn')}")
    
    action_type = pending.get("action_type")
    prompt = pending.get("prompt", "")
    valid_targets = pending.get("valid_targets_info", [])
    allow_skip = pending.get("allow_skip", False)
    extra_context = pending.get("extra_context", {})
    
    st.info(prompt)
    
    if extra_context.get("is_werewolf_discussion"):
        ai_proposals = extra_context.get("ai_proposals", [])
        if ai_proposals:
            with st.expander(f"🐺 {i18n('werewolf_teammates_suggestions')}", expanded=True):
                for proposal in ai_proposals:
                    target_name = proposal.get("proposed_target_name", proposal.get("proposed_target", ""))
                    wolf_name = proposal.get("werewolf_name", "")
                    reasoning = proposal.get("reasoning", "")
                    st.markdown(f"""
                    **{wolf_name}** {i18n('werewolf_suggests_kill')} **{target_name}**
                    > {reasoning}
                    """)
    
    if action_type == "target_selection":
        options: list = [""] + [f"#{t['seat_number']} {t['name']}" for t in valid_targets]
        option_ids: list = [None] + [t["id"] for t in valid_targets]
        
        if allow_skip:
            options.insert(1, f"({i18n('werewolf_skip')})")
            option_ids.insert(1, "skip")
        
        selected = st.selectbox(
            i18n("werewolf_select_target"),
            options=options,
            key="werewolf_action_target_select",
        )
        
        if st.button(i18n("werewolf_confirm_action"), type="primary", key="werewolf_confirm_action_btn"):
            idx = options.index(selected) if selected else 0
            target_id = option_ids[idx] if idx > 0 else None
            
            if target_id == "skip":
                session.submit_action("skip", None, None, None)
            else:
                session.submit_action(action_type, target_id, None, None)
            
            st.session_state.werewolf_pending_action = None
            st.session_state.werewolf_action_submitted = True
            st.success(i18n("werewolf_action_submitted"))
            time.sleep(0.5)
            st.rerun()
    
    elif action_type == "yes_no":
        col1, col2 = st.columns(2)
        with col1:
            if st.button(i18n("yes"), type="primary", use_container_width=True, key="werewolf_yes_btn"):
                session.submit_action(action_type, None, None, True)
                st.session_state.werewolf_pending_action = None
                st.session_state.werewolf_action_submitted = True
                st.rerun()
        with col2:
            if st.button(i18n("no"), use_container_width=True, key="werewolf_no_btn"):
                session.submit_action(action_type, None, None, False)
                st.session_state.werewolf_pending_action = None
                st.session_state.werewolf_action_submitted = True
                st.rerun()
    
    elif action_type == "text_input":
        text = st.text_area(
            i18n("werewolf_enter_speech"),
            key="werewolf_speech_input",
            height=100,
        )
        
        if st.button(i18n("werewolf_submit"), type="primary", key="werewolf_submit_text_btn"):
            session.submit_action(action_type, None, text, None)
            st.session_state.werewolf_pending_action = None
            st.session_state.werewolf_action_submitted = True
            st.success(i18n("werewolf_action_submitted"))
            time.sleep(0.5)
            st.rerun()


def render_event_log(session, i18n: I18n):
    st.subheader(f"📜 {i18n('werewolf_game_log')}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button(i18n("werewolf_clear_events"), key="werewolf_clear_events_btn"):
            session.events.clear()
            st.rerun()
    
    filter_options = {
        "all": i18n("werewolf_all"),
        "speech": f"💬 {i18n('werewolf_speech')}",
        "vote": f"🗳️ {i18n('werewolf_vote')}",
        "death": f"💀 {i18n('werewolf_death')}",
        "sheriff": f"👑 {i18n('werewolf_sheriff')}",
        "system": f"📢 {i18n('werewolf_narration')}",
    }
    
    with col2:
        selected_filter = st.selectbox(
            i18n("werewolf_event_filter") if i18n("werewolf_event_filter") else "Filter",
            options=list(filter_options.keys()),
            format_func=lambda x: filter_options[x],
            key="werewolf_event_filter_select",
            label_visibility="collapsed",
        )
    
    events = session.get_events()
    
    if not events:
        st.info(i18n("werewolf_no_events"))
        return
    
    def get_event_category(event) -> str:
        event_type = event.event_type
        if event_type in ["speech", "last_words", "sheriff_campaign_speech"]:
            return "speech"
        elif event_type in ["vote_cast", "vote_result", "sheriff_vote"]:
            return "vote"
        elif event_type in ["death_announcement", "lynch", "hunter_shot", "night_kill", 
                           "witch_poison", "wolf_self_explode"]:
            return "death"
        elif event_type in ["sheriff_election", "sheriff_elected", "badge_pass", "badge_tear"]:
            return "sheriff"
        else:
            return "system"
    
    filtered_events = []
    for event in events:
        if selected_filter == "all":
            filtered_events.append(event)
        else:
            category = get_event_category(event)
            if category == selected_filter:
                filtered_events.append(event)
    
    event_container = st.container(height=600)
    
    with event_container:
        display_events = filtered_events[-100:]
        
        last_day = 0
        last_phase = ""
        
        for event in display_events:
            if event.day_number != last_day or event.phase != last_phase:
                if last_day != 0 or last_phase != "":
                    phase_icon = "🌙" if event.phase == "night" else "☀️"
                    phase_text = i18n("werewolf_night") if event.phase == "night" else i18n("werewolf_day")
                    st.divider()
                    st.markdown(f"**{phase_icon} {i18n('werewolf_day')} {event.day_number} - {phase_text}**")
                last_day = event.day_number
                last_phase = event.phase
            
            event_type = event.event_type
            
            if event_type in ["speech", "last_words", "sheriff_campaign_speech"]:
                st.chat_message("user", avatar="🗣️").write(event.description)
            elif event_type in ["death_announcement", "lynch", "hunter_shot", 
                               "night_kill", "witch_poison", "wolf_self_explode"]:
                st.error(event.description)
            elif event_type in ["vote_cast", "vote_result", "sheriff_vote"]:
                st.info(event.description)
            elif event_type in ["sheriff_election", "sheriff_elected", "badge_pass", "badge_tear"]:
                st.warning(event.description)
            else:
                st.write(event.description)


def render_winner_modal(winning_team: str, i18n: I18n):
    if winning_team == "village":
        st.balloons()
        st.success(f"""
        # 🎉 {i18n('werewolf_village_wins')}
        
        {i18n('werewolf_good_team_victory')}
        """)
    else:
        st.snow()
        st.error(f"""
        # 🐺 {i18n('werewolf_werewolf_wins')}
        
        {i18n('werewolf_evil_team_victory')}
        """)
    
    if st.button(i18n("close"), key="werewolf_close_winner_btn"):
        st.session_state.werewolf_show_winner_modal = False
        st.session_state.werewolf_winner_team = None
        st.rerun()


def render_werewolf_main_content(i18n: I18n):
    session = _get_werewolf_session()
    
    if session is None:
        st.session_state.werewolf_winner_shown_for_game = None
        
        winner_team = st.session_state.get("werewolf_winner_team")
        if st.session_state.get("werewolf_show_winner_modal") and winner_team:
            render_winner_modal(winner_team, i18n)
            return
        
        st.title(f"{WEREWOLF_ICON} {i18n('werewolf_app_title')}")
        
        st.markdown(f"""
        ### {i18n('werewolf_no_game_running')}
        
        {i18n('werewolf_click_start')}
        
        ---
        
        **{i18n('werewolf_watch_mode')}**: {i18n('werewolf_watch_desc')}
        
        **{i18n('werewolf_play_mode')}**: {i18n('werewolf_play_desc')}
        """)
        return
    
    if session.status == "completed":
        game_id = session.game_id
        if st.session_state.werewolf_winner_shown_for_game != game_id:
            game_state = session.get_state()
            winning_team = game_state.get("winning_team")
            st.session_state.werewolf_show_winner_modal = True
            st.session_state.werewolf_winner_team = winning_team
            st.session_state.werewolf_winner_shown_for_game = game_id
    
    winner_team = st.session_state.get("werewolf_winner_team")
    if st.session_state.get("werewolf_show_winner_modal") and winner_team:
        render_winner_modal(winner_team, i18n)
        return
    
    if session.mode == "play":
        col1, col2 = st.columns([2, 1])
        
        with col1:
            render_game_arena(session, i18n)
            render_event_log(session, i18n)
        
        with col2:
            render_human_panel(session, i18n)
            render_action_panel(session, i18n)
    else:
        col1, col2 = st.columns([3, 2])
        
        with col1:
            render_game_arena(session, i18n)
        
        with col2:
            render_event_log(session, i18n)
    
    if session.status == "running":
        time.sleep(1)
        st.rerun()


def render_werewolf_page():
    render_css()
    
    i18n = state.get_i18n()
    
    _load_werewolf_config()
    
    with st.sidebar:
        if st.button(f"🏠 {i18n('btn_home')}", key="werewolf_back_home_btn", use_container_width=True):
            state.set_current_game("home")
            st.rerun()
        
        st.divider()
        
        render_werewolf_sidebar(i18n)
    
    render_werewolf_main_content(i18n)
