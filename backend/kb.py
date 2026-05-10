"""LoL Knowledge Base — corpus extendido a partir del glosario del wiki Fandom."""

KNOWLEDGE_BASE: list[dict[str, str]] = [
    # === Términos generales / numéricos ===
    {
        "pregunta": "¿Qué es un 1v1?",
        "respuesta": "Un 1v1 es una partida personalizada entre 2 jugadores. Se arma normalmente en el Abismo de los Lamentos o en el carril medio de la Grieta. Gana el que saca primera sangre, llega a 100 CS o tira la torre.",
    },
    {
        "pregunta": "¿Qué significa 3's?",
        "respuesta": "3's hace referencia al Bosque Retorcido, el mapa donde se enfrentan dos equipos de 3 integrantes.",
    },
    {
        "pregunta": "¿Qué significa 5's?",
        "respuesta": "5's es la Grieta del Invocador, el mapa principal donde se enfrentan dos equipos de 5.",
    },

    # === A ===
    {
        "pregunta": "¿Qué es un AA o autoataque?",
        "respuesta": "AA significa Auto Attack: el ataque básico de tu campeón al hacer clic derecho sobre un enemigo. Sin habilidades, solo el golpe normal.",
    },
    {
        "pregunta": "¿Qué es ABAM?",
        "respuesta": "ABAM (All Blind All Mid) es una partida custom donde todos eligen campeón en Blind Pick para pelear solo en mid.",
    },
    {
        "pregunta": "¿Qué es un Ace?",
        "respuesta": "Un Ace ocurre cuando todos los miembros de un equipo son eliminados al mismo tiempo. Suele abrir la ventana para tomar Barón o terminar la partida.",
    },
    {
        "pregunta": "¿Qué es una habilidad activa?",
        "respuesta": "Una activa es una habilidad de campeón o item que requiere clic o tecla para funcionar, a diferencia de las pasivas que están siempre encendidas.",
    },
    {
        "pregunta": "¿Qué es AD o Attack Damage?",
        "respuesta": "AD (Attack Damage) es el daño físico de tu campeón. Escala con items como Filo Infinito, BF Sword, etc.",
    },
    {
        "pregunta": "¿Qué es ADAM?",
        "respuesta": "ADAM (All Draft All Mid) es una partida custom donde se elige campeón en modo Draft Pick y se pelea solo en mid.",
    },
    {
        "pregunta": "¿Qué es un ADC?",
        "respuesta": "ADC (Attack Damage Carry) es el campeón que basa su daño en autoataques. Suele ir bot lane y se equipa con AD, velocidad de ataque y crítico.",
    },
    {
        "pregunta": "¿Qué significa AFK?",
        "respuesta": "AFK (Away From Keyboard) significa que el jugador no está controlando a su campeón. También se usa para señalar a desconectados.",
    },
    {
        "pregunta": "¿Qué es el aggro?",
        "respuesta": "Aggro es a quién está apuntando un agente controlado por la IA: súbditos, torretas o monstruos neutrales. Si tomas aggro de torre te empieza a pegar.",
    },
    {
        "pregunta": "¿Qué es AoE o área de efecto?",
        "respuesta": "AoE (Area of Effect) son habilidades que hacen daño en un área y no a un solo objetivo. Ejemplo: la ulti de Kennen o la R de Miss Fortune.",
    },
    {
        "pregunta": "¿Qué es AP o Ability Power?",
        "respuesta": "AP (Ability Power) es el Poder de Habilidad. Escala el daño mágico de tus skills. Items como Sombrero de Rabadon o Cetro de Rylai dan AP.",
    },
    {
        "pregunta": "¿Qué es ARAM?",
        "respuesta": "ARAM (All Random All Mid) es el modo donde se eligen campeones aleatoriamente y se pelea solo en el carril medio del Abismo de los Lamentos.",
    },
    {
        "pregunta": "¿Qué es ArPen o penetración de armadura?",
        "respuesta": "ArPen (Armor Penetration) es la estadística que ignora parte de la armadura del enemigo, haciendo que tu daño físico pegue más fuerte.",
    },
    {
        "pregunta": "¿Qué es AS o velocidad de ataque?",
        "respuesta": "AS (Attack Speed) es la velocidad a la que tu campeón ejecuta autoataques. Tope: 2.5 ataques por segundo.",
    },
    {
        "pregunta": "¿Qué es un asesino?",
        "respuesta": "Un asesino es un campeón que emboscar y elimina rápido a sus enemigos. Suelen tener invisibilidad o embestidas fuertes. Ejemplos: Zed, Talon, Kha'Zix.",
    },
    {
        "pregunta": "¿Qué es una asistencia?",
        "respuesta": "Una asistencia es ayudar a un aliado a eliminar a un campeón enemigo. Te dan oro y experiencia aunque no des el último golpe.",
    },
    {
        "pregunta": "¿Qué es un aura?",
        "respuesta": "Un aura es una habilidad pasiva que beneficia a los campeones aliados que están dentro del rango del item o campeón que la posee.",
    },

    # === B ===
    {
        "pregunta": "¿Qué significa backear o presionar B?",
        "respuesta": "Backear es volver a la base presionando B. Se hace para recuperar vida, maná o comprar items. Tarda 8 segundos en canalizarse.",
    },
    {
        "pregunta": "¿Qué es babysit o niñera?",
        "respuesta": "Babysit es cuando un campeón (típicamente el jungla) cubre tu carril para que no te tiren la torre mientras tú no estás.",
    },
    {
        "pregunta": "¿Qué es hacer bait o carnada?",
        "respuesta": "Bait es ofrecerse de señuelo para atraer al enemigo a una trampa. Por ejemplo, fingir estar bajo de vida para que te persigan al arbusto.",
    },
    {
        "pregunta": "¿Qué es Baron Nashor?",
        "respuesta": "Baron es el monstruo neutral más fuerte del mapa. Te da un buff que hace tus minions mucho más poderosos y te da AD/AP. Aparece a partir del minuto 20.",
    },
    {
        "pregunta": "¿Qué es la base?",
        "respuesta": "La base es el área protegida con la Tienda, el Nexo y los Inhibidores. Ahí resurges al morir y compras items.",
    },
    {
        "pregunta": "¿Qué es backdoor o BD?",
        "respuesta": "Backdoor es atacar el nexo enemigo sin que el enemigo esté en su base y sin minions de soporte. Estrategia de ninja para cerrar partidas perdidas.",
    },
    {
        "pregunta": "¿Qué significa BG o bad game?",
        "respuesta": "BG significa Bad Game (mal juego). Se dice al final de una partida que estuvo mala o frustrante.",
    },
    {
        "pregunta": "¿Qué es Blind o Ceguera?",
        "respuesta": "Blind es un control de masas que hace que el objetivo falle todos sus autoataques mientras dura el efecto. Teemo es famoso por aplicar Blind.",
    },
    {
        "pregunta": "¿Qué es Blind Pick?",
        "respuesta": "Blind Pick es un modo de selección donde todos eligen campeón al mismo tiempo sin ver lo que pickea el enemigo. El mismo campeón puede estar en ambos equipos.",
    },
    {
        "pregunta": "¿Qué es el buff azul?",
        "respuesta": "El buff azul (Blue Buff) lo da el Gólem Ancestral. Te da regeneración de maná y reducción de enfriamiento. Esencial para magos y junglas.",
    },
    {
        "pregunta": "¿Qué es BotRK?",
        "respuesta": "BotRK (Blade of the Ruined King) es la Espada del Rey Arruinado. Item AD que da robo de vida, velocidad de ataque y daño porcentual de vida.",
    },
    {
        "pregunta": "¿Qué es bot lane?",
        "respuesta": "Bot es el carril inferior, donde van el ADC y el support. También se le dice 'bot' a un campeón controlado por la IA.",
    },
    {
        "pregunta": "¿Qué es BRB?",
        "respuesta": "BRB (Be Right Back) significa 'vuelvo enseguida'. Se usa para avisar al equipo que estás backeando.",
    },
    {
        "pregunta": "¿Qué significa que un campeón está broken?",
        "respuesta": "Broken es cuando un campeón, item o hechizo está desbalanceado y es injustamente fuerte. 'Está broken bro, lo van a nerfear.'",
    },
    {
        "pregunta": "¿Qué es banear o ban?",
        "respuesta": "Banear es bloquear campeones durante el draft para que el enemigo no pueda usarlos. Cada equipo tiene una cantidad limitada de bans por partida.",
    },
    {
        "pregunta": "¿Qué es un bruiser?",
        "respuesta": "Un bruiser es un campeón que combina daño físico fuerte con buena resistencia. Pega duro y aguanta. Ejemplos: Darius, Renekton, Garen.",
    },
    {
        "pregunta": "¿Qué es un brush o arbusto?",
        "respuesta": "Los brushes (bushes) son los arbustos del mapa donde te puedes esconder. Si nadie tiene visión adentro, el enemigo no te ve.",
    },
    {
        "pregunta": "¿Qué es un buff?",
        "respuesta": "Un buff es un efecto positivo aplicado a un campeón (como Azul o Rojo). También se usa cuando Riot mejora un campeón con un parche. Lo opuesto a nerf.",
    },
    {
        "pregunta": "¿Qué es una build?",
        "respuesta": "Una build es el conjunto de items que compras para tu campeón en una partida. Una buena build se adapta al enemigo y a la composición de equipos.",
    },
    {
        "pregunta": "¿Qué es un bug?",
        "respuesta": "Un bug es un defecto no intencional en las mecánicas del juego. Cuando algo no funciona como debería.",
    },
    {
        "pregunta": "¿Qué es burst o daño explosivo?",
        "respuesta": "Burst es una gran cantidad de daño causada en muy poco tiempo, normalmente sobre un solo campeón. Los asesinos viven del burst.",
    },

    # === C ===
    {
        "pregunta": "¿Qué significa care o cuídate?",
        "respuesta": "Care significa 'ten cuidado'. Tu equipo te lo dice cuando hay riesgo de gank o de algún peligro inminente en tu carril.",
    },
    {
        "pregunta": "¿Qué es un carry?",
        "respuesta": "Un carry es un campeón que empieza débil pero se vuelve muy fuerte conforme escala. También 'carrear' = ser quien gana la partida llevando al equipo.",
    },
    {
        "pregunta": "¿Qué es un caster?",
        "respuesta": "Un caster es un campeón cuya principal fuente de daño son sus habilidades, no los autoataques. Puede ser AP o AD.",
    },
    {
        "pregunta": "¿Qué es CC o control de masas?",
        "respuesta": "CC (Crowd Control) son efectos negativos que impiden el movimiento o las acciones del enemigo. Stun, slow, root, taunt, fear, silence, todos son CC.",
    },
    {
        "pregunta": "¿Qué es CD o cooldown?",
        "respuesta": "CD (Cooldown) es el tiempo de enfriamiento de una habilidad ya lanzada antes de poder volver a usarla.",
    },
    {
        "pregunta": "¿Qué es CDR o reducción de enfriamiento?",
        "respuesta": "CDR (Cooldown Reduction) es la estadística que reduce el tiempo de espera de tus habilidades. Tope normalmente al 40%.",
    },
    {
        "pregunta": "¿Qué es chain CC?",
        "respuesta": "Chain CC es encadenar varios efectos de control de masas seguidos sobre el mismo enemigo, sin darle tiempo a reaccionar. Combo letal en teamfights.",
    },
    {
        "pregunta": "¿Qué es channelling o canalizar?",
        "respuesta": "Canalizar es el tiempo que necesita una habilidad para activarse. Puede ser interrumpido por hard CC como un stun. Ejemplo: la R de Katarina.",
    },
    {
        "pregunta": "¿Qué es chase o perseguir?",
        "respuesta": "Chase es perseguir a un enemigo para que retroceda o lograr matarlo. Cuidado con sobre-extenderte chaseando.",
    },
    {
        "pregunta": "¿Qué es collapsing?",
        "respuesta": "Collapsing es cuando los aliados se coordinan para converger sobre un punto y abrumar al equipo enemigo. Típico en objetivos como Drake o Barón.",
    },
    {
        "pregunta": "¿Qué significa commit?",
        "respuesta": "Commit es no retirarse: comprometerse a la pelea hasta que termine o caigas. 'Si voy, voy con todo, commit.'",
    },
    {
        "pregunta": "¿Qué es un counter gank?",
        "respuesta": "Counter gank es responder inmediatamente a un gank enemigo con tu propio gank, anulando la ventaja que ellos podrían sacar.",
    },
    {
        "pregunta": "¿Qué es counter jungle?",
        "respuesta": "Counter jungle es matar los monstruos de la jungla enemiga para privarles de oro, experiencia y buffs.",
    },
    {
        "pregunta": "¿Qué es un counter pick?",
        "respuesta": "Counter pick es elegir un campeón específico durante el draft para hacerle contra a un campeón enemigo. Por ejemplo, pickear Renekton para counterear a Riven.",
    },
    {
        "pregunta": "¿Qué son los creeps?",
        "respuesta": "Creeps es como se le dice a los minions y monstruos neutrales en general. Término heredado de DotA.",
    },
    {
        "pregunta": "¿Qué es CS o creep score?",
        "respuesta": "CS (Creep Score) es la cantidad de minions y monstruos que has matado. Un buen CS es clave para tener farm y escalar bien. 8 CS por minuto es objetivo de pro.",
    },
    {
        "pregunta": "¿Qué es una partida custom?",
        "respuesta": "Custom (Custom Game) es una partida personalizada creada por un jugador, donde tú eliges el mapa, los aliados, enemigos y demás factores.",
    },

    # === D ===
    {
        "pregunta": "¿Qué significa def o defender?",
        "respuesta": "Def es defender: proteger tus torretas o base sin atacar agresivamente. 'Vamos def, los nuestros vienen.'",
    },
    {
        "pregunta": "¿Qué significa DC o desconectado?",
        "respuesta": "DC (Disconnected) es cuando un jugador se desconecta de la partida. Sinónimo de AFK.",
    },
    {
        "pregunta": "¿Qué es un debuff?",
        "respuesta": "Un debuff es un efecto negativo aplicado sobre tu campeón. Lo opuesto a un buff.",
    },
    {
        "pregunta": "¿Qué es deny o zonear?",
        "respuesta": "Deny es eliminar minions aliados o impedir que el rival farmee, evitando que gane oro y experiencia. También se le dice zonear.",
    },
    {
        "pregunta": "¿Qué es un disable?",
        "respuesta": "Un disable es un tipo de CC que previene que el enemigo ejecute acciones específicas. Stun, snare y silence son disables.",
    },
    {
        "pregunta": "¿Qué es hacer dive a la torre?",
        "respuesta": "Dive es perseguir a un enemigo en zona peligrosa, típicamente bajo su torre. Se hace cuando crees que vas a matar antes de que la torre te baje a ti.",
    },
    {
        "pregunta": "¿Qué es dodge?",
        "respuesta": "Dodge tiene dos significados: salir de una selección de campeones antes de que arranque la carga, o esquivar habilidades enemigas (skillshots).",
    },
    {
        "pregunta": "¿Qué es DoT o daño en el tiempo?",
        "respuesta": "DoT (Damage over Time) es daño que se aplica gradualmente a lo largo del tiempo. La ulti de Karthus o el veneno de Cassiopeia son DoT.",
    },
    {
        "pregunta": "¿Qué es un double kill?",
        "respuesta": "Double kill es eliminar a dos enemigos en muy poco tiempo. El anunciador del juego te lo grita en inglés.",
    },
    {
        "pregunta": "¿Qué es DPS?",
        "respuesta": "DPS (Damage Per Second) es el daño por segundo. Un campeón DPS hace daño sostenido constante en lugar de burst.",
    },
    {
        "pregunta": "¿Qué es Draft Pick?",
        "respuesta": "Draft Pick es el modo de selección con bans, donde puedes ver lo que pickea el enemigo y no se pueden repetir campeones entre equipos.",
    },
    {
        "pregunta": "¿Qué es Drake o Dragón?",
        "respuesta": "Drake es el Dragón, monstruo neutral del mapa. Te da buffs permanentes a tu equipo según el elemento (infernal, montaña, océano, nube). Cuatro drakes = forma del alma.",
    },
    {
        "pregunta": "¿Qué es un duellist?",
        "respuesta": "Un duellist es un campeón que destaca en peleas 1v1 contra otros campeones. Fiora, Jax, Camille, Tryndamere son duellists clásicos.",
    },

    # === E ===
    {
        "pregunta": "¿Qué es Elo?",
        "respuesta": "Elo es un rating matemático que mide tu habilidad relativa al resto de jugadores. Determina tu rango y matchmaking.",
    },
    {
        "pregunta": "¿Qué es Elo hell?",
        "respuesta": "Elo hell es un rango bajo del que el jugador siente que no puede salir. Más mito que realidad — si juegas bien, subes.",
    },
    {
        "pregunta": "¿Qué significa que un campeón fue executed o ejecutado?",
        "respuesta": "Executed es una muerte producida por un elemento externo: torre, minions o monstruos neutrales. No otorga oro al equipo enemigo.",
    },
    {
        "pregunta": "¿Qué es exp o experiencia?",
        "respuesta": "Exp son los puntos de experiencia. Subes de nivel matando minions, campeones y monstruos. Llegar a nivel 6 desbloquea tu R.",
    },

    # === F ===
    {
        "pregunta": "¿Qué es face check?",
        "respuesta": "Face check es entrar a un arbusto sin visión a ver si hay enemigo. Acción muy peligrosa — colócate un ward antes.",
    },
    {
        "pregunta": "¿Qué es un fail flash?",
        "respuesta": "Fail flash es usar tu Flash mal: en huida, fallando una pared, o de manera equivocada. Te quedas sin escapatoria con CD de 5 minutos.",
    },
    {
        "pregunta": "¿Qué es farmear?",
        "respuesta": "Farmear es matar minions y monstruos para acumular oro y experiencia. Un buen farm (CS alto) es clave para escalar.",
    },
    {
        "pregunta": "¿Qué es FB o First Blood?",
        "respuesta": "FB (First Blood) es la primera muerte de la partida. Da oro extra a quien la consigue. Un FB temprano puede definir el carril.",
    },
    {
        "pregunta": "¿Qué es Fear o miedo?",
        "respuesta": "Fear es un CC que hace que el objetivo vague descontroladamente sin poder atacar. La pasiva de Fiddlesticks o el W de Hecarim aplican Fear.",
    },
    {
        "pregunta": "¿Qué significa estar feedeado?",
        "respuesta": "Un campeón feedeado es uno que se volvió muy poderoso tras conseguir muchas kills. 'Cuidado con su Vayne, está super feedeada.'",
    },
    {
        "pregunta": "¿Qué es feedear?",
        "respuesta": "Feedear es morir muchas veces dándole oro y experiencia gratis al enemigo. Un jugador que hace esto es un feeder.",
    },
    {
        "pregunta": "¿Qué es un feeder?",
        "respuesta": "Un feeder es un jugador que muere demasiado y le da oro y experiencia gratis al enemigo. 'Fedear' es el verbo.",
    },
    {
        "pregunta": "¿Qué significa FF?",
        "respuesta": "FF se refiere a /ff o forfeit (rendirse). Inicia una votación para terminar la partida antes de que tiren tu nexo.",
    },
    {
        "pregunta": "¿Qué es un fighter?",
        "respuesta": "Fighter (Luchador) es un campeón híbrido entre tanque y daño. Los bruisers entran en esta categoría.",
    },
    {
        "pregunta": "¿Qué es Flash o Destello?",
        "respuesta": "Flash es un hechizo de invocador que te teletransporta una corta distancia hacia donde apuntes. CD de 5 minutos. Hechizo más usado del juego.",
    },
    {
        "pregunta": "¿Qué es focus o focusear?",
        "respuesta": "Focus es dirigir el daño del equipo a un objetivo específico, normalmente al carry enemigo o al más débil, hasta eliminarlo.",
    },
    {
        "pregunta": "¿Qué es la fog of war?",
        "respuesta": "Fog of War (área de sombras) son las zonas oscuras del mapa fuera del rango de visión de tus campeones, minions y estructuras. No ves qué pasa ahí.",
    },
    {
        "pregunta": "¿Qué es un forced teamfight?",
        "respuesta": "Forced teamfight es cuando un equipo va a por un objetivo (como Barón) obligando al rival a pelear para detenerlos.",
    },
    {
        "pregunta": "¿Qué es la fountain o fuente?",
        "respuesta": "La fuente es la plataforma en cada base donde resurges al morir, regeneras vida y maná, y compras items.",
    },
    {
        "pregunta": "¿Qué es freezing o congelar la línea?",
        "respuesta": "Freezing es farmear dando solo el último golpe, manteniendo la oleada cerca de tu torre. Evitas que el enemigo te ganke y obligas a sobre-extenderse.",
    },

    # === G ===
    {
        "pregunta": "¿Qué es game throw o tirar la partida?",
        "respuesta": "Game throw es cuando el equipo que va ganando comete errores y pierde la ventaja, a veces toda la partida. 'No throwees, juega seguro.'",
    },
    {
        "pregunta": "¿Qué es un gank?",
        "respuesta": "Un gank es cuando el junglero (u otro aliado) viene a tu carril a emboscar al enemigo. Es coordinado y normalmente termina en kill o flash.",
    },
    {
        "pregunta": "¿Qué es un gap closer?",
        "respuesta": "Gap closer es una habilidad que cierra distancia rápido con el enemigo. Las dashes de Riven, el Q de Lee Sin, el E de Yasuo son gap closers.",
    },
    {
        "pregunta": "¿Qué significa GG?",
        "respuesta": "GG (Good Game) es 'buen juego'. Se escribe al final de la partida. 'GG WP' = good game well played.",
    },
    {
        "pregunta": "¿Qué es un ghoster?",
        "respuesta": "Ghoster es un jugador que mira el stream de su enemigo en tiempo real para tener ventaja injusta sobre él durante la partida.",
    },
    {
        "pregunta": "¿Qué significa GL o GLHF?",
        "respuesta": "GL = Good Luck (buena suerte). GLHF = Good Luck Have Fun (buena suerte y diviértete). Saludo educado al iniciar la partida.",
    },
    {
        "pregunta": "¿Qué es un glass cannon?",
        "respuesta": "Glass cannon es un campeón o build con mucho daño pero muy poca defensa. Si te alcanzan, mueres rápido, pero pegas durísimo.",
    },
    {
        "pregunta": "¿Qué es una habilidad global?",
        "respuesta": "Una habilidad global es la que puede pegar en cualquier parte del mapa. La Flecha de Ashe, la R de Karthus o el TP son globales.",
    },
    {
        "pregunta": "¿Qué es oro o gold?",
        "respuesta": "El oro es la moneda dentro de la partida. Lo ganas matando minions, campeones, monstruos, torres y por pasivas. Sirve para comprar items.",
    },
    {
        "pregunta": "¿Qué es GP10?",
        "respuesta": "GP10 (Gold per 10) son items, maestrías o runas que generan oro pasivamente cada 10 segundos. Útiles para supports.",
    },

    # === H ===
    {
        "pregunta": "¿Qué es harass o hostigar?",
        "respuesta": "Harass es presionar al rival haciéndole daño constante mientras evitas recibir tú. Lo debilita para forzar un back o setear un kill.",
    },
    {
        "pregunta": "¿Qué es hard CC?",
        "respuesta": "Hard CC es el control de masas que interrumpe canalizaciones de habilidades. Stun, knockup, suprime, taunt, knock-back son hard CC.",
    },
    {
        "pregunta": "¿Qué es hard leash?",
        "respuesta": "Hard leash es ayudar al jungla aliado pegándole fuerte al monstruo del primer buff y dejando que él dé el último golpe.",
    },
    {
        "pregunta": "¿Qué es un hitbox?",
        "respuesta": "Hitbox es la forma invisible alrededor del modelo del campeón que detecta colisiones de habilidades y unidades. Algunos campeones tienen hitbox más grande de lo que parece.",
    },
    {
        "pregunta": "¿Qué significa HF?",
        "respuesta": "HF (Have Fun) es 'diviértete'. Se dice al inicio de la partida junto con GL.",
    },
    {
        "pregunta": "¿Qué significa hold?",
        "respuesta": "Hold es proteger una línea evitando que tiren la torre, normalmente cuando tu aliado de carril no está. Tarea común del jungla.",
    },
    {
        "pregunta": "¿Qué es un hook?",
        "respuesta": "Hook es una habilidad que atrapa al enemigo y lo arrastra hacia ti. El Q de Blitzcrank, el Q de Thresh, el Q de Pyke son hooks famosos.",
    },
    {
        "pregunta": "¿Qué es HP?",
        "respuesta": "HP (Health Points) son los puntos de vida de tu campeón. Cuando llegan a cero, mueres.",
    },
    {
        "pregunta": "¿Qué es un campeón híbrido?",
        "respuesta": "Híbrido es un campeón que escala tanto con AD como con AP, así que puede armarse de varias formas. Jax, Kayle, Akali son híbridos.",
    },
    {
        "pregunta": "¿Qué es un hypercarry?",
        "respuesta": "Hypercarry es un campeón muy débil en early pero brutalmente fuerte en late game si llega bien farmeado. Vayne, Kayle, Kog'Maw, Nasus, Jax son hypercarries.",
    },

    # === I ===
    {
        "pregunta": "¿Qué es Ignite?",
        "respuesta": "Ignite es un hechizo de invocador que aplica daño verdadero al enemigo durante 5 segundos y reduce su curación. Mata residuales y cuenta para FB.",
    },
    {
        "pregunta": "¿Qué significa inc o incoming?",
        "respuesta": "Inc (Incoming) avisa que vienen enemigos hacia tu carril. A diferencia de MIA, te dice la dirección desde la que vienen.",
    },
    {
        "pregunta": "¿Qué es un inhibidor?",
        "respuesta": "Inhibidor (Inhib) es la estructura que impide que el enemigo genere super minions en ese carril. Tirarlos abre la puerta al nexo.",
    },
    {
        "pregunta": "¿Qué es un initiate o iniciador?",
        "respuesta": "Initiate es el campeón que abre la teamfight con su CC o engage. Suele tomar el primer daño. Malphite, Leona, Nautilus son grandes iniciadores.",
    },
    {
        "pregunta": "¿Qué es un instakill o instagib?",
        "respuesta": "Instakill es cuando un campeón con vida llena (o casi) muere por un combo letal de daño en muy poco tiempo, sin posibilidad de reaccionar.",
    },
    {
        "pregunta": "¿Qué es instalock?",
        "respuesta": "Instalock es lockear tu campeón al instante en draft sin escuchar al equipo. Conducta antideportiva, te puede caer un report.",
    },
    {
        "pregunta": "¿Qué es invadir o invade?",
        "respuesta": "Invade es entrar al territorio enemigo, particularmente a su jungla, antes o después del minuto 1. Se hace para robar buffs o hacer FB.",
    },
    {
        "pregunta": "¿Qué es un item u objeto?",
        "respuesta": "Item es un objeto que compras en la tienda para mejorar las estadísticas de tu campeón. Se compran con oro durante la partida.",
    },

    # === J ===
    {
        "pregunta": "¿Qué es juke?",
        "respuesta": "Juke es amagar ir en una dirección para engañar a quien te persigue, normalmente en la jungla aprovechando arbustos. También es esquivar skillshots.",
    },
    {
        "pregunta": "¿Qué es la jungla?",
        "respuesta": "La jungla son los espacios entre los carriles llenos de monstruos neutrales. Es zona del jungler.",
    },
    {
        "pregunta": "¿Qué es un jungler?",
        "respuesta": "Jungler es el campeón que farmea la jungla en lugar de ir a un carril. Su rol es ganar oro/exp matando monstruos neutrales y gankear líneas.",
    },

    # === K ===
    {
        "pregunta": "¿Qué es un kill lane?",
        "respuesta": "Kill lane es la combinación de dos campeones cuyo objetivo es matar al dúo enemigo en bot. Suele juntarse un ADC agresivo con un support iniciador.",
    },
    {
        "pregunta": "¿Qué es killing spree?",
        "respuesta": "Killing spree es matar al menos 3 enemigos consecutivos sin morir. El anunciador te lo grita y la racha sigue subiendo.",
    },
    {
        "pregunta": "¿Qué es el kit de un campeón?",
        "respuesta": "El kit es el set completo de habilidades de un campeón: pasiva, Q, W, E y R.",
    },
    {
        "pregunta": "¿Qué es kitear o kite?",
        "respuesta": "Kitear es alejarte de un enemigo mientras lo atacas continuamente. Le pegas pero él no a ti. Vayne, Kog'Maw, Ashe son kiters.",
    },
    {
        "pregunta": "¿Qué es knockback?",
        "respuesta": "Knockback es empujar al enemigo en la dirección opuesta. El R de Janna o el E de Tristana son knockbacks clásicos.",
    },
    {
        "pregunta": "¿Qué es knockup?",
        "respuesta": "Knockup es lanzar al enemigo por los aires, interrumpiendo cualquier acción. La R de Alistar, el Q de Wukong o el E de Lulu son knockups.",
    },
    {
        "pregunta": "¿Qué es KS o kill steal?",
        "respuesta": "KS (Kill Steal) es robarle la kill a un aliado dando el último golpe. Generalmente molesto pero a veces necesario para asegurar la muerte.",
    },

    # === L ===
    {
        "pregunta": "¿Qué es lag?",
        "respuesta": "Lag es la latencia/retraso entre lo que haces y lo que pasa en pantalla. Causado por mala conexión o servidor lento.",
    },
    {
        "pregunta": "¿Qué es una lane o carril?",
        "respuesta": "Lane es el carril por donde circulan los minions. En la Grieta hay tres: top, mid y bot.",
    },
    {
        "pregunta": "¿Qué es un laner?",
        "respuesta": "Laner es el campeón o jugador que ocupa un carril durante el early game. Top laner, mid laner, bot lane.",
    },
    {
        "pregunta": "¿Qué es la laning phase?",
        "respuesta": "Laning phase es la primera fase de la partida cuando todos están en sus carriles. Termina aproximadamente cuando caen las primeras torres.",
    },
    {
        "pregunta": "¿Qué es last hit?",
        "respuesta": "Last hit es dar el golpe final al minion para conseguir el oro. Si el minion lo mata otro de tus minions, no obtienes oro.",
    },
    {
        "pregunta": "¿Qué es un leaver?",
        "respuesta": "Leaver es alguien que abandona la partida antes de que termine. El sistema Leaver Buster sanciona a los reincidentes.",
    },
    {
        "pregunta": "¿Qué es LS o robo de vida?",
        "respuesta": "LS (Life Steal) es la estadística que te recupera vida según el daño físico que hagas con autoataques. Items como BoTRK o Hidra dan LS.",
    },

    # === M ===
    {
        "pregunta": "¿Qué es el main de un jugador?",
        "respuesta": "Main es el campeón favorito o el que mejor sabe usar un jugador. 'Soy main Yasuo' = juego principalmente Yasuo.",
    },
    {
        "pregunta": "¿Qué es maná?",
        "respuesta": "Maná es el recurso que muchos campeones gastan para usar habilidades. Si te quedas sin maná, no puedes castear.",
    },
    {
        "pregunta": "¿Qué es un campeón manaless?",
        "respuesta": "Manaless es un campeón que no tiene maná. Usan otro recurso como furia (Renekton), energía (Akali) o flujo sanguíneo (Vladimir).",
    },
    {
        "pregunta": "¿Qué es map awareness?",
        "respuesta": "Map awareness es estar atento al minimapa: saber dónde están los enemigos, los timers de los buffs, los movimientos del jungla. Habilidad clave para subir.",
    },
    {
        "pregunta": "¿Qué son los map objectives?",
        "respuesta": "Map objectives son los objetivos del mapa que dan ventaja: dragones, Barón, Heraldo, torres, inhibidores. Quien controla más objetivos suele ganar.",
    },
    {
        "pregunta": "¿Qué es el meta o metagame?",
        "respuesta": "El meta es el estilo de juego dominante en cada parche: qué campeones son fuertes, qué builds se usan, qué composiciones funcionan.",
    },
    {
        "pregunta": "¿Qué es mid lane?",
        "respuesta": "Mid es el carril central de la Grieta. Suele ir un mago o asesino que rotará a otros carriles para crear ventajas.",
    },
    {
        "pregunta": "¿Qué es un minion?",
        "respuesta": "Los minions son las unidades controladas por la IA que salen del nexo en oleadas y avanzan por los carriles atacando a las estructuras y unidades enemigas.",
    },
    {
        "pregunta": "¿Qué significa MIA o SS?",
        "respuesta": "MIA (Missing In Action) o SS significa que el campeón enemigo de tu carril desapareció. Avisa a tu equipo para que se cuide del posible gank.",
    },
    {
        "pregunta": "¿Qué es un marksman o tirador?",
        "respuesta": "Marksman (Tirador) es el campeón que pega daño físico desde lejos con autoataques o proyectiles. Casi todos los ADCs son marksmen.",
    },
    {
        "pregunta": "¿Qué es MOBA?",
        "respuesta": "MOBA (Multiplayer Online Battle Arena) es el género de LoL: combina elementos de RPG y RTS. Dos equipos pelean por destruir la base enemiga.",
    },
    {
        "pregunta": "¿Qué es MR o resistencia mágica?",
        "respuesta": "MR (Magic Resistance) reduce el daño mágico que recibes. Items como Capa de Negatron o Banshee dan MR.",
    },
    {
        "pregunta": "¿Qué es MS o velocidad de movimiento?",
        "respuesta": "MS (Movement Speed) es la velocidad a la que se mueve tu campeón. Botas, Furor, Dancer Espectral aumentan MS.",
    },

    # === N ===
    {
        "pregunta": "¿Qué es un nerf?",
        "respuesta": "Un nerf es una modificación oficial que debilita un campeón, item o hechizo. Lo opuesto a buff. Ocurre cuando algo está roto o demasiado dominante.",
    },
    {
        "pregunta": "¿Qué es el nexo o Nexus?",
        "respuesta": "El Nexo es la estructura primaria de cada base. Cuando lo destruyen, se acaba la partida.",
    },
    {
        "pregunta": "¿Qué significa noob?",
        "respuesta": "Noob es un jugador novato o sin habilidad. Viene de newbie. Sinónimos: nub, n00b. Generalmente se usa como insulto.",
    },
    {
        "pregunta": "¿Qué es un NPC?",
        "respuesta": "NPC (Non-Player Character) es cualquier personaje no controlado por un jugador real. Minions, monstruos y bots son NPCs.",
    },
    {
        "pregunta": "¿Qué es un nuker?",
        "respuesta": "Nuker es un campeón que hace daño mágico masivo con habilidades, normalmente en burst. Annie, Veigar, LeBlanc son nukers.",
    },

    # === O ===
    {
        "pregunta": "¿Qué es un off tank?",
        "respuesta": "Off tank es un campeón que se arma casi como tanque pero lleva al menos un item de daño para no quedar inerte en peleas.",
    },
    {
        "pregunta": "¿Qué significa OMW?",
        "respuesta": "OMW (On My Way) significa 'voy en camino'. Avisa al equipo que te diriges a un objetivo o pelea.",
    },
    {
        "pregunta": "¿Qué significa OOM?",
        "respuesta": "OOM (Out Of Mana) significa que estás sin maná. Avisa para que no se enganchen confiando en tus habilidades.",
    },
    {
        "pregunta": "¿Qué significa OP?",
        "respuesta": "OP (Overpowered) es un campeón demasiado poderoso, ya sea por stats base o por habilidades desproporcionadas. Pide nerf.",
    },

    # === P ===
    {
        "pregunta": "¿Qué es un party?",
        "respuesta": "Party es cuando invitas amigos de tu lista para jugar juntos. Si no completas el grupo, se rellena con jugadores random.",
    },
    {
        "pregunta": "¿Qué es pathing?",
        "respuesta": "Pathing es la ruta que tomarás para llegar a un lugar. Pathing del jungla = el orden en que limpia los campamentos.",
    },
    {
        "pregunta": "¿Qué es PBE?",
        "respuesta": "PBE (Public Beta Environment) es el servidor público donde Riot prueba parches, campeones nuevos y cambios antes de pasarlos al servidor live.",
    },
    {
        "pregunta": "¿Qué es peel o peeling?",
        "respuesta": "Peel es proteger a tus carries de los asesinos enemigos usando CC y posicionamiento. Tarea principal del support en teamfights.",
    },
    {
        "pregunta": "¿Qué es Penta o Pentakill?",
        "respuesta": "Pentakill es eliminar a los 5 campeones enemigos en muy poco tiempo. La kill más prestigiosa del juego. ¡PENTAKILL!",
    },
    {
        "pregunta": "¿Qué es ping?",
        "respuesta": "Ping es la latencia entre tu PC y el servidor del juego, en milisegundos. Bajo ping = respuesta rápida; alto ping = lag.",
    },
    {
        "pregunta": "¿Qué es un Pink Ward?",
        "respuesta": "Pink (Vision Ward o Guardián de Visión Rosa) es un ward que da visión y revela wards y unidades invisibles dentro de su rango. No tiene tiempo límite.",
    },
    {
        "pregunta": "¿Qué es poach?",
        "respuesta": "Poach es robarle monstruos a la jungla enemiga continuamente para dejarlo sin recursos. Versión agresiva del counter jungle.",
    },
    {
        "pregunta": "¿Qué es poke o pokear?",
        "respuesta": "Poke es hostigar al enemigo desde lejos haciéndole daño moderado mientras te mantienes seguro. Lo debilita antes de un compromiso.",
    },
    {
        "pregunta": "¿Qué es positioning o posicionamiento?",
        "respuesta": "Positioning es saber dónde colocarte en una pelea. El tank al frente, el ADC detrás. Mal posicionamiento = mueres rápido.",
    },
    {
        "pregunta": "¿Qué es premade?",
        "respuesta": "Premade es un grupo de jugadores que se conocen y entran juntos al draft. Suelen tener mejor coordinación que solos.",
    },
    {
        "pregunta": "¿Qué es proxy?",
        "respuesta": "Proxy es farmear minions entre las dos torres enemigas para atraer al jungla rival y quitar presión a tus carriles. Singed lo hace muy bien.",
    },
    {
        "pregunta": "¿Qué es push?",
        "respuesta": "Push es avanzar rápido por un carril limpiando minions y empujando contra la torre enemiga. Ganas presión y XP.",
    },

    # === Q ===
    {
        "pregunta": "¿Qué es la habilidad Q?",
        "respuesta": "Q es la primera habilidad de un campeón, asignada por defecto a la tecla Q. Suele ser la skill más usada del kit.",
    },
    {
        "pregunta": "¿Qué significa QQ?",
        "respuesta": "QQ representa un par de ojos llorosos. Se usa para señalar a un jugador quejoso. 'Stop QQ.'",
    },
    {
        "pregunta": "¿Qué es QSS?",
        "respuesta": "QSS (Quicksilver Sash) es el Fajín de Mercurio. Item que se activa para limpiar todos los CC de tu campeón. Esencial vs supresiones (Malzahar, Warwick).",
    },
    {
        "pregunta": "¿Qué es Quadra Kill?",
        "respuesta": "Quadra (Asesinato Cuádruple) es eliminar a 4 enemigos en muy poco tiempo. Un paso antes del codiciado Pentakill.",
    },

    # === R ===
    {
        "pregunta": "¿Qué es la habilidad R?",
        "respuesta": "R es la habilidad ulti del campeón. Es la más poderosa del kit, normalmente con cooldown alto. Se desbloquea a nivel 6.",
    },
    {
        "pregunta": "¿Qué es ragequit?",
        "respuesta": "Ragequit es abandonar la partida con rabia, normalmente después de insultar al equipo. Te puede caer ban.",
    },
    {
        "pregunta": "¿Qué es Recall?",
        "respuesta": "Recall es la habilidad que tienen todos los campeones para teletransportarse a la base canalizando 8 segundos. Se activa con la tecla B.",
    },
    {
        "pregunta": "¿Qué es el buff rojo?",
        "respuesta": "El buff rojo (Blessing of the Lizard Elder) lo da el Lagarto Anciano. Te da daño verdadero adicional y slow en autoataques. Ideal para AD junglers y peleas.",
    },
    {
        "pregunta": "¿Qué es report?",
        "respuesta": "Report es reportar a un jugador al final de la partida por conducta antideportiva. Se revisa y puede acabar en sanción.",
    },
    {
        "pregunta": "¿Qué es el río o river?",
        "respuesta": "El río es el agua que cruza entre los carriles en la Grieta. Ahí están los buffs azul y rojo de cada lado, además de las entradas a la jungla.",
    },
    {
        "pregunta": "¿Qué es un roamer?",
        "respuesta": "Roamer es un campeón que abandona su carril para moverse por el mapa, soporteando, gankeando o presionando objetivos.",
    },
    {
        "pregunta": "¿Qué significa roamear?",
        "respuesta": "Roamear es dejar tu carril para ir a ayudar a otros, normalmente buscando kills o presión en objetivos.",
    },
    {
        "pregunta": "¿Qué es root o snare?",
        "respuesta": "Root (también Snare o Inmovilize) es un CC que impide moverse pero permite atacar y usar habilidades. La E de Morgana o el Q de Lux son roots.",
    },
    {
        "pregunta": "¿Qué es RP?",
        "respuesta": "RP (Riot Points) es la moneda que se compra con dinero real. Sirve para skins, campeones y otros cosméticos.",
    },

    # === S ===
    {
        "pregunta": "¿Qué es scaling?",
        "respuesta": "Scaling es qué tan bien sube de poder un campeón con niveles e items. Vayne tiene scaling brutal; Pantheon tiene scaling pobre.",
    },
    {
        "pregunta": "¿Qué es un shutdown?",
        "respuesta": "Shutdown es matar a un enemigo que viene con muchas kills (killing spree). Te da oro extra y le quita momentum.",
    },
    {
        "pregunta": "¿Qué es Silence?",
        "respuesta": "Silence es un CC que impide al objetivo lanzar habilidades. Solo puede atacar normal. Le quita el kit por unos segundos.",
    },
    {
        "pregunta": "¿Qué es un skillshot?",
        "respuesta": "Skillshot es una habilidad que requiere apuntar, no es target automático. Si fallas, no pega. La Q de Ezreal o la R de Ashe son skillshots.",
    },
    {
        "pregunta": "¿Qué es un skin?",
        "respuesta": "Skin es una apariencia alternativa para un campeón. Solo cosmético, no afecta gameplay. Se compran con RP.",
    },
    {
        "pregunta": "¿Qué es slow?",
        "respuesta": "Slow es un CC que reduce la velocidad de movimiento del enemigo. La W de Nasus, el ataque básico de Ashe, etc.",
    },
    {
        "pregunta": "¿Qué es smart cast?",
        "respuesta": "Smart cast es lanzar una habilidad solo apretando la tecla, sin clic adicional para confirmar. Acelera tu reacción enormemente.",
    },
    {
        "pregunta": "¿Qué es smiteless?",
        "respuesta": "Smiteless es matar el buff azul o rojo sin usar Smite. Permite aprovechar el cooldown de Smite para invadir o robar buffs enemigos.",
    },
    {
        "pregunta": "¿Qué es snowball?",
        "respuesta": "Snowball es cuando un campeón o equipo saca ventaja temprana y la usa para crecer aún más, como una bola de nieve. Se vuelve imparable.",
    },
    {
        "pregunta": "¿Qué es soft CC?",
        "respuesta": "Soft CC son los CC que NO interrumpen canalizaciones de habilidades. Slows y heridas suelen ser soft CC.",
    },
    {
        "pregunta": "¿Qué es solo queue?",
        "respuesta": "Solo queue es entrar a la cola tú solo, sin party. Te emparejan con randoms. Es el modo competitivo principal.",
    },
    {
        "pregunta": "¿Qué es splitpush?",
        "respuesta": "Splitpush es empujar un carril solo mientras tu equipo presiona en otro lado del mapa. Estrategia de dividir la atención del enemigo. Tryndamere y Nasus son grandes splitpushers.",
    },
    {
        "pregunta": "¿Qué significa squishy?",
        "respuesta": "Squishy es un campeón fácil de matar por su poca defensa o vida. Normalmente magos y ADCs.",
    },
    {
        "pregunta": "¿Qué es SR?",
        "respuesta": "SR (Summoner's Rift) es la Grieta del Invocador, el mapa principal de LoL.",
    },
    {
        "pregunta": "¿Qué es stealth o invisibilidad?",
        "respuesta": "Stealth es la capacidad de un campeón de ser invisible al enemigo. Solo wards rosas y habilidades específicas pueden detectarlo.",
    },
    {
        "pregunta": "¿Qué es un steroid?",
        "respuesta": "Steroid es una habilidad que aumenta uno o más stats base de un campeón temporalmente. La Q de Tristana o la W de Tryndamere son steroids.",
    },
    {
        "pregunta": "¿Qué es Stun?",
        "respuesta": "Stun es un CC duro que impide al objetivo moverse, atacar o castear. Es el CC más completo. Annie, Sejuani, Pantheon tienen stuns icónicos.",
    },
    {
        "pregunta": "¿Qué es un summoner o invocador?",
        "respuesta": "Summoner es el rol del jugador. 'Llamas' o invocas a un campeón para usarlo en la batalla. Tu nombre de cuenta es tu summoner name.",
    },
    {
        "pregunta": "¿Qué es un super minion?",
        "respuesta": "Super minion es un minion mucho más fuerte que aparece en la oleada después de destruir un inhibidor enemigo. Pega muy duro a torres y campeones.",
    },
    {
        "pregunta": "¿Qué es un support?",
        "respuesta": "Support es el campeón cuya tarea es proteger y potenciar al equipo. Visión, CC, escudos y heals. Va con el ADC en bot.",
    },
    {
        "pregunta": "¿Qué es Surrender?",
        "respuesta": "Surrender es iniciar votación para rendirse antes de que tiren tu nexo. Se votar con /ff. Necesita mayoría para pasar.",
    },
    {
        "pregunta": "¿Qué es sustain?",
        "respuesta": "Sustain es la capacidad de mantenerte en línea sin volver a base, gracias a robo de vida, regeneración o curaciones. Soraka da mucho sustain.",
    },
    {
        "pregunta": "¿Qué es synergy o sinergia?",
        "respuesta": "Synergy es qué tan bien combinan dos o más campeones. Por ejemplo, Yasuo + Malphite tiene gran sinergia gracias al knockup que detona la R de Yasuo.",
    },

    # === T ===
    {
        "pregunta": "¿Qué es un tank?",
        "respuesta": "Tank es un campeón que aguanta mucho daño. Se arma con vida, armadura y MR. Es el iniciador, pero pega poco. Malphite, Sejuani, Ornn.",
    },
    {
        "pregunta": "¿Qué es taunt?",
        "respuesta": "Taunt es un CC que obliga al enemigo a atacarte a ti, ignorando lo demás. La Q de Shen, la W de Galio aplican taunt.",
    },
    {
        "pregunta": "¿Qué es team comp?",
        "respuesta": "Team comp (composición de equipo) es la combinación de campeones del equipo y el rol que cumple cada uno: poke, engage, hard CC, etc.",
    },
    {
        "pregunta": "¿Qué es un teamfight?",
        "respuesta": "Teamfight es una pelea grupal donde varios campeones de cada bando luchan en la misma área. Quien gane suele tomar objetivos importantes.",
    },
    {
        "pregunta": "¿Qué es Tenacity o Tenacidad?",
        "respuesta": "Tenacity reduce la duración de los CC que recibes. Las botas Mercurial dan Tenacity, vital contra equipos con mucho CC.",
    },
    {
        "pregunta": "¿Qué es TP o Teleport?",
        "respuesta": "TP (Teleport) es el hechizo de invocador que te teletransporta a un ward, minion aliado o estructura. Cooldown largo pero altísimo impacto en mapa.",
    },
    {
        "pregunta": "¿Qué es tower diving?",
        "respuesta": "Tower diving (TD) es perseguir y matar a un enemigo dentro del rango de su torre. Riesgoso, pero a veces vale la pena si tienes tank y daño.",
    },
    {
        "pregunta": "¿Qué es trade o tradeo?",
        "respuesta": "Trade tiene varios sentidos: intercambiar campeones en draft, intercambiar daño en línea, o intercambiar muertes en peleas.",
    },
    {
        "pregunta": "¿Qué es un Triple Kill?",
        "respuesta": "Triple Kill es eliminar a 3 enemigos en poco tiempo. Paso intermedio antes de Quadra y Penta.",
    },
    {
        "pregunta": "¿Qué es un troll?",
        "respuesta": "Troll es un jugador que perturba al equipo o a la comunidad: insulta, deja morir al enemigo, ayuda al rival. Conducta reportable.",
    },
    {
        "pregunta": "¿Qué es TT?",
        "respuesta": "TT (Twisted Treeline) es el Bosque Retorcido, el mapa de 3v3.",
    },
    {
        "pregunta": "¿Qué es una torreta?",
        "respuesta": "Turret (torre/torreta) es la estructura defensiva que protege carriles y base. Pega duro y ataca a quien dañe a tus campeones cerca.",
    },

    # === U ===
    {
        "pregunta": "¿Qué es la ult o ultimate?",
        "respuesta": "Ult (Ultimate) es la habilidad definitiva del campeón, la R. La más poderosa del kit. 'Tira la ulti' = usa la R.",
    },
    {
        "pregunta": "¿Qué significa Unique en items?",
        "respuesta": "Unique es una pasiva o aura de item que no se acumula si compras otro objeto con el mismo efecto. Solo cuenta una vez.",
    },
    {
        "pregunta": "¿Qué significa UP?",
        "respuesta": "UP (Underpowered) es un campeón demasiado débil comparado con la media. Pide buff. Lo opuesto a OP.",
    },
    {
        "pregunta": "¿Qué es una habilidad de utility?",
        "respuesta": "Utility son habilidades que benefician al equipo: escudos, curaciones, slows, heralds, etc. Los supports viven de utility.",
    },

    # === V-Z ===
    {
        "pregunta": "¿Qué es la habilidad W?",
        "respuesta": "W es la segunda habilidad de un campeón, asignada a la tecla W por defecto.",
    },
    {
        "pregunta": "¿Qué es la habilidad E?",
        "respuesta": "E es la tercera habilidad de un campeón, asignada a la tecla E por defecto.",
    },
    {
        "pregunta": "¿Qué es un ward?",
        "respuesta": "Un ward es un objeto que da visión sobre un área pequeña del mapa. Esencial para evitar ganks y controlar objetivos. Pone un ojito en el mapa.",
    },
    {
        "pregunta": "¿Qué es ward bait?",
        "respuesta": "Ward bait es colocar un Pink Ward visible para atraer al enemigo a una trampa cuando intente destruirlo.",
    },
    {
        "pregunta": "¿Qué es ward placement?",
        "respuesta": "Ward placement es saber dónde colocar tus wards para maximizar la visión útil. Habilidad clave que separa supports buenos de malos.",
    },
    {
        "pregunta": "¿Qué es waveclear?",
        "respuesta": "Waveclear es la capacidad de un campeón de limpiar oleadas de minions rápido, ideal para evitar push enemigo o presionar líneas. Ahri, Anivia, Ziggs son waveclear monsters.",
    },
    {
        "pregunta": "¿Qué es un wombo combo?",
        "respuesta": "Wombo combo es cuando un equipo encadena habilidades de forma efectiva sobre el equipo enemigo. Knockup de Malphite + R de Yasuo + R de Miss Fortune = wombo perfecto.",
    },
    {
        "pregunta": "¿Qué significa WP?",
        "respuesta": "WP (Well Played) significa 'bien jugado'. Se dice al final, normalmente acompañado de GG.",
    },
    {
        "pregunta": "¿Qué es un all-in?",
        "respuesta": "All-in es comprometerse totalmente en una pelea con todas tus habilidades y summoners para matar al enemigo. Ir con todo, sin retirada.",
    },
    {
        "pregunta": "¿Qué es zone o zonear?",
        "respuesta": "Zone (zonear) es usar tu posicionamiento o amenazas para impedir que el enemigo gane oro o experiencia. Lo mantienes lejos del minion sin matarlo.",
    },

    # === Estructuras y términos extra ===
    {
        "pregunta": "¿Qué es una wave o oleada?",
        "respuesta": "Una wave es la oleada de minions que avanza por el carril cada cierto tiempo. Limpiar la wave significa matar todos los minions enemigos.",
    },
    {
        "pregunta": "¿Qué es el canon o minion cañonero?",
        "respuesta": "El canon (minion cañonero) es el minion grande que aparece cada varias waves. Da más oro que los minions normales y es prioritario matarlo.",
    },
    {
        "pregunta": "¿Qué son las inner turrets?",
        "respuesta": "Inner turrets son las tres torretas que están justo fuera del perímetro de la base, antes de las nexus turrets.",
    },
    {
        "pregunta": "¿Qué son las outer turrets?",
        "respuesta": "Outer turrets son las tres torretas más alejadas de la base, las primeras de cada carril. Las primeras en caer normalmente.",
    },
    {
        "pregunta": "¿Qué son las nexus turrets?",
        "respuesta": "Nexus turrets son las dos torres que protegen al nexo. Si caen, el nexo está expuesto y a tiro.",
    },
]
