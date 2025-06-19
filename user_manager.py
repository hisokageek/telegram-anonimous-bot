"""
User Manager Module

Handles user session management, tracking active users and their anonymous names.
"""

from typing import Dict, Set, Optional
import time

class UserManager:
    def __init__(self):
        """Initialize user manager with empty user registry"""
        # Structure: {user_id: {'chat_id': int, 'name': str, 'joined_at': float}}
        self.active_users: Dict[int, Dict] = {}
    
    def add_user(self, user_id: int, chat_id: int, anonymous_name: str) -> bool:
        """
        Add a user to the active users registry
        
        Args:
            user_id: Telegram user ID
            chat_id: Telegram chat ID
            anonymous_name: Assigned anonymous name
            
        Returns:
            True if user was added successfully, False if already exists
        """
        if user_id in self.active_users:
            return False
        
        self.active_users[user_id] = {
            'chat_id': chat_id,
            'name': anonymous_name,
            'joined_at': time.time()
        }
        
        return True
    
    def remove_user(self, user_id: int) -> bool:
        """
        Remove a user from the active users registry
        
        Args:
            user_id: Telegram user ID to remove
            
        Returns:
            True if user was removed, False if user wasn't found
        """
        if user_id in self.active_users:
            del self.active_users[user_id]
            return True
        return False
    
    def is_user_active(self, user_id: int) -> bool:
        """
        Check if a user is currently active in the anonymous group
        
        Args:
            user_id: Telegram user ID to check
            
        Returns:
            True if user is active, False otherwise
        """
        return user_id in self.active_users
    
    def get_user_name(self, user_id: int) -> Optional[str]:
        """
        Get the anonymous name of a user
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Anonymous name of the user or None if user not found
        """
        user_info = self.active_users.get(user_id)
        return user_info['name'] if user_info else None
    
    def get_user_chat_id(self, user_id: int) -> Optional[int]:
        """
        Get the chat ID of a user
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Chat ID of the user or None if user not found
        """
        user_info = self.active_users.get(user_id)
        return user_info['chat_id'] if user_info else None
    
    def get_active_users(self) -> Dict[int, Dict]:
        """
        Get all active users
        
        Returns:
            Dictionary of all active users with their information
        """
        return self.active_users.copy()
    
    def get_used_names(self) -> Set[str]:
        """
        Get all currently used anonymous names
        
        Returns:
            Set of all anonymous names currently in use
        """
        return {user_info['name'] for user_info in self.active_users.values()}
    
    def get_active_user_count(self) -> int:
        """
        Get the number of active users
        
        Returns:
            Number of users currently active in the anonymous group
        """
        return len(self.active_users)
    
    def get_user_by_name(self, anonymous_name: str) -> Optional[int]:
        """
        Get user ID by anonymous name
        
        Args:
            anonymous_name: The anonymous name to search for
            
        Returns:
            User ID if found, None otherwise
        """
        for user_id, user_info in self.active_users.items():
            if user_info['name'] == anonymous_name:
                return user_id
        return None
    
    def get_users_joined_since(self, timestamp: float) -> Dict[int, Dict]:
        """
        Get users who joined after a specific timestamp
        
        Args:
            timestamp: Unix timestamp to filter by
            
        Returns:
            Dictionary of users who joined after the timestamp
        """
        return {
            user_id: user_info 
            for user_id, user_info in self.active_users.items()
            if user_info['joined_at'] > timestamp
        }
    
    def cleanup_user(self, user_id: int) -> Optional[str]:
        """
        Clean up a user and return their anonymous name for cleanup
        
        Args:
            user_id: User ID to clean up
            
        Returns:
            The anonymous name that was freed up, or None if user wasn't found
        """
        if user_id in self.active_users:
            anonymous_name = self.active_users[user_id]['name']
            del self.active_users[user_id]
            return anonymous_name
        return None
    
    def get_user_info(self, user_id: int) -> Optional[Dict]:
        """
        Get complete information about a user
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            User information dictionary or None if not found
        """
        return self.active_users.get(user_id)
    
    def clear_all_users(self) -> int:
        """
        Remove all users (for cleanup purposes)
        
        Returns:
            Number of users that were removed
        """
        count = len(self.active_users)
        self.active_users.clear()
        return count
