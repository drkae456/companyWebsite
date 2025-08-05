import logging
from django.utils.timezone import now
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from django.urls import reverse
from django.core.cache import cache

logger = logging.getLogger('audit_logger')

class AdminSessionMiddleware(MiddlewareMixin):
    """
    Middleware to manage admin sessions with enhanced security and monitoring
    """
    
    def process_request(self, request):
        user = request.user
        
        # Skip processing for non-authenticated users
        if not user.is_authenticated:
            return None
            
        # Check if this is an admin session
        is_admin_session = request.session.get('is_admin_session', False)
        
        if is_admin_session:
            # Verify admin session integrity
            if not self.verify_admin_session(request):
                return self.terminate_admin_session(request, 'security_violation')
            
            # Check for session timeout
            if self.is_session_expired(request):
                return self.terminate_admin_session(request, 'timeout')
            
            # Update admin session activity
            self.update_admin_session_activity(request)
            
            # Enhanced security checks for admin sessions
            if not self.validate_session_security(request):
                return self.terminate_admin_session(request, 'security_violation')
        
        return None
    
    def verify_admin_session(self, request):
        """Verify the admin session is valid and user still has admin privileges"""
        user = request.user
        
        # Check if user still has admin privileges (staff or superuser treated the same)
        if not user.is_admin_user():
            logger.warning(f"User {user.email} lost admin privileges during session")
            return False
        
        # Verify admin session record exists
        admin_session_id = request.session.get('admin_session_id')
        if admin_session_id:
            try:
                from .models import AdminSession
                admin_session = AdminSession.objects.get(
                    id=admin_session_id,
                    user=user,
                    is_active=True
                )
                return True
            except AdminSession.DoesNotExist:
                logger.warning(f"Admin session record not found for user {user.email}")
                return False
        
        return False
    
    def is_session_expired(self, request):
        """Check if admin session has expired (30 minutes of inactivity)"""
        admin_login_time = request.session.get('admin_login_time')
        if not admin_login_time:
            return True
        
        # Check against AdminSession model timeout
        admin_session_id = request.session.get('admin_session_id')
        if admin_session_id:
            try:
                from .models import AdminSession
                admin_session = AdminSession.objects.get(id=admin_session_id)
                return admin_session.is_expired(timeout_minutes=30)
            except AdminSession.DoesNotExist:
                return True
        
        return True
    
    def validate_session_security(self, request):
        """Validate session security (IP, User-Agent consistency)"""
        # Check IP address consistency
        session_ip = request.session.get('ip_address')
        current_ip = self.get_client_ip(request)
        
        if session_ip and session_ip != current_ip:
            logger.warning(f"Admin session IP mismatch: {session_ip} vs {current_ip}")
            return False
        
        # Check User-Agent consistency
        session_ua = request.session.get('user_agent')
        current_ua = request.META.get('HTTP_USER_AGENT', '')
        
        if session_ua and session_ua != current_ua:
            logger.warning(f"Admin session User-Agent mismatch")
            return False
        
        return True
    
    def update_admin_session_activity(self, request):
        """Update the last activity time for the admin session"""
        admin_session_id = request.session.get('admin_session_id')
        if admin_session_id:
            try:
                from .models import AdminSession
                admin_session = AdminSession.objects.get(id=admin_session_id)
                admin_session.update_activity()
            except AdminSession.DoesNotExist:
                pass
    
    def terminate_admin_session(self, request, reason):
        """Terminate admin session and redirect to login"""
        user = request.user
        
        # Mark admin session as logged out
        admin_session_id = request.session.get('admin_session_id')
        if admin_session_id:
            try:
                from .models import AdminSession
                admin_session = AdminSession.objects.get(id=admin_session_id)
                admin_session.mark_logout(reason=reason)
            except AdminSession.DoesNotExist:
                pass
        
        # Log the session termination
        logger.warning(f"Admin session terminated for {user.email} - Reason: {reason}")
        
        # Clear session and logout
        request.session.flush()
        logout(request)
        
        # Set appropriate message based on reason
        if reason == 'timeout':
            messages.warning(request, 'Your admin session has expired due to inactivity. Please log in again.')
        elif reason == 'security_violation':
            messages.error(request, 'Your admin session was terminated due to security concerns. Please log in again.')
        else:
            messages.info(request, 'Your admin session has ended. Please log in again.')
        
        return redirect('admin_login')
    
    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class AdminSessionSecurityMiddleware(MiddlewareMixin):
    """
    Additional security middleware for admin sessions
    """
    
    def process_request(self, request):
        # Check for admin lockout
        if request.path == reverse('admin_login'):
            client_ip = self.get_client_ip(request)
            if cache.get(f'admin_lockout_{client_ip}'):
                return redirect('rate_limit_exceeded')
        
        return None
    
    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip