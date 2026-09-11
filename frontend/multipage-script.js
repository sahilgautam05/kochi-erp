// Sidebar interactive toggle
document.addEventListener('DOMContentLoaded', function() {
    var sidebar = document.getElementById('sidebar');
    var sidebarToggle = document.getElementById('sidebar-toggle');
    var sidebarToggleIcon = document.getElementById('sidebar-toggle-icon');
    var mainContent = document.querySelector('.main-content.with-sidebar');
    if (sidebar && sidebarToggle && sidebarToggleIcon && mainContent) {
        sidebarToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            sidebar.classList.toggle('collapsed');
            mainContent.classList.toggle('collapsed');
            if (sidebar.classList.contains('collapsed')) {
                sidebarToggleIcon.className = 'fas fa-angle-double-right';
            } else {
                sidebarToggleIcon.className = 'fas fa-angle-double-left';
            }
        });
    }
});
// Sidebar dropdown toggle
document.addEventListener('DOMContentLoaded', function() {
    var sidebarDropdown = document.querySelector('.sidebar-dropdown');
    if (sidebarDropdown) {
        var toggleBtn = sidebarDropdown.querySelector('.dropdown-toggle');
        var dropdownContent = sidebarDropdown.querySelector('.sidebar-dropdown-content');
        toggleBtn.addEventListener('click', function() {
            sidebarDropdown.classList.toggle('open');
        });
        // Optional: close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!sidebarDropdown.contains(e.target)) {
                sidebarDropdown.classList.remove('open');
            }
        });
    }
});
/**
 * Multi-Page Kochi Metro Rail Management System
 * Simplified JavaScript for multi-page navigation
 * Author: Metro Rail Development Team
 * Version: 2.0.0
 */

'use strict';

// ===== GLOBAL VARIABLES =====
let currentSlide = 0;
let slideInterval;

// ===== APPLICATION INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    try {
        // Core functionality
        initializeSlideshow();
        initializeNavigation();
        initializeModals();
        initializeNotifications();
        initializeUserProfile();
        initializeThemeToggle();
        initializeLiveMap();
        initializeTrainOperations();
        initializeVerifyOperations();
        
        // Update time if element exists
        updateCurrentTime();
        setInterval(updateCurrentTime, 60000);
        
        console.log('Kochi Metro Management System initialized successfully');
    } catch (error) {
        console.error('Error initializing application:', error);
        showErrorMessage('Failed to initialize application. Please refresh the page.');
    }
}

// ===== SLIDESHOW FUNCTIONALITY =====
/**
 * Initialize hero slideshow (only on dashboard)
 */
function initializeSlideshow() {
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');
    const prevBtn = document.getElementById('prev-slide');
    const nextBtn = document.getElementById('next-slide');
    const slideshowContainer = document.querySelector('.slideshow-container');
    
    if (slides.length === 0) return; // Not on dashboard page
    
    // Auto-rotate slides
    slideInterval = setInterval(nextSlide, 6000);
    
    // Navigation buttons
    if (prevBtn) prevBtn.addEventListener('click', prevSlide);
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);
    
    // Dot navigation
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => goToSlide(index));
    });
    
    // Pause on hover
    if (slideshowContainer) {
        slideshowContainer.addEventListener('mouseenter', pauseSlideshow);
        slideshowContainer.addEventListener('mouseleave', resumeSlideshow);
    }
    
    // Touch support
    initializeTouchSupport(slideshowContainer);
}

function initializeTouchSupport(container) {
    if (!container) return;
    
    let startX = 0;
    let endX = 0;
    
    container.addEventListener('touchstart', (e) => {
        startX = e.touches[0].clientX;
    }, { passive: true });
    
    container.addEventListener('touchend', (e) => {
        endX = e.changedTouches[0].clientX;
        const deltaX = endX - startX;
        const minSwipeDistance = 50;
        
        if (Math.abs(deltaX) > minSwipeDistance) {
            if (deltaX > 0) {
                prevSlide();
            } else {
                nextSlide();
            }
        }
    }, { passive: true });
}

function nextSlide() {
    const slides = document.querySelectorAll('.slide');
    if (!slides || slides.length === 0) return;
    
    currentSlide = (currentSlide + 1) % slides.length;
    updateSlideshow();
}

function prevSlide() {
    const slides = document.querySelectorAll('.slide');
    if (!slides || slides.length === 0) return;
    
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    updateSlideshow();
}

function goToSlide(index) {
    const slides = document.querySelectorAll('.slide');
    if (!slides || slides.length === 0 || index < 0 || index >= slides.length) return;
    
    currentSlide = index;
    updateSlideshow();
}

function updateSlideshow() {
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');
    
    if (!slides || slides.length === 0) return;
    
    slides.forEach((slide, index) => {
        slide.classList.toggle('active', index === currentSlide);
    });
    
    if (dots && dots.length > 0) {
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentSlide);
        });
    }
}

function pauseSlideshow() {
    if (slideInterval) {
        clearInterval(slideInterval);
    }
}

function resumeSlideshow() {
    if (slideInterval) {
        clearInterval(slideInterval);
    }
    slideInterval = setInterval(nextSlide, 6000);
}

// ===== NAVIGATION FUNCTIONALITY =====
/**
 * Initialize navigation
 */
function initializeNavigation() {
    // Mobile menu toggle
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const mobileNav = document.getElementById('mobile-nav');
    
    if (mobileMenuToggle && mobileNav) {
        mobileMenuToggle.addEventListener('click', () => {
            const isOpen = mobileNav.classList.contains('show');
            mobileNav.classList.toggle('show');
            mobileMenuToggle.setAttribute('aria-expanded', !isOpen);
            
            const icon = mobileMenuToggle.querySelector('i');
            if (icon) {
                icon.className = mobileNav.classList.contains('show') ? 'fas fa-times' : 'fas fa-bars';
            }
        });
    }
    
    // Dropdown functionality
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            const dropdown = toggle.closest('.nav-dropdown');
            const isOpen = dropdown.classList.contains('show');
            
            // Close all dropdowns
            document.querySelectorAll('.nav-dropdown').forEach(d => d.classList.remove('show'));
            
            // Toggle current dropdown
            if (!isOpen) {
                dropdown.classList.add('show');
                toggle.setAttribute('aria-expanded', 'true');
            } else {
                toggle.setAttribute('aria-expanded', 'false');
            }
        });
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', () => {
        document.querySelectorAll('.nav-dropdown').forEach(dropdown => {
            dropdown.classList.remove('show');
            const toggle = dropdown.querySelector('.dropdown-toggle');
            if (toggle) toggle.setAttribute('aria-expanded', 'false');
        });
        closeMobileMenu();
    });
    
    // Emergency button
    const emergencyBtn = document.getElementById('emergency-btn');
    if (emergencyBtn) {
        emergencyBtn.addEventListener('click', showEmergencyContacts);
    }
}

function closeMobileMenu() {
    const mobileNav = document.getElementById('mobile-nav');
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    
    if (mobileNav) {
        mobileNav.classList.remove('show');
    }
    
    if (mobileMenuToggle) {
        mobileMenuToggle.setAttribute('aria-expanded', 'false');
        const icon = mobileMenuToggle.querySelector('i');
        if (icon) {
            icon.className = 'fas fa-bars';
        }
    }
}

// ===== MODAL FUNCTIONALITY =====
/**
 * Initialize modals
 */
function initializeModals() {
    // Add Train Modal
    const addTrainBtn = document.getElementById('add-train-btn');
    const addTrainModal = document.getElementById('add-train-modal');
    const addTrainModalClose = document.getElementById('add-train-modal-close');
    const cancelAddTrain = document.getElementById('cancel-add-train');
    const submitTrain = document.getElementById('submit-train');
    
    if (addTrainBtn) addTrainBtn.addEventListener('click', () => showModal('add-train-modal'));
    if (addTrainModalClose) addTrainModalClose.addEventListener('click', () => hideModal('add-train-modal'));
    if (cancelAddTrain) cancelAddTrain.addEventListener('click', () => hideModal('add-train-modal'));
    
    if (submitTrain) {
        submitTrain.addEventListener('click', () => {
            const trainId = document.getElementById('train-id')?.value;
            const trainDriver = document.getElementById('train-driver')?.value;
            const trainRoute = document.getElementById('train-route')?.value;
            
            if (trainId && trainDriver && trainRoute) {
                hideModal('add-train-modal');
                showSuccessMessage(`Train ${trainId} added successfully!`);
                const form = document.getElementById('add-train-form');
                if (form) form.reset();
            } else {
                showErrorMessage('Please fill in all required fields.');
            }
        });
    }
    
    // Verification Modal
    const verificationModal = document.getElementById('verification-modal');
    const verificationModalClose = document.getElementById('verification-modal-close');
    const cancelVerification = document.getElementById('cancel-verification');
    const confirmVerification = document.getElementById('confirm-verification');
    
    if (verificationModalClose) verificationModalClose.addEventListener('click', () => hideModal('verification-modal'));
    if (cancelVerification) cancelVerification.addEventListener('click', () => hideModal('verification-modal'));
    
    if (confirmVerification) {
        confirmVerification.addEventListener('click', () => {
            hideModal('verification-modal');
            showSuccessMessage('Operations verified successfully!');
        });
    }
    
    // Close modals when clicking outside
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            hideModal(e.target.id);
        }
    });
    
    // Close modals with ESC key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                hideModal(openModal.id);
            }
        }
    });
}

function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        
        const focusableElements = modal.querySelectorAll('button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
        if (focusableElements.length > 0) {
            focusableElements[0].focus();
        }
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('show');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }
}

// ===== NOTIFICATION FUNCTIONALITY =====
/**
 * Initialize notifications
 */
function initializeNotifications() {
    const notificationBtn = document.getElementById('notification-btn');
    const notificationDropdown = document.getElementById('notification-dropdown');
    const profileBtn = document.getElementById('profile-btn');
    const profileDropdown = document.getElementById('profile-dropdown');
    const logoutBtn = document.getElementById('logout-btn');
    const mobileLogoutBtn = document.getElementById('mobile-logout-btn');
    
    if (notificationBtn && notificationDropdown) {
        notificationBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isOpen = notificationDropdown.classList.contains('show');
            
            // Close profile dropdown
            if (profileDropdown) profileDropdown.classList.remove('show');
            if (profileBtn) profileBtn.classList.remove('active');
            
            // Toggle notification dropdown
            if (!isOpen) {
                notificationDropdown.classList.add('show');
                notificationBtn.setAttribute('aria-expanded', 'true');
            } else {
                notificationDropdown.classList.remove('show');
                notificationBtn.setAttribute('aria-expanded', 'false');
            }
        });
    }
    
    if (profileBtn && profileDropdown) {
        profileBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            const isOpen = profileDropdown.classList.contains('show');
            
            // Close notification dropdown
            if (notificationDropdown) notificationDropdown.classList.remove('show');
            if (notificationBtn) notificationBtn.setAttribute('aria-expanded', 'false');
            
            // Toggle profile dropdown
            if (!isOpen) {
                profileDropdown.classList.add('show');
                profileBtn.classList.add('active');
                profileBtn.setAttribute('aria-expanded', 'true');
            } else {
                profileDropdown.classList.remove('show');
                profileBtn.classList.remove('active');
                profileBtn.setAttribute('aria-expanded', 'false');
            }
        });
    }
    
    // Logout functionality
    if (logoutBtn) logoutBtn.addEventListener('click', handleLogout);
    if (mobileLogoutBtn) mobileLogoutBtn.addEventListener('click', handleLogout);
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', () => {
        if (notificationDropdown) {
            notificationDropdown.classList.remove('show');
            if (notificationBtn) notificationBtn.setAttribute('aria-expanded', 'false');
        }
        if (profileDropdown) {
            profileDropdown.classList.remove('show');
            if (profileBtn) {
                profileBtn.classList.remove('active');
                profileBtn.setAttribute('aria-expanded', 'false');
            }
        }
    });
}

function handleLogout() {
    if (confirm('Are you sure you want to log out?')) {
        localStorage.clear();
        sessionStorage.clear();
        showSuccessMessage('Logged out successfully');
        setTimeout(() => {
        window.location.href = 'index.html';
        }, 1500);
    }
}

// ===== USER PROFILE & MODAL FUNCTIONALITY =====
const DEFAULT_USER_PROFILE = {
    name: "Sahil Gautam",
    username: "admin",
    email: "sahil2312056@akgec.ac.in",
    role: "admin",
    department: "Operations Management",
    designation: "System Administrator",
    phone: "+91 98470 12345",
    avatar: "https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg?auto=compress&cs=tinysrgb&w=96&h=96&fit=crop&crop=face"
};

function getActiveUserProfile() {
    try {
        const stored = localStorage.getItem('kmrl_current_user');
        if (stored) {
            const parsed = JSON.parse(stored);
            if (parsed && typeof parsed === 'object') {
                return Object.assign({}, DEFAULT_USER_PROFILE, parsed);
            }
        }
    } catch (e) {
        console.warn("Could not read stored user profile:", e);
    }
    return Object.assign({}, DEFAULT_USER_PROFILE);
}

function saveActiveUserProfile(profile) {
    try {
        localStorage.setItem('kmrl_current_user', JSON.stringify(profile));
        fetch('/api/storage/kmrl_current_user', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ value: profile })
        }).catch(err => console.warn('Storage sync notification:', err));
    } catch (e) {
        console.error('Error saving user profile:', e);
    }
}

function renderUserProfile(profile) {
    const user = profile || getActiveUserProfile();
    
    // Update name
    const profileNameEls = document.querySelectorAll('.profile-name');
    profileNameEls.forEach(el => {
        el.textContent = user.name || user.username || 'Admin User';
        el.style.display = 'inline';
    });

    // Update dropdown header details
    const profileDetailH4s = document.querySelectorAll('.profile-details h4');
    profileDetailH4s.forEach(el => {
        el.textContent = user.name || user.username || 'Admin User';
    });

    const profileDetailPs = document.querySelectorAll('.profile-details p');
    profileDetailPs.forEach(el => {
        el.textContent = user.designation || (user.role === 'admin' ? 'System Administrator' : 'Passenger');
    });

    // Update avatar images
    const avatars = document.querySelectorAll('.profile-avatar, .profile-avatar-large');
    avatars.forEach(img => {
        if (user.avatar) {
            img.src = user.avatar;
        }
    });

    // If there's a welcome header on customer/admin pages
    const welcomeHeading = document.getElementById('user-welcome-heading');
    if (welcomeHeading) {
        welcomeHeading.textContent = `Welcome, ${user.name || user.username}`;
    }
}

function initializeUserProfile() {
    const profile = getActiveUserProfile();
    renderUserProfile(profile);
    initializeProfileModal();
    initializePasswordModal();
}

function initializeProfileModal() {
    // Check if modal already exists in DOM; if not, inject it
    let modal = document.getElementById('profile-settings-modal');
    if (!modal) {
        const modalHtml = `
        <div id="profile-settings-modal" class="modal" aria-hidden="true" role="dialog" aria-labelledby="profile-modal-title">
            <div class="modal-dialog" style="max-width: 520px; width: 92%; margin: 30px auto; background: var(--bg-card, #ffffff); border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.25); border: 1px solid var(--border-color, #e2e8f0); color: var(--text-primary, #1e293b); animation: fadeIn 0.3s ease;">
                <div class="modal-header" style="display: flex; justify-content: space-between; align-items: center; padding: 18px 24px; border-bottom: 1px solid var(--border-color, #e2e8f0); background: var(--bg-secondary, #f8fafc);">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 36px; height: 36px; border-radius: 50%; background: #2563eb; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 1.1rem;">
                            <i class="fas fa-user-edit"></i>
                        </div>
                        <div>
                            <h3 id="profile-modal-title" style="margin: 0; font-size: 1.15rem; font-weight: 700;">Admin Profile Settings</h3>
                            <p style="margin: 0; font-size: 0.8rem; color: var(--text-secondary, #64748b);">Manage account credentials & system profile</p>
                        </div>
                    </div>
                    <button type="button" id="profile-settings-close" style="background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text-secondary, #64748b); padding: 4px 8px; border-radius: 6px;">&times;</button>
                </div>
                <form id="profile-settings-form" style="padding: 24px; display: flex; flex-direction: column; gap: 16px;">
                    <!-- Avatar Section -->
                    <div style="display: flex; align-items: center; gap: 16px; padding: 12px; background: var(--bg-secondary, #f8fafc); border-radius: 12px; border: 1px solid var(--border-color, #e2e8f0);">
                        <img id="profile-modal-avatar-preview" src="${DEFAULT_USER_PROFILE.avatar}" alt="Avatar Preview" style="width: 60px; height: 60px; border-radius: 50%; object-fit: cover; border: 2px solid #2563eb; flex-shrink: 0;" />
                        <div style="flex: 1;">
                            <label style="display: block; font-size: 0.82rem; font-weight: 600; margin-bottom: 4px;">Profile Avatar URL</label>
                            <input type="url" id="profile-modal-avatar-input" placeholder="https://..." style="width: 100%; box-sizing: border-box; padding: 7px 10px; border-radius: 6px; border: 1px solid var(--border-color, #cbd5e1); font-size: 0.82rem; background: var(--bg-card, #fff); color: inherit;" />
                            <div style="display: flex; gap: 6px; margin-top: 6px; flex-wrap: wrap;">
                                <button type="button" class="avatar-preset-btn" data-url="https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg?auto=compress&cs=tinysrgb&w=96&h=96&fit=crop&crop=face" style="font-size: 0.72rem; padding: 3px 8px; border-radius: 4px; border: 1px solid #cbd5e1; background: var(--bg-card, #fff); cursor: pointer; color: inherit;">Avatar 1</button>
                                <button type="button" class="avatar-preset-btn" data-url="https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=96&h=96&fit=crop&crop=face" style="font-size: 0.72rem; padding: 3px 8px; border-radius: 4px; border: 1px solid #cbd5e1; background: var(--bg-card, #fff); cursor: pointer; color: inherit;">Avatar 2</button>
                                <button type="button" class="avatar-preset-btn" data-url="https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=96&h=96&fit=crop&crop=face" style="font-size: 0.72rem; padding: 3px 8px; border-radius: 4px; border: 1px solid #cbd5e1; background: var(--bg-card, #fff); cursor: pointer; color: inherit;">Avatar 3</button>
                            </div>
                        </div>
                    </div>

                    <!-- Personal Information -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div>
                            <label style="display: block; font-size: 0.82rem; font-weight: 600; margin-bottom: 4px;">Full Name *</label>
                            <input type="text" id="profile-modal-name" required style="width: 100%; box-sizing: border-box; padding: 9px 12px; border-radius: 6px; border: 1px solid var(--border-color, #cbd5e1); font-size: 0.88rem; background: var(--bg-card, #fff); color: inherit;" />
                        </div>
                        <div>
                            <label style="display: block; font-size: 0.82rem; font-weight: 600; margin-bottom: 4px;">Username</label>
                            <input type="text" id="profile-modal-username" readonly style="width: 100%; box-sizing: border-box; padding: 9px 12px; border-radius: 6px; border: 1px solid var(--border-color, #cbd5e1); font-size: 0.88rem; background: var(--bg-secondary, #f1f5f9); color: var(--text-secondary, #64748b); cursor: not-allowed;" />
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div>
                            <label style="display: block; font-size: 0.82rem; font-weight: 600; margin-bottom: 4px;">Email Address *</label>
                            <input type="email" id="profile-modal-email" required style="width: 100%; box-sizing: border-box; padding: 9px 12px; border-radius: 6px; border: 1px solid var(--border-color, #cbd5e1); font-size: 0.88rem; background: var(--bg-card, #fff); color: inherit;" />
                        </div>
                        <div>
                            <label style="display: block; font-size: 0.82rem; font-weight: 600; margin-bottom: 4px;">Phone Number</label>
                            <input type="tel" id="profile-modal-phone" style="width: 100%; box-sizing: border-box; padding: 9px 12px; border-radius: 6px; border: 1px solid var(--border-color, #cbd5e1); font-size: 0.88rem; background: var(--bg-card, #fff); color: inherit;" />
                        </div>
                    </div>

                    <!-- Role & Department -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div>
                            <label style="display: block; font-size: 0.82rem; font-weight: 600; margin-bottom: 4px;">Department</label>
                            <select id="profile-modal-department" style="width: 100%; box-sizing: border-box; padding: 9px 12px; border-radius: 6px; border: 1px solid var(--border-color, #cbd5e1); font-size: 0.88rem; background: var(--bg-card, #fff); color: inherit;">
                                <option value="Operations Management">Operations Management</option>
                                <option value="Signaling & Telecom">Signaling & Telecom</option>
                                <option value="Rolling Stock & Fleet">Rolling Stock & Fleet</option>
                                <option value="Finance & Accounts">Finance & Accounts</option>
                                <option value="Safety & Verification">Safety & Verification</option>
                                <option value="IT & Infrastructure">IT & Infrastructure</option>
                            </select>
                        </div>
                        <div>
                            <label style="display: block; font-size: 0.82rem; font-weight: 600; margin-bottom: 4px;">Designation</label>
                            <input type="text" id="profile-modal-designation" style="width: 100%; box-sizing: border-box; padding: 9px 12px; border-radius: 6px; border: 1px solid var(--border-color, #cbd5e1); font-size: 0.88rem; background: var(--bg-card, #fff); color: inherit;" />
                        </div>
                    </div>

                    <!-- Change Password Shortcut inside Profile Modal -->
                    <div style="padding-top: 6px; display: flex; justify-content: space-between; align-items: center; border-top: 1px dashed var(--border-color, #e2e8f0);">
                        <span style="font-size: 0.82rem; color: var(--text-secondary, #64748b);">Account Security</span>
                        <button type="button" id="open-pwd-from-profile" style="background: none; border: none; color: #2563eb; font-weight: 600; font-size: 0.82rem; cursor: pointer; display: flex; align-items: center; gap: 6px;">
                            <i class="fas fa-key"></i> Change Password
                        </button>
                    </div>

                    <div class="modal-footer" style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 10px; padding-top: 16px; border-top: 1px solid var(--border-color, #e2e8f0);">
                        <button type="button" id="profile-modal-cancel" style="padding: 10px 18px; border-radius: 8px; border: 1px solid var(--border-color, #cbd5e1); background: transparent; color: inherit; font-weight: 600; cursor: pointer;">Cancel</button>
                        <button type="submit" style="padding: 10px 22px; border-radius: 8px; border: none; background: #2563eb; color: #fff; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 6px;">
                            <i class="fas fa-save"></i> Save Profile
                        </button>
                    </div>
                </form>
            </div>
        </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        modal = document.getElementById('profile-settings-modal');
    }

    // Bind Avatar Preset buttons
    const presetBtns = modal.querySelectorAll('.avatar-preset-btn');
    const avatarInput = document.getElementById('profile-modal-avatar-input');
    const avatarPreview = document.getElementById('profile-modal-avatar-preview');

    presetBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const url = btn.getAttribute('data-url');
            if (avatarInput) avatarInput.value = url;
            if (avatarPreview) avatarPreview.src = url;
        });
    });

    if (avatarInput && avatarPreview) {
        avatarInput.addEventListener('input', () => {
            if (avatarInput.value.trim()) {
                avatarPreview.src = avatarInput.value.trim();
            }
        });
    }

    // Open profile modal buttons
    const profileSettingsBtns = document.querySelectorAll('#profile-settings, #mobile-profile-settings, .open-profile-settings');
    profileSettingsBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            // Populate form with current user details
            const user = getActiveUserProfile();
            const nameIn = document.getElementById('profile-modal-name');
            const userIn = document.getElementById('profile-modal-username');
            const emailIn = document.getElementById('profile-modal-email');
            const phoneIn = document.getElementById('profile-modal-phone');
            const deptIn = document.getElementById('profile-modal-department');
            const desigIn = document.getElementById('profile-modal-designation');
            const avIn = document.getElementById('profile-modal-avatar-input');
            const avPrev = document.getElementById('profile-modal-avatar-preview');

            if (nameIn) nameIn.value = user.name || '';
            if (userIn) userIn.value = user.username || 'admin';
            if (emailIn) emailIn.value = user.email || '';
            if (phoneIn) phoneIn.value = user.phone || '+91 98470 12345';
            if (deptIn) deptIn.value = user.department || 'Operations Management';
            if (desigIn) desigIn.value = user.designation || 'System Administrator';
            if (avIn) avIn.value = user.avatar || '';
            if (avPrev) avPrev.src = user.avatar || DEFAULT_USER_PROFILE.avatar;

            // Close profile dropdown if open
            const profileDropdown = document.getElementById('profile-dropdown');
            if (profileDropdown) profileDropdown.classList.remove('show');

            showModal('profile-settings-modal');
        });
    });

    // Shortcut button from profile modal to password modal
    const openPwdBtn = document.getElementById('open-pwd-from-profile');
    if (openPwdBtn) {
        openPwdBtn.addEventListener('click', () => {
            hideModal('profile-settings-modal');
            openChangePasswordModal();
        });
    }

    // Close buttons
    const closeBtn = document.getElementById('profile-settings-close');
    const cancelBtn = document.getElementById('profile-modal-cancel');
    if (closeBtn) closeBtn.addEventListener('click', () => hideModal('profile-settings-modal'));
    if (cancelBtn) cancelBtn.addEventListener('click', () => hideModal('profile-settings-modal'));

    // Handle Form Submit
    const form = document.getElementById('profile-settings-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const currentUser = getActiveUserProfile();
            const updatedUser = Object.assign({}, currentUser, {
                name: document.getElementById('profile-modal-name')?.value?.trim() || currentUser.name,
                email: document.getElementById('profile-modal-email')?.value?.trim() || currentUser.email,
                phone: document.getElementById('profile-modal-phone')?.value?.trim() || currentUser.phone,
                department: document.getElementById('profile-modal-department')?.value || currentUser.department,
                designation: document.getElementById('profile-modal-designation')?.value?.trim() || currentUser.designation,
                avatar: document.getElementById('profile-modal-avatar-input')?.value?.trim() || currentUser.avatar,
                updated_at: new Date().toISOString()
            });

            saveActiveUserProfile(updatedUser);
            renderUserProfile(updatedUser);
            hideModal('profile-settings-modal');
            showSuccessMessage('Admin profile updated successfully!');
        });
    }
}

// ===== PASSWORD MANAGEMENT MODAL =====
function openChangePasswordModal() {
    const modal = document.getElementById('change-password-modal');
    if (modal) {
        // Reset inputs
        const currIn = document.getElementById('pwd-modal-current');
        const newIn = document.getElementById('pwd-modal-new');
        const confIn = document.getElementById('pwd-modal-confirm');
        const alertEl = document.getElementById('pwd-modal-alert');
        if (currIn) currIn.value = '';
        if (newIn) newIn.value = '';
        if (confIn) confIn.value = '';
        if (alertEl) {
            alertEl.textContent = '';
            alertEl.style.display = 'none';
        }
        
        // Close profile dropdown
        const profileDropdown = document.getElementById('profile-dropdown');
        if (profileDropdown) profileDropdown.classList.remove('show');

        showModal('change-password-modal');
    }
}

function initializePasswordModal() {
    let modal = document.getElementById('change-password-modal');
    if (!modal) {
        const modalHtml = `
        <div id="change-password-modal" class="modal" aria-hidden="true" role="dialog" aria-labelledby="pwd-modal-title">
            <div class="modal-dialog" style="max-width: 440px; width: 92%; margin: 40px auto; background: var(--bg-card, #ffffff); border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.25); border: 1px solid var(--border-color, #e2e8f0); color: var(--text-primary, #1e293b); animation: fadeIn 0.3s ease;">
                <div class="modal-header" style="display: flex; justify-content: space-between; align-items: center; padding: 18px 24px; border-bottom: 1px solid var(--border-color, #e2e8f0); background: var(--bg-secondary, #f8fafc);">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 36px; height: 36px; border-radius: 50%; background: #2563eb; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 1.1rem;">
                            <i class="fas fa-lock"></i>
                        </div>
                        <div>
                            <h3 id="pwd-modal-title" style="margin: 0; font-size: 1.15rem; font-weight: 700;">Change Password</h3>
                            <p style="margin: 0; font-size: 0.8rem; color: var(--text-secondary, #64748b);">Update your account login password</p>
                        </div>
                    </div>
                    <button type="button" id="pwd-modal-close" style="background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text-secondary, #64748b); padding: 4px 8px; border-radius: 6px;">&times;</button>
                </div>
                <form id="change-password-form" style="padding: 24px; display: flex; flex-direction: column; gap: 14px;">
                    <div id="pwd-modal-alert" style="display: none; padding: 10px 14px; border-radius: 8px; font-size: 0.85rem; font-weight: 500; line-height: 1.4;"></div>

                    <div>
                        <label style="display: block; font-size: 0.82rem; font-weight: 600; margin-bottom: 4px;">Current Password *</label>
                        <input type="password" id="pwd-modal-current" required placeholder="Enter current password" style="width: 100%; box-sizing: border-box; padding: 10px 12px; border-radius: 6px; border: 1px solid var(--border-color, #cbd5e1); font-size: 0.88rem; background: var(--bg-card, #fff); color: inherit;" />
                    </div>

                    <div>
                        <label style="display: block; font-size: 0.82rem; font-weight: 600; margin-bottom: 4px;">New Password *</label>
                        <input type="password" id="pwd-modal-new" required minlength="4" placeholder="Enter new password (min 4 chars)" style="width: 100%; box-sizing: border-box; padding: 10px 12px; border-radius: 6px; border: 1px solid var(--border-color, #cbd5e1); font-size: 0.88rem; background: var(--bg-card, #fff); color: inherit;" />
                    </div>

                    <div>
                        <label style="display: block; font-size: 0.82rem; font-weight: 600; margin-bottom: 4px;">Confirm New Password *</label>
                        <input type="password" id="pwd-modal-confirm" required minlength="4" placeholder="Re-enter new password" style="width: 100%; box-sizing: border-box; padding: 10px 12px; border-radius: 6px; border: 1px solid var(--border-color, #cbd5e1); font-size: 0.88rem; background: var(--bg-card, #fff); color: inherit;" />
                    </div>

                    <div class="modal-footer" style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 10px; padding-top: 16px; border-top: 1px solid var(--border-color, #e2e8f0);">
                        <button type="button" id="pwd-modal-cancel" style="padding: 10px 18px; border-radius: 8px; border: 1px solid var(--border-color, #cbd5e1); background: transparent; color: inherit; font-weight: 600; cursor: pointer;">Cancel</button>
                        <button type="submit" id="pwd-modal-submit" style="padding: 10px 22px; border-radius: 8px; border: none; background: #2563eb; color: #fff; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 6px;">
                            <i class="fas fa-key"></i> Update Password
                        </button>
                    </div>
                </form>
            </div>
        </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        modal = document.getElementById('change-password-modal');
    }

    // Attach listeners to all change password buttons across the page
    const changePwdBtns = document.querySelectorAll('#change-password, #mobile-change-password, .open-change-password');
    changePwdBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            openChangePasswordModal();
        });
    });

    // Close handlers
    const closeBtn = document.getElementById('pwd-modal-close');
    const cancelBtn = document.getElementById('pwd-modal-cancel');
    if (closeBtn) closeBtn.addEventListener('click', () => hideModal('change-password-modal'));
    if (cancelBtn) cancelBtn.addEventListener('click', () => hideModal('change-password-modal'));

    // Form submit handler
    const form = document.getElementById('change-password-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const alertEl = document.getElementById('pwd-modal-alert');
            const submitBtn = document.getElementById('pwd-modal-submit');
            const originalBtnHtml = submitBtn.innerHTML;

            const currentPassword = document.getElementById('pwd-modal-current')?.value || '';
            const newPassword = document.getElementById('pwd-modal-new')?.value || '';
            const confirmPassword = document.getElementById('pwd-modal-confirm')?.value || '';

            if (newPassword !== confirmPassword) {
                if (alertEl) {
                    alertEl.textContent = 'New passwords do not match. Please verify!';
                    alertEl.style.display = 'block';
                    alertEl.style.background = '#fee2e2';
                    alertEl.style.color = '#991b1b';
                    alertEl.style.border = '1px solid #f87171';
                }
                return;
            }

            const user = getActiveUserProfile();
            submitBtn.disabled = true;
            submitBtn.innerHTML = `<div class="spinner" style="width:16px; height:16px; border:2px solid #fff; border-top-color:transparent; border-radius:50%; animation:spin 1s linear infinite;"></div> Updating...`;

            try {
                const res = await fetch('/api/auth/change-password', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        username: user.username || 'admin',
                        current_password: currentPassword,
                        new_password: newPassword,
                        confirm_password: confirmPassword
                    })
                });

                const data = await res.json();

                if (!res.ok) {
                    if (alertEl) {
                        alertEl.textContent = data.detail || 'Password update failed. Please check your current password.';
                        alertEl.style.display = 'block';
                        alertEl.style.background = '#fee2e2';
                        alertEl.style.color = '#991b1b';
                        alertEl.style.border = '1px solid #f87171';
                    }
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnHtml;
                    return;
                }

                // Success
                if (alertEl) {
                    alertEl.textContent = 'Password updated successfully in database!';
                    alertEl.style.display = 'block';
                    alertEl.style.background = '#dcfce7';
                    alertEl.style.color = '#166534';
                    alertEl.style.border = '1px solid #86efac';
                }
                submitBtn.innerHTML = `<i class="fas fa-check"></i> Updated!`;

                setTimeout(() => {
                    hideModal('change-password-modal');
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnHtml;
                    showSuccessMessage('Password changed successfully!');
                }, 800);

            } catch (err) {
                console.error('Password change error:', err);
                if (alertEl) {
                    alertEl.textContent = 'Network or server error while updating password.';
                    alertEl.style.display = 'block';
                    alertEl.style.background = '#fee2e2';
                    alertEl.style.color = '#991b1b';
                    alertEl.style.border = '1px solid #f87171';
                }
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnHtml;
            }
        });
    }
}

// ===== THEME TOGGLE FUNCTIONALITY =====
/**
 * Initialize theme toggle
 */
function initializeThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    
    // Load saved theme or detect system preference
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = savedTheme || (systemPrefersDark ? 'dark' : 'light');
    
    setTheme(initialTheme);
    
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            setTheme(newTheme);
        });
    }
}

function setTheme(theme) {
    const themeIcon = document.getElementById('theme-icon');
    const themeToggle = document.getElementById('theme-toggle');
    
    document.documentElement.setAttribute('data-theme', theme);
    
    if (themeIcon && themeToggle) {
        if (theme === 'dark') {
            themeIcon.className = 'fas fa-moon theme-icon';
            themeToggle.setAttribute('aria-label', 'Switch to light theme');
        } else {
            themeIcon.className = 'fas fa-sun theme-icon';
            themeToggle.setAttribute('aria-label', 'Switch to dark theme');
        }
    }
    
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
        metaThemeColor.setAttribute('content', theme === 'dark' ? '#1e293b' : '#2563eb');
    }
    
    localStorage.setItem('theme', theme);
    // Notify other modules about theme change
    try {
        document.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
    } catch (e) {
        // no-op if CustomEvent not supported
    }
}

// ===== INTERACTIVE BACKGROUND =====
/**
 * Initialize a full-viewport canvas that renders a subtle particle field.
 * The visuals adapt to the current theme (dark/light). It is interactive
 * on pointer move and respects prefers-reduced-motion.
 */
function initializeInteractiveBackground() {
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    const existing = document.querySelector('.interactive-bg');
    if (existing) return;

    const wrapper = document.createElement('div');
    wrapper.className = 'interactive-bg';
    const canvas = document.createElement('canvas');
    canvas.className = 'interactive-canvas';
    wrapper.appendChild(canvas);
    // Insert as first child so header/main remain visually above (z-index in CSS)
    document.body.insertBefore(wrapper, document.body.firstChild);

    const ctx = canvas.getContext('2d');
    let width = 0;
    let height = 0;
    let particles = [];
    let animationId = null;
    let pointer = { x: -9999, y: -9999 };
    let theme = document.documentElement.getAttribute('data-theme') || 'light';

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
        const area = width * height;
        const base = Math.max(30, Math.min(120, Math.floor(area / 10000)));
        createParticles(base);
    }

    function createParticles(count) {
        particles = [];
        for (let i = 0; i < count; i++) {
            particles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                vx: (Math.random() - 0.5) * 0.6,
                vy: (Math.random() - 0.5) * 0.6,
                r: Math.random() * 1.8 + 0.8
            });
        }
    }

    function getColorsForTheme(t) {
        if (t === 'dark') {
            return { particle: 'rgba(180,220,255,0.9)', line: 'rgba(120,180,255,0.12)', bg: 'transparent' };
        }
        // light theme: subtle gray particles
        return { particle: 'rgba(30,41,59,0.12)', line: 'rgba(30,41,59,0.06)', bg: 'transparent' };
    }

    function step() {
        ctx.clearRect(0, 0, width, height);
        const colors = getColorsForTheme(theme);

        // draw lines
        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];
            for (let j = i + 1; j < particles.length; j++) {
                const q = particles[j];
                const dx = p.x - q.x;
                const dy = p.y - q.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 120) {
                    ctx.strokeStyle = colors.line;
                    ctx.lineWidth = 1 * (1 - dist / 120) * 0.9;
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(q.x, q.y);
                    ctx.stroke();
                }
            }
        }

        // draw particles and update
        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];
            // interaction with pointer
            const dx = pointer.x - p.x;
            const dy = pointer.y - p.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 120) {
                const force = (1 - dist / 120) * 0.6;
                p.vx += (dx / dist) * force * 0.08;
                p.vy += (dy / dist) * force * 0.08;
            }

            p.x += p.vx;
            p.y += p.vy;

            // wrap
            if (p.x < -10) p.x = width + 10;
            if (p.x > width + 10) p.x = -10;
            if (p.y < -10) p.y = height + 10;
            if (p.y > height + 10) p.y = -10;

            ctx.fillStyle = getColorsForTheme(theme).particle;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fill();
        }

        animationId = requestAnimationFrame(step);
    }

    function onPointerMove(e) {
        const rect = canvas.getBoundingClientRect();
        pointer.x = e.clientX - rect.left;
        pointer.y = e.clientY - rect.top;
    }

    function onPointerLeave() {
        pointer.x = -9999;
        pointer.y = -9999;
    }

    function applyTheme(t) {
        theme = t;
        // colors will adapt on next frame
    }

    // Initialize
    resize();
    window.addEventListener('resize', resize);
    window.addEventListener('pointermove', onPointerMove);
    window.addEventListener('pointerleave', onPointerLeave);
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) cancelAnimationFrame(animationId);
        else animationId = requestAnimationFrame(step);
    });

    // Observe theme changes
    document.addEventListener('themechange', (ev) => {
        if (ev && ev.detail && ev.detail.theme) applyTheme(ev.detail.theme);
    });

    // Start animation
    animationId = requestAnimationFrame(step);
}

// ===== TRAIN OPERATIONS FUNCTIONALITY =====
/**
 * Initialize train operations (only on train operations page)
 */
function initializeTrainOperations() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const trainSearch = document.getElementById('train-search');
    
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const filter = btn.getAttribute('data-filter');
            filterTrains(filter);
        });
    });
    
    if (trainSearch) {
        trainSearch.addEventListener('input', debounce((e) => {
            searchTrains(e.target.value);
        }, 300));
    }
}

function filterTrains(filter) {
    const trainItems = document.querySelectorAll('.train-item');
    
    trainItems.forEach(item => {
        const status = item.getAttribute('data-status');
        const shouldShow = filter === 'all' || status === filter;
        
        item.style.display = shouldShow ? 'flex' : 'none';
    });
}

function searchTrains(searchTerm) {
    const trainItems = document.querySelectorAll('.train-item');
    const term = searchTerm.toLowerCase().trim();
    
    trainItems.forEach(item => {
        const text = item.textContent.toLowerCase();
        const shouldShow = !term || text.includes(term);
        
        item.style.display = shouldShow ? 'flex' : 'none';
    });
}

// ===== VERIFY OPERATIONS FUNCTIONALITY =====
/**
 * Initialize verification operations
 */
function initializeVerifyOperations() {
    const verifyBtns = document.querySelectorAll('.btn-verify');
    
    verifyBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const trainId = btn.getAttribute('data-train');
            showVerificationModal(trainId);
        });
    });
}

function showVerificationModal(trainId) {
    const verifyTrainId = document.getElementById('verify-train-id');
    if (verifyTrainId) {
        verifyTrainId.textContent = trainId;
    }
    showModal('verification-modal');
}

// ===== LIVE MAP FUNCTIONALITY =====
/**
 * Initialize live map (only on live map page)
 */
function initializeLiveMap() {
    const stations = document.querySelectorAll('.station');
    
    stations.forEach(station => {
        station.addEventListener('click', () => {
            const stationName = station.getAttribute('data-station');
            showStationDetails(stationName);
            
            stations.forEach(s => s.classList.remove('active'));
            station.classList.add('active');
        });
    });
}

function showStationDetails(stationName) {
    const stationDetails = document.getElementById('station-details');
    const noSelection = stationDetails?.querySelector('.no-selection');
    const stationInfo = stationDetails?.querySelector('.station-info');
    const selectedStationName = document.getElementById('selected-station-name');
    
    if (noSelection) noSelection.style.display = 'none';
    if (stationInfo) stationInfo.style.display = 'block';
    if (selectedStationName) selectedStationName.textContent = stationName;
    
    const stationOfficers = document.getElementById('station-officers');
    const stationTrains = document.getElementById('station-trains');
    
    if (stationOfficers) stationOfficers.textContent = Math.floor(Math.random() * 5) + 2;
    if (stationTrains) stationTrains.textContent = Math.floor(Math.random() * 30) + 15;
}

// ===== UTILITY FUNCTIONS =====
/**
 * Update current time display
 */
function updateCurrentTime() {
    const timeElement = document.getElementById('current-time');
    if (timeElement) {
        const now = new Date();
        const options = {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        timeElement.textContent = now.toLocaleDateString('en-IN', options);
    }
}

/**
 * Show success message
 */
function showSuccessMessage(message) {
    showToast(message, 'success');
}

/**
 * Show error message
 */
function showErrorMessage(message) {
    showToast(message, 'error');
}

/**
 * Show toast notification
 */
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
        info: '#3b82f6'
    };
    
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colors[type] || colors.success};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        z-index: 1100;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
        font-size: 0.875rem;
        font-weight: 500;
    `;
    
    if (window.innerWidth <= 576) {
        toast.style.cssText += `
            top: 10px;
            right: 10px;
            left: 10px;
            max-width: none;
            transform: translateY(-100%);
        `;
    }
    
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        if (window.innerWidth <= 576) {
            toast.style.transform = 'translateY(0)';
        } else {
            toast.style.transform = 'translateX(0)';
        }
    }, 100);
    
    setTimeout(() => {
        if (window.innerWidth <= 576) {
            toast.style.transform = 'translateY(-100%)';
        } else {
            toast.style.transform = 'translateX(100%)';
        }
        setTimeout(() => {
            if (document.body.contains(toast)) {
                document.body.removeChild(toast);
            }
        }, 300);
    }, 4000);
}

/**
 * Emergency contacts function
 */
function showEmergencyContacts() {
    const emergencyInfo = `
Emergency Contacts:

Control Room: +91 484 400 6000
Fire Department: 101
Police: 100
Medical Emergency: 108
Station Master: +91 484 400 6001
Security: +91 484 400 6002

For immediate assistance, contact the Control Room.
    `;
    
    alert(emergencyInfo);
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ===== ERROR HANDLING =====
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    showErrorMessage('An unexpected error occurred. Please try again.');
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    showErrorMessage('A network error occurred. Please check your connection.');
});













// ---------------------
// Status Chart
// ---------------------
async function loadStatusChart() {
    try {
        const canvas = document.getElementById("statusChart");
        if (!canvas) return; // Null check
        const ctx = canvas.getContext("2d");

        const res = await fetch("/api/rules");
        if (!res.ok) throw new Error("Network response was not ok");
        const data = await res.json();

        const eligible = data.filter(r => r.status === "Eligible").length;
        const blocked = data.filter(r => r.status !== "Eligible").length;

        if (window.statusChartInstance) window.statusChartInstance.destroy();

        window.statusChartInstance = new Chart(ctx, {
            type: "pie",
            data: { labels: ["Eligible", "Blocked"], datasets: [{ data: [eligible, blocked], backgroundColor: ["#28a745", "#dc3545"] }] },
            options: { responsive: false, maintainAspectRatio: false }
        });
    } catch (err) {
        console.error("Failed to load Status chart:", err);
    }
}


function downloadStatusReport() {
    window.open("/api/report/status-pdf", "_blank");
}

// ---------------------
// What-If Chart
// ---------------------
async function loadWhatIfChart() {
    try {
        const canvas = document.getElementById("whatifChart");
        if (!canvas) return; // Null check
        const ctx = canvas.getContext("2d");

        const defaultsRes = await fetch("/api/whatif/defaults");
        const defaults = await defaultsRes.json();

        const k = document.getElementById("whatifK")?.value ? Number(document.getElementById("whatifK").value) : defaults.k;
        const branding_weight = document.getElementById("brandingWeight")?.value ? Number(document.getElementById("brandingWeight").value) : defaults.branding_weight;
        const stabling_weight = document.getElementById("stablingWeight")?.value ? Number(document.getElementById("stablingWeight").value) : defaults.stabling_weight;

        const res = await fetch(`/api/whatif?k=${k}&branding_weight=${branding_weight}&stabling_weight=${stabling_weight}`, { method: "POST" });
        if (!res.ok) throw new Error("Network response was not ok");
        const data = await res.json();

        const beforeScores = data.map(r => r.mileage);
        const afterScores = data.map(r => r.score);

        if (window.whatIfChartInstance) window.whatIfChartInstance.destroy();

        window.whatIfChartInstance = new Chart(ctx, {
            type: "bar",
            data: {
                labels: data.map(r => r.id),
                datasets: [
                    { label: "Before (Mileage)", data: beforeScores, backgroundColor: "#007bff" },
                    { label: "After (Score)", data: afterScores, backgroundColor: "#28a745" }
                ]
            },
            options: { responsive: false, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
        });
    } catch (err) {
        console.error("Failed to load What-If chart:", err);
    }
}


function downloadWhatIfReport() {
    const k = document.getElementById("whatifK")?.value ? Number(document.getElementById("whatifK").value) : 3;
    const branding_weight = document.getElementById("brandingWeight")?.value ? Number(document.getElementById("brandingWeight").value) : 2000;
    const stabling_weight = document.getElementById("stablingWeight")?.value ? Number(document.getElementById("stablingWeight").value) : 5;

    const url = `/api/report/whatif-pdf?k=${k}&branding_weight=${branding_weight}&stabling_weight=${stabling_weight}`;
    window.open(url, "_blank");
}

// ---------------------
// Alerts Distribution Chart
// ---------------------
async function loadAlertsChart() {
    try {
        const canvas = document.getElementById("alertsChart");
        if (!canvas) return; // Null check
        const ctx = canvas.getContext("2d");

        const res = await fetch("/api/rules");
        if (!res.ok) throw new Error("Network response was not ok");
        const data = await res.json();

        const alertCounts = {};
        data.forEach(row => {
            if (row.alerts && row.alerts !== "-") {
                row.alerts.split(",").forEach(alert => {
                    alertCounts[alert.trim()] = (alertCounts[alert.trim()] || 0) + 1;
                });
            }
        });

        if (window.alertsChartInstance) window.alertsChartInstance.destroy();

        window.alertsChartInstance = new Chart(ctx, {
            type: "bar",
            data: { labels: Object.keys(alertCounts), datasets: [{ label: "Number of Trains", data: Object.values(alertCounts), backgroundColor: "#ffc107" }] },
            options: { responsive: false, maintainAspectRatio: false, scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } } }
        });
    } catch (err) {
        console.error("Failed to load Alerts chart:", err);
    }
}


function downloadAlertsReport() {
    window.open("/api/report/alerts-pdf", "_blank");
}

// ---------------------
// Auto-load charts on page load
// ---------------------
window.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById("statusChart")) loadStatusChart();
    if (document.getElementById("whatifChart")) loadWhatIfChart();
    if (document.getElementById("alertsChart")) loadAlertsChart();
});
