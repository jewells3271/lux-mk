
(function () {
    // Lux Loader Script v1.1 - The "Unblocker"
    // Embed this on any site to load the Lux Chat Widget
    const WIDGET_URL = "https://revolution-frontend-zeta.vercel.app/?mode=embed";

    // Prevent duplicate injection
    if (document.getElementById('lux-widget-container')) {
        console.warn("Lux Widget already loaded.");
        return;
    }

    // Create container for Iframe
    const container = document.createElement('div');
    container.id = 'lux-widget-container';
    container.style.position = 'fixed';
    container.style.bottom = '0';
    container.style.right = '0';
    container.style.width = '100%';
    container.style.height = '100%';
    container.style.pointerEvents = 'none'; // Allow clicks to pass through empty space
    container.style.zIndex = '999999';
    container.style.overflow = 'hidden';

    // Create Iframe
    const iframe = document.createElement('iframe');
    iframe.src = WIDGET_URL;
    iframe.style.width = '100%';
    iframe.style.height = '100%';
    iframe.style.border = 'none';
    iframe.style.background = 'transparent';
    iframe.allow = "microphone; camera; clipboard-write";

    // Append
    container.appendChild(iframe);
    document.body.appendChild(container);

    console.log("Lux Widget Loaded via Loader.");
})();
