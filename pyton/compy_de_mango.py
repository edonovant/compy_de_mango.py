import streamlit as st
import random
import os
import re

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Compy de Mango", page_icon="🍹", layout="centered")

# --- 2. SERVIDOR GLOBAL ---
@st.cache_resource
def obtener_servidor():
    return {} 
servidor = obtener_servidor()

# --- 3. FUNCIONES LÓGICAS ---
def obtener_burla():
    burlas = ["🐣 ¡Vaya pollito!", "🏳️ ¡Bandera blanca!", "🍺 ¡Fondo!", "🤡 ¡Payaso!",  "📉 Tu dignidad acaba de caer por los suelos. ¡Salud!",
        "🐢 ¡Lento y miedoso! Tómate ese shot por cobarde.",
        "🤡 ¡Payaso! Para la otra mejor quédate en casa.",
        "🧊 Alguien se congeló bajo presión. ¡A beber!"
        "🐔 ¡Gallina detectada! Ese shot no se va a tomar solo.",
"😱 ¡Uy! El miedo se sentó contigo en la mesa.",
"🥃 No cumpliste... ya sabes lo que toca. ¡Salud!",
"🎭 Mucho teatro y poco valor. ¡Shot!",
"🚨 Cobardía detectada. Penalización inmediata.",
"🧃 Parece que hoy alguien vino a beber gratis.",
"🫠 La presión te derritió. ¡Toma ese shot!",
"🎯 Fallaste el objetivo… pero no falles el trago.",
"💤 Despierta campeón, esto es un juego de valientes.",
"🪦 Tu valentía acaba de morir. Brindemos por ella.",
"📢 Atención: se reporta cobardía en esta mesa.",
"🐭 ¡Ratón! El reto no muerde… pero el tequila sí.",
"🎮 Game over para tu valentía. ¡A beber!",
"🧊 Frío, frío… congelado bajo presión.",
"🍹 Alguien eligió el camino fácil. ¡Salud!",
"🫣 ¿Vergüenza? No, eso se cura con tequila.",
"🥲 Qué triste espectáculo… toma y sigue.",
"⚠️ Sistema detecta falta de agallas.",
"🍻 Si no haces el reto, al menos haz el shot.",
"😶 Silencio incómodo… y un shot obligatorio.",
"🤏 Muy cerca del valor… pero no llegaste.",
"🦥 Más lento que un perezoso. Shot por miedo.",
"😬 El reto te ganó esta vez.",
"🔥 Mucho calor en la mesa… menos en tu valentía.",
"🥴 Bueno… al menos el tequila nunca decepciona.",
"🍸 Tu orgullo acaba de pagar ese shot.",
"💀 Descansa en paz tu dignidad.",
"📉 Nivel de valentía: crítico.",
"😈 El tequila está esperando por ti.",
"🏆 Premio al más cobarde del turno."]
    return random.choice(burlas)

def obtener_frase(modo, nivel, tipo):
    ruta = f"Niveles/{modo}/{tipo}{nivel}.txt"
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            lineas = [l.strip() for l in f.readlines() if l.strip()]
            if lineas: return random.choice(lineas)
    return "¿Qué es lo primero que haces cuando tienes resaca?"

# --- 4. LOBBY ---
if "sala_id" not in st.session_state:
    st.title("🍹 Compy de Mango")
    tipo = st.radio("Selecciona:", ["🏠 Local", "🌐 Multijugador"])
    with st.expander("📝 Configurar", expanded=True):
        sala_nombre = st.text_input("Nombre Sala:") if "Multijugador" in tipo else "Local_" + str(random.randint(100, 999))
        nombres = st.text_input("Jugadores (separados por coma):")
        modo_juego = st.selectbox("Ambiente:", ["peda", "amigos", "pareja"])

    if st.button("🚀 ¡EMPEZAR!"):
        if nombres and sala_nombre:
            lista_j = [n.strip() for n in nombres.split(",") if n.strip()]
            datos = {"jugadores": lista_j, "shots": {n: 0 for n in lista_j}, "turno": 1, "mazo": lista_j.copy(), "modo": modo_juego, "reto_actual": "", "mensaje_burla": ""}
            random.shuffle(datos["mazo"])
            if "Multijugador" in tipo: servidor[sala_nombre] = datos
            else: st.session_state["datos_locales"] = datos
            st.session_state.sala_id = sala_nombre
            st.rerun()
else:
    # --- 5. CARGA DE DATOS ---
    state = st.session_state["datos_locales"] if st.session_state.sala_id.startswith("Local_") else servidor[st.session_state.sala_id]
    if not state["mazo"]:
        state["mazo"] = state["jugadores"].copy()
        random.shuffle(state["mazo"])
    jugador_actual = state["mazo"][0]
    nivel_actual = min(((state["turno"] - 1) // 10) + 1, 10)

    # --- 6. DISEÑO SIN ENCIMAMIENTOS (CSS REVISADO) ---
    colores = {
        "pareja": {"bg": "#ff4d6d", "card": "#ff758f", "border": "#c9184a", "icon": "❤️"},
        "amigos": {"bg": "#4361ee", "card": "#4895ef", "border": "#3f37c9", "icon": "✨"},
        "peda": {"bg": "#fb5607", "card": "#ff7043", "border": "#9e0059", "icon": "🍾"}
    }
    estilo = colores[state["modo"]]
    icono = estilo["icon"]

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Outfit:wght@900&display=swap');
    .stApp {{ background-color: {estilo['bg']} !important; overflow-x: hidden; }}
    
    /* Partículas ajustadas */
    @keyframes falling {{ 0% {{ top: -10%; transform: rotate(0deg); }} 100% {{ top: 110%; transform: rotate(360deg); }} }}
    .particle {{ position: fixed; font-size: 2rem; z-index: 0; animation: falling 6s linear infinite; opacity: 0.6; }}

    /* Tarjeta Compacta para no cubrir botones */
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
    
    /* Cuadros de texto legibles */
    .stAlert {{ background-color: rgba(0,0,0,0.8) !important; color: white !important; border-radius: 15px; border: 2px solid white; }}
    </style>
    
    <div class="particle" style="left:10%">{icono}</div>
    <div class="particle" style="left:80%; animation-delay:3s">{icono}</div>

    <div class="toy-card">
        <div style="font-family: 'Outfit'; font-size: 0.9rem; font-weight: 900;">🕹️ TURNO DE:</div>
        <div class="player-name">{jugador_actual.upper()}</div>
        <div style="margin-top: 10px;">
            {"".join([f'<div style="background:white; color:{estilo["border"]}; padding:4px 10px; border-radius:12px; display:inline-block; margin:3px; border:2px solid {estilo["border"]}; font-weight:900; font-size:0.8rem;">{j.upper()}: {s}🥃</div>' for j, s in state["shots"].items()])}
        </div>
    </div>
    """, unsafe_allow_html=True)

 # --- 7. LÓGICA DE ACCIONES Y RULETA ---
    if state["mensaje_burla"]:
        st.error(state["mensaje_burla"])

    es_ruleta = state["turno"] % 10 == 0
    
    if es_ruleta:
        st.markdown("<h3 style='text-align:center; color:white;'>🎰 RULETA ESPECIAL</h3>", unsafe_allow_html=True)
        if st.button("🎲 GIRAR RULETA"):
            if state["modo"] == "pareja":
                # Ruleta Picante para Parejas
                ruleta = [ 
                     "CONFESIÓN: ¿Qué fue lo primero que pensaste de tu pareja cuando la conociste?", "BAILE: Bailen una canción lenta abrazados durante un minuto completo.", "SECRETOS: Muestra la foto más antigua que tengas de ambos en tu galería.", "CARICIAS: Hazle cosquillas a tu pareja hasta que te pida que te detengas.", "PROMESA: Haz una promesa romántica que debas cumplir la próxima semana.", "CINE: Describe a tu pareja usando solo títulos de películas.",
                         "CITA IDEAL: Describe cómo sería tu cita perfecta de 24 horas.", "MIRADAS: Mírense a los ojos fijamente por 1 minuto sin hablar.", "PIROPO: Di el piropo más naco o divertido que te sepas.", "SUSURRO: Susurra algo atrevido al oído de tu pareja.", "CALOR: Quítate una prenda que tu pareja elija.", "PODER: Tu pareja puede pedirte cualquier favor pequeño ahora mismo.", "TATUAJE: Dibuja algo con un marcador en la piel de tu pareja.", "COMPLICIDAD: Cuenten un secreto que solo ustedes dos sepan.", "FOTO HOT: Tómense una foto sugerente (solo para ustedes).", "FUTURO: ¿Dónde se ven viviendo juntos en 5 años?", "GUSTO: ¿Cuál es la parte del cuerpo de tu pareja que más te atrae?", "PRIMERA VEZ: Cuenta un detalle gracioso de su primera vez juntos.", "CANCIÓN: Dedícale una canción que te recuerde a ella/él.", "REGLA: Prohíbe una palabra cariñosa por el resto del juego.", "ABRAZO LARGO: Abrázalo/a por la espalda mientras el siguiente jugador toma su turno.", "VALOR: ¿Qué es lo que más admiras de tu pareja?", "SUEÑO: Cuenta un sueño extraño que hayas tenido con tu pareja."
                    "HIELO: Pasa un hielo por el cuello de tu pareja usando solo la boca.",
                    "CALOR: Quítale una prenda a tu pareja usando solo los dientes.",
                    "MASAJE: Dale un masaje de 1 minuto en la zona que tu pareja elija.",
                    "SUSURRO: Susúrrale al oído tu fantasía más sucia.",
                    "BÉSAME MUCHO: Besa a tu pareja en 3 lugares sorpresa.",
                    "MORDIDA: Dale una mordida suave en el lóbulo de la oreja.",
                    "CIEGO: Tápale los ojos a tu pareja y dale 5 besos.",
                    "REGLA DE 10 SEG: Beso francés intenso durante 10 segundos.",
                    "NALGADA: Dale una nalgada a tu pareja (con amor).",
                    "FINAL HOT: ¡Beso de 30 segundos o ambos beben 3 shots!"
                    "HIELO: Pasa un hielo por el cuello de tu pareja usando solo la boca.",
                    "CALOR: Quítale una prenda a tu pareja usando solo los dientes.",
                    "MASAJE: Dale un masaje de 1 minuto en la zona que tu pareja elija.",
                    "SUSURRO: Susúrrale al oído tu fantasía más sucia.",
                    "BÉSAME MUCHO: Besa a tu pareja en 3 lugares sorpresa.",
                    "MORDIDA: Dale una mordida suave en el lóbulo de la oreja.",
                    "CIEGO: Tápale los ojos a tu pareja y dale 5 besos.",
                    "REGLA DE 10 SEG: Beso francés intenso durante 10 segundos.",
                    "NALGADA: Dale una nalgada a tu pareja (con amor).",
                    "FINAL HOT: ¡Beso de 30 segundos o ambos beben 3 shots!"
                ]
            else:
                # Ruleta de Peda (la lista larga que me pediste)
                ruleta = [
                    "CASCADA: Todos beben hasta que el de su derecha pare.",
                    "FONDO: Los últimos 2 en tocarse la nariz beben doble shot.",
                    "TRES MOSQUETEROS: Tú y los 2 de a lado beben 2 shots.",
                    "ESPEJO: Eliges a alguien; lo que bebas tú, lo bebe esa persona.",
                    "EL MAESTRO: Todos beben excepto tú.",
                    "SHOT COMUNITARIO: Todos los que tengan el celular en la mano beben.",
                    "PISO ES LAVA: El último en levantarse de su asiento bebe 2 shots.",
                    "DICTADOR: Eliges quién bebe 3 shots ahora mismo.",
                    "SOLTEROS: Todos los solteros beben 2 shots.",
                    "FINAL ÉPICO: ¡TODOS BEBEN DOS SHOTS!"
                                        "ESPEJO: Eliges a alguien; lo que bebas tú, lo bebe esa persona.",
                    "EL MAESTRO: Todos beben excepto tú.",
                                         "SHOT COMUNITARIO: Todos los que tengan el celular en la mano beben.",
                    "PISO ES LAVA: El último en levantarse de su asiento bebe 2 shots.",
                                           "DICTADOR: Eliges quién bebe 3 shots ahora mismo.",
                    "SOLTEROS: Todos los solteros beben 2 shots.",
                                          "FINAL ÉPICO: ¡TODOS BEBEN DOS SHOTS!", 
                    "CASCADA: Todos empiezan a beber y nadie para hasta que el de su derecha se detenga.", 
                                               "DICTADOR: Inventa una regla absurda; quien la rompa bebe 2 shots.", 
                    "PUNTERO: El que tenga menos batería en el celular se toma 2 shots de castigo.", 
                                                            "TIRO AL BLANCO: Elige a una víctima para que beba 3 shots contigo ahora mismo.", 
                    "EL MAESTRO: Todos deben imitar tus movimientos; el último en notar el cambio bebe.", 
                                    "SHOT POR ALTURA: El más alto y el más bajo del grupo brindan y beben.", 
                    "SANGRE FRÍA: Elige a alguien para un duelo de miradas; el primero en parpadear bebe.",
                                                          "BARMAN: El grupo te prepara una mezcla extraña y debes beberla sin hacer caras.", 
                      "CHISMOSO: El último en poner el dedo en la nariz recibe penalización de bebida.", 
                                  "ESPEJO: Elige a un gemelo; todo lo que tú bebas, él debe beberlo también.", 
                                           "SENTADILLA: Haz 5 sentadillas; si te tambaleas, bebes doble.", 
                         "TELÉFONO DESCOMPUESTO: Susurra algo al oído del de al lado; si el mensaje llega mal, todos beben.", 
                                                    "CATEGORÍAS: Di marcas de cerveza; el primero en repetir o tardar bebe.", 
                                 "REY DEL SHOT: Tienes el poder de obligar a cualquiera a beber un shot gratis.", 
                                           "FONDO: Elige a alguien para que termine su vaso de un solo trago.",
                                 "CERO CONTACTO: No puedes tocar tu celular por 3 turnos o bebes 2 shots.",
                         "EL MUDO: No puedes hablar hasta que sea tu turno otra vez o bebes.",
                              "ZURDO: Todos deben beber con la mano izquierda; el que use la derecha bebe doble.", 
                          "MEDIO TIEMPO: Todos los que tengan su vaso a la mitad o menos deben terminarlo.", 
                            "BRINDIS: Di un brindis épico; si nadie aplaude, bebes 2 shots.", 
                          "CUMPLEAÑOS: Todos los que cumplan años en mes par beben un shot.", 
                          "VULNERABLE: Elige a alguien para que te confiese un secreto o ambos beben.", 
                          "SUERTE: Lanza una moneda; si sale cara bebes tú, si sale cruz beben todos menos tú.", 
                          "REGLA DE TRES: El número 3 está prohibido; el que lo diga en cualquier frase bebe.", 
                          "TRES MOSQUETEROS: Tú y los dos de tus lados beben un shot de la amistad.",
                          
                          "VENGANZA: El último que te hizo beber ahora debe beber el doble.", 
                          "CÓDIGO DE VESTIMENTA: Todos los que traigan color negro beben un shot.",
                           "EL SUBMARINO: Pon un shot dentro de un vaso de cerveza y tómatelo.", 
                           "SIN RESPIRAR: Bebe medio vaso sin despegar los labios.", 
                           "RULETA RUSA: Sirve 5 vasos de agua y 1 de vodka; alguien debe elegir al azar.", 
                           "BARTENDER PROFESIONAL: Mezcla dos tipos de alcohol y dáselo al que peor te caiga.", 
                           "INFANTIL: El último en decir '¡Chiquitibum!' bebe 2 shots.", 
                           "EL HATER: Di algo que odies; todos los que estén de acuerdo beben.",
                            "SABIO: Di un dato curioso; si alguien ya lo sabía, bebes tú.", 
                    "FINAL ÉPICO: ¡Todos los jugadores beben un shot de despedida!"
                ]
            state["reto_actual"] = random.choice(ruleta)

        if state["reto_actual"]:
            st.warning(state["reto_actual"])
            if st.button("SIGUIENTE TURNO ➡️"):
                state["turno"] += 1
                state["reto_actual"] = ""
                st.rerun()
    else:
        # Botones normales de Verdad/Reto
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🧐 VERDAD"):
                state["reto_actual"] = f"VERDAD: {obtener_frase(state['modo'], nivel_actual, 'v')}"
        with c2:
            if st.button("😈 RETO"):
                state["reto_actual"] = f"RETO: {obtener_frase(state['modo'], nivel_actual, 'r')}"

        if state["reto_actual"]:
            texto = state["reto_actual"]
            # Lógica de reemplazar "OTRO" por un nombre real
            if "otro" in texto.lower():
                otros = [j for j in state["jugadores"] if j.lower() != jugador_actual.lower()]
                if otros:
                    elegido = random.choice(otros)
                    texto = re.sub(r'\botro\b', f"👉 {elegido.upper()} 👈", texto, flags=re.IGNORECASE)
            
            st.info(texto)
            
            r1, r2 = st.columns(2)
            with r1:
                if st.button("✅ LO HICE"):
                    state["mazo"].pop(0) # Corregido: .pop(0) para avanzar de turno
                    state["turno"] += 1
                    state["reto_actual"] = ""
                    state["mensaje_burla"] = ""
                    st.rerun()
            with r2:
                if st.button("🥃 SHOT"):
                    state["mensaje_burla"] = f"⚠️ {jugador_actual}: {obtener_burla()}"
                    state["shots"][jugador_actual] += 1
                    state["mazo"].pop(0)
                    state["turno"] += 1
                    state["reto_actual"] = ""
                    st.rerun()

    # --- 8. BOTÓN DE REINICIAR (EN LA BARRA LATERAL) ---
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 REINICIAR / SALIR", use_container_width=True):
        del st.session_state.sala_id
        if "datos_locales" in st.session_state:
            del st.session_state["datos_locales"]
        st.rerun()
