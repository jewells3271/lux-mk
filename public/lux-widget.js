
(function () {
    // Lux Widget - Robust Loader v3.1
    const WIDGET_URL = "https://lux-mk-frontend-cr53.vercel.app/?mode=embed";

    if (document.getElementById('lux-widget-container')) return;

    // Create container - Full screen transparent to prevent clipping
    const container = document.createElement('div');
    container.id = 'lux-widget-container';
    container.style.position = 'fixed';
    container.style.top = '0';
    container.style.left = '0';
    container.style.width = '100vw';
    container.style.height = '100vh';
    container.style.zIndex = '999999';
    container.style.pointerEvents = 'none'; // Mouse passes through empty space
    container.style.overflow = 'hidden';

    // Create Iframe
    const iframe = document.createElement('iframe');
    iframe.src = WIDGET_URL;
    iframe.style.width = '100%';
    iframe.style.height = '100%';
    iframe.style.border = 'none';
    iframe.style.background = 'transparent';
    iframe.style.pointerEvents = 'auto'; // Re-enable pointer events for the iframe content
    iframe.allow = "microphone; camera; clipboard-write";

    container.appendChild(iframe);
    document.body.appendChild(container);

    console.log("Lux Widget Loaded (v3.1 Robust).");
})();
