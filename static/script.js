(function() {
    const theme = localStorage.getItem('theme') || 'auto';
    if (theme !== 'auto') {
        document.documentElement.setAttribute('data-theme', theme);
    }
    window.initialTheme = theme;
})();

document.addEventListener('DOMContentLoaded', function() {
    const themeSelect = document.getElementById('theme-select');
    themeSelect.value = localStorage.getItem('theme') || 'auto';
    
    function updateBanner(theme) {
        const isLcars = theme === 'lcars';
        const bannerType = isLcars ? 'lcars' : 'banner';
        
        document.getElementById('banner-small').srcset = `assets/${bannerType}-small.webp`;
        document.getElementById('banner-medium').srcset = `assets/${bannerType}-medium.webp`;
        document.getElementById('banner-large').src = `assets/${bannerType}-large.webp`;
    }
    
    themeSelect.addEventListener('change', (e) => {
        const theme = e.target.value;
        localStorage.setItem('theme', theme);
        if (theme === 'auto') {
            document.documentElement.removeAttribute('data-theme');
            updateBanner('auto');
        } else {
            document.documentElement.setAttribute('data-theme', theme);
            updateBanner(theme);
        }
    });
    
    updateBanner(window.initialTheme || themeSelect.value);
});