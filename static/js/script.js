document.addEventListener('DOMContentLoaded', () => {
    // Inicializar ícones Lucide
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // --- Mobile Menu ---
    const setupMobileMenu = () => {
        const menuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');

        if (!menuBtn || !mobileMenu) return;

        menuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });

        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
            });
        });
    };

    // --- Scroll Effects ---
    const setupScrollEffects = () => {
        const header = document.getElementById('header');
        const backToTopBtn = document.getElementById('back-to-top-btn');

        if (!header && !backToTopBtn) return;

        window.addEventListener('scroll', () => {
            const scrollY = window.scrollY;
            if (header) {
                header.classList.toggle('glass-nav', scrollY > 50);
            }
            if (backToTopBtn) {
                backToTopBtn.classList.toggle('opacity-0', scrollY <= 300);
                backToTopBtn.classList.toggle('pointer-events-none', scrollY <= 300);
            }
        }, { passive: true });

        if (backToTopBtn) {
            backToTopBtn.addEventListener('click', () => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        }
    };

    // --- Scroll Animation (Intersection Observer) ---
    const setupScrollAnimation = () => {
        const revealElements = document.querySelectorAll('.reveal');
        if (revealElements.length === 0) return;

        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    // Opcional: para de observar o elemento após a animação
                    // revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        revealElements.forEach(el => revealObserver.observe(el));
    };

    // --- Inicialização ---
    setupMobileMenu();
    setupScrollEffects();
    setupScrollAnimation();
});