# --- 6. DISEÑO SIN ENCIMAMIENTOS (CSS REVISADO) ---
    # ... (tus colores y estilo de icono se mantienen igual)

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Outfit:wght@900&display=swap');
    .stApp {{ background-color: {estilo['bg']} !important; overflow-x: hidden; }}
    
    /* Partículas ajustadas */
    @keyframes falling {{ 0% {{ top: -10%; transform: rotate(0deg); }} 100% {{ top: 110%; transform: rotate(360deg); }} }}
    .particle {{ position: fixed; font-size: 2rem; z-index: 0; animation: falling 6s linear infinite; opacity: 0.6; }}

    /* Tarjeta Compacta */
    .toy-card {{
        background: {estilo['card']};
        border: 6px solid {estilo['border']};
        border-radius: 30px;
        padding: 20px 10px;
        text-align: center;
        box-shadow: 0px 10px 0px {estilo['border']};
        color: white;
        margin-bottom: 2rem;
        position: relative; z-index: 1;
    }}
    .player-name {{ font-family: 'Fredoka One', cursive; font-size: 3.5rem; text-shadow: 3px 3px 0px {estilo['border']}; }}
    
    /* ESTA ES LA PARTE QUE CAMBIA LAS LETRAS A BLANCO */
    .stAlert p {{
        color: white !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }}
    /* Quita el color azul/rojo de fondo de los iconos para que no distraigan */
    .stAlert {{
        background-color: rgba(0,0,0,0.8) !important;
        border: 2px solid white !important;
    }}
    </style>
    
    <div class="particle" style="left:70%">{icono}</div>
    <div class="particle" style="left:80%; animation-delay:3s">{icono}</div>

    <div class="toy-card">
        <div style="font-family: 'Outfit'; font-size: 0.9rem; font-weight: 900;">🕹️ TURNO DE:</div>
        <div class="player-name">{jugador_actual.upper()}</div>
        <div style="margin-top: 10px;">
            {"".join([f'<div style="background:white; color:{estilo["border"]}; padding:4px 10px; border-radius:12px; display:inline-block; margin:3px; border:2px solid {estilo["border"]}; font-weight:900; font-size:0.8rem;">{j.upper()}: {s}🥃</div>' for j, s in state["shots"].items()])}
        </div>
    </div>
    """, unsafe_allow_html=True)
