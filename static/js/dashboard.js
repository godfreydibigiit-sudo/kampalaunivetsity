// ==========================================
// KIU Result Management System - Dashboard JavaScript
// ==========================================

document.addEventListener('DOMContentLoaded', function() {
    initializeSidebar();
    initializeDashboard();
});

// Sidebar functionality
function initializeSidebar() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
            if (sidebarOverlay) {
                sidebarOverlay.classList.toggle('active');
            }
        });
    }
    
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function() {
            sidebar.classList.remove('active');
            sidebarOverlay.classList.remove('active');
        });
    }
    
    // Close sidebar on window resize (for mobile)
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768 && sidebar) {
            sidebar.classList.remove('active');
            if (sidebarOverlay) {
                sidebarOverlay.classList.remove('active');
            }
        }
    });
}

// Dashboard specific functionality
function initializeDashboard() {
    // Set active nav link based on current page
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath && currentPath.includes(linkPath)) {
            link.classList.add('active');
        }
    });
    
    // Initialize GPA progress bars
    initializeGPAProgress();
}

// GPA progress bar animation
function initializeGPAProgress() {
    const progressBars = document.querySelectorAll('.gpa-progress-bar');
    
    progressBars.forEach(bar => {
        const targetWidth = bar.getAttribute('data-target');
        if (targetWidth) {
            setTimeout(() => {
                bar.style.width = targetWidth + '%';
            }, 100);
        }
    });
}

// Print result slip
function printResult(semesterId) {
    window.open(`/results/download/${semesterId}/`, '_blank');
}

// Confirm action
function confirmAction(message) {
    return confirm(message || 'Are you sure you want to perform this action?');
}