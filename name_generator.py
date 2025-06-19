"""
Name Generator Module

Handles generation and management of unique anonymous names for users.
"""

import random
from typing import Set, Optional, Dict

class NameGenerator:
    def __init__(self):
        """Initialize with a pool of creative anonymous names"""
        self.name_pool = [
            # Animals
            ("Lobo Misterioso", "🐺"), ("Gato Sombra", "🐱"), ("Águila Nocturna", "🦅"), ("Zorro Astuto", "🦊"),
            ("Oso Silencioso", "🐻"), ("Tigre Fantasma", "🐅"), ("León Oculto", "🦁"), ("Puma Secreto", "🐾"),
            ("Halcón Negro", "🦅"), ("Serpiente Sabia", "🐍"), ("Ciervo Veloz", "🦌"), ("Búho Sabio", "🦉"),
            ("Pantera Rosa", "🐆"), ("Delfín Azul", "🐬"), ("Cobra Dorada", "🐍"), ("Jaguar Plateado", "🐯"),
            ("Rana Verde", "🐸"), ("Tortuga Sabia", "🐢"), ("Conejo Rápido", "🐰"), ("Elefante Gris", "🐘"),
            ("Pingüino Frío", "🐧"), ("Koala Dormilón", "🐨"), ("Mono Travieso", "🐵"), ("Hipopótamo Gordo", "🦛"),
            ("Rinoceronte Fuerte", "🦏"), ("Jirafa Alta", "🦒"), ("Cebra Rayada", "🦓"), ("Murciélago Negro", "🦇"),
            
            # Colors + Adjectives
            ("Sombra Violeta", "🌫️"), ("Fuego Esmeralda", "🔥"), ("Hielo Carmesí", "❄️"), ("Rayo Dorado", "⚡"),
            ("Brisa Plateada", "🌬️"), ("Tormenta Azul", "⛈️"), ("Aurora Roja", "🌅"), ("Niebla Gris", "🌫️"),
            ("Cristal Verde", "💎"), ("Viento Negro", "💨"), ("Luna Blanca", "🌙"), ("Sol Naranja", "☀️"),
            ("Estrella Púrpura", "⭐"), ("Mar Turquesa", "🌊"), ("Cielo Rosa", "🌸"), ("Tierra Marrón", "🌍"),
            ("Nube Suave", "☁️"), ("Roca Dura", "🪨"), ("Flor Bella", "🌺"), ("Lluvia Fresca", "🌧️"),
            ("Nevada Blanca", "🌨️"), ("Arcoíris Colorido", "🌈"), ("Cometa Brillante", "☄️"), ("Galaxia Infinita", "🌌"),
            
            # Mystical/Fantasy
            ("Mago Anónimo", "🧙‍♂️"), ("Ninja Silencioso", "🥷"), ("Fantasma Amable", "👻"), ("Espíritu Libre", "🕊️"),
            ("Alma Errante", "👤"), ("Sombra Danzante", "💃"), ("Eco Perdido", "📢"), ("Susurro Nocturno", "🌙"),
            ("Guardián Secreto", "🛡️"), ("Viajero Oculto", "🎒"), ("Ermitaño Sabio", "🧙‍♂️"), ("Nómada Digital", "💻"),
            ("Poeta Invisible", "📝"), ("Soñador Eterno", "💭"), ("Pensador Profundo", "🤔"), ("Observador Callado", "👁️"),
            ("Hechicero Mudo", "🪄"), ("Brujo Verde", "🧙‍♀️"), ("Elfo Perdido", "🧝"), ("Duende Travieso", "🧚"),
            ("Vampiro Nocturno", "🧛"), ("Zombi Amistoso", "🧟"), ("Robot Inteligente", "🤖"), ("Alien Curioso", "👽"),
            
            # Elements
            ("Fuego Danzante", "🔥"), ("Agua Cristalina", "💧"), ("Aire Puro", "🌬️"), ("Tierra Firme", "🌍"),
            ("Rayo Brillante", "⚡"), ("Trueno Lejano", "⛈️"), ("Lluvia Suave", "🌧️"), ("Nieve Blanca", "❄️"),
            ("Volcán Dormido", "🌋"), ("Río Sereno", "🏞️"), ("Montaña Alta", "⛰️"), ("Valle Profundo", "🏔️"),
            ("Lava Caliente", "🌶️"), ("Hielo Frío", "🧊"), ("Arena Dorada", "🏖️"), ("Bosque Verde", "🌲"),
            ("Desierto Seco", "🏜️"), ("Océano Azul", "🌊"), ("Playa Tranquila", "🏝️"), ("Cueva Oscura", "🕳️"),
            
            # Abstract Concepts
            ("Enigma Viviente", "❓"), ("Misterio Andante", "🔍"), ("Secreto Susurrante", "🤫"), ("Incógnita Alegre", "❓"),
            ("Paradoja Sonriente", "🤹"), ("Dilema Danzante", "🤷"), ("Acertijo Amistoso", "🧩"), ("Puzzle Parlante", "🧩"),
            ("Laberinto Mental", "🌀"), ("Código Cifrado", "🔐"), ("Señal Perdida", "📡"), ("Mensaje Oculto", "💌"),
            ("Idea Brillante", "💡"), ("Sueño Profundo", "😴"), ("Memoria Perdida", "🧠"), ("Tiempo Eterno", "⏰"),
            ("Espacio Infinito", "🌌"), ("Silencio Total", "🤐"), ("Caos Ordenado", "🌪️"), ("Paz Interior", "☮️"),
            
            # Professions (Anonymous)
            ("Artista Nocturno", "🎨"), ("Músico Fantasma", "🎵"), ("Escritor Sombra", "✍️"), ("Pintor Invisible", "🖌️"),
            ("Chef Secreto", "👨‍🍳"), ("Jardinero Oculto", "🌱"), ("Arquitecto Misterioso", "🏗️"), ("Piloto Fantasma", "✈️"),
            ("Capitán Anónimo", "⚓"), ("Doctor Invisible", "⚕️"), ("Profesor Secreto", "📚"), ("Inventor Oculto", "🔬"),
            ("Soldado Valiente", "🪖"), ("Bombero Heroico", "🚒"), ("Policía Justo", "👮"), ("Astronauta Perdido", "👨‍🚀"),
            ("Científico Loco", "🥽"), ("Programador Ninja", "👨‍💻"), ("Diseñador Creativo", "🎭"), ("Fotógrafo Oculto", "📸"),
            
            # Time-related
            ("Medianoche Azul", "🌃"), ("Amanecer Dorado", "🌅"), ("Atardecer Rojo", "🌆"), ("Crepúsculo Violeta", "🌇"),
            ("Aurora Boreal", "🌌"), ("Solsticio Verde", "🌞"), ("Equinoccio Gris", "⚖️"), ("Eclipse Negro", "🌑"),
            ("Eternidad Breve", "♾️"), ("Momento Infinito", "⏰"), ("Segundo Eterno", "⏱️"), ("Minuto Mágico", "🎯"),
            ("Hora Perdida", "🕐"), ("Día Gris", "📅"), ("Semana Larga", "📆"), ("Mes Corto", "🗓️"),
            ("Año Nuevo", "🎊"), ("Siglo Pasado", "📜"), ("Futuro Incierto", "🔮"), ("Presente Eterno", "🎁"),
            
            # Nature Elements
            ("Bosque Susurrante", "🌲"), ("Océano Profundo", "🌊"), ("Desierto Infinito", "🏜️"), ("Glaciar Eterno", "🧊"),
            ("Pradera Verde", "🌾"), ("Selva Densa", "🌿"), ("Lago Espejo", "🪞"), ("Cascada Cantarina", "💦"),
            ("Cueva Misteriosa", "🕳️"), ("Isla Perdida", "🏝️"), ("Coral Colorido", "🪸"), ("Arena Dorada", "🏖️"),
            
            # Food & Objects
            ("Pizza Caliente", "🍕"), ("Café Negro", "☕"), ("Helado Frío", "🍦"), ("Taco Sabroso", "🌮"),
            ("Hamburguesa Grande", "🍔"), ("Sushi Fresco", "🍣"), ("Chocolate Dulce", "🍫"), ("Cerveza Fría", "🍺"),
            ("Libro Viejo", "📖"), ("Llave Dorada", "🔑"), ("Espada Brillante", "⚔️"), ("Escudo Fuerte", "🛡️"),
            ("Corona Real", "👑"), ("Anillo Mágico", "💍"), ("Botella Misteriosa", "🍶"), ("Mapa Antiguo", "🗺️"),
            
            # Emotions & Actions
            ("Risa Contagiosa", "😂"), ("Llanto Silencioso", "😭"), ("Abrazo Cálido", "🤗"), ("Beso Dulce", "😘"),
            ("Sonrisa Tímida", "😊"), ("Guiño Travieso", "😉"), ("Salto Alto", "🤸"), ("Baile Loco", "💃"),
            ("Carrera Rápida", "🏃"), ("Caminar Lento", "🚶"), ("Dormir Profundo", "😴"), ("Despertar Temprano", "⏰"),
            
            # Technology & Modern
            ("Wi-Fi Perdido", "📶"), ("Batería Baja", "🔋"), ("Pantalla Rota", "📱"), ("Código Oculto", "💻"),
            ("App Misteriosa", "📲"), ("Chat Secreto", "💬"), ("Email Fantasma", "📧"), ("Video Viral", "📹"),
            ("Meme Divertido", "😂"), ("Selfie Perfecto", "🤳"), ("Like Perdido", "👍"), ("Follow Falso", "👥"),
            
            # Space & Universe
            ("Planeta Azul", "🌍"), ("Estrella Fugaz", "🌠"), ("Luna Llena", "🌕"), ("Sol Brillante", "🌞"),
            ("Meteoro Veloz", "☄️"), ("Satélite Perdido", "🛰️"), ("Cohete Espacial", "🚀"), ("Ovni Misterioso", "🛸"),
            ("Astronauta Solo", "👨‍🚀"), ("Galaxia Lejana", "🌌"), ("Agujero Negro", "🕳️"), ("Big Bang", "💥")
        ]
        
        # Keep track of used names to ensure uniqueness
        self.used_names: Set[str] = set()
        # Store permanent assignments: {user_id: (name, emoji)}
        self.user_assignments: Dict[int, tuple] = {}
    
    def get_unique_name(self, current_used_names: Set[str], user_id: int = None) -> Optional[str]:
        """Get a unique random name or return existing name for user"""
        # Check if user already has an assigned name
        if user_id and user_id in self.user_assignments:
            assigned_name, assigned_emoji = self.user_assignments[user_id]
            return f"{assigned_emoji} {assigned_name}"
        
        # Update internal used names set
        self.used_names = current_used_names.copy()
        
        # Find available names (excluding permanently assigned ones)
        assigned_base_names = {name for name, emoji in self.user_assignments.values()}
        available_names = [
            (name, emoji) for name, emoji in self.name_pool 
            if f"{emoji} {name}" not in self.used_names and name not in assigned_base_names
        ]
        
        if not available_names:
            return None
        
        # Select random name from available ones
        selected_name, selected_emoji = random.choice(available_names)
        full_name = f"{selected_emoji} {selected_name}"
        
        # Store permanent assignment for this user
        if user_id:
            self.user_assignments[user_id] = (selected_name, selected_emoji)
        
        self.used_names.add(full_name)
        return full_name
    
    def release_name(self, name: str, user_id: int = None) -> None:
        """Release a name back to the available pool (but keep permanent assignment)"""
        if name in self.used_names:
            self.used_names.remove(name)
    
    def get_available_count(self) -> int:
        """Get the number of available names"""
        return len(self.name_pool) - len(self.used_names)
    
    def get_total_count(self) -> int:
        """Get the total number of names in the pool"""
        return len(self.name_pool)
    
    def is_name_valid(self, name: str) -> bool:
        """Check if a name exists in the name pool"""
        for base_name, emoji in self.name_pool:
            if f"{emoji} {base_name}" == name or base_name == name:
                return True
        return False
    
    def get_user_assignment(self, user_id: int) -> Optional[tuple]:
        """Get the permanent name assignment for a user"""
        return self.user_assignments.get(user_id)
    
    def remove_permanent_assignment(self, user_id: int) -> bool:
        """Remove permanent assignment for a user (for admin actions)"""
        if user_id in self.user_assignments:
            del self.user_assignments[user_id]
            return True
        return False