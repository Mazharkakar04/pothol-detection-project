
        document.addEventListener('DOMContentLoaded', function() {
            // Navigation
            const navLinks = document.querySelectorAll('.nav-link');
            const pages = document.querySelectorAll('.page');
            const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
            const navMenu = document.querySelector('nav ul');
            
            // Mobile menu toggle
            mobileMenuBtn.addEventListener('click', function() {
                navMenu.classList.toggle('show');
            });
            
            // Page navigation
            navLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    const targetPage = this.getAttribute('data-target');
                    
                    // Hide all pages
                    pages.forEach(page => {
                        page.classList.remove('active');
                    });
                    
                    // Show target page
                    document.getElementById(targetPage).classList.add('active');
                    
                    // Close mobile menu if open
                    navMenu.classList.remove('show');
                });
            });
            
            // Login tabs
            const loginTabs = document.querySelectorAll('.login-tab');
            const loginForms = document.querySelectorAll('.login-form');
            
            loginTabs.forEach(tab => {
                tab.addEventListener('click', function() {
                    const tabId = this.getAttribute('data-tab');
                    
                    // Update active tab
                    loginTabs.forEach(t => t.classList.remove('active'));
                    this.classList.add('active');
                    
                    // Show corresponding form
                    loginForms.forEach(form => {
                        form.classList.remove('active');
                        if (form.id === `${tabId}-login`) {
                            form.classList.add('active');
                        }
                    });
                });
            });
            
            // Login form submission
            const loginFormsArray = document.querySelectorAll('.login-form');
            loginFormsArray.forEach(form => {
                form.addEventListener('submit', function(e) {
                    e.preventDefault();
                    
                    // Simple validation
                    const email = this.querySelector('input[type="email"], input[type="text"]');
                    const password = this.querySelector('input[type="password"]');
                    
                    if (email.value && password.value) {
                        if (this.id === 'user-login') {
                            // Hide all pages
                            pages.forEach(page => {
                                page.classList.remove('active');
                            });
                            
                            // Show user dashboard
                            document.getElementById('user-dashboard').classList.add('active');
                        } else if (this.id === 'admin-login') {
                            // Hide all pages
                            pages.forEach(page => {
                                page.classList.remove('active');
                            });
                            
                            // Show admin dashboard
                            document.getElementById('admin-dashboard').classList.add('active');
                        }
                    }
                });
            });
            
            // Dashboard sidebar navigation
            const sidebarItems = document.querySelectorAll('.sidebar-menu li:not(.nav-link)');
            const dashboardSections = document.querySelectorAll('.dashboard-section');
            
            sidebarItems.forEach(item => {
                item.addEventListener('click', function() {
                    const sectionId = this.getAttribute('data-section');
                    
                    // Update active sidebar item
                    sidebarItems.forEach(i => i.classList.remove('active'));
                    this.classList.add('active');
                    
                    // Show corresponding section
                    dashboardSections.forEach(section => {
                        section.classList.remove('active');
                        if (section.id === sectionId) {
                            section.classList.add('active');
                        }
                    });
                });
            });
            
            // Image upload preview
            const imageUploadArea = document.getElementById('image-upload-area');
            const imageInput = document.getElementById('pothole-image');
            const imagePreview = document.getElementById('image-preview');
            
            imageUploadArea.addEventListener('click', function() {
                imageInput.click();
            });
            
            imageInput.addEventListener('change', function() {
                const file = this.files[0];
                if (file) {
                    const reader = new FileReader();
                    
                    reader.addEventListener('load', function() {
                        imagePreview.src = reader.result;
                        imagePreview.style.display = 'block';
                    });
                    
                    reader.readAsDataURL(file);
                }
            });
            
            // Allow drag and drop for image upload
            imageUploadArea.addEventListener('dragover', function(e) {
                e.preventDefault();
                this.style.borderColor = '#1a4480';
            });
            
            imageUploadArea.addEventListener('dragleave', function() {
                this.style.borderColor = '#e0e0e0';
            });
            
            imageUploadArea.addEventListener('drop', function(e) {
                e.preventDefault();
                this.style.borderColor = '#e0e0e0';
                
                const file = e.dataTransfer.files[0];
                if (file && file.type.startsWith('image/')) {
                    imageInput.files = e.dataTransfer.files;
                    
                    const reader = new FileReader();
                    
                    reader.addEventListener('load', function() {
                        imagePreview.src = reader.result;
                        imagePreview.style.display = 'block';
                    });
                    
                    reader.readAsDataURL(file);
                }
            });
        });
