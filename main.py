"""
Telegram Anonymous Group Chat Bot - Render Version

A bot that creates an anonymous group chat where users are assigned
random unique names and can chat without revealing their identities.
"""

import os
import logging
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from name_generator import NameGenerator  
from user_manager import UserManager

# Para Render - servidor web simple
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import json

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Handler para mantener activo en Render
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'active',
                'service': 'telegram-anonymous-bot',
                'timestamp': time.time()
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Silenciar logs del servidor HTTP
        pass

class AnonymousChatBot:
    def __init__(self):
        """Initialize the bot with token from environment variable"""
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        
        # Initialize components
        self.name_generator = NameGenerator()
        self.user_manager = UserManager()
        
        # Admin configuration
        admin_id = os.getenv('ADMIN_USER_ID')
        self.admin_user_id = int(admin_id) if admin_id else None
        
        # Create application
        self.application = Application.builder().token(self.token).build()
        
        # Iniciar servidor HTTP para Render
        self.start_health_server()
        
        # Setup handlers
        self.setup_handlers()
    
    def start_health_server(self):
        """Iniciar servidor HTTP para health checks de Render"""
        def run_server():
            port = int(os.getenv('PORT', 8000))
            server = HTTPServer(('0.0.0.0', port), HealthHandler)
            logging.info(f"Health server starting on port {port}")
            server.serve_forever()
        
        # Ejecutar servidor en hilo separado
        health_thread = threading.Thread(target=run_server, daemon=True)
        health_thread.start()
    
    def setup_handlers(self):
        """Setup all command and message handlers"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("leave", self.leave_command))
        self.application.add_handler(CommandHandler("users", self.users_command))
        self.application.add_handler(CommandHandler("admin", self.admin_command))
        self.application.add_handler(CommandHandler("realusers", self.real_users_command))
        self.application.add_handler(CommandHandler("kickuser", self.kick_user_command))
        self.application.add_handler(CommandHandler("resetuser", self.reset_user_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command - join the anonymous group"""
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        
        # Check if user is already in the group
        if self.user_manager.is_user_active(user_id):
            current_name = self.user_manager.get_user_name(user_id)
            await update.message.reply_text(
                f"Ya estás en el grupo anónimo como: {current_name}\n"
                f"Envía un mensaje y se retransmitirá a todos los miembros."
            )
            return
        
        # Get current used names
        used_names = self.user_manager.get_used_names()
        
        # Try to get a unique name
        anonymous_name = self.name_generator.get_unique_name(used_names, user_id)
        
        if not anonymous_name:
            await update.message.reply_text(
                "❌ Lo siento, no hay nombres disponibles en este momento. "
                "Intenta de nuevo más tarde."
            )
            return
        
        # Add user to the group
        success = self.user_manager.add_user(user_id, chat_id, anonymous_name)
        
        if success:
            await update.message.reply_text(
                f"🎭 ¡Bienvenido al grupo anónimo!\n\n"
                f"Tu identidad anónima es: **{anonymous_name}**\n\n"
                f"Ahora puedes enviar mensajes y se retransmitirán a todos los miembros "
                f"del grupo con tu nombre anónimo.\n\n"
                f"Comandos disponibles:\n"
                f"• /users - Ver usuarios conectados\n"
                f"• /leave - Salir del grupo\n"
                f"• Envía cualquier mensaje para chatear"
            )
            
            # Notify other users
            notification = f"📢 {anonymous_name} se ha unido al grupo anónimo"
            await self.broadcast_message(notification, exclude_user_id=user_id)
        else:
            await update.message.reply_text(
                "❌ Error al unirte al grupo. Intenta de nuevo."
            )

    async def leave_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /leave command - leave the anonymous group"""
        user_id = update.effective_user.id
        
        if not self.user_manager.is_user_active(user_id):
            await update.message.reply_text(
                "❌ No estás en el grupo anónimo. Usa /start para unirte."
            )
            return
        
        # Get user's anonymous name before removing
        anonymous_name = self.user_manager.get_user_name(user_id)
        
        # Remove user from the group
        success = self.user_manager.remove_user(user_id)
        
        if success:
            # Release the name back to the pool (but keep permanent assignment)
            self.name_generator.release_name(anonymous_name, user_id)
            
            await update.message.reply_text(
                f"👋 Has salido del grupo anónimo.\n"
                f"Usa /start para volver a unirte cuando quieras."
            )
            
            # Notify other users
            notification = f"📢 {anonymous_name} ha salido del grupo anónimo"
            await self.broadcast_message(notification, exclude_user_id=user_id)
        else:
            await update.message.reply_text("❌ Error al salir del grupo.")

    async def users_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /users command - show connected users"""
        user_id = update.effective_user.id
        
        if not self.user_manager.is_user_active(user_id):
            await update.message.reply_text(
                "❌ Debes estar en el grupo para ver esta información. Usa /start para unirte."
            )
            return
        
        active_users = self.user_manager.get_active_users()
        user_count = len(active_users)
        
        if user_count == 0:
            await update.message.reply_text("👥 No hay usuarios conectados.")
            return
        
        # Create list of anonymous names
        user_list = []
        for uid, user_info in active_users.items():
            user_list.append(f"• {user_info['name']}")
        
        users_text = "\n".join(user_list)
        
        await update.message.reply_text(
            f"👥 **Usuarios conectados ({user_count}):**\n\n{users_text}"
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle regular messages - broadcast to all users anonymously"""
        user_id = update.effective_user.id
        message_text = update.message.text
        
        # Check if user is in the anonymous group
        if not self.user_manager.is_user_active(user_id):
            await update.message.reply_text(
                "❌ Debes unirte al grupo anónimo primero.\n"
                "Usa /start para comenzar."
            )
            return
        
        # Get user's anonymous name
        anonymous_name = self.user_manager.get_user_name(user_id)
        
        # Format the message
        formatted_message = f"{anonymous_name}: {message_text}"
        
        # Broadcast to all users except the sender
        broadcast_count = await self.broadcast_message(formatted_message, exclude_user_id=user_id)
        
        # Confirm message sent
        await update.message.reply_text(
            f"✅ Mensaje enviado como {anonymous_name} a {broadcast_count} usuario(s)"
        )

    async def broadcast_message(self, message: str, exclude_user_id: int = None) -> int:
        """Broadcast a message to all active users except the excluded one"""
        active_users = self.user_manager.get_active_users()
        sent_count = 0
        
        for user_id, user_info in active_users.items():
            # Skip the excluded user
            if exclude_user_id and user_id == exclude_user_id:
                continue
            
            try:
                await self.application.bot.send_message(
                    chat_id=user_info['chat_id'],
                    text=message
                )
                sent_count += 1
            except Exception as e:
                logger.warning(f"Failed to send message to user {user_id}: {e}")
                # Optionally remove user if they blocked the bot
                # self.user_manager.remove_user(user_id)
        
        return sent_count

    def is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        return self.admin_user_id is not None and user_id == self.admin_user_id

    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /admin command - show admin panel"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ No tienes permisos de administrador.")
            return
        
        active_users = self.user_manager.get_active_users()
        total_names = self.name_generator.get_total_count()
        available_names = self.name_generator.get_available_count()
        
        admin_text = (
            f"🔧 **Panel de Administrador**\n\n"
            f"👥 Usuarios activos: {len(active_users)}\n"
            f"🎭 Nombres disponibles: {available_names}/{total_names}\n\n"
            f"**Comandos de admin:**\n"
            f"• /realusers - Ver información real de usuarios\n"
            f"• /kickuser [nombre] - Expulsar usuario por nombre anónimo\n"
            f"• /resetuser [nombre] - Resetear asignación permanente"
        )
        
        await update.message.reply_text(admin_text)

    async def real_users_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /realusers command - show real user information"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ No tienes permisos de administrador.")
            return
        
        active_users = self.user_manager.get_active_users()
        
        if not active_users:
            await update.message.reply_text("👥 No hay usuarios activos.")
            return
        
        user_list = []
        for uid, user_info in active_users.items():
            user_list.append(
                f"• {user_info['name']}\n"
                f"  ID: {uid}\n"
                f"  Unido: {time.strftime('%Y-%m-%d %H:%M', time.localtime(user_info['joined_at']))}"
            )
        
        users_text = "\n\n".join(user_list)
        
        await update.message.reply_text(
            f"🔍 **Información real de usuarios:**\n\n{users_text}"
        )

    async def kick_user_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /kickuser command - kick user by anonymous name"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ No tienes permisos de administrador.")
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /kickuser [nombre_anónimo]\n"
                "Ejemplo: /kickuser 🐺🌙 Lobo Misterioso"
            )
            return
        
        target_name = " ".join(context.args)
        target_user_id = self.user_manager.get_user_by_name(target_name)
        
        if not target_user_id:
            await update.message.reply_text(f"❌ Usuario '{target_name}' no encontrado.")
            return
        
        # Remove user
        success = self.user_manager.remove_user(target_user_id)
        
        if success:
            # Release name
            self.name_generator.release_name(target_name, target_user_id)
            
            # Notify admin
            await update.message.reply_text(f"✅ Usuario '{target_name}' expulsado del grupo.")
            
            # Notify user
            try:
                target_chat_id = self.user_manager.get_user_chat_id(target_user_id)
                if target_chat_id:
                    await self.application.bot.send_message(
                        chat_id=target_chat_id,
                        text="❌ Has sido expulsado del grupo anónimo por un administrador."
                    )
            except Exception as e:
                logger.warning(f"Could not notify kicked user: {e}")
            
            # Notify group
            await self.broadcast_message(f"📢 {target_name} ha sido expulsado del grupo")
        else:
            await update.message.reply_text("❌ Error al expulsar usuario.")

    async def reset_user_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /resetuser command - reset permanent name assignment"""
        user_id = update.effective_user.id
        
        if not self.is_admin(user_id):
            await update.message.reply_text("❌ No tienes permisos de administrador.")
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ Uso: /resetuser [nombre_anónimo]\n"
                "Ejemplo: /resetuser 🐺🌙 Lobo Misterioso"
            )
            return
        
        target_name = " ".join(context.args)
        target_user_id = self.user_manager.get_user_by_name(target_name)
        
        if not target_user_id:
            await update.message.reply_text(f"❌ Usuario '{target_name}' no encontrado.")
            return
        
        # Reset permanent assignment
        reset_success = self.name_generator.remove_permanent_assignment(target_user_id)
        
        if reset_success:
            await update.message.reply_text(
                f"✅ Asignación permanente resetada para '{target_name}'.\n"
                f"La próxima vez que se una, recibirá un nombre diferente."
            )
        else:
            await update.message.reply_text(f"❌ No se encontró asignación permanente para '{target_name}'.")

    def run(self):
        """Start the bot"""
        # Start the bot
        logging.info("Starting Anonymous Chat Bot for Render...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function"""
    try:
        bot = AnonymousChatBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    main()