document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-link');
    const pages = document.querySelectorAll('.page');
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('nav ul');

    mobileMenuBtn.addEventListener('click', function() {
        navMenu.classList.toggle('show');
    });

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetPage = this.getAttribute('data-target');
            if (targetPage) {
                e.preventDefault();
                pages.forEach(page => {
                    page.classList.remove('active');
                });
                const targetElement = document.getElementById(targetPage);
                if (targetElement) {
                    targetElement.classList.add('active');
                }
                navMenu.classList.remove('show');
            }
        });
    });

    const loginTabs = document.querySelectorAll('.login-tab');
    const loginForms = document.querySelectorAll('.login-form');

    loginTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            loginTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');

            loginForms.forEach(form => {
                form.classList.remove('active');
                if (form.id === `${tabId}-login`) {
                    form.classList.add('active');
                }
            });
        });
    });

    const sidebarItems = document.querySelectorAll('.sidebar-menu li:not(.nav-link)');
    const dashboardSections = document.querySelectorAll('.dashboard-section');

    sidebarItems.forEach(item => {
        item.addEventListener('click', function() {
            const sectionId = this.getAttribute('data-section');
            sidebarItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            dashboardSections.forEach(section => {
                section.classList.remove('active');
                if (section.id === sectionId) {
                    section.classList.add('active');
                }
            });
        });
    });

    const imageUploadArea = document.getElementById('image-upload-area');
    const imageInput = document.getElementById('pothole-image');
    const imagePreview = document.getElementById('image-preview');

    if (imageUploadArea && imageInput && imagePreview) {
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
    }
});
