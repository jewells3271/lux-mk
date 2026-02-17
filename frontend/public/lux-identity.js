
(function () {
    // Lux Identity Registry - Robust Loader v3.1
    const WIDGET_URL = "https://revolution-frontend-zeta.vercel.app/?mode=identity";

    if (document.getElementById('lux-identity-container')) return;

    const container = document.createElement('div');
    container.id = 'lux-identity-container';
    container.style.position = 'fixed';
    container.style.top = '0';
    container.style.left = '0';
    container.style.width = '100vw';
    container.style.height = '100vh';
    container.style.zIndex = '999999';
    container.style.pointerEvents = 'none';
    container.style.overflow = 'hidden';

    const iframe = document.createElement('iframe');
    iframe.src = WIDGET_URL;
    iframe.style.width = '100%';
    iframe.style.height = '100%';
    iframe.style.border = 'none';
    iframe.style.background = 'transparent';
    iframe.style.pointerEvents = 'auto';

    container.appendChild(iframe);
    document.body.appendChild(container);

    console.log("Lux Identity Registry Loaded (v3.1 Robust).");
})();
